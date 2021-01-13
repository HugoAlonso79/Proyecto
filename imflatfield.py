from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse

gamma = 0.724

path = r'C:\Users\maria\Downloads\Frame1.jpg'

img = cv.imread(path)
img_original = img[:,:,2]

def gammaCorrection():
    ## [changing-contrast-brightness-gamma-correction]
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    res = cv.LUT(img_original, lookUpTable)
    ## [changing-contrast-brightness-gamma-correction]

    img_gamma_corrected = cv.hconcat([img_original, res])
    cv.imshow("Gamma correction", img_gamma_corrected)

def on_gamma_correction_trackbar(val):
    global gamma
    gamma = val / 100
    gammaCorrection()

cv.namedWindow('Gamma correction')

gamma_init = int(gamma * 100)

on_gamma_correction_trackbar(gamma_init)

cv.waitKey()
cv.destroyAllWindows()