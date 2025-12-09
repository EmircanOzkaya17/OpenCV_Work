import cv2
import numpy as np
image = cv2.imread('petersburg.jpg', 0) 
image=cv2.resize(image,(250,250))

# Kernel
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
sharp_kernel  = cv2.filter2D(image, -1, kernel)

# Laplacian 
laplacian = cv2.Laplacian(src=image, ddepth=cv2.CV_64F, ksize=3)
laplacian_abs = cv2.convertScaleAbs(laplacian)
sharpened_laplacian = cv2.addWeighted(image, 1.5, laplacian_abs, -0.5, 0)

# Sobel 
sobel_x = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
sobel_y = cv2.Sobel(src=image, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
abs_sobel_x = cv2.convertScaleAbs(sobel_x)
abs_sobel_y = cv2.convertScaleAbs(sobel_y)
combined_sobel = cv2.addWeighted(abs_sobel_x, 0.5, abs_sobel_y, 0.5, 0)

# Canny 
canny_edges = cv2.Canny(image, threshold1=100, threshold2=200)

# UmsharpMasking
g_blurring=cv2.GaussianBlur(image,(9,9),0)
sharp_image = cv2.addWeighted(image, 1.5, g_blurring, -0.5, 0)

# Collage

collage =cv2.hconcat([image,sharp_kernel,sharpened_laplacian,combined_sobel,canny_edges,sharp_image])
cv2.imshow("Orginal image --> Kernel --> Laplacian --> Sobel --> Canny --> UmsharpMasking", collage)
cv2.waitKey(0)
cv2.destroyAllWindows()