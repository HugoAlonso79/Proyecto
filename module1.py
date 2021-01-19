
import cv2 as cv2
import imflatfield as ff
from PIL import Image, ImageEnhance

img1 = cv2.imread('prueba.png',0)

converter = PIL.ImageEnhance.Color(img)
img2 = converter.enhance(0.5)

cv.imshow("Gamma correction", img2)

cv.waitKey()
cv.destroyAllWindows()