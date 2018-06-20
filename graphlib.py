import cv2
from matplotlib import pyplot as plt
import numpy as np, math
import imutils
from os import listdir
from os.path import isfile, join	

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

def approximateAllContours(contours):
	for x in range (0, len(contours)):
		contours[x] = getContourApproximation(contours, x)
	return contours
	
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
	if len(contours)==0:
		print("NO CONTOURS FOUND")
		return -1
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

	size = 500

	im1 = scaleImage(im1, size, size)
	im2 = scaleImage(im2, size, size)

	return (im1, im2)
"""

	#Determine which has max width. Scale up width of other one.
	if (im1.shape[1] > im2.shape[1]):	#Compare widths
		#Change the width of im2 to match im1
		# im1 = imutils.resize(im1, width = im2.shape[1])
		im1 = scaleImage(im1, width = im2.shape[1])
		print("scaling im1 width down")
	else:	
		#Change the width of im1 to match im2
		# im2 = imutils.resize(im2, width = im1.shape[1])
		im2 = scaleImage(im2, width = im1.shape[1])
		print("Scaling im2 width down")
	
	#Determine which has max height. Scale up height of other one.
	if (im1.shape[0] > im2.shape[0]):	#Compare heights
		#Change the height of im1 to match im2
		# im1 = imutils.resize(im1, height = im2.shape[0])
		im1 = scaleImage(im1, height = im2.shape[0])
		print("Scaling im1 height down")
	else:
		#Change the height of im2 to match im1`
		# im2 = imutils.resize(im2, height = im1.shape[0])
		im2 = scaleImage(im2, height = im1.shape[0])
		print("Scaling im2 height down")
	#cv2.imshow("scales", np.hstack([im1, im2]))
	#cv2.waitKey()
	return (im1, im2)	
"""		

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

def scaleImage(img, width = None, height = None):
	if width == None: width = img.shape[1]
	if height == None: height = img.shape[0]
	imnew = cv2.resize(img, (width, height))
	return imnew
	
def setupHDComp():
	global hd
	hd = cv2.createHausdorffDistanceExtractor()

"""Get the Hausdorff Distance between the two contours"""
def getHDDistance(contour1, contour2):
	#d1 = hd.computeDistance(contour1, contour2)
	#return d1

	#For each point in c1
		#Find the closest point in c2
		#If this is larger than the current largest min
			#Set the largest min to this
	largestMin = -1
	for point1 in contour1:
		minDist = -1
		for point2 in contour2:
			dist = math.sqrt(pow((point1[0][0] - point2[0][0]), 2) + pow((point1[0][1] - point2[0][1]), 2))
			if minDist == -1 or dist < minDist:
				minDist = dist
		if minDist > largestMin:
			largestMin = minDist
	return largestMin
	
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
	
	
class RefChar(object):
	file = ""
	identity = ""
	hd_val = None
	img = None
	img_orig = None
	
	def __init__(self, file, identity, hd_val = None, img = None, img_orig = None):
		self.file = file
		self.identity = identity
		self.hd_val = hd_val
	
	def set_hd_val(self, val):
		self.hd_val = val
	def set_img(self, img, img_orig):
		self.img = img
		self.img_orig = img_orig

def getRefList():
	refList = []
	refList.append(RefChar("0.jpg", "0"))
	refList.append(RefChar("1.jpg", "1"))
	refList.append(RefChar("2.jpg", "2"))
	#refList.append(RefChar("3.jpg", "3"))
	refList.append(RefChar("3-3.jpg", "3"))
	refList.append(RefChar("4.jpg", "4"))
	refList.append(RefChar("5.jpg", "5"))
	#refList.append(RefChar("6.jpg", "6"))
	#refList.append(RefChar("7.jpg", "7"))
	refList.append(RefChar("7-2.jpg", "7"))
	#refList.append(RefChar("8.jpg", "8"))
	#refList.append(RefChar("9.jpg", "9"))
	#refList.append(RefChar("div.jpg", "/"))
	#refList.append(RefChar("fracbar.jpg", "/"))
	#refList.append(RefChar("minus.jpg", "-"))
	#refList.append(RefChar("multdot.jpg", "*"))
	refList.append(RefChar("plus2.jpg", "+"))
	#refList.append(RefChar("times.jpg", "*"))
	refList.append(RefChar("times2.jpg", "*"))
	#refList.append(RefChar("times3.jpg", "*"))
	return refList
		
def getMatchesFromImage(im1):
	path="chars"
	path="refnums"
	fileList = [f for f in listdir(path) if isfile(join(path, f))]

	setupHDComp()

	refList = getRefList()
	#refList = []
	#for file in fileList:
	#	refList.append(RefChar(file, file[:len(file)-3]))

		
	for ref in refList:
		im2 = cv2.imread(path + "/" + ref.file, 0)
		im2 = imutils.resize(im2, width = 400)
		im2 = blurImage(im2)
		
		contour1, contour2, im1New, im2 = getBestContours(im1.copy(), im2.copy())
		#contour1, contour2 = alignContoursCenter(contour1, contour2)
		hd_val = getHDDistance(contour1, contour2)

		#hd_val = hd_val *1.0 / im1New.shape[1] #ratio of hd to width (to compare with differently-sized images)
		
		print(ref.file + ": hd = " + str(hd_val))
		
		im1New = cv2.drawContours(im1New.copy(), contour1, -1, (0, 255, 0), 3)
		im2New = cv2.drawContours(im1New, contour2, -1, (255, 0, 0), 3)
		
		
		
		ref.set_hd_val(hd_val)
		ref.set_img(im2New, im1New)

		#cv2.imshow("sdf", np.hstack([im1New, im2]))
		#cv2.waitKey()

	refSorted = sorted(refList, key=lambda x:x.hd_val) #sort least to greatest by HD val

	#for r in refSorted:
		#print (r.file + ": hd = " + str(r.hd_val))	

	print("Guess: " + refSorted[0].identity + " (" + refSorted[0].file + ") (hd = " + str(refSorted[0].hd_val)+ ")")

	print()

	im1 = refSorted[0].img_orig
	im2 = refSorted[0].img


	#cv2.imshow("guess", np.hstack([im1, im2]))
	#if cv2.waitKey() & 0xFF==ord('q'):
	#	cv2.destroyAllWindows()
	return refSorted