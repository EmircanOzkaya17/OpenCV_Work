import cv2 
import numpy as np
import os
from application_Functions import Def_Application

def main():
    output_dir = r"C:\OpenCV_Work\src\Example_4\results"
    os.makedirs(output_dir, exist_ok=True)
    # We will try to separate the rose from the background using thresholding techniques and paint it purple.
    img = cv2.imread(r"C:\OpenCV_Work\assets\rose.jpg")

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask=Def_Application.make_red_mask(hsv)

    mask=Def_Application.apply_morphological_processing(mask)

    # Soften the mask but then make it double again.
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    _, mask = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)

    hsv_new=Def_Application.edit_color_channels(hsv, mask)

    result = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)

    cv2.imwrite(os.path.join(output_dir, "rose_mask.png"), mask)
    cv2.imwrite(os.path.join(output_dir, "rose_purple.png"), result)

    cv2.imshow("Final Mask", mask)
    cv2.imshow("Final Result", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    