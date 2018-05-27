import cv2
import imutils
import numpy as np


def trackbarRes(x):
	return x

im1 = cv2.imread("line1.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)

#Anything above the threshold value with receive the brightness value
cv2.namedWindow("t")
cv2.createTrackbar("threshold", "t", 0, 255, trackbarRes) 
cv2.createTrackbar("brightness", "t", 255, 255, trackbarRes) 
cv2.createTrackbar("blocksize", "t", 11, 100, trackbarRes) 
cv2.createTrackbar("constant", "t", 2, 30, trackbarRes) 

while True:

	threshval = cv2.getTrackbarPos("threshold", "t")
	brightness = cv2.getTrackbarPos("brightness", "t")
	blocksize = int(cv2.getTrackbarPos("blocksize", "t"))
	constant = cv2.getTrackbarPos("constant", "t")

	#Block size must be > 1 and odd
	if blocksize <= 1: blocksize = 3
	if blocksize % 2 == 0: blocksize+=1

	ret, normalThresh = cv2.threshold(im1, threshval, brightness, cv2.THRESH_BINARY)
	adaptiveThresh = cv2.adaptiveThreshold(im1, brightness, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blocksize, constant)
		
	cv2.imshow("result", np.hstack([im1, normalThresh, adaptiveThresh]))
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break;
cv2.destroyAllWindows()


