import cv2

def draw_rectangle(image):
    try:
        
        x1=int(input("Please enter point x1:"))
        y1=int(input("Please enter point y1:"))
        x2=int(input("Please enter point x2:"))
        y2=int(input("Please enter point y2:"))

        color=input("for red : r \n" \
        "for green : g\n" \
        "for blue: b\n" \
        "Select color : \n")
        
        if(color=="r"):
            cv2.rectangle(image, (x1,y1),(x2,y2),(0,0,255),thickness=5 )
        elif(color=="g"):
            cv2.rectangle(image, (x1,y1),(x2,y2),(0,255,0),thickness=5 )
        else:
            cv2.rectangle(image, (x1,y1),(x2,y2), (255,0,0), thickness=5 )

        cv2.imshow("Rectangle",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        print("You have logged in incorrectly. You are being redirected to the main menu.")
         

                      

