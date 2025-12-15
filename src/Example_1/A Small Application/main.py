from rectangle import draw_rectangle
from circle import drwa_circle
from line import drwa_line
from draw import ciz
import cv2

def main():
    albert_r=cv2.resize(cv2.imread("albert.jpg"),(600,400))
    cloud_r=cv2.resize(cv2.imread("cloud.jpg"), (600,400))
    swartz_r=cv2.resize(cv2.imread("swartz.jpg"),(600,400))
    petersburg_r=cv2.resize(cv2.imread("petersburg.jpg"),(600,400))

    row1 = cv2.hconcat([albert_r, cloud_r])
    row2 = cv2.hconcat([swartz_r, petersburg_r])
    combined = cv2.vconcat([row1, row2])
    cv2.imshow("Combined", combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    albert=cv2.imread("albert.jpg")
    cloud=cv2.imread("cloud.jpg")
    swartz=cv2.imread("swartz.jpg")
    petersburg=cv2.imread("petersburg.jpg")

    while True:
        draw=input(
        "For rectangle: 1\n"
        "For cricle : 2 \n"
        "For line : 3 \n"
        "What do you want to draw: \n"
        )


        select=input("For Albert : a\n"
        "For Swartz : s\n"
        "For Cloud: c\n"
        "For Petersburg: p\n" \
        "For exit : e \n"
        "Your choose : \n")
        select=select.lower()

        if(select=="a"):
          ciz(draw,albert)  
                                       
        elif(select=="s"):
          ciz(draw,swartz)  

        elif(select=="c"):
           ciz(draw,cloud)            
            
        elif(select=="p"):
           ciz(draw,petersburg)
        elif(select=="e"):
           break
        else:
            print("Incorrect entry")   
            
if __name__ == "__main__":
    main() 