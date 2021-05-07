import numpy as np
import cv2
import urllib.request
from src.lib.qrReader import getQRS

def getPosNorm(img):
    result = []
    W, H, _ = img.shape
    for QR in getQRS(img): # considerando múltiples QR en una imagen
        print(QR)
        wc, hc = QR['rect'].width, QR['rect'].height # dimensiones del QR
        Cx, Cy = 0, 0 # se inicializan coordenadas del centroide en 0
        for point in QR['polygon']: # se recorren los puntos del polígono del QR
            Cx += point.x
            Cy += point.y
        Cx/=4; Cy/=4 # se obtiene el centroide
        [xn,yn]=[Cx/W,Cy/H] # posición normalizada
        [wn,hn]=[wc/W,hc/H] # tamaño normalizado
        result.append({"x":xn,"y":yn,"w":wn,"h":hn}) # agregando el resultado a la lista
    return result

while True:
    url = "http://192.168.100.3:8080/shot.jpg"
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    cv2.imshow('test',img)
    print(getPosNorm(img))
    if ord('q')==cv2.waitKey(10): exit(0)