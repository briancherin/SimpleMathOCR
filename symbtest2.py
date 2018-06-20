import cv2, graphlib as gl, numpy as np, imutils
from os import listdir
from os.path import isfile, join
import itertools


gl.setContourPrecision(0.01)

"""
Work decently:
test 1, 2, 6, 9, 10
"""

#IMAGE IN QUESTION (multiple characters)
im1 = cv2.imread("testchars/test10.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 1200)
im1 = gl.blurImage(im1, 5)


contours = gl.getContours(im1)
contours = gl.approximateAllContours(contours)
#cv2.imshow("sdf",cv2.drawContours(im1, contours, -1, (0,255,0), 3))
#cv2.waitKey()

contours = sorted(contours, key = lambda x: cv2.arcLength(x, True)) #TODO: ONLY GET THE TOP X CONTOURS (for false contours)
list.reverse(contours)

cutoffPoint = 5
if len(contours)<5: cutoffPoint = len(contours)
contours = contours[:cutoffPoint] #TODO: figure out how much to cancel out (improve threshold?)
contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0]) #Sort the contours left-to-right


res = ""

slots = []

for contour in contours:
	cv2.imshow("dddd", cv2.drawContours(im1.copy(), contour, -1, (0, 255, 0), 3))
	cv2.waitKey()
	cropped = gl.cropAroundContour(im1, contour)
	matches = gl.getMatchesFromImage(cropped)
	res += matches[0].identity + " "
	
	slots.append(matches[:2])

print("Most likely: " + res)

resList = list(itertools.product(*slots)) #Get all permutations of the possibilities for each slot

for set in resList:
	res = ""
	for char in set:
		res += char.identity + " "
	print (res)
	
#for x in range (0, len(slots[0]): #The number of possbilities for each slot
#	for pos in slots[x]
	
	
#print(res)











