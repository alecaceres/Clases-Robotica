import cv2
import numpy as np

#moments results raw 
# moment---> m00--->Area
# moment---> m10
# moment---> m01
# moment---> m20
# moment---> m11
# moment---> m02
# moment---> m30
# moment---> m21
# moment---> m12
# moment---> m03


#raw moments Problems
    #Dependiente de la traslation,scale,rotation





#moments=sume((x^i)*(y^k)*pixelV(x,y))

#leyendo la imagen 
image=cv2.imread("./shapes.jpg")

#convertir a HSV
imageHSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


#filtrado

minH=np.array([22,0,0])
maxH=np.array([23,255,255])
binaryImage=cv2.inRange(imageHSV,minH,maxH)

cv2.imwrite("binary.png",binaryImage)



#mostrar los resultados 
# cv2.imshow("binary",binaryImage)
# cv2.waitKey(0)


#calcular los momentos
#Segundo argumento normaliza en caso de que sea binario 

moments=cv2.moments(binaryImage,True);


#El area de la imagen 
areaObject=moments['m00']

#area Image
areaImage=binaryImage.shape[0]*binaryImage.shape[1]

#posicion centro de masa
xcenter=moments['m10']/moments['m00']
ycenter=moments['m01']/moments['m00']

print("Area",areaObject/areaImage)

print(xcenter/binaryImage.shape[0],ycenter/binaryImage.shape[1])



