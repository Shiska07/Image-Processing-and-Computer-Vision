import cv2
import numpy as np
from sklearn.metrics import pairwise

background = None
accumulated_weight = 0.5

# coordinates for ROI rectangle diagonaa points
y1 = 70
y2 = 300
x2 = 350
x1 = 600

# this function will set the background values to distinguish the hand as a foreground object
def calculate_accum_avg(frame, accumulated_weight):
    global background
    
    if background is None:
        background = frame.copy().astype('float')
        return None
    
    cv2.accumulateWeighted(frame, background, accumulated_weight)

# this function will convert the had and the background into a binary image and extract contours
def segment_hand(frame,threshold_min = 25):
    
    global backgound 
    
    diff = cv2.absdiff(background.astype('uint8'),frame)
    
    ret, thresholded_img = cv2.threshold(diff,threshold_min,255, cv2.THRESH_BINARY)
    
    image, contours, hirearchy = cv2.findContours(thresholded_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None
    else:
        # we just need the largest external contour in the roi
        hand_contour = max(contours, key = cv2.contourArea)
        
        # reutrning thresholded image and largest contour
        return (thresholded_img, hand_contour)

def count_fingers(thresholded_img, hand_contour):
    
    # to obtain the set of extreme points in the polygon
    conv_hull = cv2.convexHull(hand_contour)
    
    # extracting extreme points
    top = tuple(conv_hull[conv_hull[:, :, 1].argmin()][0])
    bottom = tuple(conv_hull[conv_hull[:, :, 1].argmax()][0])
    left   = tuple(conv_hull[conv_hull[:, :, 0].argmin()][0])
    right  = tuple(conv_hull[conv_hull[:, :, 0].argmax()][0])
    
    # calculate center values
    c_x = (left[0] + right[0]) // 2
    c_y = (top[1] + bottom[1]) // 2
    
    # calculate distance from center to four extreme ponits
    distance = pairwise.euclidean_distances([(c_x,c_y)], Y = [left,right,top,bottom])[0]
    
    max_distance = distance.max()
    
    # if the contour points extend beyond this radius, the finger is assumed to be raised
    radius = int(0.85*max_distance)
    circumference = (2*np.pi*radius)
    circ_roi = np.zeros(thresholded_img.shape[:2], dtype = 'uint8')
    
    cv2.circle(circ_roi,(c_x,c_y), radius, 255, 10)
    
    circ_roi = cv2.bitwise_and(thresholded_img, thresholded_img, mask = circ_roi)
    
    image, contours, hirearchy = cv2.findContours(circ_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    count = 0
    
    for cnt in contours:
        
        (x,y,w,h) = cv2.boundingRect(cnt)
        
        above_wrist = ((c_y+(c_y*0.25)) > (y+h))
        
        within_limit_points = ((circumference*0.25) > cnt.shape[0])
        
        if above_wrist and within_limit_points:
            count += 1
            
    return count

cap = cv2.VideoCapture(0)

num_frames = 0

while True:

    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    frame_copy = frame.copy()
    
    roi = frame[y1:y2, x2:x1]     #x2,x1 since the frame was flipped
    
    gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    
    if num_frames < 60:
        calculate_accum_avg(gray,accumulated_weight)
        
        if num_frames <= 59:
            cv2.putText(frame_copy, 'Wait, getting background info ...',(200,200),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
            cv2.imshow('Finger_count', frame_copy)
    else:
        hand = segment_hand(gray)    #remember this returns thresholded image and largest contour
        
        if hand is not None:
            
            thresholded_img, hand_contour = hand
            
            # draw contour around real hand in the live stream
            cv2.drawContours(frame_copy,[hand_contour + (x2,y1)],-1,(255,0,0),1)
            
            fingers = count_fingers(thresholded_img, hand_contour)
            
            cv2.putText(frame_copy,str(fingers),(70,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            
            cv2.imshow('Thresholded',thresholded_img)
            
    cv2.rectangle(frame_copy,(x1, y1), (x2, y2),(0,0,255),5)
    
    num_frames += 1
    
    cv2.imshow('Finger Count', frame_copy)
    
    k = cv2.waitKey(1) & 0xFF
    
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

