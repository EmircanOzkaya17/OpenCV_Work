import cv2
from tresholding import cls_tresholding
def main():
    thresholding = cls_tresholding()
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

    cv2.imshow("Otus --> Binary --> Gaussian --> Mean", combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    