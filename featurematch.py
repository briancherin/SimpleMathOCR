import cv2
import numpy as np
from matplotlib import pyplot as plt

#Crop the image around each of the contours, then use it as query or train for each standard digit.
#Whichever has the most similarity (length of matches?) is the correct digit match


def getMeanDist(standardImg, idImage):

	orb = cv2.ORB_create() #initiate the ORB detector
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True) #NORM_HAMMING: dist measurement
	#find keypoints and descriptors
	kp1, des1 = orb.detectAndCompute(standardImg, None)
	kp2, des2 = orb.detectAndCompute(idImage, None)

	#BFMatcher === Brute Force Matcher
	matches = bf.match(des1, des2)

	distances = []
	for x in matches:
		distances.append(x.distance)
	distances = np.array(distances)
	return np.mean(distances)

questionImg = "chars/five2.jpg" #filename of character we want to identify

imgFileNames = ["four.jpg", "five.jpg", "six.jpg"]

#queryImg = cv2.imread("chars/four.jpg", 0) #Standard image
trainImg = cv2.imread(questionImg, 0) #Image on which we are looking for the standard



chars = {} #dictionary of {fileName (possible char match) : meanDistance}
for imgFileName in imgFileNames:
	meanDist = getMeanDist(trainImg, cv2.imread("chars/" + imgFileName, 0))
	chars[imgFileName] = meanDist
	print("Mean distance for " + imgFileName[:imgFileName.index(".")] + ": " + str(meanDist))

#Calculate character with min distance values
min = min(chars.items(), key=lambda x:x[1])[0]
print("Identified as: " + str(min))
	

	


#matches = sorted(matches, key = lambda x:x.distance) #sort by distance

"""#Draw first 10 matches
draw = cv2.drawMatches(queryImg, kp1, trainImg, kp2, matches[:50], None, flags=2)
plt.imshow(draw), plt.show()"""