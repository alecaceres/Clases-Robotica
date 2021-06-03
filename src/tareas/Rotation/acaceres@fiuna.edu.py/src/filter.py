import cv2
import numpy as np
import json

path = "./src/tareas/Rotation/acaceres@fiuna.edu.py/src/params.json"

def get_params(path):
    with open(path) as params_json:
        params = json.load(params_json)
        return params

def get_image(path):
    frame=cv2.imread(path)
    scale_percent = 60 # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

def filter_image(path):
    params = get_params(path)
    imageRGB = get_image(params["imagePath"])

    filter_params = params.filterParams
    imageRGB[:filter_params["minHeight"]+1,:,:]=255
    imageRGB[filter_params["maxHeight"]:,:,:]=255

    minRAB=np.array([filter_params["minB"], filter_params["minG"], filter_params["minR"]])
    maxRAB=np.array([filter_params["maxB"], filter_params["maxG"], filter_params["maxR"]])
    mask=255-cv2.inRange(imageRGB,minRAB,maxRAB)
    return mask