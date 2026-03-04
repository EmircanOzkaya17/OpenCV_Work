import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class HistogramProcessing:
    
    
    def __init__(self, image_path):
        
        self.image_path = image_path
        self.original_image = self._load_grayscale()
        self.equalized_image = None

    def _load_grayscale(self):
        
        img = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Image could not be loaded: {self.image_path}")
        return img

    def compute_histogram(self, image):
        
        hist = cv2.calcHist([image], [0], None, [256], [0, 256])
        return hist.flatten()

    def equalize_histogram(self):
        """It performs histogram equalization."""
        self.equalized_image = cv2.equalizeHist(self.original_image)
        return self.equalized_image

    def plot_comparison(self, save_path):
       
        if self.equalized_image is None:
            self.equalize_histogram()

       
        hist_orig = self.compute_histogram(self.original_image)
        hist_eq = self.compute_histogram(self.equalized_image)

        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle("Histogram Equalization Comparison", fontsize=16)

        # Original Image
        axes[0, 0].imshow(self.original_image, cmap='gray')
        axes[0, 0].set_title("Original Image")
        axes[0, 0].axis('off')

        
        axes[0, 1].imshow(self.equalized_image, cmap='gray')
        axes[0, 1].set_title("Histogram Synchronized")
        axes[0, 1].axis('off')

        # original histogram
        axes[1, 0].plot(hist_orig, color='black')
        axes[1, 0].set_title("Original Histogram")
        axes[1, 0].set_xlim([0, 256])

        # Synchronized histogram
        axes[1, 1].plot(hist_eq, color='black')
        axes[1, 1].set_title("Synchronized Histogram")
        axes[1, 1].set_xlim([0, 256])

        plt.tight_layout()
        # Save
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Comparison image saved: {save_path}")

    def process_and_save(self, save_path):
        
        self.equalize_histogram()
        self.plot_comparison(save_path)