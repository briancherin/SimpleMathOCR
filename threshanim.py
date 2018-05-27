import cv2
import imutils
import numpy as np
import time

#THRESH_MEAN_C worked better for line1/2.jpg
#THRESH_GAUSSIAN_C worked better for nums.jpg


im1 = cv2.imread("nums.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)

font = cv2.FONT_HERSHEY_SIMPLEX
loc1 = (10, 35)
loc2 = (10, 50)
loc3 = (10, 20)
fontScale = 0.5
fontColor = (255,255,255)
lineType = 2

threshType = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
# thresType = cv2.ADAPTIVE_THRESH_MEAN_C

while True:

	for constant in range (0,10):	#constant is subtracted from mean 
		for blocksize in range (3, 100, 2):	#size of area to calculate mean
			adaptiveThresh = cv2.adaptiveThreshold(im1, 255, threshType, cv2.THRESH_BINARY, blocksize, constant)
			text = "Constant: " + str(constant)
			text2 = "Blocksize: " + str(blocksize)
		#	text3 = "Adaptive Mean Threshold"
			text3 = "Adaptive Gaussian Threshold"
			cv2.rectangle(adaptiveThresh, (8, 1), (250, 60), (0,0,0), -1)

			cv2.putText(adaptiveThresh, text, loc1, font, fontScale, fontColor, lineType)
			cv2.putText(adaptiveThresh, text2, loc2, font, fontScale, fontColor, lineType)
			cv2.putText(adaptiveThresh, text3, loc3, font, fontScale, fontColor, lineType)
			cv2.imshow("result", adaptiveThresh)
			
			time.sleep(0.03)
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break;

	
	
	
cv2.destroyAllWindows()


