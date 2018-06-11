import graphlib as gl
import cv2
import imutils
from matplotlib import pyplot as plt

im1 = cv2.imread("symb.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)

index = 11

contours = gl.getContours(im1)
contour1 = gl.getContourApproximation(contours, index)

x, y = gl.splitContoursCoords(contour1)
gl.graph(x, y)