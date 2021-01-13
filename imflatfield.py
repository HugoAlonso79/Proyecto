from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse

def gammaCorrection(img_original,gamma):
    
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    res = cv.LUT(img_original, lookUpTable)
    return res