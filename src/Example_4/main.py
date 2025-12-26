import cv2
from src import tresholding
import os

def main():
    output_dir = r"C:\OpenCV_Work\src\Example_4\results"
    os.makedirs(output_dir, exist_ok=True)
    thresholding = tresholding.Tresholding()
    original_image = cv2.imread(r"C:\OpenCV_Work\assets\rose.jpg", 0)
    original_image=cv2.resize(original_image,(400,400))
    binary_image = thresholding.binary_tresholding()
    otsu_image = thresholding.otsu_tresholding()
    adaptive_mean, adaptive_gaussian = thresholding.adaptive_thresholding()

    cv2.imshow("Original Image", original_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Combine images
    top_row = cv2.hconcat([otsu_image, binary_image])
    bottom_row = cv2.hconcat([adaptive_gaussian, adaptive_mean])

    combined_image = cv2.vconcat([top_row, bottom_row])
    cv2.imwrite(os.path.join(output_dir, "otsu_imahe.png"), otsu_image)
    cv2.imwrite(os.path.join(output_dir, "binary_image.png"),binary_image)
    cv2.imwrite(os.path.join(output_dir, "adaptive_gaussian.png"), adaptive_gaussian)
    cv2.imwrite(os.path.join(output_dir, "adaptive_mean.png"), adaptive_mean)
    cv2.imshow("Otus --> Binary --> Gaussian --> Mean", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    