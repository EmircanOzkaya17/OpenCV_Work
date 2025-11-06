import cv2

img = cv2.imread("petersburg.jpg") # We took the image and put it into the variable

cv2.imshow("St Petersburg Landscape", img) # title and variable

cv2.waitKey(0)     # waits until you press a key

cv2.imwrite("yeni_resim.png", img)
cv2.destroyAllWindows() 



