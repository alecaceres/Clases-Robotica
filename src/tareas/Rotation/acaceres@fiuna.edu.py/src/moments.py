import cv2

def get_object_info(image):
    '''
        input:
            - imagen binarizada (numpy array)
        output:
            - área (relativa al tamaño de la imagen, float del 0 al 100)
            - coordenadas del centro de masa (relativas al tamaño de la imagen,
              como tupla de floats del 0 al 100)
    '''
    binaryImage=image
    moments=cv2.moments(binaryImage,True)
    areaObject=moments['m00']
    areaImage=binaryImage.shape[0]*binaryImage.shape[1]

    print(areaObject)
    print(areaImage)
    print(binaryImage)

    area=areaObject/areaImage*100
    xcenter=(moments['m10']/moments['m00'])/binaryImage.shape[1]*100
    ycenter=(moments['m01']/moments['m00'])/binaryImage.shape[0]*100

    return round(area,2), (round(xcenter,2), round(ycenter,2))



