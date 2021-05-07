import cv2
import numpy as np 

cv2.namedWindow("original")
cv2.namedWindow("filtered")

def callback(x):
    pass

cv2.createTrackbar("minH","original",0,255,callback)
cv2.createTrackbar("maxH","original",0,255,callback)

#video capture args 
#Si es un numerico 0,1,2
#Si es una url lee el buffer de video
cam=cv2.VideoCapture(0)

while(cam.isOpened()):
    r,frame=cam.read()
    cv2.imshow("original",frame)
    #waitkey devuelve el asci de la tecla oprimida
    key=cv2.waitKey(1)
    if(key==ord("q")):
        break

cv2.destroyAllWindows();




