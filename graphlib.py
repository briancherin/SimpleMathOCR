import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils


"""Translate the graph such that the center (mean) of the graph is at (0,0)
		@param xcoords, ycoords: numpy arrays of coordinates
		@return tuple (xcoords, ycoords)
"""

hd = None


def originToCenter(xcoords, ycoords):
	#determine center coordinates
	xcenter = np.sum(xcoords) / len(xcoords)
	ycenter = np.sum(ycoords) / len(ycoords)
	newx = []
	newy = []
	#shift the graph so the center is at the origin
	for x in xcoords:
		newx.append(x-xcenter)
	for y in ycoords:
		newy.append(y-ycenter)
	return (np.array(newx), np.array(newy))

def getContourCenter(contour):
	x, y = splitContoursCoords(contour)
	xcenter = np.sum(x) / len(x)
	ycenter = np.sum(y) / len(y)
	return (xcenter, ycenter)
	
blocksize = 99
constant = 10
contourPrecision = 0.05

def setBlocksize(b):
	global blocksize
	blocksize = b
def setConstant(c):
	global constant
	constant = c
def setContourPrecision(p):
	global contourPrecision
	contourPrecision = p


def getAdaptiveThresh(img):
	thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blocksize, constant)
	return thresh
	
def getContours(img):
	thresh = getAdaptiveThresh(img)
	image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	return contours

def getContourApproximation(contours, index):
	#Simplify the contours by approximating the polygonal curves of the contour	
	contour = contours[index]
	epsilon = contourPrecision * cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, epsilon, True)
	return approx

def getSingleContourApproximation(contour):
	epsilon = contourPrecision * cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, epsilon, True)
	return approx
	
def splitContoursCoords(contour):
	x = []
	y = []
	for coord in contour:
		x.append(coord[0][0])
		y.append(-1*coord[0][1])
	return (x, y)

def getMaxContour(contours):
	#max = sorted(contours, key = lambda x:len(x)) #sort by length
	#max = sorted(contours, key = cv2.contourArea) #sort by area
	max = sorted(contours, key=lambda x:cv2.arcLength(x, True))
	#print(max)
	#TODO: Change to key=cv2.contourArea
	max = max[len(max)-1]

	
	return max

def getMaxContourIndex(contours):
	#sortedPairs = sorted(enumerate(contours), key=lambda x:len(x))
	sortedPairs = sorted(enumerate(contours), key=lambda x:cv2.arcLength(x[1], True))
	list.reverse(sortedPairs)

	maxInd = sortedPairs[0][0]
	print("max index: ", maxInd, "val: ", cv2.arcLength(sortedPairs[0][1],True))
	return maxInd
	
	
def cropImage(img, x1, y1, x2, y2):
	return img[y1:y2, x1:x2]

	
def cropAroundContour(img, contour):
	#Find the top left and bottom right corners of the contour
	#Crop the image so that the image only contains that part of the contour
	xmin = tuple(contour[contour[:, :, 0].argmin()][0])[0]
	xmax = tuple(contour[contour[:, :, 0].argmax()][0])[0]
	ymin = tuple(contour[contour[:, :, 1].argmin()][0])[1]
	ymax = tuple(contour[contour[:, :, 1].argmax()][0])[1]
	#print(str(xmin) + " " + str(xmax) + " " + str(ymin)+ " " + str(ymax))
	return cropImage(img, xmin, ymin, xmax, ymax)

def equalizeScale(im1, im2):
	#Determine which has max width. Scale width of other one.
	if (im1.shape[1] > im2.shape[1]):	#Compare widths
		#Change the width of im1 to match im2
		im1 = imutils.resize(im1, width = im2.shape[1])
	else:	
		#Change the width of im2 to match im1
		im2 = imutils.resize(im2, width = im1.shape[1])
	
	#Determine which has max height. Scale height of other one.
	if (im1.shape[0] > im2.shape[0]):	#Compare heights
		#Change the height of im1 to match im2
		im1 = imutils.resize(im1, height = im2.shape[0])
	else:
		#Change the height of im2 to match im1`
		im2 = imutils.resize(im2, height = im1.shape[0])
	return (im1, im2)	
		

#TODO: Make this not disgustingly inefficient
def getBestContours(im1, im2):
	c1 = getContours(im1) #Get initial contours
	c1 = getMaxContour(c1) #Find contour with most points
	im1 = cropAroundContour(im1, c1) #Crop the image to bound the contour
	c1 = getContours(im1) #Find the contours again, since the coordinates/indicies changed
	c1 = getMaxContour(c1) #Find contour with most points
	
	c2 = getContours(im2) #Get initial contours
	c2 = getMaxContour(c2) #Find contour with most points
	im2 = cropAroundContour(im2, c2) #Crop the image to bound the contour
	c2 = getContours(im2) #Find the contours again, since the coordinates/indicies changed
	c2 = getMaxContour(c2) #Find contour with most points
	
	im1, im2 = equalizeScale(im1, im2)
	c1 = getContours(im1) #Find the contours again, since the coordinates/indicies changed
	c1 = getMaxContour(c1) #Find contour with most points
	c2 = getContours(im2) #Find the contours again, since the coordinates/indicies changed
	c2 = getMaxContour(c2) #Find contour with most points
	c1 = getSingleContourApproximation(c1)
	c2 = getSingleContourApproximation(c2)
	
	return (c1, c2, im1, im2)

def blurImage(img, radius=21):
	return cv2.GaussianBlur(img, (radius, radius), 0)

def setupHDComp():
	global hd
	hd = cv2.createHausdorffDistanceExtractor()

"""Get the Hausdorff Distance between the two contours"""
def getHDDistance(contour1, contour2):
	d1 = hd.computeDistance(contour1, contour2)
	return d1

"""Vertically shift the contour by [shift], by modifying each point in the contour (go up by [shift] amount)"""
def contourVerticalShift(contour, shift):
	cntCopy = list(contour) #make a copy of the contour (TODO: THIS DOESN'T WORK. THE ORIGINAL IS MODIFIED)
	for point in cntCopy:
		point[0][1] += shift * -1
	return np.array(cntCopy)

"""Horizontally shift the contour (go right by [shift] amount)"""
def contourHorizontalShift(contour, shift):
	cntCopy = list(contour)
	for point in cntCopy:
		point[0][0] += shift
	return np.array(cntCopy)

"""Realign one of the contours such that its center (mean of all points) is at the same point as that of the other"""
def alignContoursCenter(contour1, contour2):
	xcenter1, ycenter1 = getContourCenter(contour1)
	xcenter2, ycenter2 = getContourCenter(contour2)

	contour1 = contourVerticalShift(contour1, ycenter2-ycenter1) #vertical shift by difference in center y-vals
	contour1 = contourHorizontalShift(contour1, xcenter2-xcenter1) #horizontal shift by diff in center x-vals
	
	return (contour1, contour2)
	
def graph(x, y):
	plt.scatter(x, y)
	