import cv2, graphlib as gl, numpy as np, imutils
from os import listdir
from os.path import isfile, join

#Given an image file representing a character
#for each reference character image in chars/
	#Get the HD value and store it in an array containing the character being compared
#Find the min HD value and return the associated character

gl.setContourPrecision(0.05)

class RefChar(object):
	file = ""
	identity = ""
	hd_val = None
	img = None
	img_orig = None
	
	def __init__(self, file, identity, hd_val = None, img = None, img_orig = None):
		self.file = file
		self.identity = identity
		self.hd_val = hd_val
	
	def set_hd_val(self, val):
		self.hd_val = val
	def set_img(self, img, img_orig):
		self.img = img
		self.img_orig = img_orig


#IMAGE / CHARACTER IN QUESTION
im1 = cv2.imread("testchars/three1.jpg", 0) #Import image as grayscale
im1 = imutils.resize(im1, width = 400)
im1 = gl.blurImage(im1)

path="chars"
fileList = [f for f in listdir(path) if isfile(join(path, f))]

gl.setupHDComp()

refList = []
for file in fileList:
	refList.append(RefChar(file, file[:len(file)-3]))

	
for ref in refList:
	im2 = cv2.imread("chars/" + ref.file, 0)
	im2 = imutils.resize(im2, width = 400)
	im2 = gl.blurImage(im2)
	
	contour1, contour2, im1New, im2 = gl.getBestContours(im1.copy(), im2)
	hd_val = gl.getHDDistance(contour1, contour2)
	
	#print(ref.file + ": hd = " + str(hd_val))
	
	im1New = cv2.drawContours(im1New.copy(), contour1, -1, (0, 255, 0), 3)
	im2 = cv2.drawContours(im2.copy(), contour2, -1, (0, 255, 0), 3)
	
	ref.set_hd_val(hd_val)
	ref.set_img(im2, im1New)

refSorted = sorted(refList, key=lambda x:x.hd_val) #sort least to greatest by HD val

for r in refSorted:
	print (r.file + ": hd = " + str(r.hd_val))

print("Guess: " + refSorted[0].identity + " (hd = " + str(refSorted[0].hd_val)+ ")")

im1 = refSorted[0].img_orig
im2 = refSorted[0].img


cv2.imshow("guess", np.hstack([im1, im2]))
if cv2.waitKey() & 0xFF==ord('q'):
	cv2.destroyAllWindows()

