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

while True:

	threshval = cv2.getTrackbarPos("threshold", "t")
	brightness = cv2.getTrackbarPos("brightness", "t")

	ret, thresh = cv2.threshold(im1, threshval, brightness, cv2.THRESH_BINARY)
		
	cv2.imshow("result", np.hstack([im1, thresh]))
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break;
cv2.destroyAllWindows()


