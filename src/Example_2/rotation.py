import cv2

image= cv2.imread("swartz.jpg")
image=cv2.resize(image,None, fx=0.5,fy=0.5)

# To rotate 90 degrees and multiples of 90 degrees
rot_image=cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE) #rotate 90 degrees clockwise
cv2.imshow("image", rot_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

rot_image=cv2.rotate(image,cv2.ROTATE_180) # turning upside down
cv2.imshow("image", rot_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

rot_image=cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE) # rotate 90 degrees counterclockwise
cv2.imshow("image", rot_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# To rotate at desired angles

# center determination
(h,w)=image.shape[:2] # Row, Column --> y,x  iamge is a matris
center=(w//2, h//2) # Cartesian Coordinate System (x, y)

# Creating a Rotation Matrix (Center, Angle, Scale)
angle=75
scale=1
M = cv2.getRotationMatrix2D(center, angle, scale)

result=cv2.warpAffine(image, M, (h,w))

cv2.imshow("Turning angle 75",result)
cv2.waitKey(0)
cv2.destroyAllWindows()

