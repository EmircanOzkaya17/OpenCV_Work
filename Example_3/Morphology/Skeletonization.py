import cv2
import numpy as np
# Purpose: To reduce an object to a 1 pixel thick line while preserving its general shape and connections (topology).

# Mathematically, this process is usually done as follows:
# We shrink the object by performing continuous erosion.

# At each erosion step, we note the critical pieces (skeletal pieces) that will be lost, using Opening and Subtraction.

# Finally, when we combine these noted pieces, the skeleton emerges.

# Areas of use: Character Recognition (OCR), Fingerprint Analysis and Data Compression

image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(500,500))

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

cv2.imshow("Skeleton", skeleton)
cv2.waitKey(0)
cv2.destroyAllWindows()