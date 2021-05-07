import cv2
import numpy as np

image=cv2.imread("./test.jpg")

#resuze de la imagen 

image=cv2.resize(image,(700,700))

#convertimos a LAB
imageLAB=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)

imageH=imageLAB[:,:,0]

imageS=imageLAB[:,:,1]

imageV=imageLAB[:,:,2]

cv2.imshow("L",imageH)
cv2.imshow("A",imageS)
cv2.imshow("B",imageV)


cv2.waitKey(0);

