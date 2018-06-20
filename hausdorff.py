import cv2, graphlib as gl, numpy as np, math

hd = cv2.createHausdorffDistanceExtractor()

def printHD():
	#print(hd.computeDistance(contour1, contour2))
	print(getHausdorffDistance(contour1, contour2))
	

def getHausdorffDistance(c1, c2):
	#For each point in c1
		#Find the closest point in c2
		#If this is larger than the current largest min
			#Set the largest min to this
	largestMin = -1
	for point1 in c1:
		minDist = -1
		for point2 in c2:
			dist = math.sqrt(pow((point1[0][0] - point2[0][0]), 2) + pow((point1[0][1] - point2[0][1]), 2))
			if minDist == -1 or dist < minDist:
				minDist = dist
		if minDist > largestMin:
			largestMin = minDist
	return largestMin


def changeFlag(x):
	global flag
	global hd
	if x == 1:
		flag = cv2.NORM_L1
	else:
		flag = cv2.NORM_L2
	hd.setDistanceFlag(flag)
	printHD()

def changeRank(x):
	global rank, hd
	hd.setRankProportion(x / 100.0)
	printHD()

gl.setContourPrecision(0)

cv2.namedWindow("t")
cv2.createTrackbar("flag", "t", 0, 1, changeFlag)
cv2.createTrackbar("rank", "t", 0, 100, changeRank)

im1 = cv2.imread("testchars/testplus5.jpg", 0)
im2 = cv2.imread("refnums/plus2.jpg", 0)
#im2 = cv2.imread("refnums/1.jpg", 0)

contour1, contour2, im1, im2 = gl.getBestContours(im1, im2)

bothContours = cv2.drawContours(im1.copy(), contour1, -1, (0, 255, 0), 3)
bothContours = cv2.drawContours(bothContours, contour2, -1, (255, 0, 0), 3)


printHD()

cv2.imshow("sf", np.hstack([bothContours, im2]))
cv2.waitKey()