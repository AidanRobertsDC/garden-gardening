import cv2
import time
import numpy as np
import serial.tools.list_ports
from pySerialTransfer import pySerialTransfer as txfer

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portslist = []

for one in ports:
    portslist.append(str(one))
    print(str(one))

com_ports = [port.split(' ')[0] for port in portslist]


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

contoursf, hierarchyf = cv2.findContours(blur_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

c = 0 
thing = {}
for i in range(0, len(contoursf)):
    if cv2.contourArea(contoursf[i]) >= 1000:
        M = cv2.moments(contoursf[i])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        thing[c]=(cX,cY)
        c+=1
                
try:

    link = txfer.SerialTransfer(com_ports[0])
        
    link.open()
    time.sleep(2) # allow some time for the Arduino to completely reset            
    print('linked')
    while True:
        check, image = cam.read()
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([110,50,50])
        upper_green = np.array([130,255,255])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        res = cv2.bitwise_and(image,image, mask= mask)
        blur_image = cv2.GaussianBlur(mask, (5,5), 0)

        contours, hierarchy = cv2.findContours(blur_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        print('found')
        good_plants = []
        bad_plants = []
        
        for i in range(0, len(contours)):
            if cv2.contourArea(contours[i]) >= 1000:
                for c in range(0, len(thing)): 
                    if cv2.pointPolygonTest(contours[i],thing[c], False) >= 0:
                        good_plants.append(contours[i])
                    else:
                        bad_plants.append(contours[i])  
        print('assined')
        cv2.drawContours(image, bad_plants, -1, (255,0,0), 3)
        cv2.drawContours(image, good_plants, -1, (0,0,255), 3)

        
        sbX = []
        sbY = []
        for weed in bad_plants :
            bM = cv2.moments(weed)
            bX = int(bM["m10"] / bM["m00"])
            bY = int(bM["m01"] / bM["m00"])
            sbX.append(bX)
            sbY.append(bY)

        sgX = []
        sgY = []
        for plant in good_plants:
            gM = cv2.moments(plant)
            gX = int(gM["m10"] / gM["m00"])
            gY = int(gM["m01"] / gM["m00"])
            sgX.append(gX)
            sgY.append(gY)
 
        send_size = 0
        if len(sgX) > 0: 
            list_gX = [sgX]
            list_size = link.tx_obj(list_gX)
            send_size += list_size
        
        str_sgX = 'sgX'
        str_size = link.tx_obj(str_sgX, send_size) - send_size
        send_size += str_size

        link.send(send_size)
        print('sent')
        while not link.available():
                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))

        if len(sgX) > 0:
            rec_list_  = link.rx_obj(obj_type=type(list_gX),
                                        obj_byte_size=list_size,
                                        list_format='i')
        
            rec_str_   = link.rx_obj(obj_type=type(str_sgX),
                                     obj_byte_size=str_size,
                                     start_pos=list_size)
            
            print('SENT: {} {}'.format(list_gX,str_sgX))
            print('RCVD: {} {}'.format(rec_list_,rec_str_))
            print(' ')

        else:
            rec_str_   = link.rx_obj(obj_type=type(str_sgX),
                                     obj_byte_size=str_size,
                                     start_pos=0)
            
            print('SENT: {}'.format(str_sgX))
            print('RCVD: {}'.format(rec_str_))
            print(' ')

        cv2.imshow('image', image)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        cv2.imshow('blur_image',blur_image)


        if check_exit():
            break

except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass
cam.release()
cv2.destroyAllWindows()
