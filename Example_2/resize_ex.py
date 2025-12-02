import cv2
image=cv2.imread("albert.jpg")

# cv2.resize(image , size, fx, fy, interpolation) 
# interpolation determines how pixels are spaced
# interpolation techniques --->>> INTER_AREA, INTER_CUBIC, INTER_LINEAR,  INTER_NEAREST
# This parameter should be selected according to the purpose and size type.

target_size=(400,400)
resize_image= cv2.resize(image,target_size)

cv2.imshow("Resized Image", resize_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Resize the image without changing its aspect ratio
resize_image= cv2.resize(image,None, fx=0.6,fy=0.6, interpolation=cv2.INTER_AREA) # the edges are multiplied by fx and fy
cv2.imshow("Resized Image", resize_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

