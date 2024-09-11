import cv2
import time
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(3,640)
cam.set(4,480)

def check_exit():
    key = cv2.waitKey(1)
    if key == 27:
        return True
    return False
check, image = cam.read()
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([110,50,50])
    upper_green = np.array([130,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(image,image, mask= mask)
    blur_image = cv2.GaussianBlur(mask, (5,5), 0)

    contours, hierarchy = cv2.findContours(blur_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    c = 0    
for i in range(0, len(contours)):
    if cv2.contourArea(contours[i]) >= 1000:
        M = cv2.moments(contours[i])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        thing[c]=(cX,cY)
        c+=1
            

while True:
    check, image = cam.read()
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([110,50,50])
    upper_green = np.array([130,255,255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(image,image, mask= mask)
    blur_image = cv2.GaussianBlur(mask, (5,5), 0)

    contours, hierarchy = cv2.findContours(blur_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for i in range(0, len(contours)):
        if cv2.contourArea(contours[i]) >= 1000:
            cv2.drawContours(image, contours, i, (0,255,0), 3)
    
        
    
    
    cv2.imshow('image', image)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('blur_image',blur_image)


    if check_exit():
        break
cam.release()
cv2.destroyAllWindows()
