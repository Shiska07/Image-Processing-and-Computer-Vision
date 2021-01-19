You will need the following libraries to run this program:

1. OpenCV
2. Numpy
2. Scikit learn

This program uses image segmentation and object detection to detect a hand present in the region of interest(roi). It uses background subtraction and convexHull to find contours around the hand. 

With end points obtained from the contours, the program counts the number of fingers raised as long as the edge of the polygon is detected outside the palm area but not below the wrist. 