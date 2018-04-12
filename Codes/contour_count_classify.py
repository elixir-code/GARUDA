import numpy as np
import cv2 as cv

cap = cv.VideoCapture('VID-20180327-WA0010.mp4')

items = {'A':[], 'B':[]}
# item_index = 0

while cap.isOpened():

	for i in range(26):
		ret, img = cap.read()

		if not ret:
			break

		cv.imshow('image',img[35:325, 170:475])
		cv.waitKey(20)

	if not ret:
		break
	
	gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	# Display machine parts image
	cv.imshow('image',gray_img)
	cv.waitKey(0)

	# if item_index==0:
	# 	cv.imwrite('mp1.tiff', gray_img[35:325, 170:475])

	img_roi = gray_img[35:325, 170:475]
	smooth_img = cv.GaussianBlur(img_roi,(5,5),0)

	edges = cv.Canny(smooth_img,100,200)
	contour_img, contour, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	
	if len(contour)<=5:
		items['A'].append(item_index)

	else:
		items['B'].append(item_index)

	item_index += 1

	# cv.imshow('contours',contour_img)
	# cv.waitKey(0)

	for i in range(28):
		ret, img = cap.read()

		if not ret:
			break

		cv.imshow('image',img[35:325, 170:475])
		cv.waitKey(20)

	if not ret:
			break

	gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

	# Display machine parts image
	cv.imshow('image',gray_img[35:325, 170:475])
	cv.waitKey(0)

	# if item_index==1:
	# 	cv.imwrite('mp2.tiff', gray_img[35:325, 170:475])

	img_roi = gray_img[35:325, 170:475]
	smooth_img = cv.GaussianBlur(img_roi,(5,5),0)

	edges = cv.Canny(smooth_img,100,200)
	contour_img, contour, _ = cv.findContours(edges,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

	if len(contour)<=5:
		items['A'].append(item_index)

	else:
		items['B'].append(item_index)

	item_index += 1

	# cv.imshow('contours',contour_img)
	# cv.waitKey(0)

	for i in range(13):
		ret, img = cap.read()

		if not ret:
			break

		cv.imshow('image',img[35:325, 170:475])
		cv.waitKey(20)

	if not ret:
			break

print('Summary of Items')
print('No. of Item A :',len(items['A']))
print('Index of Item A :',items['A'])

print('No. of Item B :',len(items['B']))
print('Index of Item B :',items['B'])

cap.release()
cv.destroyAllWindows()

