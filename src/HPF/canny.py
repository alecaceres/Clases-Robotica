import cv2 

cv2.namedWindow('canny')
cv2.namedWindow('main')

def callback():
    pass

cv2.createTrackbar('min_canny','canny',100,300,callback)
cv2.createTrackbar('max_canny','canny',200,300,callback)

cam=cv2.VideoCapture(0)
while(cam.isOpened()):
    r,image=cam.read();
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    minCanny=cv2.getTrackbarPos('min_canny','canny')
    maxCanny=cv2.getTrackbarPos('max_canny','canny')
    canny=cv2.Canny(gray,minCanny,maxCanny)
    cv2.imshow('canny',cv2.resize(canny,(700,700)))
    cv2.imshow('main',cv2.resize(image,(700,700)))
    key=cv2.waitKey(1)
    if(key==ord('q')):
        break

cv2.destroyAllWindows()
