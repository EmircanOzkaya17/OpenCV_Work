import cv2
import sys
import os
from dotenv import load_dotenv  

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from application_func import ImageProcessor

def main():
   
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Upload the .env file
    dotenv_path = os.path.join(base_dir, '.env')
    load_dotenv(dotenv_path)
    
    # --- Specify image path ---
    default_image = os.path.join(base_dir, 'assets', 'fruits.jpg')
    env_image = os.getenv('IMAGE_PATH', '')
    
    if env_image:
        if os.path.isabs(env_image):
            image_path = env_image
        else:
            
            image_path = os.path.join(base_dir, env_image)
    else:
        image_path = default_image
    
    # --- Read numerical parameters from environmental variables. ---
    def get_int_env(key, default):
        val = os.getenv(key)
        if val is not None:
            try:
                return int(val)
            except ValueError:
                print(f"Warning: {key} It must be a numerical value, default ({default}) is being used.")
        return default
    
    threshold1 = get_int_env('THRESHOLD1', 100)
    threshold2 = get_int_env('THRESHOLD2', 200)
    min_area   = get_int_env('MIN_AREA', 500)
    max_area   = get_int_env('MAX_AREA', 50000)
    
    
    output_dir = os.getenv('OUTPUT_DIR', base_dir)
    if not os.path.isabs(output_dir):
        output_dir = os.path.join(base_dir, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # --- Start ImageProcessor ---
    try:
        processor = ImageProcessor(
            image_path=image_path,
            threshold1=threshold1,
            threshold2=threshold2,
            min_area=min_area,
            max_area=max_area
        )
    except ValueError as e:
        print(f"Error: {e}")
        print("Please check the path to the image file.")
        return
    
    # Global variables 
    threshold1 = processor.threshold1
    threshold2 = processor.threshold2
    min_area = processor.min_area
    max_area = processor.max_area
    
    def update_display():
        """Update screen."""
        try:
            fruit_count, _, processed_img, edges = processor.detect_and_count_fruits()
            cv2.imshow('Edge Detection', edges)
            cv2.imshow('Fruit Counting', processed_img)
        except Exception as e:
            print(f"Image processing error: {e}")
    
    # Trackbar callback functions
    def update_threshold1(val):
        nonlocal threshold1
        threshold1 = val
        processor.update_parameters(threshold1=val)
        update_display()
    
    def update_threshold2(val):
        nonlocal threshold2
        threshold2 = val
        processor.update_parameters(threshold2=val)
        update_display()
    
    def update_min_area(val):
        nonlocal min_area
        min_area = val
        processor.update_parameters(min_area=val)
        update_display()
    
    def update_max_area(val):
        nonlocal max_area
        max_area = val
        processor.update_parameters(max_area=val)
        update_display()
    
   
    cv2.namedWindow('Fruit Counting', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Edge Detection', cv2.WINDOW_NORMAL)
    
   
    cv2.resizeWindow('Fruit Counting', 800, 600)
    cv2.resizeWindow('Edge Detection', 800, 600)
    
    
    cv2.createTrackbar('Canny Th1', 'Fruit Counting', threshold1, 500, update_threshold1)
    cv2.createTrackbar('Canny Th2', 'Fruit Counting', threshold2, 500, update_threshold2)
    cv2.createTrackbar('Min Area', 'Fruit Counting', min_area, 5000, update_min_area)
    cv2.createTrackbar('Max Area', 'Fruit Counting', max_area, 100000, update_max_area)
    
    
    update_display()
    
    scale = 1.0
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):  
            break
            
        elif key == ord('r'):  
            processor.reset_parameters()
            threshold1 = processor.threshold1
            threshold2 = processor.threshold2
            min_area = processor.min_area
            max_area = processor.max_area
            
            cv2.setTrackbarPos('Canny Th1', 'Fruit Counting', threshold1)
            cv2.setTrackbarPos('Canny Th2', 'Fruit Counting', threshold2)
            cv2.setTrackbarPos('Min Area', 'Fruit Counting', min_area)
            cv2.setTrackbarPos('Max Area', 'Fruit Counting', max_area)
            
            update_display()
            print("Settings have been reset!")
            
        elif key == ord('s'):  # Save
            # Save the output to the specified folder.
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            out_path = os.path.join(output_dir, f"{base_name}_results.jpg")
            processor.save_results(out_path)
            
        elif key == ord('n'): 
            import tkinter as tk
            from tkinter import filedialog
            
            root = tk.Tk()
            root.withdraw()
            
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
            )
            
            if file_path:
                try:
                    # Rebuild the processor for the new image (with the current parameters)
                    processor = ImageProcessor(
                        image_path=file_path,
                        threshold1=threshold1,
                        threshold2=threshold2,
                        min_area=min_area,
                        max_area=max_area
                    )
                    update_display()
                    print(f"New image uploaded: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif key == ord('+'):  
            scale = min(scale * 1.1, 3.0)
            # resize_and_show fonksiyonu şimdilik pasif
            print(f"Zoom: {scale:.2f}")
            
        elif key == ord('-'):  
            scale = max(scale * 0.9, 0.5)
            print(f"Removal: {scale:.2f}")
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()