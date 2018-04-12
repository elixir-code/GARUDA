# import necessary libraries
import numpy as np
import cv2 as cv

############################## For Image Part 1 ###################################################
image = cv.imread('mp1.tiff', cv.IMREAD_COLOR)

# Use OpenCL for processing
img = cv.UMat(image)

mean_shift_img = cv.pyrMeanShiftFiltering(img, 21, 51)
cv.imshow("image", mean_shift_img)

while cv.waitKey(0) & 0xFF != ord('\r'):
	pass

gray_img = cv.cvtColor(mean_shift_img, cv.COLOR_BGR2GRAY)
thresh_img = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

cv.imshow("image", thresh_img)

while cv.waitKey(0) & 0xFF != ord('\r'):
	pass

contours = cv.findContours(thresh_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

for index, contour in enumerate(contours):
	cv.drawContours(img, [contour], -1, (0, 0, 255), 2)

cv.imshow("image", img)

while cv.waitKey(0) & 0xFF != ord('\r'):
	pass


############################## For Image Part 2 ###################################################

image = cv.imread('mp2.tiff', cv.IMREAD_COLOR)

# Use OpenCL for processing
img = cv.UMat(image)

mean_shift_img = cv.pyrMeanShiftFiltering(img, 21, 51)
cv.imshow("image", mean_shift_img)

while cv.waitKey(0) & 0xFF != ord('\r'):
	pass

gray_img = cv.cvtColor(mean_shift_img, cv.COLOR_BGR2GRAY)
thresh_img = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

cv.imshow("image", thresh_img)

while cv.waitKey(0) & 0xFF != ord('\r'):
	pass

contours = cv.findContours(thresh_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]

for index, contour in enumerate(contours):
	cv.drawContours(img, [contour], -1, (0, 0, 255), 2)

cv.imshow("image", img)

while cv.waitKey(0) & 0xFF != ord('\r'):
	pass	

cv.destroyAllWindows()