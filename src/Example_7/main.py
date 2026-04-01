import os
import sys

from dotenv import load_dotenv

# .env dosyasının tam yolunu oluştur ve garantili şekilde yükle
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)

# src klasörünü Python yoluna ekle
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from app_func import KiwiFilter


def _get_env_int(key: str, default: int) -> int:
    return int(os.getenv(key, default))


def _get_env_float(key: str, default: float) -> float:
    return float(os.getenv(key, default))


def main() -> None:
    # ── 1. Parametreleri .env'den oku ─────────────────────────────────────────
    input_path  = os.getenv("INPUT_IMAGE_PATH",  "kiwi.jpg")
    output_path = os.getenv("OUTPUT_IMAGE_PATH", "output.jpg")

    # KRİTİK NOKTA: Sınıfı başlatırken output_path'i içeri gönderiyoruz.
    # Böylece her adımda nereye kayıt yapacağını biliyor.
    kf = KiwiFilter(output_dir=output_path)

    h_min = _get_env_int("HSV_H_MIN", 25)
    h_max = _get_env_int("HSV_H_MAX", 85)
    s_min = _get_env_int("HSV_S_MIN", 40)
    s_max = _get_env_int("HSV_S_MAX", 255)
    v_min = _get_env_int("HSV_V_MIN", 110)
    v_max = _get_env_int("HSV_V_MAX", 255)

    kernel_size      = _get_env_int("MORPH_KERNEL_SIZE",       5)
    open_iterations  = _get_env_int("MORPH_OPEN_ITERATIONS",   2)
    close_iterations = _get_env_int("MORPH_CLOSE_ITERATIONS",  3)
    erode_iterations = _get_env_int("MORPH_ERODE_ITERATIONS",  1)

    min_area              = _get_env_float("CONTOUR_MIN_AREA",               1000)
    max_area              = _get_env_float("CONTOUR_MAX_AREA",             500000)
    circularity_threshold = _get_env_float("CONTOUR_CIRCULARITY_THRESHOLD",   0.45)
    convexity_threshold   = _get_env_float("CONTOUR_CONVEXITY_THRESHOLD",     0.65)

    # ── 2. Görüntüyü oku ve HSV'ye dönüştür ──────────────────────────────────
    print(f"[1/5] Görüntü okunuyor: {input_path}")
    bgr_image = kf.load_image(input_path)

    print("[2/5] BGR → HSV dönüşümü yapılıyor...")
    hsv_image = kf.convert_to_hsv(bgr_image)

    # ── 3. Yeşil/sarımsı maske oluştur ve uygula ─────────────────────────────
    print(f"[3/5] HSV maskesi oluşturuluyor (V_MIN={v_min} → yaprak eleme)...")
    mask = kf.create_green_mask(hsv_image, h_min, h_max, s_min, s_max, v_min, v_max)
    _ = kf.apply_mask(hsv_image, mask)

    # ── 4. Morfolojik açma + kapama ──────────────────────────────────────────
    print("[4/5] Morfolojik işlemler (açma + kapama + aşındırma) uygulanıyor...")
    refined_mask = kf.apply_morphology(mask, kernel_size, open_iterations, close_iterations, erode_iterations)

    # ── 5. Kontur tespiti ve siyah arka plan üzerine çizim ───────────────────
    print("[5/5] Konturlar tespit ediliyor (circ OR conv filtresi)...")
    contours = kf.find_kiwi_contours(
        refined_mask, min_area, max_area,
        circularity_threshold, convexity_threshold
    )
    print(f"      → {len(contours)} geçerli kiwi konturu bulundu.")

    result = kf.draw_contours_on_black(bgr_image, contours)

    # ── 6. Sonucu kaydet (GEREKSİZ OLDUĞU İÇİN SİLDİK) ────────────────────────
    # kf.save_image(result, output_path)  <-- Bu satırı tamamen kaldırdık
    print(f"\n✓ İşlem tamamlandı. Tüm adımlar '{output_path}' dizinine kaydedildi.")


if __name__ == "__main__":
    main()