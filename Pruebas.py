import cv2 as cv
import imflatfield as ff
import imadjust as ij

path = r'C:\Users\Ryzen\Documents\GitHub\Proyecto\Frame1.jpg'

img = cv.imread(path)
img_original = img[:,:,2]

gamma = 0.724

res = ff.gammaCorrection(img_original,gamma)
m_e = ij.imadjust(res, (0.18,0.32))

cv.imshow("Gamma correction", res)
cv.imshow("Imadjust", m_e)


cv.waitKey()
cv.destroyAllWindows()
