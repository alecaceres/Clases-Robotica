import cv2
import numpy as np
import glob
from scipy.spatial.distance import cdist


#cdist example
#v1=[1,2,3]
#v2=[2,3,4]
#v3=[3,4,5]

#euclidean
#       v1     v2    v2
#  v1   0      111    222
#  v2   1.23   0      222
#  v3   1.34   222    0

def filterImage(image,centralHSV,deltaHSV):
    imageHSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    minHsv=np.array(centralHSV)-np.array(deltaHSV)
    maxHsv=np.array(centralHSV)+np.array(deltaHSV)
    return cv2.inRange(imageHSV,minHsv,maxHsv)


def getHuMoments(binaryImage):
    moments=cv2.moments(binaryImage)
    return cv2.HuMoments(moments)


imagePaths=glob.glob("./huImages/*.jpg")
imagesBGR=[cv2.imread(imagePath) for imagePath in imagePaths]


centerHSV=[117,127,127];
deltaHSV=[2,100,100];

filteredImages=[filterImage(imageBGR,centerHSV,deltaHSV) for imageBGR in imagesBGR]

#solo para visualizacion
# for image,path in zip(filteredImages,imagePaths):
#     cv2.imshow("image",image)
#     print("imagePath",path)
#     cv2.waitKey(0)

huMoments=np.array([getHuMoments(filteredImage) for filteredImage in filteredImages])
huMoments=huMoments[:,:,0]
distMatrix=cdist(huMoments,huMoments,'euclidean')*1e7
for path in imagePaths:
    print(path)

print(distMatrix)



#results 
# ./huImages/rotation.jpg 0
# ./huImages/squareOriginal.jpg
# ./huImages/translation.jpg
# ./huImages/scale.jpg 3
# ./huImages/squarerotation.jpg
# ./huImages/original.jpg

# fila 0 columna 3 es la distancia entre rotation.jpg y scale.jpg

#matriz simetrica 

# [0.00000000e+00 8.56965991e+02 2.57369747e+00 2.44222256e+00 8.57307680e+02 1.38193260e+00]
# [8.56965991e+02 0.00000000e+00 8.54392294e+02 8.59408214e+02 3.41690526e-01 8.55584059e+02]
# [2.57369747e+00 8.54392294e+02 0.00000000e+00 5.01591989e+00 8.54733983e+02 1.19176488e+00]
# [2.44222256e+00 8.59408214e+02 5.01591989e+00 0.00000000e+00 8.59749903e+02 3.82415506e+00]
# [8.57307680e+02 3.41690526e-01 8.54733983e+02 8.59749903e+02 0.00000000e+00 8.55925748e+02]
# [1.38193260e+00 8.55584059e+02 1.19176488e+00 3.82415506e+00 8.55925748e+02 0.00000000e+00]








