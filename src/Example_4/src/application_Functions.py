import cv2
import numpy as np

class Def_Application():
    def make_red_mask(hsv):
        # RED MASK (DECEMBER 2nd + low saturation tolerance)
        lower_red1 = np.array([0, 40, 40])
        upper_red1 = np.array([10, 255, 255])

        lower_red2 = np.array([170, 40, 40])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        mask = cv2.bitwise_or(mask1, mask2)

        return mask
    

    def apply_morphological_processing(mask):
        # Morphology: first closing, then opening.
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=6)

        return mask
    
    def edit_color_channels(hsv, mask):
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
        return hsv_new