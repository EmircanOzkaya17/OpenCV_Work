from sharp import ssharpening
from morphology__ import morphology
from blur__ import blurring
import cv2
import numpy as np

def main():
    image=cv2.imread("petersburg.jpg",0)
    image=cv2.resize(image,(250,250))
    print()
    ss=ssharpening()
    mm=morphology()
    bb=blurring()
    canny=ss.canny()
    kernel=ss.kernel()
    laplacian=ss.laplacian()
    sobel=ss.sobel()
    unsharp=ss.unsharp_masking()

    collage_1=cv2.hconcat([image,canny,kernel,laplacian,sobel,unsharp])
    cv2.imshow("Original Image--> Canny--> Kernel--> Laplacian--> Sobel--> Unsharp Masking  ", collage_1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image2=cv2.imread("swartz.jpg")
    image2=cv2.resize(image2,(300,300))
    average=bb.average()
    biletral=bb.bilateral()
    gaussian=bb.gaussian()
    median=bb.median()
    collage_2=cv2.hconcat([image2, average, biletral,gaussian,median])
    cv2.imshow("Original Image--> Average-->Biletral--> Gaussian--> Median", collage_2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image_3=cv2.imread("swartz.jpg",0)
    image_3=cv2.resize(image_3,(200,200))
    closing=mm.closing()
    opening=mm.opening()
    dilation=mm.dilation()
    erosion=mm.erosion()
    skeletonization=mm.skeletonization()
    thinning=mm.thinning()
    top_hat_transform=mm.top_hat_transform()
    collage_3=cv2.hconcat([image_3,closing,opening,dilation,erosion,skeletonization,thinning,top_hat_transform])
    cv2.imshow("Original Image--> Closing-->Opening--> Dilation--> Erosion--> Skeletonization--> Thinning--> Top Hat Transform",collage_3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()