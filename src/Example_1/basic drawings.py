import cv2
import numpy as np 
# OpenCV works according to BGR (blue, green,red)
# The origin of the coordinate plane is located in the upper left corner of the screen.

img = cv2.imread(r"C:\OpenCV_Work\assets\albert.jpg")


# draw a LİNE
cv2.line(img,(300,300),(800,500), color=(0,0,255),thickness=5 )# parameters--> iamge, start point, end point, color, thickness

cv2.imshow("Line",img )

cv2.waitKey(0)
cv2.destroyAllWindows()

# draw a rectangle

cv2.rectangle(img,(600,600),(750,800),(255,0,0), thickness=4 )# points ---> A=(X1,Y1) and B=(X2,Y2) A and B are diagonal corners

cv2.imshow("Rectangle",img )

cv2.waitKey(0)
cv2.destroyAllWindows()

# draw a solid square
x=200
y=200
size=150
cv2.rectangle(img, (x,y),(x+size,y+size), (0,255,0),-1) # The value thickness = -1 ensures the inside is solid

cv2.imshow("Solid Square",img )
cv2.waitKey(0)
cv2.destroyAllWindows()

# draw a circle

cv2.circle(img, (300,300),150, (125,125,125),thickness=7 ) # parameters--> image, center, radius, color, thickness 

cv2.imshow("Cricle",img )
cv2.waitKey(0)
cv2.destroyAllWindows()

# draw a polygon

points = np.array([[100, 50], [400, 80], [350, 300], [120, 250]], np.int32) # points must be integers
points = points.reshape((-1, 1, 2)) # Bring it to the format that OpenCV wants


cv2.polylines(img, [points], True, (170,100,255),5) # parameters--> imag, [points] list, close or open, color, thickness
cv2.imshow("Polygon",img )

cv2.waitKey(0)
cv2.destroyAllWindows()