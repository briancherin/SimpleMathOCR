import cv2
import imutils
import numpy as np

im1 = cv2.imread("line1.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)


while True:
	
	ret0, thNormal = cv2.threshold(im1, 200, 255, cv2.THRESH_BINARY)
	ret, thO = cv2.threshold(im1, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	blur = cv2.GaussianBlur(im1, (5,5), 0)
	ret2, thO2 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	cv2.imshow("result", np.hstack([im1, thNormal, thO, thO2]))
	
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break;
cv2.destroyAllWindows()


