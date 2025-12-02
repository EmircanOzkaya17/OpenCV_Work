import cv2

def c_rotation(image):
    print("To rotate clockwise to the desired angle : 1 \n" \
    "To rotate 90 degrees counterclockwise : 2 \n" \
    "To turn upside down : 3 \n")

    try:
        choice =int(input("Your choice : "))
        if(choice==1):
            (h,w)=image.shape[:2] # Row, Column --> y,x  iamge is a matris
            center=(w//2, h//2) # Cartesian Coordinate System (x, y)

            angle=int(input("Enter the angle : "))
            scale=1
            M = cv2.getRotationMatrix2D(center, angle, scale)
            image = cv2.warpAffine(image, M, (w, h))

        elif(choice==2):
            image=cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE)

        elif(choice==3):
            image=cv2.rotate(image,cv2.ROTATE_180)

        return image

    except:
            print("Wrong entry, you will be redirected to the main menu.")
            return 0


    
