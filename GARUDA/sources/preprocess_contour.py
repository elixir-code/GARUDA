''' Python Implementation of Equal Area Sector Shape Descriptor

Reference: 	Machine parts recognition and defect detection in automated assembly systems using computer vision techniques 
			- P.Arjun, T.T.Mirnalinee			
'''

# Some experiments on 'IMAGE SEGMENTATION'
import numpy as np
import cv2 as cv

# Calibrate and find ROI region
roi_indices = (35,325,170,475)


def preprocess_image(image):

	# Perform step 1 of Mean Shift Segmentation (blurring details)
	mean_shift_img = cv.pyrMeanShiftFiltering(image, 10, 101)

	# Perform OTSU's thresholding
	gray_img = cv.cvtColor(mean_shift_img, cv.COLOR_BGR2GRAY)
	thresh_value, thresh_img = cv.threshold(gray_img, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

	# Smoothen edges: SigmaX=0 => Sigma computed from windowSize
	smooth_img = cv.GaussianBlur(thresh_img,(5,5),0)

	return smooth_img


def compute_shape_info(preprocessed_img):

	# Extract longest contour from preprocessed image
	contours = cv.findContours(preprocessed_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)[1]
	longest_contour = contours[np.argmax([len(contour) for contour in contours])].reshape(-1, 2)

	#  cv.imshow('image', preprocessed_img)
	# cv.waitKey(0)
	
	# Filing Holes : Fill interior of 'longest' contour with white
	cv.drawContours(preprocessed_img, [longest_contour], -1, 255, cv.FILLED)

	# Compute contour centroid, radiuses and area of object shape
	shape_centroid = np.mean(longest_contour, axis=0).astype(np.uint8)
	contour_radiuses = np.linalg.norm(longest_contour - shape_centroid, axis=1)

	shape_area = cv.countNonZero(preprocessed_img)

	return longest_contour, shape_centroid, contour_radiuses, shape_area


def gen_shape_descriptor(preprocessed_img, N):

	longest_contour, shape_centroid, contour_radiuses, shape_area = compute_shape_info(preprocessed_img)
	contour_length = len(longest_contour)
	equal_parts_area = shape_area/N

	# Normalised contour points
	normalised_contour_pts = np.empty((N, 2), dtype=longest_contour.dtype)

	contour_p1_index = contour_p2_index = np.argmax(contour_radiuses)
	normalised_contour_pts[0] = longest_contour[contour_p1_index]

	for i in range(1, N):
		
		contour_p1_index = contour_p2_index
		sector_area = 0
		
		while sector_area < equal_parts_area:

			contour_p2_index = (contour_p2_index-1)%contour_length
			avg_radius = (contour_radiuses[contour_p1_index]+contour_radiuses[contour_p2_index])/2

			vector1 = longest_contour[contour_p1_index] - shape_centroid
			normalised_vector1 = vector1/np.linalg.norm(vector1)
			vector2 = longest_contour[contour_p2_index] - shape_centroid
			normalised_vector2 = vector2/np.linalg.norm(vector2)

			cos_theta = np.dot(normalised_vector1, normalised_vector2)
			theta = np.arccos(cos_theta)

			sector_area = 0.5*np.power(avg_radius, 2)*theta

		normalised_contour_pts[i] = longest_contour[contour_p2_index]

	shape_descriptor = np.linalg.norm(normalised_contour_pts - shape_centroid ,axis=1)
	return shape_descriptor


def correlation_coeff(part_features, model_features):

	fpart_mean = np.mean(part_features)
	fmodel_mean = np.mean(model_features)

	corr_coeff = np.sum((part_features - fpart_mean)*(model_features - fmodel_mean))
	norm_factor = np.linalg.norm(part_features - fpart_mean)*np.linalg.norm(model_features - fmodel_mean)

	norm_corr_coef = corr_coeff/norm_factor
	return norm_corr_coef


if __name__ == '__main__':
	
	# Open Video for reading
	cap = cv.VideoCapture('VID-20180327-WA0010.mp4')

	while cap.isOpened():

		for i in range(26):
			ret, img = cap.read()

			if not ret:
				break

		if not ret:
			break

		# Fixing a ROI for the image
		img_roi = cv.UMat(img[roi_indices[0]:roi_indices[1], roi_indices[2]:roi_indices[3]])

		# Preprocess the image
		preprocessed_img = preprocess_image(img_roi)
		
		# Generate shape descriptor
		shape_descriptor = gen_shape_descriptor(preprocessed_img, 10)
		print("Shape Desc (Part A) = ",shape_descriptor)
		print()

		for i in range(28):
			ret, img = cap.read()

			if not ret:
				break

		if not ret:
			break

		# Fixing a ROI for the image
		img_roi = cv.UMat(img[roi_indices[0]:roi_indices[1], roi_indices[2]:roi_indices[3]])

		# Preprocess the image
		preprocessed_img = preprocess_image(img_roi)
		
		# Generate shape descriptor
		shape_descriptor = gen_shape_descriptor(preprocessed_img, 10)
		print("Shape Desc (Part B) = ",shape_descriptor)
		print('\n\n')
		
		for i in range(13):
			ret, img = cap.read()
			
			if not ret:
				break

	# Release VideoCapture and destroy Windows
	cap.release()
	cv.destroyAllWindows()