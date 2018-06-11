# SimpleMathOCR
Task: Identify basic characters/digits and mathematical symbols from an image and convert them to LaTeX.

# What are these files?!
graphlib.py - support library for common graphing / image processing functions - adaptive threshold, get contours/approximation, pyplot scatter

hsv.py - playing with color space and threshold manipulation. 

nobg.py - initial attempt at background isolation, but it doesn't work so don't look at it

thresh.py - basic threshold demo

threshadapt.py - adaptive threshold demo

threshanim.py - animation of adaptive threshold, cycling through blocksize/constant variables

threshOtsu.py - Otsu threshold - not as good as adaptive for the sample image

featurematch.py - Brute Force Matching (BTMatching). A basis for directly comoparing a given image to other possible standard images.
