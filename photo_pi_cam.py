#! /usr/bin/python
# - *- coding: utf- 8 - *-

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

name = "İsim"  
#resmi çekilen kişinin ve resimlerin kaydedileceği klasörün ismi

cam = PiCamera()
cam.resolution = (512, 304) #çözünürlük
cam.framerate = 10
rawCapture = PiRGBArray(cam, size=(512, 304))
    
img_counter = 0

while True:
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Fotoğraf Çekmek için Boşluk Tuşuna Basın", image) 
        #Farklı açılardan 15 fotoğraf yeterli olacaktır.
        rawCapture.truncate(0)
    
        k = cv2.waitKey(1)
        rawCapture.truncate(0)
        if k%256 == 27: # ESC tuşuna basıldıysa kapatır.
            break
        elif k%256 == 32: #Boşluk tuşuna basıldıysa foto çeker
            
            img_name = "data/"+ name +"/image_{}.jpg".format(img_counter) 
            cv2.imwrite(img_name, image)
            print("{} kaydedildi!".format(img_name))
            img_counter += 1
            #Fotomuzu ilgili klasöre kaydettik.
            
    if k%256 == 27:
        print("Kapatılıyor...")
        break

cv2.destroyAllWindows()
