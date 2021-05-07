import cv2
import numpy as np

#central moments results 
# Moment--> mu20
# Moment--> mu11
# Moment--> mu02
# Moment--> mu30
# Moment--> mu21
# Moment--> mu12
# Moment--> mu03




#central moments Ventajas
    #Independiente de la translacion

#desventajas 
    #dependiente de la scale, rotation 






#moments=sume((x^i)*(y^k)*pixelV(x,y))

#leyendo la imagen 
image=cv2.imread("./shapes.jpg")

#convertir a HSV
imageHSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)


#filtrado

minH=np.array([22,0,0])
maxH=np.array([23,255,255])
binaryImage=cv2.inRange(imageHSV,minH,maxH)



#mostrar los resultados 
# cv2.imshow("binary",binaryImage)
# cv2.waitKey(0)


#calcular los momentos
#Segundo argumento normaliza en caso de que sea binario 

moments=cv2.moments(binaryImage,True);

for moment in moments:
    print("Moment-->",moment)



