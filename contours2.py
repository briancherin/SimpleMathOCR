import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt
import time

def nothing(x):
	pass
	
	

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

	cv2.imshow("result", cont)
	
	
	plt.axis("scaled")
	
	plt.show()

	k = cv2.waitKey(1)
	if k & 0xFF == ord("q"):
		break
cv2.destroyAllWindows()


