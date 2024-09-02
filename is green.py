import cv2
import time
import numpy as np

cam = cv2.VideoCapture(0)

def check_exit():
    key = cv2.waitKey(1)
    if key == 27:
        return True
    return False


while True:
    check, frame = cam.read()
    image = cv2.resize(frame,(320,240))
    image_height, image_width, _ = image.shape
    cv2.imshow('image', image)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([110,50,50])
    upper_green = np.array([130,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('image', image)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    if check_exit():
        break
cam.release()
cv2.destroyAllWindows()
