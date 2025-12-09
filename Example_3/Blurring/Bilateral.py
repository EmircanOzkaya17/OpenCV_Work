import cv2
# The bilateral filter is "selective." It processes not only nearby pixels but also pixels with similar color values. 

image=cv2.imread("swartz.jpg")
image=cv2.resize(image,(300,300))

b_blurring = cv2.bilateralFilter(image, 9, 75, 75) #(image, Neighborhood diameter,  sigmaColor, sigmaSpace)
# sigmaColor=75: Color mixing tolerance
# sigmaSpace=75: Area of ​​effect of distant pixels

collage=cv2.hconcat([image,b_blurring])
cv2.imshow("Bilateral Blurring",collage )
cv2.waitKey(0)
cv2.destroyAllWindows()