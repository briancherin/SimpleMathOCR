import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt
import time

def nothing(x):
	pass
	
	
def getHorizSymmetricPoints(x, y, xcenter, ycenter):
	h_symmetric_points_x = []
	h_symmetric_points_y = []
	horiz_symmetric_points = set()
	
	seen = set([])	#coordinates that have already been looked at
	for n in range (0, len(x)):
		seen.add((x[n], y[n]))	#mark this point as seen
		reflected_x = x[n]
		reflected_y = -1 * (y[n] - ycenter)	#vertical translation so the center is the origin, and then reflection across x-axis
		#now find another point that is about equal to the reflected point
		for k in range (0, len(x)):
			#if not (x[k],y[k]) in seen: #do not compare with self or previously seen point
			new_x = x[k]
			new_y = y[k] - ycenter #translate to origin
			symmetrical_precision_y = 3		#allowance for slight deviation from symmetry
			symmetrical_precision_x = 7
			if (abs(new_y-reflected_y) <= symmetrical_precision_y and abs(new_x - reflected_x) <= symmetrical_precision_x):
				print("Found horizontally symmetric point: ("+str(x[n]) + ", " + str(y[n]) + ") --> (" + str(new_x) + ", " + str(y[k]) + ")")
				h_symmetric_points_x.append(x[k])
				h_symmetric_points_y.append(y[k])
				horiz_symmetric_points.add((x[k], y[k]))
	return (h_symmetric_points_x, h_symmetric_points_y, horiz_symmetric_points)
	
def getVertSymmetricPoints(x, y, xcenter, ycenter):
	v_symmetric_points_x = []
	v_symmetric_points_y = []
	vert_symmetric_points = set()
	
	seen = set([])	#coordinates that have already been looked at
	for n in range (0, len(x)):
		seen.add((x[n], y[n]))	#mark this point as seen
		reflected_x = -1 * (x[n] -  xcenter)
		reflected_y = y[n]	#vertical translation so the center is the origin, and then reflection across x-axis
		#now find another point that is about equal to the reflected point
		for k in range (0, len(x)):
			#if not (x[k],y[k]) in seen: #do not compare with self or previously seen point
			new_x = x[k] - xcenter
			new_y = y[k] #translate to origin
			symmetrical_precision_y = 7		#allowance for slight deviation from symmetry
			symmetrical_precision_x = 3
			if (abs(new_y-reflected_y) <= symmetrical_precision_y and abs(new_x - reflected_x) <= symmetrical_precision_x):
				print("Found vertically symmetric point: ("+str(x[n]) + ", " + str(y[n]) + ") --> (" + str(new_x) + ", " + str(new_y) + ")")
				v_symmetric_points_x.append(x[k])
				v_symmetric_points_y.append(y[k])
				vert_symmetric_points.add((x[k], y[k]))
	return (v_symmetric_points_x, v_symmetric_points_y, vert_symmetric_points)

im1 = cv2.imread("symb.jpg") #Import image as grayscale
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY);
im1 = imutils.resize(im1, width = 400)




plt.gca().set_aspect("equal", adjustable="box")	#Makes the axes equally scaled so digits are not warped
	
blocksize = 99
constant = 10
thresh = cv2.adaptiveThreshold(im1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blocksize, constant)

im_copy = im1

image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cv2.namedWindow('t')
#cv2.createTrackbar('precision', 't', 0, 100, nothing)
cv2.createTrackbar('ind', 't', 0, len(contours)-1, nothing)


print(str(len(contours)))
for c in sorted(contours, key=len):
	print(len(c))

#ind = max(enumerate(contours), key=lambda x: len(x[1]))[0]
#print("ind: " + str(ind))


while True:
	precision = 0.05 	#cv2.getTrackbarPos('precision', 't') / 100.0 #level of approximation precision
	ind = cv2.getTrackbarPos('ind', 't') #index of contours to use (?)

	#Simplify the contours by approximating the polygonal curves of the contour
	epsilon = precision * cv2.arcLength(contours[ind], True)
	approx = cv2.approxPolyDP(contours[ind], epsilon, True)

	cont = cv2.drawContours(im1.copy(), approx, -1, (0,255,0),3)
	print("approximated contour:")
	print(type(approx[0][0][1]))

	coordinates = approx

	x = []
	y = []

	print("There are " + str(len(coordinates)) + " coordinates")

	for coord in coordinates:
		x.append(coord[0][0])
		y.append(-1*coord[0][1])
	for n in range (0, len(x)):
		print(str(x[n]) + ", " + str(y[n]))

	x = np.array(x)
	y = np.array(y)

	plt.scatter(x, y) #begin graph of points in this contour

	#determine center coordinate:
	xcenter = np.sum(x.copy()) / len(x)
	ycenter = np.sum(y.copy()) / len(y)

	print("Center: " + str(xcenter) + ", " + str(ycenter))

	#check for horizontal symmetry (can be folded parallel to x-axis)
	#for each point
		#if there is another point that is approximately the reflected point
			#this point has horizontal symmetry

	h_symmetric_points_x, h_symmetric_points_y, horiz_symmetric_points = getHorizSymmetricPoints(x, y, xcenter, ycenter)
	v_symmetric_points_x, v_symmetric_points_y, vert_symmetric_points = getVertSymmetricPoints(x, y, xcenter, ycenter)
	
	num_horiz_symmetric_points = len(horiz_symmetric_points)
	num_vert_symmetric_points = len(vert_symmetric_points)
			
	cv2.imshow("result", cont)
	
	total_points = float(len(x))
	plt.scatter(np.array(v_symmetric_points_x), np.array(v_symmetric_points_y), c="green")
	plt.text(plt.xlim()[0], plt.ylim()[1]+4, "Horizontally symmetric points: " + str(num_horiz_symmetric_points) + "/" + str(total_points) + ": " + str(round(num_horiz_symmetric_points/total_points*100, 2)) + "%")
	plt.text(plt.xlim()[0], plt.ylim()[1]+2, "Vertically symmetric points: " + str(num_vert_symmetric_points) + "/" + str(total_points) + ": " + str(round(num_vert_symmetric_points/total_points*100, 2)) + "%")
	
	plt.axis("scaled")
	
	plt.show()

	k = cv2.waitKey(1)
	if k & 0xFF == ord("q"):
		break
cv2.destroyAllWindows()


