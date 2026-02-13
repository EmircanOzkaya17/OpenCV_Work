import cv2
import numpy as np
import os

class ImageProcessor:
    def __init__(self, image_path):
        """Launch the image processor class"""
        self.image_path = image_path
        self.original = None
        self.gray = None
        self.blurred = None
        self.edges = None
        self.processed_image = None
        
        # Default parameters
        self.threshold1 = 100
        self.threshold2 = 200
        self.min_area = 500
        self.max_area = 50000
        
        
        self.load_image()
    
    def load_image(self):
        
        if not os.path.exists(self.image_path):
            raise ValueError(f"No images found: {self.image_path}")
        
        self.original = cv2.imread(self.image_path)
        if self.original is None:
            raise ValueError(f"Could not load image: {self.image_path}")
        
        self.gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        self.blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)
        self.processed_image = self.original.copy()
    
    def apply_canny(self):
        """Apply Canny edge detection."""
        self.edges = cv2.Canny(self.blurred, self.threshold1, self.threshold2)
        return self.edges
    
    def detect_and_count_fruits(self):
        """Identify, count, and number the fruits."""
    
        edges = self.apply_canny()

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self.processed_image = self.original.copy()
        
        fruit_count = 0
        fruit_contours = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Apply area filter
            if self.min_area < area < self.max_area:
                fruit_count += 1
                fruit_contours.append(contour)
                
                cv2.drawContours(self.processed_image, [contour], -1, (0, 255, 0), 2)

                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    cv2.putText(self.processed_image, str(fruit_count), (cX, cY),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Add information text
        self.add_info_text(fruit_count)
        
        return fruit_count, fruit_contours, self.processed_image, edges
    
    def add_info_text(self, fruit_count):
       
        # Draw a rectangle for the background.
        cv2.rectangle(self.processed_image, (5, 5), (350, 95), (50, 50, 50), -1)
        cv2.rectangle(self.processed_image, (5, 5), (350, 95), (255, 255, 255), 1)
        
        # Write the number of fruits
        cv2.putText(self.processed_image, f"Number of Fruits: {fruit_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        cv2.putText(self.processed_image, f"Th1: {self.threshold1} Th2: {self.threshold2}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 100), 2)
        cv2.putText(self.processed_image, f"Area: {self.min_area}-{self.max_area}", 
                   (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 100), 2)
    
    def update_parameters(self, threshold1=None, threshold2=None, min_area=None, max_area=None):
        """Update processing parameters."""
        if threshold1 is not None:
            self.threshold1 = threshold1
        if threshold2 is not None:
            self.threshold2 = threshold2
        if min_area is not None:
            self.min_area = min_area
        if max_area is not None:
            self.max_area = max_area
    
    def reset_parameters(self):
        """Reset parameters to default values."""
        self.threshold1 = 100
        self.threshold2 = 200
        self.min_area = 500
        self.max_area = 50000
    
    def save_results(self, output_path=None):
        """Save results"""
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            output_path = f"{base_name}_results.jpg"
        
        cv2.imwrite(output_path, self.processed_image)
        cv2.imwrite(f"edge_{output_path}", self.edges)
        print(f"Results recorded: {output_path} and edge_{output_path}")


