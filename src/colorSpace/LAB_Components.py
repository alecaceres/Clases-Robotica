import cv2
import numpy as np

image=cv2.imread("../tareas/Rotation/acaceres@fiuna.edu.py/imgs/birds.jpg")

#resuze de la imagen 

image=cv2.resize(image,(600,600))

#convertimos a LAB
imageLAB=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)

imageL=imageLAB[:,:,0]

imageA=imageLAB[:,:,1]

imageB=imageLAB[:,:,2]

cv2.imshow("L",imageL)
cv2.imshow("A",imageA)
cv2.imshow("B",imageB)


cv2.waitKey(0)