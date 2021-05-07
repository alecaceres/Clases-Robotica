import numpy as np
import cv2
import urllib.request
from src.lib import qrReader

while True:
    url = "http://192.168.100.3:8080/shot.jpg"
    imgResp=urllib.request.urlopen(url)
    print(imgResp)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    cv2.imshow('test',img)
    if ord('q')==cv2.waitKey(10): exit(0)