import cv2
# We can actually think of this method not as a formula, but as a three-stage logical chain:

# Blur: First, we create a blurred copy of the original image. (This is where the name "Unsharp Mask" comes from.)

# Subtraction: We mathematically subtract this blurred copy from the original image.

# Addition: We add the result of this subtraction to the original image.

# First we get a blurred version of the original image

image =cv2.imread("swartz.jpg")
image=cv2.resize(image,(500,500))

g_blurring=cv2.GaussianBlur(image,(9,9),0)

sharp_image = cv2.addWeighted(image, 1.5, g_blurring, -0.5, 0)


collage=cv2.hconcat([image,sharp_image])
cv2.imshow("Gasussian Blurring",collage)
cv2.waitKey(0)
cv2.destroyAllWindows()