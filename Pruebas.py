import cv2 as cv
import imflatfield as ff

path = r'C:\Users\maria\Downloads\Frame1.jpg'

img = cv.imread(path)
img_original = img[:,:,2]

gamma = 0.724

res = ff.gammaCorrection(img_original,gamma)

cv.imshow("Gamma correction", res)

cv.waitKey()
cv.destroyAllWindows()
