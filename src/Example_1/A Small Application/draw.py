from rectangle import draw_rectangle
from circle import drwa_circle
from line import drwa_line

def ciz(d,image):
        
    if(d=="1"):
        result=draw_rectangle(image)
    elif(d=="2"):
        result=drwa_circle(image)
    elif(d=="3"):
        result=drwa_line(image)
    else:
        print("Incorrect entry")
        