import cv2

img1 = cv2.imread('albert.jpg')
img2 = cv2.imread('petersburg.jpg')

# TO AVOID ERRORS: We must make the dimensions equal.
img1 = cv2.resize(img1, (300, 200))
img2 = cv2.resize(img2, (300, 200))

# Horizontal Merge
horizontal  = cv2.hconcat([img1, img2])

# Vertical Merge 
vertical = cv2.vconcat([img1, img2])


cv2.imshow('1', horizontal)
cv2.imshow('2', vertical)
cv2.waitKey(0)
cv2.destroyAllWindows()