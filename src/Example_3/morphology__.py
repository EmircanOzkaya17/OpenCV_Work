import cv2 
import numpy as np

class morphology:
    def __init__(self, image_path="swartz.jpg"):
        
        self.image = cv2.imread(image_path,0)

        if self.image is None:
            raise ValueError("image not found :  " + image_path)
        
        self.image = cv2.resize(self.image, (200, 200))

    def closing(self,image=None):
        if image is None:
            image = self.image
        # The formula is: Closing = First Dilation + Then Erosion
        # Without changing the overall size of the object, you fill in the spaces within and integrate the shape

        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    
    def dilation(self,image=None):
        if image is None:
            image=self.image
# How it works: The kernel slides over the image pixel by pixel.
# Rule: If there's even a single "1" (white) pixel in the area covered by the kernel, it sets the center pixel to "1" (white).
        kernel = np.ones((5, 5), np.uint8)

        # Applying the Dilation Process
        # iterations = 1 -> The process is applied once.
        # If you increase the number, the object will gradually expand.

        return cv2.dilate(image, kernel, iterations=1)
    
    def erosion(self, image=None):
        if image is None:
            image=self.image
        # Kernel (Structuring Element) is used
        # If all pixels below the kernel are "1" (white), the center pixel is preserved (remains white). 
# However, if there is even a single "0" (black) below the kernel, the center pixel is made a "0" (converted to black/deleted).
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1) # iterations=1 means the operation is performed once
    
    def opening(self,image=None):
        if image is None:
            image=self.image
        # The formula is: Opening = First Erosion + Then Dilation
        # By preserving the object's size, you clear out any noise that might appear as "fly droppings" around it.
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

    def skeletonization(self, image=None):
        if image is None:
            image=self.image
        # Purpose: To reduce an object to a 1 pixel thick line while preserving its general shape and connections (topology).
        # Mathematically, this process is usually done as follows:
        # We shrink the object by performing continuous erosion.
        # At each erosion step, we note the critical pieces (skeletal pieces) that will be lost, using Opening and Subtraction.
        # Finally, when we combine these noted pieces, the skeleton emerges.
        # Areas of use: Character Recognition (OCR), Fingerprint Analysis and Data Compression

        # For skeleton extraction, the image must be completely black and completely white (0 and 255). 
        # We guarantee this with the Threshold operation.
        ret,  image= cv2.threshold(image, 127, 255, 0)
        # We create a blank (black) canvas where the skeleton will accumulate.
        size = np.size(image)
        skeleton = np.zeros(image.shape, np.uint8)

        # Using a cross-shaped (+) kernel makes the skeleton appear smoothe
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        while True:
            # Step A: Perform Opening (Noise-free version)
            opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

            # Step B: Subtract the opening result from the original
            # This process yields the skeleton fragment that would be lost through erosion
            temp = cv2.subtract(image, opening)

            # Step C: Add the found piece to the main skeleton image
            # The Bitwise OR operation acts as an "addition/combination"
            skeleton = cv2.bitwise_or(skeleton, temp)

            # Step D: Etch the image (Peel off one layer)
            image = cv2.erode(image, kernel)

            # Step E: If there are no white pixels left in the image, end the loop
            if cv2.countNonZero(image) == 0:
                break

        return skeleton

    def thinning(self, image=None):
        if image is None:
            image=self.image
        # Binarize
        # For thinning, pixels must be clearly 0 (black) or 255 (white).
        # Automatic matching is possible with the Otsu method.
        ret,binary_img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Thinning generally works on white objects (255). 
        # If your image has black text on a white background, you need to invert it:
        # binary_img = cv2.bitwise_not(binary_img)

        # Thinning Process
        # We use the ximgproc module.
        # The thinningType parameter selects the algorithm (ZHANGSUEN or GUOHALL)

        return cv2.ximgproc.thinning(binary_img, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
        
    def top_hat_transform(self, image=None):
        if image is None:
            image=self.image
        # The formula is: Top-Hat = Original Image - Opening
        # Amacı, resimdeki büyük nesneleri görmezden gelip, sadece küçük ve parlak (beyaz) detayları ortaya çıkarmaktır.

        # Let's establish the logic step by step:
        # Original Image: We have large white objects and small bright details next to them.

        # What Happens If We Open?: Remember, the Opening process (Erosion + Dilation) 
        # erased the small white dots it considered noise, preserving the large objects.

        # Subtraction (Difference): Now it's time for math:
        # (Large Objects + Small Details) minus (Large Objects Only) = Small Details Only.

        # In summary: the Top-Hat process erases the main body of the image (background and large objects), 
        # leaving only those small bright parts that were lost during the Opening process.
          
        kernel = np.ones((9, 9), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)      
