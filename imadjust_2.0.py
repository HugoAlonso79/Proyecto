import numpy as np
import cv2
from matplotlib import pyplot as plt

def imadjust(img,In=(0,1.0),Out=(0,1.0),gamma=1.0):
    low_in,high_in = In
    low_out, high_out = Out
    J = (((img - low_in) / (high_in - low_in)) ** gamma) * (high_out - low_out) + low_out
    return J

img = cv2.imread('prueba.png',0)

gamma = imadjust(img,(0.5,1))

cv2.imshow('img', img)
cv2.imshow('gamma', gamma)

cv2.waitKey(0)
cv2.destroyAllWindows()