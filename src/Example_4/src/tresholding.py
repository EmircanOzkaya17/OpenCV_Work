import cv2 

class Tresholding:
    def __init__(self, image_path=r"C:\OpenCV_Work\assets\rose.jpg"):
        
        self.image = cv2.imread(image_path,0)

        if self.image is None:
            raise ValueError("image not found :  " + image_path)

        self.image = cv2.resize(self.image, (400, 400))

    def binary_tresholding(self,image=None):
        # A specific threshold is selected. Each pixel in the image is compared to this value;
        # if the pixel value is greater than the threshold, it is assigned a value (usually 255 - white), 
        # and if it is smaller, it is assigned another value (usually 0 - black).
        if image is None:
            image = self.image

        ret, threshold_image = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY) # image, threshold value, max value, type

        return threshold_image
    
    def otsu_tresholding(self,image=None):
        if image is None:
            image=self.image
        # Instead of manually selecting the threshold value through trial and error, 
        # it is an intelligent method that automatically determines it by looking at the statistical data of the image.    
        ret, otsu_img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # We enter 0 in the threshold value section (because Otsu will find the value, not us).

        return otsu_img
    
    def adaptive_thresholding(self,image=None):
        if image is None:
            image=self.image
        # This method calculates a different threshold value for each region of the image.
        # There are two main calculation methods:
        # The threshold value is the average of the neighboring region.
        # The threshold value is the weighted sum of neighboring pixels (pixels in the center are more important).

        # Adaptive Mean Thresholding
        th_mean = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                cv2.THRESH_BINARY, 11, 2)

        # Adaptive Gaussian Thresholding
        th_gaussian = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                    cv2.THRESH_BINARY, 11, 2)

        return [th_mean,th_gaussian]    