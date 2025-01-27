import cv2
import numpy as np 

cv2.namedWindow("original")
cv2.namedWindow("filtered")

def callback(x):
    pass

cv2.createTrackbar("minH","original",0,179,callback)
cv2.createTrackbar("maxH","original",179,179,callback)
cv2.createTrackbar("minS","original",0,255,callback)
cv2.createTrackbar("maxS","original",255,255,callback)
cv2.createTrackbar("minV","original",0,255,callback)
cv2.createTrackbar("maxV","original",255,255,callback)

#video capture args 
#Si es un numerico 0,1,2
#Si es una url lee el buffer de video
#cam=cv2.VideoCapture(0)


#while(cam.isOpened()):
while True:
    frame=cv2.imread("../tareas/Rotation/acaceres@fiuna.edu.py/imgs/birds.jpg")
    scale_percent = 60 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    cv2.imshow("original",frame)

    #obtener imagen en HSV
    imageHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #getTrackbarpos obtiene el valor actual del slider 
    minH=cv2.getTrackbarPos("minH","original")
    maxH=cv2.getTrackbarPos("maxH","original")
    minS=cv2.getTrackbarPos("minS","original")
    maxS=cv2.getTrackbarPos("maxS","original")
    minV=cv2.getTrackbarPos("minV","original")
    maxV=cv2.getTrackbarPos("maxV","original")

    #Definicion del rango
    #120,20,20 minH=140 maxH=200
    minHSV=np.array([minH,minS,minV])
    maxHSV=np.array([maxH,maxS,maxV])

    #inrange convierte a 255 todos los pixeles en el rango de minHSV y maxHSV, y el resto los deja en 0
    mask=cv2.inRange(imageHSV,minHSV,maxHSV)
    cv2.imshow("filtered",mask)
    cv2.imshow("original",frame)


    #waitkey devuelve el asci de la tecla oprimida
    key=cv2.waitKey(1)
    if(key==ord("q")):
        break

cv2.destroyAllWindows();




