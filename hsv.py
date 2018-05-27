import imutils
import numpy as np
import cv2

#Range of color values (in HSV pixel values)
lower = np.array([0, 100, 20], dtype = "uint8")
upper = np.array([39, 35, 255], dtype = "uint8")

# camera = cv2.VideoCapture(4)

#?????????
def nothing(x):
	pass

cv2.namedWindow("res")
#h,s,v = 100, 100, 100

#determine a color's min hsv color values
cv2.createTrackbar('h', 'res', 0, 179, nothing)
cv2.createTrackbar('s', 'res', 0, 255, nothing)
cv2.createTrackbar('v', 'res', 0, 255, nothing)

im1 = cv2.imread("eoyp/line1.jpg")

 
while True:
	# (gotImage, frame) =  camera.read()
	frame = im1
	
	frame = imutils.resize(frame, width = 400)
	converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)	#convert to HSV color space
	
	h = cv2.getTrackbarPos('h', 'res')
	s = cv2.getTrackbarPos('s', 'res')
	v = cv2.getTrackbarPos('v', 'res')
	
	lower_color = np.array([11, 20, 0])
	upper_white = np.array([179, 255, 255])
	
	mask = cv2.inRange(converted, lower_color, upper_white)
	frame2 = cv2.bitwise_and(converted, frame, mask=mask)
	
	
	# mask = cv2.inRange(converted, lower, upper)	
	print mask
	# frame2 = cv2.bitwise_and(frame, frame, mask = mask)
	
	
	
	
	cv2.imshow("result", np.hstack([frame, converted,  frame2]))
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()