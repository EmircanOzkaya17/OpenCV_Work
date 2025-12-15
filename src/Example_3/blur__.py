import cv2
import numpy as np

class blurring:
    def __init__(self, image_path="swartz.jpg"):
        
        self.image = cv2.imread(image_path)

        if self.image is None:
            raise ValueError("image not found :  " + image_path)
        
        self.image = cv2.resize(self.image, (300, 300))

    def average(self,image=None):
        if image is None:
            image = self.image
        # Every pixel covered by the kernel is affected equally
        kernel = np.ones((5,5),np.float32)/25

         # All elements of the matrix are 1. Multiplication coefficient of 25 matrices
         # This is a method to create a kernel 
        return cv2.filter2D(image, -1, kernel)

        # Or you can directly apply the process as follows
        # blurring_2=cv2.blur(image, (5,5))

    def bilateral(self,image=None):
        if image is None:
            image = self.image

        # The bilateral filter is "selective." It processes not only nearby pixels but also pixels with similar color values. 
        #(image, Neighborhood diameter,  sigmaColor, sigmaSpace)
        # sigmaColor=75: Color mixing tolerance
        # sigmaSpace=75: Area of ​​effect of distant pixels        
        return cv2.bilateralFilter(image, 9, 75, 75)
        
    def gaussian(self,image=None):
        if image is None:
            image = self.image
        # The values ​​of the kernel matrix's central elements are high, and the values ​​decrease as you move away from the center.
        # Example -->> [ [1, 2, 1] , [2, 4, 2] , [1, 2, 1] ]
        # This allows the pixel in the center of the image to be multiplied by a larger factor.
        # If the sum of the elements of the kernel matrix is ​​N, the kernel is multiplied by 1/N.
        
        return cv2.GaussianBlur(image,(9,9),0)
        # (image, (kernel_width, kernel_height)
        # We usually write 0 instead of sigmaX, in which case OpenCV says 
        # "You wrote 0, but I will calculate the optimal standard deviation myself, looking at the kernel size."

    def median(self, image=None):
        if image is None:
            image = self.image
        # It is especially effective against noise consisting of black and white dots, which we call "Salt and Pepper".
        #Median Blurring sorts the pixels under the kernel and selects the value in the exact middle.

        # Since the kernel must be a square, the 5 here represents the length of one side of the square.
        return cv2.medianBlur(image,5)
    
    