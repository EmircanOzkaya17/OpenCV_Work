import os
from dotenv import load_dotenv
from src.app_func import HistogramProcessing

def main():
    # .env dosyasını yükle
    load_dotenv()

    img_path = os.getenv("IMG_PATH")
    results_path = os.getenv("RESULTS_PATH")

    if not img_path or not results_path:
        print("Error: .IMG_PATH and RESULTS_PATH must be defined in the env file..")
        return

    
    output_file = os.path.join(results_path, "histogram_comparison.png")

    
    processor = HistogramProcessing(img_path)

    
    processor.process_and_save(output_file)

if __name__ == "__main__":
    main()