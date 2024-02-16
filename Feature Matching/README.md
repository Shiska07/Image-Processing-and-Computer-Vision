This is a short program on jupyter notebook which shows how various feature matching methods work in OpenCV. The feature matching methods used in the program are:

1. Brute-Force Matching with ORB Descriptors
2. Brute-Force Matching with SIFT Descriptors and Ratio Test
3. FLANN(Fast Library for Approximating Nearest Neighbors) Matcher

Feature matching algorithms do not require an exact copy of the the primary image(the image that will be used to identify feature) to be present in the target image. The algorithm extracts defining key fatures from the primary image and uses a distance calculation to find all possible feature matches in the target image.
