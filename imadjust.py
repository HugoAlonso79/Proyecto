import numpy as np
import cv2
from matplotlib import pyplot as plt
 
 #Image adjustment
def imadjust(img, In=(0,1.0), Out=(0,1.0), gamma=1.0):
    "J = low_out +(high_out - low_out).* ((I - low_in)/(high_in - low_in)).^ gamma"
    low_in,high_in = In
    low_out, high_out = Out
 
    low_in *= 255.0
    high_in *= 255.0
 
    low_out *= 255.0
    high_out *= 255.0    
    
    k = (high_out - low_out) / (high_in - low_in)
    
    h,w = img.shape[:2]
    
    imgOut = np.zeros((h,w), np.uint8)
    
    for r in range(h):
        for c in range(w):
            if img[r,c] <= low_in:
                imgOut[r,c] = low_out                
            elif img[r,c] > high_in:
                imgOut[r,c] = high_out
            else:
                res = round(k*(img[r,c]-low_in) + low_out)
                imgOut[r,c] = res              
    return imgOut

img = cv2.imread('prueba.png',0)

gamma = imadjust(img,(0.18,0.32))

cv2.imshow('img', img)
cv2.imshow('gamma', gamma)

cv2.waitKey()
cv2.destroyAllWindows()