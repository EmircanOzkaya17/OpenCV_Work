import cv2

def change_channel(image):
    print("For HSV enter 1 \n" \
    "For GRAY enter 2 \n" \
    "For HLS enter 3 \n" \
    "For RGB enter 4 \n")

    
    try:
        choise =int(input("Your choise : "))
        if(choise==1):
            image=cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
        elif(choise==2):
            image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif(choise==3):
            image=cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        elif(choise==4):
            image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            print("Invalid number selection.")
            return 0            

        return image    
    
    except:
         print("Wrong entry, you will be redirected to the main menu.")
         return 0           

    