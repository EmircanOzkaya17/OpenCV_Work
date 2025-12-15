import cv2

def select_img():
    while True:
        try:
            print("Select the image you want to process \n" \
            "For ALbert 1 \n" \
            "For Swartz 2 \n" \
            "For cloud 3 \n" \
            "For Petersburg 4 \n")
            select=int(input("Your choice : "))

            if(select==1):
                img=cv2.imread("albert.jpg")

            elif(select==2):
                img=cv2.imread("swartz.jpg")

            elif(select==3):
                img=cv2.imread("cloud.jpg")

            elif(select==4):
                img=cv2.imread("petersburg.jpg")

            else:
                print("You have not entered correctly. Please select a number by entering a suitable number.")    
                continue
            return [img,select]
        except:
            print("You did not enter a number. You are being directed to the main menu.")
            return [0]
            
