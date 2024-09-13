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
thing = {}
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

    good_plants = []
    bad_plants = []
    
    for i in range(0, len(contours)):
        if cv2.contourArea(contours[i]) >= 1000:
              for c in range(0, len(thing)): 
                if cv2.pointPolygonTest(contours[i],thing[c], False) >= 0:
                  good_plants.append(contours[i])
                else:
                  bad_plants.append(contours[i])  
    
    cv2.drawContours(image, bad_plants, -1, (255,0,0), 3)
    cv2.drawContours(image, good_plants, -1, (0,0,255), 3)

    

    b = 0
    bad = {}
    for weed in bad_plants :
      bM = cv2.moments(weed)
      bX = int(bM["m10"] / bM["m00"])
      bY = int(bM["m01"] / bM["m00"])
      bad[b] = (bX,bY)
      b+=1

    g = 0
    good = {}
    for plant in good_plants:
        gM = cv2.moments(plant)
        gX = int(gM["m10"] / gM["m00"])
        gY = int(gM["m01"] / gM["m00"])
        good[g] = (gX,gY)
        g+=1 

    send = [good,bad] 
    
    cv2.imshow('image', image)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('blur_image',blur_image)


    if check_exit():
        break
cam.release()
cv2.destroyAllWindows()

