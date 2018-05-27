import cv2
import imutils
import numpy as np

im1 = cv2.imread("line1.jpg")


while True:

	im1 = imutils.resize(im1, width = 400)
	
	gray = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)	#convert to grayscale
	#ret, mask = cv2.threshold(gray, 10, 100, cv2.THRESH_BINARY)
	
	#masked = cv2.bitwise_and(gray, gray, mask = mask)
	
	
	lower_color = np.array([0, 100, 100])
	upper_red = np.array([10, 255, 255])
	mask = cv2.inRange(gray, lower_color, upper_red)
	masked = cv2.bitwise_and(gray, gray, mask=mask)
	
	
	cv2.imshow("result", np.hstack([gray, masked]))
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break;
cv2.destroyAllWindows()