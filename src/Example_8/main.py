import os
import sys

# --- main.py'nin bulundugu klasoru yola ekle ---
# Boylece 'src' paketi, hangi dizinden calistirilirsa calistirilsin bulunur
# ve ust seviyedeki diger 'src' klasorleriyle cakismaz.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import dotenv_values

# Modulu dogrudan ice aktariyoruz; bu, src/__init__.py'nin yeniden
# disa aktarmasina bagli kalmadan calisir.
from src.orb_matcher import ORBMatcher


def load_config() -> dict:
    """main.py ile ayni klasordeki .env dosyasini okur."""
    env_path = os.path.join(BASE_DIR, ".env")
    if not os.path.exists(env_path):
        raise RuntimeError(f".env dosyasi bulunamadi: {env_path}")

    config = dotenv_values(env_path)
    if not config:
        raise RuntimeError(".env dosyasi bos.")

    
    if not os.path.isabs(config["RESULTS_DIR"]):
        config["RESULTS_DIR"] = os.path.join(BASE_DIR, config["RESULTS_DIR"])

    return config


def main():
    # 1) Ayarlari yukle
    config = load_config()

    # 2) Matcher'i kur
    matcher = ORBMatcher(config)

    # 3) Gorselleri yukle (gri tonlama ORB icin, renkli cizim icin)
    img1_gray = matcher.load_image(config["IMAGE_1_PATH"], grayscale=True)
    img2_gray = matcher.load_image(config["IMAGE_2_PATH"], grayscale=True)
    img1_color = matcher.load_image(config["IMAGE_1_PATH"], grayscale=False)
    img2_color = matcher.load_image(config["IMAGE_2_PATH"], grayscale=False)

    # 4) ORB keypoint + descriptor cikar
    kp1, desc1 = matcher.detect_and_compute(img1_gray)
    kp2, desc2 = matcher.detect_and_compute(img2_gray)
    print(f"[ORB] 1. gorsel: {len(kp1)} keypoint")
    print(f"[ORB] 2. gorsel: {len(kp2)} keypoint")

    # 5) Keypoint gorsellerini kaydet
    kp_img1 = matcher.draw_keypoints(img1_color, kp1)
    kp_img2 = matcher.draw_keypoints(img2_color, kp2)
    path_kp1 = matcher.save_result(kp_img1, config["KEYPOINTS_1_OUTPUT_NAME"])
    path_kp2 = matcher.save_result(kp_img2, config["KEYPOINTS_2_OUTPUT_NAME"])
    print(f"[KAYIT] {path_kp1}")
    print(f"[KAYIT] {path_kp2}")

    # 6) Eslestir
    matches = matcher.match_descriptors(desc1, desc2)
    print(f"[BFMatcher] Toplam {len(matches)} eslesme bulundu")

    # 7) Eslesmeleri ciz ve kaydet
    limit = int(config["MATCHES_TO_DRAW"])
    matched_img = matcher.draw_matches(
        img1_color, kp1, img2_color, kp2, matches, limit=limit
    )
    path_matches = matcher.save_result(matched_img, config["MATCHES_OUTPUT_NAME"])
    print(f"[KAYIT] En iyi {min(limit, len(matches))} eslesme -> {path_matches}")

    print("\nIslem tamamlandi. Sonuclar 'results/' klasorunde.")


if __name__ == "__main__":
    main()