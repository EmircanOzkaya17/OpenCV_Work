"""
app_func.py
-----------
Kivi filtreleme uygulamasının çekirdek modülü.
Görüntü yükleme, segmentasyon, ellipse fitting ve
GrabCut rafine işlemlerini sınıf tabanlı olarak sunar.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np


# ───Data Structures ────────────────────────────────────────────────────────────

@dataclass
class KiwiEllipse:
    """A data class representing a detected kiwi region."""
    index: int
    center: Tuple[float, float]
    axes: Tuple[float, float]
    angle: float
    hull_area: float

    @property
    def aspect_ratio(self) -> float:
        """It returns the ratio of the long axis to the short axis."""
        return max(self.axes) / (min(self.axes) + 1e-5)

    @property
    def radius_approx(self) -> float:
        """Approximate radius (half of the major axis)."""
        return max(self.axes) / 2.0


@dataclass
class SegmentationConfig:
    """A configuration class that holds segmentation parameters."""
    saturation_threshold: int   = 55
    min_area_ratio: float       = 0.009
    max_aspect_ratio: float     = 2.0
    min_hull_circularity: float = 0.40
    ellipse_scale: float        = 1.06
    grabcut_iterations: int     = 4
    grabcut_border_px: int      = 18
    save_intermediate: bool     = True


# ─── Auxiliary Functions ────────────────────────────────────────────────────

def compute_circularity(area: float, perimeter: float) -> float:
    """
    Calculates the circularity of the contour. 
    Formula: (4π × area) / perimeter² → 1.0 = perfect circle
    """
    if perimeter <= 0:
        return 0.0
    return (4.0 * np.pi * area) / (perimeter ** 2)


def ensure_output_dir(path: str) -> Path:
    """
    It ensures that the output sequence exists; if it doesn't, it creates it.
    """
    output_path = Path(path)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


# ─── Main Transaction Classes ──────────────────────────────────────────────────────

class ImageLoader:
    """The class responsible for image uploading and preprocessing."""

    def __init__(self, image_path: str):
        # Save the image file path.
        self.image_path = image_path
        self.image: Optional[np.ndarray] = None
        self.hsv: Optional[np.ndarray] = None
        self.height: int = 0
        self.width: int = 0

    def load(self) -> np.ndarray:
        """
    It loads the image from disk and prepares for HSV conversion. 
    If the file is not found, it throws a FileNotFoundError.
        """
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"No images found: {self.image_path}")

        # Load in BGR format (OpenCV default)
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"Image could not be read: {self.image_path}")

        self.height, self.width = self.image.shape[:2]

        # HSV conversion - necessary for the saturation channel.
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        print(f"[ImageLoader] Image loaded: {self.width}x{self.height}px")
        return self.image


class BlobDetector:
    """
    HSV is a class that detects kiwi blobs via the saturation channel. 
    It produces a raw blob mask through morphological processing and contour analysis.
    """

    def __init__(self, config: SegmentationConfig):
        self.config = config
        self._saturation_mask: Optional[np.ndarray]  = None
        self._cleaned_mask: Optional[np.ndarray]     = None

    def detect(self, hsv: np.ndarray) -> List[np.ndarray]:
        """
        Detects and rotates kiwi contours from HSV image. Processing steps:
        1. Threshold saturation channel
        2. Clean noise with small morphological OPEN
        3. Extract outer contours
        """
        # ── Step 1: Saturation thresholding ──────────────────────────────────────
        # Marble background S≈5-13, kiwi peel S≈100-255 → clean separation
        saturation_channel = hsv[:, :, 1]
        _, self._saturation_mask = cv2.threshold(
            saturation_channel,
            self.config.saturation_threshold,
            255,
            cv2.THRESH_BINARY
        )

        # ── Step 2: Small OPEN (noise cleaning) ───────────────────────────
        # We're not using a large kernel — so the kiwi blobs don't merge.
        kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        self._cleaned_mask = cv2.morphologyEx(
            self._saturation_mask,
            cv2.MORPH_OPEN,
            kernel_open,
            iterations=1
        )

        # ── Step 3: Find the outer contours. ───────────────────────────────────────
        contours, _ = cv2.findContours(
            self._cleaned_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return list(contours)

    @property
    def saturation_mask(self) -> Optional[np.ndarray]:
        return self._saturation_mask

    @property
    def cleaned_mask(self) -> Optional[np.ndarray]:
        return self._cleaned_mask


class EllipseFitter:
    """
    A class that extracts kiwi ellipses from raw contours and filters out leaves/noise.

    Approach:
    - Convex Hull for each contour → closes the central white hole, increasing circularity
    - Leaves are filtered out with hull circularity and aspect ratio filter
    - A smooth geometric shape is obtained with fitEllipse
    """

    def __init__(self, config: SegmentationConfig, image_shape: Tuple[int, int]):
        self.config = config
        # Total pixel count — for minimum area calculation.
        self.total_pixels = image_shape[0] * image_shape[1]
        self.min_area = self.total_pixels * config.min_area_ratio

    def fit(self, contours: List[np.ndarray]) -> List[KiwiEllipse]:
        """
        Removes valid kiwi ellipses from the contour list.
        Filter sequence for each contour:
        1. Minimum area check
        2. Hull circularity check (long shapes are eliminated)
        3. Aspect ratio check (leaf shape is eliminated)
        FitEllipse is applied to those that pass.
        """
        ellipses: List[KiwiEllipse] = []

        # Sort the items from largest to smallest (larger kiwis processed first).
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

        print(f"\n[EllipseFitter] {len(sorted_contours)} contour being analyzed"
              f"(min_alan={self.min_area:.0f}px):")

        for cnt in sorted_contours:
            area = cv2.contourArea(cnt)

            # ── Filter 1: Minimum space ────────────────────────────────────────
            if area < self.total_pixels * 0.003:
                continue  # very small → skip completely

            # ── Convex Hull ───────────────────────────────────────────────────
            # The kiwi saturation mask produces a ring with a hole in the center. 
            # Convex hull fills this ring, increasing the circularity to ~0.96.
            hull = cv2.convexHull(cnt)
            hull_area = cv2.contourArea(hull)
            hull_perim = cv2.arcLength(hull, True)
            hull_circ = compute_circularity(hull_area, hull_perim)

            # ── Filter 2: Hull circularity ───────────────────────────────────
            if hull_circ < self.config.min_hull_circularity:
                print(f"  ❌ area={hull_area:.0f}  circularity={hull_circ:.3f} "
                      f"→ low circularity")
                continue

            # ── Filtre 3: Minimum alan (hull üzerinden) ───────────────────────
            if hull_area < self.min_area:
                print(f"  ❌ area={hull_area:.0f}  circularity={hull_circ:.3f} "
                      f"→ small (leaf/noise)")
                continue

            # ── Sufficient point control for ellipse fit. ───────────────────────
            if len(hull) < 5:
                continue

            # ── fitEllipse ───────────────────────────────────────────────────
            (ex, ey), (ea, eb), angle = cv2.fitEllipse(hull)
            aspect = max(ea, eb) / (min(ea, eb) + 1e-5)

            # ── Filtre 4: Aspect ratio ────────────────────────────────────────
            if aspect > self.config.max_aspect_ratio:
                print(f"  ❌ area={hull_area:.0f}  aspect={aspect:.2f} "
                      f"→ long/thin (leaf)")
                continue

            idx = len(ellipses)
            ellipses.append(KiwiEllipse(
                index=idx,
                center=(ex, ey),
                axes=(ea, eb),
                angle=angle,
                hull_area=hull_area
            ))
            print(f"  ✅ [{idx}] center=({ex:.0f},{ey:.0f})  "
                  f"axes=({ea:.0f},{eb:.0f})  "
                  f"aspect={aspect:.2f}  "
                  f"circularity={hull_circ:.3f}")

        print(f"\n[EllipseFitter] {len(ellipses)} kiwi ellipse was accepted.")
        return ellipses


class GrabCutRefiner:
    """
    Class that applies independent GrabCut segmentation for each kiwi ellipse.

    Each kiwi is processed SEPARATELY — preventing spillover into neighboring kiwis. Masking strategy:
    - Inside the ellipse → PR_FGD (possible foreground)
    - Eroded center → FGD (definite foreground)
    - Dilated edge → PR_BGD (possible background — GrabCut decides here)
    - Rest → BGD (definite background)
    """

    def __init__(self, config: SegmentationConfig, image_shape: Tuple[int, int]):
        self.config = config
        self.height, self.width = image_shape

    def refine(
        self,
        image: np.ndarray,
        ellipses: List[KiwiEllipse]
    ) -> np.ndarray:
        """
        It applies GrabCut to all kiwi ellipses and returns a combined final mask.
        """
        final_mask = np.zeros((self.height, self.width), dtype=np.uint8)

        for ellipse in ellipses:
            refined = self._refine_single(image, ellipse)
            # Combine each kiwi mask with OR (so the kiwis don't crush each other)
            final_mask = cv2.bitwise_or(final_mask, refined)

        return final_mask

    def _refine_single(
        self,
        image: np.ndarray,
        ellipse: KiwiEllipse
    ) -> np.ndarray:
        """
        Creates a GrabCut mask for a single kiwi. 
        In case of an error, it reverts to the ellipse fill (fallback).
        """
        ex, ey = ellipse.center
        ea, eb = ellipse.axes
        border  = self.config.grabcut_border_px
        scale   = self.config.ellipse_scale

        # ── Ellipse mask ───────────────────────────────────────────────────
        single_mask = np.zeros((self.height, self.width), dtype=np.uint8)
        cv2.ellipse(
            single_mask,
            ((ex, ey), (ea * scale, eb * scale), ellipse.angle),
            255, -1
        )

        # ── Bounding box (GrabCut rect parameter) ───────────────────────────
        x1 = max(0, int(ex - ea / 2 - border))
        y1 = max(0, int(ey - eb / 2 - border))
        x2 = min(self.width,  int(ex + ea / 2 + border))
        y2 = min(self.height, int(ey + eb / 2 + border))
        rect = (x1, y1, x2 - x1, y2 - y1)

        # ── GrabCut starter mask ─────────────────────────────────────────
        gc_mask = np.full(
            (self.height, self.width),
            cv2.GC_BGD,          # default: exact background
            dtype=np.uint8
        )
        gc_mask[single_mask > 0] = cv2.GC_PR_FGD  # inside of the ellipse → possible foreground

        # Erosion and center → definite foreground
        k_erode = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
        sure_fg = cv2.erode(single_mask, k_erode, iterations=2)
        gc_mask[sure_fg > 0] = cv2.GC_FGD

        # Dilation of the border strip → possible background
        k_dilate = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        border_mask = cv2.dilate(single_mask, k_dilate, iterations=2)
        gc_mask[(border_mask > 0) & (single_mask == 0)] = cv2.GC_PR_BGD

        # ── Run GrabCut ──────────────────────────────────────────────────
        try:
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            cv2.grabCut(
                image, gc_mask, rect,
                bgd_model, fgd_model,
                self.config.grabcut_iterations,
                cv2.GC_INIT_WITH_MASK
            )
            # Consider FGD and PR_FGD pixels as foreground.
            result = np.where(
                (gc_mask == cv2.GC_FGD) | (gc_mask == cv2.GC_PR_FGD),
                255, 0
            ).astype(np.uint8)

            # Avoid spilling onto the neighboring kiwi — keep it only within the dilated area.
            result = cv2.bitwise_and(result, border_mask)

            # Close the small holes left by GrabCut.
            k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
            result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, k_close)

            fg_pixels = int(np.sum(result > 0))
            print(f"  [GrabCut] Kiwi {ellipse.index} ✅  "
                  f"foreground_pixel={fg_pixels}")
            return result

        except cv2.error as err:
            #If GrabCut fails, revert to ellipse filler.
            print(f"  [GrabCut] Kiwi {ellipse.index} ⚠ error ({err}) "
                  f"→ ellipse fallback")
            return single_mask


class ResultSaver:
    """
   A class that saves the results of operations and intermediate images to disk. 
   File names are kept descriptive and sequential.
    """

    # Search image names
    INTERMEDIATE_FILES = {
        "saturation_mask": "01_saturation_mask.jpg",
        "cleaned_mask": "02_cleaned_mask.jpg",
        "debug_ellipses": "03_debug_ellipses.jpg",
    }

    # Final output names
    FINAL_FILES = {
        "binary_mask":      "04_final_binary_mask.jpg",
        "overlay":          "05_overlay.jpg",
        "comparison":       "06_comparison.jpg",
    }

    def __init__(self, output_dir: str):
        # Prepare the output index.
        self.output_dir = ensure_output_dir(output_dir)

    def save_intermediate(
        self,
        saturation_mask: np.ndarray,
        cleaned_mask: np.ndarray,
        debug_ellipses: np.ndarray
    ) -> None:
        """It saves the intermediate step images."""
        images = {
            "saturation_mask": saturation_mask,
            "cleaned_mask":    cleaned_mask,
            "debug_ellipses":  debug_ellipses,
        }
        for key, img in images.items():
            path = self.output_dir / self.INTERMEDIATE_FILES[key]
            cv2.imwrite(str(path), img)
            print(f"  [Record] {path.name}")

    def save_final(
        self,
        original: np.ndarray,
        final_mask: np.ndarray
    ) -> None:
        """
        The final binary mask saves the semi-transparent overlay and side-by-side comparison images.
        """
        # ── 1. Binary mask ───────────────────────────────────────────────────
        mask_path = self.output_dir / self.FINAL_FILES["binary_mask"]
        cv2.imwrite(str(mask_path), final_mask)
        print(f"  [Record] {mask_path.name}")

        # ── 2. Overlay (green transparent mask over the original) ──────────────────
        green_layer = np.full_like(original, (0, 200, 0))
        overlay = np.where(
            final_mask[:, :, None] > 0,
            (original * 0.35 + green_layer * 0.65).astype(np.uint8),
            (original * 0.45).astype(np.uint8)
        )
        overlay_path = self.output_dir / self.FINAL_FILES["overlay"]
        cv2.imwrite(str(overlay_path), overlay)
        print(f"  [Record] {overlay_path.name}")

        # ── 3.Side-by-side comparison (original | mask | overlay) ────────────
        mask_bgr = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)
        comparison = np.hstack([original, mask_bgr, overlay])
        comp_path = self.output_dir / self.FINAL_FILES["comparison"]
        cv2.imwrite(str(comp_path), comparison)
        print(f"  [Record] {comp_path.name}")

    def save_all(
        self,
        original: np.ndarray,
        final_mask: np.ndarray,
        saturation_mask: Optional[np.ndarray] = None,
        cleaned_mask: Optional[np.ndarray]    = None,
        debug_ellipses: Optional[np.ndarray]  = None,
        save_intermediate: bool = True
    ) -> None:
        """
        It saves all images. If save_intermediate=False, only the final outputs are saved.
        """
        print("\n[ResultSaver] Images are being saved:")

        if save_intermediate and all(
            x is not None for x in [saturation_mask, cleaned_mask, debug_ellipses]
        ):
            self.save_intermediate(saturation_mask, cleaned_mask, debug_ellipses)

        self.save_final(original, final_mask)
        print(f"\n[ResultSaver] All outputs → {self.output_dir}")


class KiwiSegmentor:
    """
    The orchestrator class that manages the kiwi segmentation pipeline end-to-end.

    Pipeline:
      ImageLoader → BlobDetector → EllipseFitter → GrabCutRefiner → ResultSaver
    """

    def __init__(self, config: SegmentationConfig, image_path: str, output_dir: str):
        self.config     = config
        self.image_path = image_path
        self.output_dir = output_dir

        # Components are created in the constructor and used in run().

        self._loader:   ImageLoader          = ImageLoader(image_path)
        self._saver:    ResultSaver          = ResultSaver(output_dir)

        #Components to be assigned during runtime

        self._detector: Optional[BlobDetector]   = None
        self._fitter:   Optional[EllipseFitter]  = None
        self._refiner:  Optional[GrabCutRefiner] = None

    def run(self) -> np.ndarray:
        """
        It starts the segmentation pipeline and returns the final mask.
        """
        print("=" * 60)
        print("  Kiwi Filtering Launched")
        print("=" * 60)

        # ── 1. Upload image ────────────────────────────────────────────────
        image = self._loader.load()
        shape = (self._loader.height, self._loader.width)

        # ── 2. Blob detection ───────────────────────────────────────────────────
        self._detector = BlobDetector(self.config)
        contours = self._detector.detect(self._loader.hsv)
        print(f"[BlobDetector] {len(contours)} the raw contour was identified.")

        # ── 3. Ellipse fitting + leaf filtration ────────────────────────────
        self._fitter = EllipseFitter(self.config, shape)
        ellipses = self._fitter.fit(contours)

        if not ellipses:
            print("[KiwiSegmentor] ⚠ No kiwi ellipses were found!")
            return np.zeros(shape, dtype=np.uint8)

        # ── 4. Debug image (ellipse numbering) ────────────────────────
        debug_img = self._build_debug_image(image, ellipses)

        # ── 5. GrabCut rafine ─────────────────────────────────────────────────
        print(f"\n[GrabCutRefiner] {len(ellipses)} GrabCut is being applied to kiwi:")
        self._refiner = GrabCutRefiner(self.config, shape)
        final_mask = self._refiner.refine(image, ellipses)

        # ── 6. Save ─────────────────────────────────────────────────────────
        self._saver.save_all(
            original         = image,
            final_mask       = final_mask,
            saturation_mask  = self._detector.saturation_mask,
            cleaned_mask     = self._detector.cleaned_mask,
            debug_ellipses   = debug_img,
            save_intermediate= self.config.save_intermediate
        )

        print("\n" + "=" * 60)
        print(f"  Completed. Number of kiwis identified.: {len(ellipses)}")
        print("=" * 60)
        return final_mask

    def _build_debug_image(
        self,
        image: np.ndarray,
        ellipses: List[KiwiEllipse]
    ) -> np.ndarray:
        """
       It creates a numbered debug image by drawing the detected ellipses onto the original image.
        """
        debug = image.copy()
        for e in ellipses:
            ex, ey = e.center
            ea, eb = e.axes
            # Ellipsi green line
            cv2.ellipse(
                debug,
                ((ex, ey), (ea * self.config.ellipse_scale,
                            eb * self.config.ellipse_scale),
                 e.angle),
                (0, 255, 0), 2
            )
            # central red dot
            cv2.circle(debug, (int(ex), int(ey)), 5, (0, 0, 255), -1)
            # index tag
            cv2.putText(
                debug, str(e.index),
                (int(ex) - 8, int(ey) + 6),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                (255, 255, 0), 2
            )
        return debug