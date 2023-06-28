import numpy as np
import cv2 

video = "https://5a78c55e99e82.streamlock.net/ButtimKavsagi/smil:ButtimKavsagi/chunklist_w1281486873_b700000_tkd293emF0b2tlbmVuZHRpbWU9MTY4MzU1NDE5MCZ3b3d6YXRva2VuaGFzaD1jOTdGUlJ1VzdYV3FKdGJBV09kaUhPTzZXaDFvaWVnYkFtX1UwcWZEcG5tU1JTWlRBMTBiVDNPMERGNlBNU3NNJndvd3phdG9rZW5zdGFydHRpbWU9MTY4MzU1MjM5MA==.m3u8"
#video = "./video.avi"

webcam = cv2.VideoCapture(video)
kernal = np.ones((5,5), "uint8")
fgbg=cv2.createBackgroundSubtractorMOG2()

while(1):
    _, frame = webcam.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # BGR renk tonundaki videoyu HSV tonuna çevirdim.

    red_lower = np.array([136,87,111],np.uint8)  #kırmızı renk için düşük değer
    red_upper = np.array([180, 255, 255],np.uint8) # kırmızı renk için yüksek değer
    red_mask = cv2.inRange(hsv_frame, red_lower, red_upper) # kırmızı renk için verilen renk aralığı
    #red = cv2.bitwise_and(frame, frame, mask=red_mask)

    blue_lower = np.array([94, 80, 2],np.uint8) #mavi renk için düşük değer
    blue_upper = np.array([140, 255, 255],np.uint8) #mavi renk için yüksek değer
    blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)
    #blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    green_lower = np.array([40, 55, 80],np.uint8) #yeşil renk için düşük değer
    green_upper = np.array([70, 255, 255],np.uint8) #yeşil renk için yüksek değer
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)
    #green = cv2.bitwise_and(frame, frame, mask=green_mask)

    yellow_lower = np.array([20, 100, 100],np.uint8) #sarı renk için düşük değer
    yellow_upper = np.array([30, 255, 255],np.uint8) #sarı renk için yüksek değer
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    #yellow = cv2.bitwise_and(frame,frame,mask=yellow_mask)


    white_lower = np.array([40, 0, 193],np.uint8) #beyaz renk için düşük değer
    white_upper = np.array([180, 255, 255],np.uint8) #beyaz renk için yüksek değer
    white_mask = cv2.inRange(hsv_frame, white_lower, white_upper)
    #white = cv2.bitwise_and(frame, frame, mask=white_mask)



    #For red color
    red_mask = cv2.dilate(red_mask,kernal)
    res_red = cv2.bitwise_and(frame, frame, mask= red_mask)
    #For blue color
    blue_mask = cv2.dilate(blue_mask,kernal)
    res_blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    #For green color
    green_mask = cv2.dilate(green_mask,kernal)
    res_green = cv2.bitwise_and(frame, frame, mask=green_mask)
    
    yellow_mask = cv2.dilate(yellow_mask,kernal)
    res_yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    white_mask = cv2.dilate(white_mask,kernal)
    res_white = cv2.bitwise_and(frame, frame, mask=white_mask)
    #cv2.imshow("Ehite",white_mask)

    #creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(frame,"Red Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255))
     
    
    #creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area >300):
                x,y,w,h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(frame,"Green Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,255,0))


    #creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(frame,"Blue Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,0))  

    #creating contour to track yellow color
    contours, hierarchy = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,100,100),2)
            cv2.putText(frame,"Yellow Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,100,100))

    #creating contour to track white color
    contours, hierarchy = cv2.findContours(white_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(255, 255, 255),2)
            cv2.putText(frame,"White Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 255, 255))       
    

    cv2.imshow("Multiple Color Detection in Real-Time",frame)
    if cv2.waitKey(60) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break     

cv2.destroyAllWindows()
