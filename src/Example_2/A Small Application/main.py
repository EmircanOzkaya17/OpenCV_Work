
import cv2
from change_color_channel import change_channel
from change_crop import c_crop
from change_rotation import c_rotation
from collage_img import img_collage
from select_img import select_img
import sys

def main():
    try:
        print("Set the size of all images")

        width=int(input("Enter width :"))
        height= int(input("Enter height :"))

        albert=cv2.resize(cv2.imread("albert.jpg"),(width,height))
        petersburg=cv2.resize(cv2.imread("petersburg.jpg"),(width,height))
        cloud=cv2.resize(cv2.imread("cloud.jpg"),(width,height))
        swartz=cv2.resize(cv2.imread("swartz.jpg"),(width,height))

        horizontal1  = cv2.hconcat([albert, petersburg])
        horizontal2  = cv2.hconcat([swartz,cloud])

        vertical = cv2.vconcat([horizontal1, horizontal2])

        cv2.imshow("Initial situation",vertical)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        print("wrong entry bye bye :))") 
        sys.exit()
     
    h_con = None 
    v_con = None

    while True:
        img=select_img()
        if isinstance(img[0], int): 
            continue
       
        img[0] = cv2.resize(img[0], (width, height))
        print("To change color channels 1 \n"
        "To crop the image 2 \n"
        "To rotate the image 3 \n"
        "To combine images 4 \n "
        "To log out 5 \n")
        select1=int(input("Your choice :  \n"))

        if(select1==1):
            temporary=change_channel(img[0])
            if not isinstance(temporary, int):
                if(img[1]==1):
                    albert=temporary
                    cv2.imshow("Transaction Result",albert)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                elif(img[1]==2):
                    swartz=temporary
                    cv2.imshow("Transaction Result",swartz)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                elif(img[1]==3):
                    cloud=temporary
                    cv2.imshow("Transaction Result",cloud)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()    
                elif(img[1]==4):
                    petersburg=temporary
                    cv2.imshow("Transaction Result",petersburg)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()


        if(select1==2):
            temporary=c_crop(img[0],width,height)
            if not isinstance(temporary, int):
                if(img[1]==1):
                    cv2.imshow("Transaction Result",albert)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()                    
                    albert=temporary
                elif(img[1]==2):
                    cv2.imshow("Transaction Result",swartz)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()                    
                    swartz=temporary
                elif(img[1]==3):
                    cv2.imshow("Transaction Result",cloud)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()                    
                    cloud=temporary    
                elif(img[1]==4):
                    petersburg=temporary
                    cv2.imshow("Transaction Result",petersburg)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()                    

        if(select1==3):
            temporary=c_rotation(img[0])
            if not isinstance(temporary, int):
                if(img[1]==1):
                    albert=temporary
                    cv2.imshow("Transaction Result",albert)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                elif(img[1]==2):
                    swartz=temporary
                    cv2.imshow("Transaction Result",swartz)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()                    
                elif(img[1]==3):
                    cloud=temporary 
                    cv2.imshow("Transaction Result",cloud)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()                      
                elif(img[1]==4):
                    petersburg=temporary
                    cv2.imshow("Transaction Result",petersburg)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()                    
        if(select1==4):
            img2=select_img()
            img2[0] = cv2.resize(img2[0], (width, height))

            if isinstance(img2[0], int): 
                continue

            temporary=img_collage(img[0],img2[0])
            if(temporary[0]==1):
                if h_con is None:
                    h_con = temporary[1]
                else:
                    if h_con.shape[0] != temporary[1].shape[0]:
                        new_height = h_con.shape[0]
                        new_width = int(temporary[1].shape[1] * (new_height / temporary[1].shape[0]))
                        temporary[1] = cv2.resize(temporary[1], (new_width, new_height))    
                cv2.imshow("Transaction Result",h_con)
                cv2.waitKey(0)
                cv2.destroyAllWindows()                

            if(temporary[0]==2):
                if v_con is None:
                    v_con=temporary[1]
                
                else: 
                    if v_con.shape[1] != temporary[1].shape[1]:
                        target_width = v_con.shape[1]
                        scale_factor = target_width / temporary[1].shape[1]
                        new_height = int(temporary[1].shape[0] * scale_factor)
                        temporary[1] = cv2.resize(temporary[1], (target_width, new_height))

                    v_con = cv2.vconcat([v_con, temporary[1]])

                cv2.imshow("Transaction Result",v_con)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        if(select1 == 5):
            print("Goog bye !! :))")
            cv2.destroyAllWindows()
            sys.exit()        
                   
if __name__ == "__main__":
    main()     

