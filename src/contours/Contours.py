import cv2
import numpy as np 

image=cv2.imread("./shapes.jpg")
minCanny=100;
maxCanny=300;
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Siempre aplicar canny para dejar solo los bordes 
canny=cv2.Canny(gray,minCanny,maxCanny)
contours,hierarchy=cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)



for contour in contours:
    #cada contour es una lista de componentes (x,y) indicando las posiciones de los pixels 
    print("The contour Area---->",cv2.contourArea(contour))
    cv2.drawContours(image,[contour],-1,(0,0,255),6)
    cv2.imshow("contour",cv2.resize(image,(700,700)))
    cv2.waitKey(0)

# cv2.imshow("original",image)
# cv2.imshow("canny",canny)

# cv2.waitKey(0)