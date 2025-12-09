import cv2
# Let's compare them all at once.

image=cv2.imread("swartz.jpg")
image=cv2.resize(image,(250,250))


avg_blurring=cv2.blur(image, (5,5))
gs_blurring=cv2.GaussianBlur(image,(5,5),0) 
m_blurring=cv2.medianBlur(image,5)
b_blurring = cv2.bilateralFilter(image, 9, 75, 75)

collage=cv2.hconcat([image,avg_blurring,gs_blurring,m_blurring,b_blurring])

cv2.imshow("Original image --> Mean blur --> Gaussian blur --> Median blur --> Bilateral blur ", collage)
cv2.waitKey(0)
cv2.destroyAllWindows()