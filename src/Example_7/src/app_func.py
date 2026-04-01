"""
Kiwi filtreleme işlemlerini gerçekleştiren sınıf modülü.
Tüm görüntü işleme adımları KiwiFilter sınıfı içinde tanımlanmıştır.
"""

import os
import cv2
import numpy as np

class KiwiFilter:
    def __init__(self, output_dir: str = None):
        
        self.output_dir = output_dir
        if self.output_dir:
            if self.output_dir.lower().endswith(('.jpg', '.jpeg', '.png')):
                self.output_dir = os.path.dirname(self.output_dir)
            
            # Klasör yoksa oluştur
            os.makedirs(self.output_dir, exist_ok=True)
            
        self._step_counter = 1

    def _save_step(self, image: np.ndarray, step_name: str) -> None:
        """Her adımdan sonra görüntüyü ilgili isimle otomatik kaydeder."""
        if not self.output_dir:
            return
        
        filename = f"{self._step_counter:02d}_{step_name}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        cv2.imwrite(filepath, image)
        self._step_counter += 1

    # ── Görüntü Okuma / Yazma ─────────────────────────────────────────────────

    def load_image(self, image_path: str) -> np.ndarray:
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Image could not be read: {image_path}")
        
        self._save_step(image, "original_bgr")
        return image

    def save_image(self, image: np.ndarray, output_path: str) -> None:
        if os.path.isdir(output_path):
            output_path = os.path.join(output_path, "final_output.jpg")
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        cv2.imwrite(output_path, image)

    # ── Renk Uzayı Dönüşümü ──────────────────────────────────────────────────

    def convert_to_hsv(self, bgr_image: np.ndarray) -> np.ndarray:
        hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        self._save_step(hsv, "hsv_conversion")
        return hsv

    # ── Yeşil / Sarımsı Maske ────────────────────────────────────────────────

    def create_green_mask(self, hsv_image: np.ndarray, h_min: int, h_max: int, s_min: int, s_max: int, v_min: int, v_max: int) -> np.ndarray:
        lower_bound = np.array([h_min, s_min, v_min], dtype=np.uint8)
        upper_bound = np.array([h_max, s_max, v_max], dtype=np.uint8)
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        
        self._save_step(mask, "raw_mask")
        return mask

    def apply_mask(self, hsv_image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        masked_hsv = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
        self._save_step(masked_hsv, "masked_hsv")
        return masked_hsv

    # ── Morfolojik İşlemler ───────────────────────────────────────────────────

    def apply_morphology(self, mask: np.ndarray, kernel_size: int, open_iterations: int, close_iterations: int, erode_iterations: int) -> np.ndarray:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        
        # 1. Açma
        opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=open_iterations)
        self._save_step(opened, "morphology_01_opening")
        
        # 2. Kapama
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel, iterations=close_iterations)
        self._save_step(closed, "morphology_02_closing")
        
        #  Kapama sonrası Aşındırma (Erosion)
        if erode_iterations > 0:
            eroded = cv2.erode(closed, kernel, iterations=erode_iterations)
            self._save_step(eroded, "morphology_03_erosion")
            return eroded
            
        return closed

    # ── Kontur Tespiti ve Çizimi ──────────────────────────────────────────────

    def find_kiwi_contours(self, refined_mask: np.ndarray, min_area: float, max_area: float, circularity_threshold: float, convexity_threshold: float) -> list:
        contours, _ = cv2.findContours(refined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if not (min_area <= area <= max_area):
                continue

            perimeter = cv2.arcLength(contour, closed=True)
            if perimeter == 0:
                continue

            circularity = (4 * np.pi * area) / (perimeter ** 2)

            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            convexity = area / hull_area if hull_area > 0 else 0

            if circularity >= circularity_threshold or convexity >= convexity_threshold:
                valid_contours.append(contour)

        return valid_contours

    def draw_contours_on_black(self, original_bgr: np.ndarray, contours: list) -> np.ndarray:
        canvas = np.zeros_like(original_bgr)

        filled_mask = np.zeros(original_bgr.shape[:2], dtype=np.uint8)
        cv2.drawContours(filled_mask, contours, contourIdx=-1, color=255, thickness=cv2.FILLED)
        canvas[filled_mask == 255] = (255, 255, 255)

        cv2.drawContours(canvas, contours, contourIdx=-1, color=(0, 255, 0), thickness=2)
        
        self._save_step(canvas, "result_drawing")
        return canvas