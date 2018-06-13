import graphlib as gl
import cv2
import imutils
from matplotlib import pyplot as plt

gl.setConstant(1)

im1 = cv2.imread("chars/five3.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)
im1 = blurImage(im1)

im2 = cv2.imread("chars/five2.jpg", 0)
im2 = imutils.resize(im2, width = 400)
im2 = blurImage(im2)

index1 = 0
#TODO: Get index for each image, with max number of points

contours = gl.getContours(im1)
#
#contour1 = gl.getMaxContour(contours) #get contour with greatest amt of points
#contour1 = gl.getContourApproximation([contour1], 0)


contour1 = gl.getContourApproximation(contours, 0)

im1 = gl.cropAroundContour(im1, contour1) #Crop the image to contain only the character
#Find the contours for the new image (TODO: MAKE THIS NOT AS INEFFICIENT)
contours = gl.getContours(im1)			
contour1 = gl.getContourApproximation(contours, 0)



#TODO: Find the img with the larger width / height, and scale the other one to match, so coords are the same

cnt2 = gl.getContours(im2)
cnt2 = gl.getContourApproximation(cnt2, 1)

im2 = gl.cropAroundContour(im2, cnt2)
cnt2 = gl.getContours(im2)
cnt2 = gl.getContourApproximation(cnt2, 0)

im1, im2 = gl.equalizeScale(im1, im2)
contours = gl.getContours(im1)			
contour1 = gl.getContourApproximation(contours, 0)
cnt2 = gl.getContours(im2)
cnt2 = gl.getContourApproximation(cnt2, 0)

x, y = gl.splitContoursCoords(contour1)	#get x and y lists from the contour
x, y = gl.originToCenter(x, y)	#Center the character at the origin, for uniformity during the comparison
gl.graph(x, y)

x2, y2 = gl.splitContoursCoords(cnt2)
x2, y2 = gl.originToCenter(x2, y2)
gl.graph(x2, y2)

plt.axis("scaled")
plt.show()
if cv2.waitKey(1) & 0xFF==ord('q'):
	cv2.closeAllWindows()