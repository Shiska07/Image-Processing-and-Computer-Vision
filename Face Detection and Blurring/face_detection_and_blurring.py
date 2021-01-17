import cv2
import numpy as np 

# store paths for all required files
cascade_path = 'C:/Users/shisk/Desktop/OpenCV Shared/Notes/Projects/Face Detection and Blurring/haarcascades/haarcascade_frontalface_alt2.xml'

# create haarcascade object for face detection
face_cascade = cv2.CascadeClassifier(cascade_path)

def detect_face_and_blur(image):
    # make a copy of the passed frame
    face_image = image.copy()

    # this detects faces and returns rectangle values for each face
    face_rectangles = face_cascade.detectMultiScale(face_image, scaleFactor = 1.1, minNeighbors = 5)

    # for each face detected, draw a rectangle using the values in face_rectangles
    for (x,y,w,h) in face_rectangles:
        face_image[y:y+h,x:x+w] = cv2.blur(face_image[y:y+h,x:x+w],ksize = (25,25))

    # return image with rectangles
    return face_image

cap = cv2.VideoCapture(0)

while True:

    #start reading from the camera
    ret, frame = cap.read(0)

    # store detected faces with rectangles in faces
    faces = detect_face_and_blur(frame)
    
    # display detected faces
    cv2.imshow('Face',faces)

    k = cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
