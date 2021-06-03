import numpy as np
from math import atan, pi

def image_pca(X, center):
    (x_c, y_c) = center
    height, width = X.shape
    x_c *= width/100
    y_c *= height/100
    y,x = np.nonzero(X)
    x = x - np.mean(x)
    y = y - np.mean(y)
    coords = np.vstack([x, y])
    cov = np.cov(coords)
    evals, evecs = np.linalg.eig(cov)
    sort_indices = np.argsort(evals)[::-1]
    x_v1, y_v1 = evecs[:, sort_indices[0]]  # Eigenvector with largest eigenvalue
    x_v2, y_v2 = evecs[:, sort_indices[1]]
    x_width = 0.25*width # estrictamente hablando, esta variable representa la mitad del largo
    y_width = 0.25*height
    sec_scale = 0.5 # para que el eje secundario se vea más chico

    first = [[int(x_c-x_width*x_v1),
            int(y_c-y_width*y_v1)],
            [int(x_c+x_width*x_v1),
            int(y_c+y_width*y_v1)]]
            
    second = [[int(x_c-x_width*x_v2*sec_scale),
                int(y_c-y_width*y_v2*sec_scale)],
                [int(x_c+x_width*x_v2*sec_scale),
                int(y_c+y_width*y_v2*sec_scale)]]

    rot = round(180-atan(y_v1/x_v1)*180/pi,2)

    return first, second, rot