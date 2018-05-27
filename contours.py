import cv2
import imutils
import numpy as np

im1 = cv2.imread("nums.jpg") #Import image as grayscale
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY);
im1 = imutils.resize(im1, width = 400)


def nothing(x):
	pass



	
blocksize = 99
constant = 10
thresh = cv2.adaptiveThreshold(im1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blocksize, constant)

im_copy = im1

image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cv2.namedWindow('t')
cv2.createTrackbar('precision', 't', 0, 100, nothing)
cv2.createTrackbar('ind', 't', 0, len(contours)-1, nothing)


print(str(len(contours)))
for c in sorted(contours, key=len):
	print(len(c))

#ind = max(enumerate(contours), key=lambda x: len(x[1]))[0]
#print("ind: " + str(ind))


while True:
	
	precision = cv2.getTrackbarPos('precision', 't') / 100.0 #level of approximation precision
	ind = cv2.getTrackbarPos('ind', 't') #index of contours to use (?)
	
	#Simplify the contours by approximating the polygonal curves of the contour
	epsilon = precision * cv2.arcLength(contours[ind], True)
	approx = cv2.approxPolyDP(contours[ind], epsilon, True)

	cont = cv2.drawContours(im1.copy(), approx, -1, (0,255,0),3)
	

	cv2.imshow("result", np.hstack([thresh, cont]))
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break;
cv2.destroyAllWindows()


