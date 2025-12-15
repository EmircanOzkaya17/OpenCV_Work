import cv2

def img_collage(img1, img2):
    print("To combine side by side : 1 \n" \
    "To combine on top of each other : 2 \n")

    choice =input("Your choice : ")

    if(choice=="1"):
        img=cv2.hconcat([img1,img2])
        return [1,img]
    elif(choice=="2"):
        img=cv2.vconcat([img1,img2])
        return [2,img]
    else:
        print("You have logged in incorrectly and are being redirected to the main menu.")    
        return [0] 







