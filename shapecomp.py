import graphlib as gl, cv2, numpy as np, imutils
from matplotlib import pyplot as plt

gl.setConstant(1)
gl.setContourPrecision(0.05)

im1 = cv2.imread("chars/three.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)
im1 = gl.blurImage(im1)


im2 = cv2.imread("chars/three2.jpg", 0)
im2 = imutils.resize(im2, width = 400)
im2 = gl.blurImage(im2)

contour1, contour2, im1, im2 = gl.getBestContours(im1, im2)

c1 = cv2.drawContours(im1.copy(), contour1, -1, (0, 255, 0), 3)
c2 = cv2.drawContours(im2.copy(), contour2, -1, (0, 255, 0), 3)




hd = cv2.createHausdorffDistanceExtractor()
sd = cv2.createShapeContextDistanceExtractor()

#order of c1, c2 does't matter (could be c2, c1)
d1 = hd.computeDistance(contour1, contour2)
d2 = sd.computeDistance(contour1, contour2) #TODO: Not working (0.0 every time)

print (d1, " ", d2)

cv2.imshow("magic", np.hstack([c1, c2]))
if cv2.waitKey() & 0xFF==ord('q'):
	cv2.destroyAllWindows()