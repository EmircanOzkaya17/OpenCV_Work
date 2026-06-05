"""
orb_matcher.py
--------------
Aynı alanın iki farklı açıdan çekilmiş görselleri üzerinde:
  1. ORB ile keypoint ve descriptor çıkarma
  2. BFMatcher ile eşleştirme
  3. cv2.drawMatches ile sonuçları çizme

"""

import os
import cv2


_NORM_TYPES = {
    "NORM_HAMMING": cv2.NORM_HAMMING,
    "NORM_HAMMING2": cv2.NORM_HAMMING2,
    "NORM_L1": cv2.NORM_L1,
    "NORM_L2": cv2.NORM_L2,
}


class ORBMatcher:
    """ORB + BFMatcher tabanlı görsel eşleştirme iş akışını yöneten sınıf."""

    def __init__(self, config: dict):
        
        self.config = config

        # --- ORB dedektörü ---
        self.orb = cv2.ORB_create(
            nfeatures=int(config["ORB_N_FEATURES"]),
            scaleFactor=float(config["ORB_SCALE_FACTOR"]),
            nlevels=int(config["ORB_N_LEVELS"]),
            edgeThreshold=int(config["ORB_EDGE_THRESHOLD"]),
            patchSize=int(config["ORB_PATCH_SIZE"]),
            fastThreshold=int(config["ORB_FAST_THRESHOLD"]),
        )

        # --- BFMatcher ---
        norm_type = _NORM_TYPES.get(config["BF_NORM_TYPE"], cv2.NORM_HAMMING)
        cross_check = str(config["BF_CROSS_CHECK"]).strip().lower() == "true"
        self.matcher = cv2.BFMatcher(norm_type, crossCheck=cross_check)

        
        os.makedirs(config["RESULTS_DIR"], exist_ok=True)

    # ------------------------------------------------------------------
    #  1) Görsel yükleme
    # ------------------------------------------------------------------
    def load_image(self, path: str, grayscale: bool = True):
        """
        Verilen yoldan görseli okur.
        grayscale=True ise ORB için gri tonlamalı döndürür.
        Dosya bulunamazsa anlamlı bir hata fırlatır.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Görsel bulunamadi: {path}")

        flag = cv2.IMREAD_GRAYSCALE if grayscale else cv2.IMREAD_COLOR
        image = cv2.imread(path, flag)

        if image is None:
            raise ValueError(f"Görsel okunamadi (bozuk veya desteklenmeyen format): {path}")
        return image

    # ------------------------------------------------------------------
    #  2) Keypoint ve descriptor çıkarma (ORB)
    # ------------------------------------------------------------------
    def detect_and_compute(self, image):
        """
        ORB ile görselden keypoint'leri ve descriptor'ları çıkartma.
        Dönüş: (keypoints, descriptors)
        """
        keypoints, descriptors = self.orb.detectAndCompute(image, None)
        return keypoints, descriptors

    # ------------------------------------------------------------------
    #  3) Descriptor eşleştirme (BFMatcher)
    # ------------------------------------------------------------------
    def match_descriptors(self, desc1, desc2):
        """
        İki descriptor kümesini BFMatcher ile eşleştirir.
        Eşleşmeleri mesafeye göre (en iyiden kötüye) sıralayarak döndürür.
        """
        if desc1 is None or desc2 is None:
            raise ValueError("Descriptor'lar bos; görsellerde yeterli özellik bulunamadi.")

        matches = self.matcher.match(desc1, desc2)
        matches = sorted(matches, key=lambda m: m.distance)
        return matches

    # ------------------------------------------------------------------
    #  4) Keypoint'leri tek görsel üzerine çizme
    # ------------------------------------------------------------------
    def draw_keypoints(self, image, keypoints):
        """Tek bir görsel üzerine tespit edilen keypoint'leri çizer."""
        return cv2.drawKeypoints(
            image,
            keypoints,
            None,
            color=(0, 255, 0),
            flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
        )

    # ------------------------------------------------------------------
    #  5) Eşleşmeleri iki görsel arasında çizme
    # ------------------------------------------------------------------
    def draw_matches(self, img1, kp1, img2, kp2, matches, limit=None):
        """
        cv2.drawMatches ile iki görsel arasındaki eşleşmeleri çizer.
        limit: çizilecek en iyi eşleşme sayısı (None ise hepsi).
        """
        if limit is not None:
            matches = matches[:limit]

        matched_img = cv2.drawMatches(
            img1, kp1,
            img2, kp2,
            matches, None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
        )
        return matched_img

    # ------------------------------------------------------------------
    #  6) Sonucu kaydetme
    # ------------------------------------------------------------------
    def save_result(self, image, filename: str) -> str:
        """
        Verilen görseli RESULTS_DIR altına belirtilen isimle kaydeder.
        Kaydedilen dosyanın tam yolunu döndürür.
        """
        output_path = os.path.join(self.config["RESULTS_DIR"], filename)
        cv2.imwrite(output_path, image)
        return output_path
