import cv2
# We use the array slicing feature of Python and the NumPy library.
# (Y,X)
# img=img(Y_start:Y_finsh, X_start:X_finsh)

img=cv2.imread("cloud.jpg")

cv2.imshow("Original image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

x_s=200
x_f=400

y_s=200
y_f=400

crp_img=img[y_s:y_f, x_s:x_f] 

cv2.imshow("Cropped image",crp_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

