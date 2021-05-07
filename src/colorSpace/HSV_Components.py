import cv2
import numpy as np

image=cv2.imread("./test.jpg")

#resuze de la imagen 

image=cv2.resize(image,(700,700))

#convertimos a HSV
imageHSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

imageH=imageHSV[:,:,0];

imageS=imageHSV[:,:,1];

imageV=imageHSV[:,:,2];

cv2.imshow("H",imageH)
cv2.imshow("S",imageS)
cv2.imshow("V",imageV)


cv2.waitKey(0);

