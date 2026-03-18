"""
main.py
-------
The entry point for the Kiwi filtering application.
Reads configuration parameters from the .env file,
creates SegmentationConfig, and starts the KiwiSegmentor pipeline.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
import os

# Add the project root directory to the Python path (to access the src module)
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from src.app_func import KiwiSegmentor, SegmentationConfig


def load_config() -> tuple[SegmentationConfig, str, str]:
    """
    Loads the .env file and returns the application configuration. 
    Defaults are used for missing or incorrect values.
    """
    # Upload the .env file — it must be in the same directory as main.py.
    env_path = ROOT_DIR / ".env"
    if not env_path.exists():
        print(f"[Warning] .env file not found: {env_path}")
        print("[Warning] Default values ​​will be used.")
    load_dotenv(dotenv_path=env_path)

    # ── File paths ──────────────────────────────────────────────────────────
    image_path  = os.getenv("IMAGE_PATH",  "kiwi.jpg")
    output_dir  = os.getenv("OUTPUT_DIR",  "results")

    # ── Segmentation parameters ─────────────────────────────────────────────
    config = SegmentationConfig(
        # Saturation threshold: distinguishes marble background (S≈5-13) from kiwi (S≈100-255).
        saturation_threshold  = int(os.getenv("SATURATION_THRESHOLD",  "55")),

        # Minimum area: blobs smaller than this ratio of total pixels create leaf/noise.
        min_area_ratio        = float(os.getenv("MIN_AREA_RATIO",       "0.009")),

        # Maximum aspect ratio: leaves long-thin → high ratio → sifted
        max_aspect_ratio      = float(os.getenv("MAX_ASPECT_RATIO",     "2.0")),

        # Convex hull circularity threshold: kiwi ~0.96, elongated shapes lower.
        min_hull_circularity  = float(os.getenv("MIN_HULL_CIRCULARITY", "0.40")),

        # Ellipse expansion: compensates for edge pixel loss.
        ellipse_scale         = float(os.getenv("ELLIPSE_SCALE",        "1.06")),

        # GrabCut iteration count: more = more precise but slower.
        grabcut_iterations    = int(os.getenv("GRABCUT_ITERATIONS",     "4")),

        # GrabCut edge buffer (px): width of the indeterminate region around the ellipse
        grabcut_border_px     = int(os.getenv("GRABCUT_BORDER_PX",      "18")),

        # Save intermediate images: True → debug images are also written to disk.
        save_intermediate     = os.getenv("SAVE_INTERMEDIATE", "True").lower() == "true",
    )

    return config, image_path, output_dir


def main() -> None:
    """
    Main application flow:
    1. Load configuration from .env
    2. Create KiwiSegmentor
    3. Run Pipeline
    """
    
    config, image_path, output_dir = load_config()

    print(f"[main] Image  : {image_path}")
    print(f"[main] Output    : {output_dir}")
    print(f"[main] Parameters:")
    print(f"       saturation_threshold  = {config.saturation_threshold}")
    print(f"       min_area_ratio        = {config.min_area_ratio}")
    print(f"       max_aspect_ratio      = {config.max_aspect_ratio}")
    print(f"       min_hull_circularity  = {config.min_hull_circularity}")
    print(f"       ellipse_scale         = {config.ellipse_scale}")
    print(f"       grabcut_iterations    = {config.grabcut_iterations}")
    print(f"       grabcut_border_px     = {config.grabcut_border_px}")
    print(f"       save_intermediate     = {config.save_intermediate}")

    # Start the segmentation pipeline.
    segmentor = KiwiSegmentor(
        config     = config,
        image_path = image_path,
        output_dir = output_dir,
    )

    try:
        segmentor.run()
    except FileNotFoundError as err:
        print(f"\n[Error] {err}")
        print("[Error] Check the IMAGE_PATH value in the .env file.")
        sys.exit(1)
    except Exception as err:
        print(f"\n[Unexpected Error] {err}")
        raise


if __name__ == "__main__":
    main()