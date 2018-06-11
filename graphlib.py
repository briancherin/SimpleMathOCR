import cv2
from matplotlib import pyplot as plt

"""Translate the graph such that the center (mean) of the graph is at (0,0)
		@param xcoords, ycoords: numpy arrays of coordinates
		@return tuple (xcoords, ycoords)
"""
def originToCenter(xcoords, ycoords):
	#determine center coordinates
	xcenter = np.sum(xcoords.copy()) / len(xcoords)
	ycenter = np.sum(ycoords.copy()) / len(ycoords)
	print("Center: (" + str(xcenter) + ", " + ycenter + ")")
	
blocksize = 99
constant = 10
contourPrecision = 0.05
def getAdaptiveThresh(img):
	thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blocksize, constant)
	return thresh
	
def getContours(img):
	thresh = getAdaptiveThresh(img)
	image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	return contours

def getContourApproximation(contours, index):
	contour = contours[index]
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

def graph(x, y):
	plt.scatter(x, y)
	plt.show()
	if cv2.waitKey(1) & 0xFF==ord('q'):
		cv2.closeAllWindows()