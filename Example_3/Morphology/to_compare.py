import cv2 
import numpy as np
image = cv2.imread('petersburg.jpg', 0)
image=cv2.resize(image,(150,150))
img_for_skel = image.copy()

# Closing 
kernel = np.ones((5, 5), np.uint8)
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# Dilation
dilation = cv2.dilate(image, kernel, iterations=1)

# Erosion 
erosion = cv2.erode(image, kernel, iterations=1)

# Opening 
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# Skeletonization
img = img_for_skel.copy()
skeleton = np.zeros(img.shape, np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

while True: 
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    temp = cv2.subtract(img, opening)
    skeleton = cv2.bitwise_or(skeleton, temp)
    img = cv2.erode(img, kernel)

    if cv2.countNonZero(img) == 0:
        break
    
# Thining 
ret,binary_img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thinning_result = cv2.ximgproc.thinning(binary_img, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)    

# Top-hat Transform 
tophat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)


collage = cv2.hconcat([image,binary_img,dilation,erosion,opening,skeleton,thinning_result,tophat])
cv2.imshow("Original image--> Binary--> Dilation--> Erosion--> Opening--> Skeleton--> Thining--> Top-Hat",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()