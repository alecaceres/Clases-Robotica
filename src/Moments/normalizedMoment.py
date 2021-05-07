import cv2
import numpy as np

#normalized Central moments results 
# Moment--> nu20
# Moment--> nu11
# Moment--> nu02
# Moment--> nu30
# Moment--> nu21
# Moment--> nu12
# Moment--> nu03




#normalized Central moments Ventajas
    #Independiente de la translacion, scale

#desventajas normalized Central 
    #dependiente de la rotation 






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



