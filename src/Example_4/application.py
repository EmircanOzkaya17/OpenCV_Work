import cv2 
import numpy as np
# We will try to separate the rose from the background using thresholding techniques and paint it purple.
img = cv2.imread(r"C:\OpenCV_Work\assets\rose.jpg")



# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# RED MASK (DECEMBER 2nd + low saturation tolerance)
lower_red1 = np.array([0, 40, 40])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 40, 40])
upper_red2 = np.array([180, 255, 255])

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = cv2.bitwise_or(mask1, mask2)

# Morphology: first closing, then opening.
kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

# Soften the mask but then make it double again.
mask = cv2.GaussianBlur(mask, (5, 5), 0)
_, mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)


h, s, v = cv2.split(hsv)

# The "Tone" value where the mask is white (where the rose is located) is 135. 
# In HSV, around 135 corresponds to purple/lilac tones.
h[mask == 255] = 135

# To make the rose's color more vibrant, it increases the saturation by 50%. `np.clip` ensures the value doesn't exceed 255.
s[mask == 255] = np.clip(s[mask == 255] * 1.5, 0, 255)

# Light is preserved
v[mask == 255] = v[mask == 255]

# HSV -> BGR
hsv_new = cv2.merge([h, s, v])  # It brings together the channels we've changed.
result = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)


cv2.imshow("Final Mask", mask)
cv2.imshow("Final Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()