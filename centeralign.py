import cv2, imutils, graphlib as gl, numpy as np
 
"""
im1 = cv2.imread("chars/three.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)

contour = gl.getMaxContour(gl.getContours(im1))
cnormal = cv2.drawContours(im1.copy(), contour, -1, (255, 0, 0), 3)

contourShifted = gl.contourVerticalShift(contour, 10)
contourShifted = gl.contourHorizontalShift(contour, 50)

cshifted = cv2.drawContours(cnormal, contourShifted, -1, (0, 255, 0), 3)
"""

gl.setConstant(1)
gl.setContourPrecision(0)

im1 = cv2.imread("chars/mult.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)
im1 = gl.blurImage(im1)

im2 = cv2.imread("chars/mult2.jpg", 0)
im2 = imutils.resize(im2, width = 400)
im2 = gl.blurImage(im2)

contour1, contour2, im1, im2 = gl.getBestContours(im1, im2)

normal = cv2.drawContours(im1.copy(), contour1, -1, (0, 255, 0), 3)
normal = cv2.drawContours(normal, contour2, -1, (255, 0, 0), 3)

xcenter1, ycenter1 = gl.getContourCenter(contour1)
xcenter2, ycenter2 = gl.getContourCenter(contour2)

contour1 = gl.contourVerticalShift(contour1, ycenter2-ycenter1) #vertical shift by difference in center y-vals
contour1 = gl.contourHorizontalShift(contour1, xcenter2-xcenter1)

shifted = cv2.drawContours(im1.copy(), contour1, -1, (0, 255, 0), 3)
shifted = cv2.drawContours(shifted, contour2, -1, (255, 0, 0), 3)


cv2.imshow("normal ---- shifted", np.hstack([normal, shifted]))
if cv2.waitKey() & 0xFF==ord('q'):
	cv2.destroyAllWindows()