import numpy as np
import cv2 as cv

cap = cv.VideoCapture('VID-20180327-WA0010.mp4')

while cap.isOpened():

	for i in range(26):
		ret, img = cap.read()

		if not ret:
			break

		cv.imshow('image',img[35:325, 170:475])
		cv.waitKey(20)

	if not ret:
		break
	
	img_roi = img[35:325, 170:475]
	mean_shift_img = cv.pyrMeanShiftFiltering(img_roi, 101, 101)
	gray_img = cv.cvtColor(mean_shift_img, cv.COLOR_BGR2GRAY)

	# Display machine parts image
	cv.imshow('image',gray_img)
	while cv.waitKey(0) & 0XFF != ord('\r'):
		pass
	
	smooth_img = cv.GaussianBlur(gray_img,(5,5),0)

	edges = cv.Canny(smooth_img,100,200)
	contours = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[1]
	
	for contour in contours:

		contour_img = img_roi.copy()
		cv.drawContours(contour_img, [contour], -1, (0, 0, 255), 2)

		cv.imshow('image',contour_img)
		while cv.waitKey(0) & 0XFF != ord('\r'):
			pass

	for i in range(28):
		ret, img = cap.read()

		if not ret:
			break

		cv.imshow('image',img[35:325, 170:475])
		cv.waitKey(20)

	if not ret:
			break

	img_roi = img[35:325, 170:475]
	mean_shift_img = cv.pyrMeanShiftFiltering(img_roi, 101, 101)
	gray_img = cv.cvtColor(mean_shift_img, cv.COLOR_BGR2GRAY)

	# Display machine parts image
	cv.imshow('image',gray_img)
	while cv.waitKey(0) & 0XFF != ord('\r'):
		pass

	smooth_img = cv.GaussianBlur(gray_img,(5,5),0)

	edges = cv.Canny(smooth_img,100,200)
	contours = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[1]
	
	for contour in contours:

		contour_img = img_roi.copy()
		cv.drawContours(contour_img, [contour], -1, (0, 0, 255), 2)
		
		cv.imshow('image',contour_img)
		while cv.waitKey(0) & 0XFF != ord('\r'):
			pass

	for i in range(13):
		ret, img = cap.read()

		if not ret:
			break

		cv.imshow('image',img[35:325, 170:475])
		cv.waitKey(20)

cap.release()
cv.destroyAllWindows()

