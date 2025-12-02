import cv2

def c_crop(image,width,height):

    try:
        x_1=int(input("Enter x1 :"))
        x_2=int(input("Enter x2 :"))
        y_1=int(input("enter y1 :"))
        y_2=int(input("Enter y2 :"))

        image=image[y_1:y_2, x_1:x_2]
        image=cv2.resize(image,(width,height))
        return image
    except:
        print("Incorrect login, you are being redirected to the main menu")
        return 0


     