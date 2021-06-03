import cv2
import numpy as np 

cv2.namedWindow("original")
cv2.namedWindow("filtered")

def callback(x):
    pass

def get_frame():
    frame=cv2.imread("../tareas/Rotation/acaceres@fiuna.edu.py/imgs/birds.jpg")
    scale_percent = 60 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

frame = get_frame()
height = frame.shape[0]

cv2.createTrackbar("minHeight", "original",0,height-1,callback)
cv2.createTrackbar("maxHeight", "original", height-1, height-1,callback)
cv2.createTrackbar("minR","original",0,255,callback)
cv2.createTrackbar("maxR","original",255,255,callback)
cv2.createTrackbar("minG","original",0,255,callback)
cv2.createTrackbar("maxG","original",255,255,callback)
cv2.createTrackbar("minB","original",0,255,callback)
cv2.createTrackbar("maxB","original",255,255,callback)

#video capture args 
#Si es un numerico 0,1,2
#Si es una url lee el buffer de video
#cam=cv2.VideoCapture(0)


#while(cam.isOpened()):
while True:
    frame=get_frame()
    cv2.imshow("original",frame)

    #obtener imagen en RGB
    imageRGB=frame

    #getTrackbarpos obtiene el valor actual del slider 
    minHeight=cv2.getTrackbarPos("minHeight", "original")
    maxHeight=cv2.getTrackbarPos("maxHeight", "original")
    minR=cv2.getTrackbarPos("minR","original")
    maxR=cv2.getTrackbarPos("maxR","original")
    minG=cv2.getTrackbarPos("minG","original")
    maxG=cv2.getTrackbarPos("maxG","original")
    minB=cv2.getTrackbarPos("minB","original")
    maxB=cv2.getTrackbarPos("maxB","original")

    frame[:minHeight+1,:,:]=255
    frame[maxHeight:,:,:]=255

    #Definicion del rango
    minRAB=np.array([minB, minG, minR])
    maxRAB=np.array([maxB, maxG, maxR])

    #inrange convierte a 255 todos los pixeles en el rango de minRGB y maxRGB, y el resto los deja en 0
    mask=cv2.inRange(imageRGB,minRAB,maxRAB)
    cv2.imshow("filtered",mask)
    cv2.imshow("original",frame)

    #waitkey devuelve el asci de la tecla oprimida
    key=cv2.waitKey(1)
    if(key==ord("q")):
        break

cv2.destroyAllWindows()

'''
    Según los resultados de las pruebas, el mejor filtro está dado por:

    minHeight:  51/187
    maxHeight:  135/187
    minR:       82/255
    maxR:       255/255
    minG:       111/255
    maxG:       255/255
    minB:       141/255
    maxB:       255/255

'''