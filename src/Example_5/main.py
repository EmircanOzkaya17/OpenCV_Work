import cv2
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from application_func import ImageProcessor

def main():
    
    image_path = r"C:\OpenCV_Work\src\Example_5\assets\fruits.jpg"
  
    
    try:
        processor = ImageProcessor(image_path)
    except ValueError as e:
        print(f"Eror: {e}")
        print("Please check the path to the image file..")
        return
    
    # Global variables (for trackbar callbacks)
    threshold1 = processor.threshold1
    threshold2 = processor.threshold2
    min_area = processor.min_area
    max_area = processor.max_area
    
    def update_display():
        """Update screen"""
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
    
    # Create window
    cv2.namedWindow('Fruit Counting', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Edge Detection', cv2.WINDOW_NORMAL)
    
    # Adjust window sizes
    cv2.resizeWindow('Fruit Counting', 800, 600)
    cv2.resizeWindow('Edge Detection', 800, 600)
    
    # Create trackbars
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
            
        elif key == ord('r'):  # Reset
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
            processor.save_results()
            
        elif key == ord('n'):  #new image
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
                    processor = ImageProcessor(file_path)
                    update_display()
                    print(f"New image uploaded: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"Eror: {e}")
        
        elif key == ord('+'):  # Zoom in
            scale = min(scale * 1.1, 3.0)
            resize_and_show(scale)
            
        elif key == ord('-'):  # Zoom out
            scale = max(scale * 0.9, 0.5)
            resize_and_show(scale)
    
    
    cv2.destroyAllWindows()

def resize_and_show(scale):
    """Resize and display the image"""
    # This function requires global variables for access from the main loop
    # As an alternative, it can be added to the ImageProcessor class
    pass

if __name__ == "__main__":
    main()