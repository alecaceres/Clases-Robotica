import cv2
import filter
import moments

path = "./src/tareas/Rotation/acaceres@fiuna.edu.py/src/params.json"

image = filter.filter_image(path)
height, width= image.shape
area, (x, y) = moments.get_object_info(image)

font = cv2.FONT_HERSHEY_SIMPLEX
obj_description = [f'Area: {area}%', f'x: {x}%', f'y: {y}%']
for i,obj in enumerate(obj_description):
    cv2.putText(image, obj, (int(width*0.20),int(height*0.85)+int(height*0.07*i)), font, 0.4,(255,255,255),1)

cv2.imshow("Resultado del filtrado", image)
cv2.waitKey(0)