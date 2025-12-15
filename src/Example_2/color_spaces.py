import cv2
image= cv2.imread("petersburg.jpg")
# image = cv2.cvtColor(iamge, color spaces)
# In OpenCV, the color space is initially set to BGR.
# If you are going to continue processing with openCV after changing the BGR color channel, 
# return the image to the BGR color channel.

image=cv2.resize(image, None,fx=0.3,fy=0.3)

gray_image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # BGR ---> Grayscale
cv2.imshow("Gray Image", gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

hsv_image=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) # BGR ---> HSV
cv2.imshow("HSV Image", hsv_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

hls_image=cv2.cvtColor(image,cv2.COLOR_BGR2HLS) # BGR ---> HLS
cv2.imshow("HLS Image", hls_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # BGR ---> RGB
cv2.imshow("RGB Image", rgb_image)

cv2.waitKey(0)
cv2.destroyAllWindows()