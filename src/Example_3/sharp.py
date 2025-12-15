import cv2
import numpy as np

class ssharpening:
    def __init__(self, image_path="petersburg.jpg"):
        
        self.image = cv2.imread(image_path,0)

        if self.image is None:
            raise ValueError("image not found :  " + image_path)
        
        self.image = cv2.resize(self.image, (250,250))

    def canny(self, image=None):
        if image is None:
            image=self.image

        # Sobel and Laplacian give us "rough" results (thick lines, noise). 
        # Canny, on the other hand, gives us thin, clean, and continuous lines. 
        # It's considered the "Gold Standard of Edge Detection" in image processing.

        # The Logic of the Canny Algorithm (4-Step Process)
        # Canny is not a single operation, but a chain of algorithms. It follows these steps:

        # Noise Reduction (Gaussian Blur): Canny is very sensitive to noise. 
        # Therefore, before starting, it blurs the image slightly (using a 5x5 Gaussian Kernel) to prevent 
        # the "noise" from being mistaken for edges.

        # Gradient Calculation (Sobel Step):

        # Non-Maximum Suppression - Thinning Step: The edges resulting from the Sobel algorithm are thick and blurry. 
        # Canny scans along this thick line, keeping only the peak (the brightest pixel) and removing the rest.

        # Result: Thick edges are converted to single-pixel thin lines.

        # Hysteresis Thresholding - Reasoning Step: This is the most critical part. Two threshold values ​​(thresholds) are determined: 
        # MinVal and MaxVal.        

        canny_edges = cv2.Canny(image, threshold1=100, threshold2=200)
        # Critical Point: Threshold Values ​​(100 and 200)
        #The threshold1 and threshold2 parameters you'll see in the code determine Canny's character:

        # Narrowing the Range (e.g., 50 - 100): It treats too much detail and noise as edges. The image becomes more complex.

        # Increasing the Range (e.g., 150 - 250): It draws only very distinct outlines and loses fine details.

        # It's perfect for "object detection" and "shape analysis" rather than "sharpening".
        return canny_edges
    
    def kernel(self,image=None):
        if image is None:
            image=self.image
        # It uses a mathematical process called convolution to make edges and details more distinct.
        # The kernel increases the contrast between the central pixel and its neighbors 
        # by changing the values ​​of the pixels it overlays.
        kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
        sharp_image = cv2.filter2D(image, -1, kernel) 

        return sharp_image

    def laplacian(self,image=None):
        if image is None:
            image=self.image

        # The Laplacian operator is based on the second derivative logic in the image.
        # A standard 3x3 Laplacian kernel that performs this calculation is as follows:
        # [ [0,1,0] , [1,-4,1] , [0,1,0] ]

        # Working Principle:
        # Multiplies the center pixel by a negative coefficient (e.g., -4).
        # Multiplies neighboring pixels by a positive coefficient (+1).
        # If the center pixel and its neighbors are the same color (solid area), the result is 0.
        # If there is a difference (edge), the result is a large value other than 0. 
        
        # Laplacian Implementation
        # ddepth=cv2.CV_64F: We use 64-bit float to avoid losing negative values.
        # ksize=3: Use a 3x3 kernel (mask).
        laplacian = cv2.Laplacian(src=image, ddepth=cv2.CV_64F, ksize=3)  

        # Converting to Absolute Value
        # We convert negative derivative values ​​to positive and convert them to uint8 (0-255) format.
        laplacian_abs = cv2.convertScaleAbs(laplacian)  


        # Sharpening Process
        # Logic: Original Image - (Coefficient * Laplacian Edges)
        # Since the center of our Laplacian kernel is negative, we are subtracting here.
        # So, negative and negative come together to create an additive effect, strengthening the central pixel.
        sharpened_image = cv2.addWeighted(image, 1.5, laplacian_abs, -0.5, 0) 
        laplacian_norm = cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX)
        laplacian_norm = np.uint8(laplacian_norm) 

        return sharpened_image
    
    def sobel(self,image=None):
        if image is None:
            image=self.image
        # Sobel looks at the 1st derivative
        # Sobel is more robust to noise than Laplacian
        # Sobel also has a Gaussian smoothing embedded in it when taking derivatives. 
        # Therefore, it is more robust to noise than Laplacian.
        # The biggest difference of Sobel is that it is Directional.
        # Horizontal Derivative (G_x) = [ [-1,0-1] , [-2,0,2] , [-1,0,1] ]
        # Vertical Derivative (G_y) = [ [-1,-2,-1] , [0,0,0] , [1,2,1] ]

        # dx=1, dy=0 -> Derivative only in the X direction (Vertical edges)
        # dx=0, dy=1 -> Derivative only in the Y direction (Horizontal edges)
        # ksize=3 -> 3x3 kernel

        sobel_x = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
        sobel_y = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)

        # Converting to Absolute Value
        # We convert negative slopes (white to black) to positive.

        abs_sobel_x = cv2.convertScaleAbs(sobel_x)
        abs_sobel_y = cv2.convertScaleAbs(sobel_y)

        # Combining Two Directions (Gradient Magnitude)
        # Approximate method: Add the two weighted (faster)
        combined_sobel = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)

        return combined_sobel
    
    def unsharp_masking(self,image=None): 
        if image is None:
            image=self.image
        # We can actually think of this method not as a formula, but as a three-stage logical chain:
        # Blur: First, we create a blurred copy of the original image. (This is where the name "Unsharp Mask" comes from.)
        # Subtraction: We mathematically subtract this blurred copy from the original image.
        # Addition: We add the result of this subtraction to the original image.
        # First we get a blurred version of the original image

        g_blurring=cv2.GaussianBlur(image,(9,9),0)

        sharp_image = cv2.addWeighted(image, 1.5, g_blurring, -0.5, 0)
        return sharp_image
