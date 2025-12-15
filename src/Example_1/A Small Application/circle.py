import cv2

def drwa_circle(image):
    try:
        x1=int(input("Please enter point x1:"))
        y1=int(input("Please enter point y1:"))
        r=int(input("Please enter radius:"))

        color=input(
        "for red : r\n" \
        "for green : g \n" \
        "for blue: b \n" \
        "Select color : \n")

        if(color=="r"):
            cv2.circle(image,(x1,y1),r,(0,0,255),thickness=5 )
        elif(color=="g"):
            cv2.circle(image,(x1,y1),r,(0,255,0),thickness=5 )
        else:
            cv2.circle(image,(x1,y1),r,(255,0,0),thickness=5 )

        cv2.imshow("Cricle",image)    
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except:
        print("You have logged in incorrectly. You are being redirected to the main menu.")
            
    
    