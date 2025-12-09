import cv2 
import numpy as np
# It is especially effective against noise consisting of black and white dots, which we call "Salt and Pepper".

#Median Blurring sorts the pixels under the kernel and selects the value in the exact middle.

image=cv2.imread("swartz.jpg")
image=cv2.resize(image,(300,300))

m_blurring=cv2.medianBlur(image,5)# Since the kernel must be a square, the 5 here represents the length of one side of the square.

collage=cv2.hconcat([image,m_blurring])
cv2.imshow("Median Blurring",collage )
cv2.waitKey(0)
cv2.destroyAllWindows()


# What does the result look like if salt and pepper is applied to an image with noise?

def sp_noise(image, prob=0.01):
    noisy = image.copy()
    rnd = np.random.rand(*image.shape[:2])

    noisy[rnd < prob] = 0       # biber
    noisy[rnd > 1 - prob] = 255 # tuz
    return noisy

noisy_image = sp_noise(image)
noisy_image=cv2.resize(noisy_image,(300,300))

m_blurring=cv2.medianBlur(noisy_image,5)

collage=cv2.hconcat([image,noisy_image,m_blurring])
cv2.imshow("Original image --> Salt and pepper noise version --> Median blur applied version",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()
