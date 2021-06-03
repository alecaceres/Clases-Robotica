import cv2

import sys
SOURCE_PATH = "./src/tareas/Rotation/acaceres@fiuna.edu.py/src/" # para poder importar
sys.path.append(SOURCE_PATH) 

import filter
import moments
import pca

path = f"{SOURCE_PATH}params.json"

image = filter.filter_image(path)
height, width= image.shape
area, (x, y) = moments.get_object_info(image)
first, second, rot = pca.image_pca(image, (x,y))

font = cv2.FONT_HERSHEY_SIMPLEX
obj_description = [f'Area: {area}%', f'x: {x}%', f'y: {y}%', f'Rotacion: {rot} grados']
for i,obj in enumerate(obj_description):
    cv2.putText(image, obj, (int(width*0.20),int(height*0.75)+int(height*0.07*i)), font, 0.4,(255,255,255),1)
print("jajaj")
cv2.line(image, *first, (255, 255, 100), thickness=2)
print(*first)
print(*second)
cv2.line(image, *second, (255, 255, 100), thickness=2)
image = cv2.circle(image, (int(x*image.shape[1]/100),int(y*image.shape[0]/100)), radius=2, color=(255, 255, 255), thickness=-1)
cv2.imshow("Resultado del filtrado", image)

cv2.waitKey(0)