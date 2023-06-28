import cv2
import numpy as np 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import xlsxwriter

planWorkBook = xlsxwriter.Workbook('veri.xlsx')  #name of the file to be saved
planSheet = planWorkBook.add_worksheet("sayfaAdi")
planSheet.write("A1","GECEN ZAMAN")   # Name of column 1
planSheet.write("B1","GELEN ARAC SAYISI") # Name of column 2
planSheet.write("C1","GELEN UZUN ARAC SAYISI") #Name of column 3
planSheet.write("D1","GİDEN ARAC SAYISI")  # Name of column 4
planSheet.write("E1","GİDEN UZUN ARAC SAYISI") # Name of column 5
planSheet.write("F1","GELEN BEYAZ ARAC SAYISI") # Name of column 6
planSheet.write("G1","GİDEN BEYAZ ARAC SAYISI")  # Name of column 7
planSheet.write("H1","GELEN KIRMIZI ARAC SAYISI") # Name of column 8
planSheet.write("I1","GİDEN KIRMIZI ARAC SAYISI")  # Name of column 9
planSheet.write("J1","GELEN MAVİ ARAC SAYISI") # Name of column 10
planSheet.write("K1","GİDEN MAVİ ARAC SAYISI")  # Name of column 11
planSheet.write("L1","GELEN SARI ARAC SAYISI") # Name of column 12
planSheet.write("M1","GİDEN SARI ARAC SAYISI")  # Name of column 13
planSheet.write("N1","GELEN YEŞİL ARAC SAYISI") # Name of column 14
planSheet.write("O1","GİDEN YEŞİL ARAC SAYISI")  # Name of column 15



def rescale(frame, scale=1):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    if (width<=0 or  height <=0):
        width = frame.shape[1]
        height = frame.shape[0]
 
    boyut = (width, height)
    return cv2.resize(frame, boyut, interpolation=cv2.INTER_AREA)

class Koordinat:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Sensor:
    def __init__(self,Koordinat1,Koordinat2,Kare_Genislik,Kare_Yükseklik):
       self.Koordinat1 = Koordinat1
       self.Koordinat2 = Koordinat2
       self.Kare_Genislik = Kare_Genislik
       self.Kare_Yükseklik = Kare_Yükseklik
       self.Maskenin_Alanı = abs(self.Koordinat2.x-self.Koordinat1.x)
       self.Maske=np.zeros((Kare_Genislik,Kare_Yükseklik,1),np.uint8)*abs(self.Koordinat2.y-self.Koordinat1.y)
       cv2.rectangle(self.Maske,(self.Koordinat1.x,self.Koordinat1.y),(self.Koordinat2.x,self.Koordinat2.y),(255),thickness=cv2.FILLED)
       self.Durum=False
       self.Algilanan_Arac_Sayisi=0
       self.Algilanan_Uzun_Arac_Sayisi = 0
       self.Sari_Arac = 0
       self.Kirmizi_Arac = 0
       self.Beyaz_Arac = 0
       self.Mavi_Arac = 0
       self.Yesil_Arac = 0


gelen_arac_sayisi = []
giden_arac_sayisi = []
gelen_uzun_arac_sayisi = []
giden_uzun_arac_sayisi = []
gelen_kirmizi_arac_sayisi = []
giden_kirmizi_arac_sayisi = []
gelen_beyaz_arac_sayisi = []
giden_beyaz_arac_sayisi = []
gelen_mavi_arac_sayisi = []
giden_mavi_arac_sayisi = []
gelen_sari_arac_sayisi = []
giden_sari_arac_sayisi = []
gelen_yesil_arac_sayisi = []
giden_yesil_arac_sayisi = []
gecen_zaman = []
gelen_arac_sayisi.append(0)
giden_arac_sayisi.append(0)
gelen_uzun_arac_sayisi.append(0)
giden_uzun_arac_sayisi.append(0)
gelen_kirmizi_arac_sayisi.append(0)
giden_kirmizi_arac_sayisi.append(0)
gelen_beyaz_arac_sayisi .append(0)
giden_beyaz_arac_sayisi.append(0)
gelen_mavi_arac_sayisi.append(0)
giden_mavi_arac_sayisi.append(0)
gelen_sari_arac_sayisi.append(0)
giden_sari_arac_sayisi .append(0)
gelen_yesil_arac_sayisi .append(0)
giden_yesil_arac_sayisi .append(0)

aralik = 1  #Determining the number of vehicles that will pass at intervals of how many minutes
aralikTOsaniye = aralik*60;
now = datetime.now()
gecen_zaman.append(now.strftime("%H:%M"))
video_bölme_bitis_zamanı = now + timedelta(seconds=aralikTOsaniye)

video = "https://5a78c55e99e82.streamlock.net/ButtimKavsagi/smil:ButtimKavsagi/chunklist_w1281486873_b700000_tkd293emF0b2tlbmVuZHRpbWU9MTY4MzU1NDE5MCZ3b3d6YXRva2VuaGFzaD1jOTdGUlJ1VzdYV3FKdGJBV09kaUhPTzZXaDFvaWVnYkFtX1UwcWZEcG5tU1JTWlRBMTBiVDNPMERGNlBNU3NNJndvd3phdG9rZW5zdGFydHRpbWU9MTY4MzU1MjM5MA==.m3u8"
#video = "./video.avi"

Video_Okuyucu=cv2.VideoCapture(video )
ret,Kare=Video_Okuyucu.read()
Kesilmis_Kare= Kare
#print(Kesilmis_Kare.shape[0])
#print(Kesilmis_Kare.shape[1])
fgbg=cv2.createBackgroundSubtractorMOG2()

Sensor1 = Sensor(
    Koordinat(720, Kesilmis_Kare.shape[1] - 980),
    Koordinat(950, Kesilmis_Kare.shape[1] - 970),
    Kesilmis_Kare.shape[0],
    Kesilmis_Kare.shape[1])

Sensor2 = Sensor(
    Koordinat(10, 420),
    Koordinat(300, 410),
    Kesilmis_Kare.shape[0],
    Kesilmis_Kare.shape[1])

font=cv2.FONT_HERSHEY_TRIPLEX

kernal = np.ones((5,5), "uint8")
fgbg=cv2.createBackgroundSubtractorMOG2()

gelen_en_kucuk = gelen_arac_sayisi[0] # I assigned the first element of the array. It doesn't really matter since it's controlled by function
gelen_en_buyuk = gelen_arac_sayisi[0] # I assigned the first element of the array. It doesn't really matter since it's controlled by function
gelen_index_kucuk = 0 # The index to find the one with the smallest value from the incoming vehicles
gelen_index_buyuk = 0 # The index to find the one with the highest value among the incoming vehicles
i = 0 # defined to find the index of the incoming vehicles array

giden_en_kucuk = giden_arac_sayisi[0] # I assigned the first element of the array. It doesn't really matter since it's controlled by function
giden_en_buyuk = giden_arac_sayisi[0] # I assigned the first element of the array. It doesn't really matter since it's controlled by function
giden_index_kucuk = 0 # index to find the one with the smallest value from the outgoing vehicles
giden_index_buyuk = 0 # index to find the vehicle with the highest value
j = 0 # defined to find the index of outgoing vehicles array

while (1):
    _, frame = Video_Okuyucu.read()
    frame = rescale(frame)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([136,87,111],np.uint8)
    red_upper = np.array([180, 255, 255],np.uint8)
    red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)

    red_mask = cv2.dilate(red_mask,kernal)
    res_red = cv2.bitwise_and(frame, frame, mask= red_mask)

    yellow_lower = np.array([20, 100, 100],np.uint8)
    yellow_upper = np.array([30, 255, 255],np.uint8)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)

    yellow_mask = cv2.dilate(yellow_mask,kernal)
    res_yellow = cv2.bitwise_and(frame, frame, mask=yellow_mask)

    white_lower = np.array([40, 0, 193],np.uint8)
    white_upper = np.array([180, 255, 255],np.uint8)
    white_mask = cv2.inRange(hsv_frame, white_lower, white_upper)

    white_mask = cv2.dilate(white_mask,kernal)
    res_white = cv2.bitwise_and(frame, frame, mask=white_mask)

    blue_lower = np.array([94, 80, 2],np.uint8)
    blue_upper = np.array([140, 255, 255],np.uint8)
    blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)

    blue_mask = cv2.dilate(blue_mask,kernal)
    res_blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    green_lower = np.array([40, 55, 80],np.uint8)
    green_upper = np.array([70, 255, 255],np.uint8)
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

    green_mask = cv2.dilate(green_mask,kernal)
    res_green = cv2.bitwise_and(frame, frame, mask=green_mask)

# resize frame
    Kesilmis_Kare= frame
    Doldurulmus_Resim=np.zeros((Kesilmis_Kare.shape[0],Kesilmis_Kare.shape[1], 1), np.uint8)

    Kesilmis_Kare_tüm= frame
    Doldurulmus_Resim_tüm=np.zeros((Kesilmis_Kare_tüm.shape[0],Kesilmis_Kare_tüm.shape[1], 1), np.uint8)

    Kesilmis_Kare_red= frame
    Doldurulmus_Resim_red=np.zeros((Kesilmis_Kare_red.shape[0],Kesilmis_Kare_red.shape[1], 1), np.uint8)

    Kesilmis_Kare_white= frame
    Doldurulmus_Resim_White=np.zeros((Kesilmis_Kare_white.shape[0],Kesilmis_Kare_white.shape[1], 1), np.uint8)

    Kesilmis_Kare_yellow= frame
    Doldurulmus_Resim_yellow=np.zeros((Kesilmis_Kare_yellow.shape[0],Kesilmis_Kare_yellow.shape[1], 1), np.uint8)

    Kesilmis_Kare_blue= frame
    Doldurulmus_Resim_blue=np.zeros((Kesilmis_Kare_blue.shape[0],Kesilmis_Kare_blue.shape[1], 1), np.uint8)

    Kesilmis_Kare_green= frame
    Doldurulmus_Resim_green=np.zeros((Kesilmis_Kare_green.shape[0],Kesilmis_Kare_green.shape[1], 1), np.uint8)

    kernel=np.ones((5,5),np.uint8)
    Arka_Plani_Silinmis_Kare=fgbg.apply(Kesilmis_Kare_tüm)
    Arka_Plani_Silinmis_Kare=cv2.morphologyEx(Arka_Plani_Silinmis_Kare,cv2.MORPH_OPEN,kernel)
    ret,Arka_Plani_Silinmis_Kare=cv2.threshold(Arka_Plani_Silinmis_Kare,127,255,cv2.THRESH_BINARY)
    cnts,_=cv2.findContours(Arka_Plani_Silinmis_Kare,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    #Sonuc=Kesilmis_Kare.copy()

    # detect moving anything with loop
    for cnt in cnts:
        x,y,w,h=cv2.boundingRect(cnt)
        if(w>30 and h>30):
            cv2.rectangle(Sonuc,(x,y),(x+w,y+h),(255,0,0),thickness=2)
            cv2.rectangle(Doldurulmus_Resim_tüm,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)

    #creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >100):
            x,y,w,h = cv2.boundingRect(contour)
            frame_red = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
            cv2.rectangle(Doldurulmus_Resim_red,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)
            cv2.putText(frame_red,"Red Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,0,255))
    
    #creating contour to track yellow color
    contours, hierarchy = cv2.findContours(yellow_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >300):
            x,y,w,h = cv2.boundingRect(contour)
            frame_yellow = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,255),2)
            cv2.rectangle(Doldurulmus_Resim_yellow,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)
            cv2.putText(frame_yellow,"Yellow Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,255,255))
    
    #creating contour to track white color
    contours, hierarchy = cv2.findContours(white_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >350):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(255, 255, 255),2)
            cv2.rectangle(Doldurulmus_Resim_White,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)
            cv2.putText(frame,"White Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255, 255, 255))

    contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >200):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(Doldurulmus_Resim_blue,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)
            cv2.putText(frame,"Blue Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,0)) 

    contours, hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if (area >400):
                x,y,w,h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                cv2.rectangle(Doldurulmus_Resim_green,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)
                cv2.putText(frame,"Green Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(0,255,0))


    # make morphology for frame
    Arka_Plani_Silinmis_Kare=fgbg.apply(Kesilmis_Kare)
    Arka_Plani_Silinmis_Kare=cv2.morphologyEx(Arka_Plani_Silinmis_Kare,cv2.MORPH_OPEN,kernal)
    ret,Arka_Plani_Silinmis_Kare=cv2.threshold(Arka_Plani_Silinmis_Kare,127,255,cv2.THRESH_BINARY)

    # detect moving anything
    cnts,_=cv2.findContours(Arka_Plani_Silinmis_Kare,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    Sonuc=Kesilmis_Kare.copy()
    
    Sensor1_Maske_Sonuc=cv2.bitwise_or(Doldurulmus_Resim_tüm,Doldurulmus_Resim_tüm,mask=Sensor1.Maske)
    Sensor1_Beyaz_Piksel_Sayisi=np.sum(Sensor1_Maske_Sonuc==255)
    Sensor1_Oran=Sensor1_Beyaz_Piksel_Sayisi/Sensor1.Maskenin_Alanı

    Sensor2_Maske_Sonuc = cv2.bitwise_or(Doldurulmus_Resim_tüm,Doldurulmus_Resim_tüm,mask=Sensor2.Maske)
    Sensor2_Beyaz_Piksel_Sayisi=np.sum(Sensor2_Maske_Sonuc==255)
    Sensor2_Oran=Sensor2_Beyaz_Piksel_Sayisi/Sensor2.Maskenin_Alanı

    if (Sensor1_Oran>=0.5 and Sensor1.Durum==False):
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor1.Durum = True
    elif (Sensor1_Oran>1 and Sensor1_Oran<=4 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Algilanan_Arac_Sayisi+=1
    elif (Sensor1_Oran>5.5 and Sensor1_Oran<=7.5 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 255,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Algilanan_Uzun_Arac_Sayisi += 1    
    else :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)


    if (Sensor2_Oran>=0.5 and   Sensor2.Durum==False):
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor2.Durum = True
    elif (Sensor2_Oran>1 and Sensor2_Oran<=4 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor2.Durum = False
        Sensor2.Algilanan_Arac_Sayisi+=1
    elif (Sensor2_Oran>5.45 and Sensor2_Oran<=7.2 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 255,255), thickness=cv2.FILLED)
        Sensor2.Durum = False
        Sensor2.Algilanan_Uzun_Arac_Sayisi += 1
    else :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)

    #RED
    Sensor2_Maske_Sonuc_Kirmizi = cv2.bitwise_or(Doldurulmus_Resim_red,Doldurulmus_Resim_red,mask=Sensor2.Maske)
    Sensor2_Beyaz_Piksel_Sayisi_Kirmizi=np.sum(Sensor2_Maske_Sonuc_Kirmizi==255)
    Sensor2_Oran_Kirmizi=Sensor2_Beyaz_Piksel_Sayisi_Kirmizi/Sensor2.Maskenin_Alanı

    Sensor1_Maske_Sonuc_Kirmizi=cv2.bitwise_or(Doldurulmus_Resim_red,Doldurulmus_Resim_red,mask=Sensor1.Maske)
    Sensor1_Beyaz_Piksel_Sayisi_Kirmizi=np.sum(Sensor1_Maske_Sonuc_Kirmizi==255)
    Sensor1_Oran_Kirmizi=Sensor1_Beyaz_Piksel_Sayisi_Kirmizi/Sensor1.Maskenin_Alanı

    if (Sensor2_Oran_Kirmizi>=0.5 and   Sensor2.Durum==False):
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor2.Durum = True
    elif (Sensor2_Oran_Kirmizi>0.1  and Sensor2_Oran_Kirmizi<3 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor2.Durum = False
        Sensor2.Kirmizi_Arac+=1
    else :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
        
    
    if (Sensor1_Oran_Kirmizi>=0.5 and   Sensor1.Durum==False):
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor1.Durum = True
    elif (Sensor1_Oran_Kirmizi>0.1 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Kirmizi_Arac+=1
    else :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
    
    
    #YELLOW
    Sensor2_Maske_Sonuc_Sari = cv2.bitwise_or(Doldurulmus_Resim_yellow,Doldurulmus_Resim_yellow,mask=Sensor2.Maske)
    Sensor2_Beyaz_Piksel_Sayisi_Sari=np.sum(Sensor2_Maske_Sonuc_Sari==255)
    Sensor2_Oran_Sari=Sensor2_Beyaz_Piksel_Sayisi_Sari/Sensor2.Maskenin_Alanı

    Sensor1_Maske_Sonuc_Sari=cv2.bitwise_or(Doldurulmus_Resim_yellow,Doldurulmus_Resim_yellow,mask=Sensor1.Maske)
    Sensor1_Beyaz_Piksel_Sayisi_Sari=np.sum(Sensor1_Maske_Sonuc_Sari==255)
    Sensor1_Oran_Sari=Sensor1_Beyaz_Piksel_Sayisi_Sari/Sensor1.Maskenin_Alanı


    if (Sensor2_Oran_Sari>=0.5 and   Sensor2.Durum==False):
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor2.Durum = True
    elif (Sensor2_Oran_Sari>0.3 and Sensor2_Oran_Sari<=4 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor2.Sari_Arac+=1
        Sensor2.Durum = False
    else :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
        
    
    if (Sensor1_Oran_Sari>=0.5 and   Sensor1.Durum==False):
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor1.Durum = True
    elif (Sensor1_Oran_Sari>0.3 and Sensor1_Oran_Sari<=2 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Sari_Arac+=1
    else :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
    
    #WHITE
    Sensor2_Maske_Sonuc_Beyaz = cv2.bitwise_or(Doldurulmus_Resim_White,Doldurulmus_Resim_White,mask=Sensor2.Maske)
    Sensor2_Beyaz_Piksel_Sayisi_Beyaz=np.sum(Sensor2_Maske_Sonuc_Beyaz==255)
    Sensor2_Oran_Beyaz=Sensor2_Beyaz_Piksel_Sayisi_Beyaz/Sensor2.Maskenin_Alanı

    Sensor1_Maske_Sonuc_Beyaz=cv2.bitwise_or(Doldurulmus_Resim_White,Doldurulmus_Resim_White,mask=Sensor1.Maske)
    Sensor1_Beyaz_Piksel_Sayisi_Beyaz=np.sum(Sensor1_Maske_Sonuc_Beyaz==255)
    Sensor1_Oran_Beyaz=Sensor1_Beyaz_Piksel_Sayisi_Beyaz/Sensor1.Maskenin_Alanı


    if (Sensor2_Oran_Beyaz>=0.5 and   Sensor2.Durum==False):
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor2.Durum = True
    elif (Sensor2_Oran_Beyaz>0.7 and Sensor2_Oran_Beyaz<=4.5 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor2.Durum = False
        Sensor2.Beyaz_Arac+=1
    else :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
        
    
    if (Sensor1_Oran_Beyaz>=0.5 and   Sensor1.Durum==False):
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor1.Durum = True
    elif (Sensor1_Oran_Beyaz>1 and Sensor1_Oran_Beyaz<=3 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Beyaz_Arac+=1
    else :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)

    #BLUE
    Sensor2_Maske_Sonuc_blue = cv2.bitwise_or(Doldurulmus_Resim_blue,Doldurulmus_Resim_blue,mask=Sensor2.Maske)
    Sensor2_Beyaz_Piksel_Sayisi_blue=np.sum(Sensor2_Maske_Sonuc_blue==255)
    Sensor2_Oran_Blue=Sensor2_Beyaz_Piksel_Sayisi_blue/Sensor2.Maskenin_Alanı

    Sensor1_Maske_Sonuc_blue=cv2.bitwise_or(Doldurulmus_Resim_blue,Doldurulmus_Resim_blue,mask=Sensor1.Maske)
    Sensor1_Beyaz_Piksel_Sayisi_blue=np.sum(Sensor1_Maske_Sonuc_blue==255)
    Sensor1_Oran_Blue=Sensor1_Beyaz_Piksel_Sayisi_blue/Sensor1.Maskenin_Alanı


    if (Sensor2_Oran_Blue>=0.5 and   Sensor2.Durum==False):
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor2.Durum = True
    elif (Sensor2_Oran_Blue>0.1 and Sensor2_Oran_Blue<=4 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor2.Mavi_Arac+=1
        Sensor2.Durum = False
    else :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
        
    
    if (Sensor1_Oran_Blue>=0.5 and   Sensor1.Durum==False):
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor1.Durum = True
    elif (Sensor1_Oran_Blue>0.1 and Sensor1_Oran_Blue<=4 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Mavi_Arac+=1
    else :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)

    #GREEN
    Sensor2_Maske_Sonuc_green = cv2.bitwise_or(Doldurulmus_Resim_green,Doldurulmus_Resim_green,mask=Sensor2.Maske)
    Sensor2_Beyaz_Piksel_Sayisi_green=np.sum(Sensor2_Maske_Sonuc_green==255)
    Sensor2_Oran_Green=Sensor2_Beyaz_Piksel_Sayisi_green/Sensor2.Maskenin_Alanı

    Sensor1_Maske_Sonuc_green=cv2.bitwise_or(Doldurulmus_Resim_green,Doldurulmus_Resim_green,mask=Sensor1.Maske)
    Sensor1_Beyaz_Piksel_Sayisi_green=np.sum(Sensor1_Maske_Sonuc_green==255)
    Sensor1_Oran_Green=Sensor1_Beyaz_Piksel_Sayisi_green/Sensor1.Maskenin_Alanı

    if (Sensor2_Oran_Green>=0.5 and   Sensor2.Durum==False):
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor2.Durum = True
    elif (Sensor2_Oran_Green>0.3 and Sensor2_Oran_Green<=3 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor2.Yesil_Arac+=1
        Sensor2.Durum = False
    else :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
        
    
    if (Sensor1_Oran_Green>=0.5 and   Sensor1.Durum==False):
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor1.Durum = True
    elif (Sensor1_Oran_Green>0.3 and Sensor1_Oran_Green<=3 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Yesil_Arac+=1
    else :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)


    cv2.putText(Sonuc,str(Sensor1.Algilanan_Arac_Sayisi),(Sensor1.Koordinat1.x,250),font,2,(0,0,0))
    cv2.putText(Sonuc,str(Sensor1.Algilanan_Uzun_Arac_Sayisi),(Sensor1.Koordinat1.x+150,250),font,2,(0,0,0))
    cv2.putText(Sonuc,str(Sensor2.Algilanan_Arac_Sayisi),(Sensor2.Koordinat1.x,250),font,2,(0,0,0))
    cv2.putText(Sonuc,str(Sensor2.Algilanan_Uzun_Arac_Sayisi),(Sensor2.Koordinat1.x+150,250),font,2,(0,0,0))

    cv2.putText(Sonuc,str(Sensor1.Kirmizi_Arac),(Sensor1.Koordinat1.x-100,150),font,2,(0,0,255))
    cv2.putText(Sonuc,str(Sensor2.Kirmizi_Arac),(Sensor2.Koordinat1.x,150),font,2,(0,0,255))
    cv2.putText(Sonuc,str(Sensor1.Sari_Arac),(Sensor1.Koordinat1.x-25,150),font,2,(0,255,255))
    cv2.putText(Sonuc,str(Sensor2.Sari_Arac),(Sensor2.Koordinat1.x+75,150),font,2,(0,255,255))
    cv2.putText(Sonuc,str(Sensor1.Beyaz_Arac),(Sensor1.Koordinat1.x+50,150),font,2,(255,255,255))
    cv2.putText(Sonuc,str(Sensor2.Beyaz_Arac),(Sensor2.Koordinat1.x+150,150),font,2,(255,255,255))
    cv2.putText(Sonuc,str(Sensor1.Mavi_Arac),(Sensor1.Koordinat1.x+125,150),font,2,(255,0,0))
    cv2.putText(Sonuc,str(Sensor2.Mavi_Arac),(Sensor2.Koordinat1.x+225,150),font,2,(255,0,0))
    cv2.putText(Sonuc,str(Sensor1.Yesil_Arac),(Sensor1.Koordinat1.x+200,150),font,2,(0,255,0))
    cv2.putText(Sonuc,str(Sensor2.Yesil_Arac),(Sensor2.Koordinat1.x+300,150),font,2,(0,255,0))


    if now < video_bölme_bitis_zamanı :   # We've added our interval to video_bölme_bitis_zamanı and we're constantly increasing it as the time gets closer to it.
      cv2.imshow("Sonuc",Sonuc)
      now = datetime.now()
    elif video_bölme_bitis_zamanı <= now:       #%H:%M:%S
      zaman = video_bölme_bitis_zamanı.strftime("%H:%M")   #converted to datetime string type
      gecen_zaman.append(zaman) 
      video_bölme_bitis_zamanı += timedelta(seconds=aralikTOsaniye)
      gelen_arac_sayisi.append(Sensor2.Algilanan_Arac_Sayisi)
      giden_arac_sayisi.append(Sensor1.Algilanan_Arac_Sayisi)
      gelen_uzun_arac_sayisi.append(Sensor2.Algilanan_Uzun_Arac_Sayisi)
      giden_uzun_arac_sayisi.append(Sensor1.Algilanan_Uzun_Arac_Sayisi)
      gelen_kirmizi_arac_sayisi.append(Sensor2.Kirmizi_Arac)
      giden_kirmizi_arac_sayisi.append(Sensor1.Kirmizi_Arac)
      gelen_beyaz_arac_sayisi.append(Sensor2.Beyaz_Arac)
      giden_beyaz_arac_sayisi.append(Sensor1.Beyaz_Arac)
      gelen_mavi_arac_sayisi.append(Sensor2.Mavi_Arac)
      giden_mavi_arac_sayisi.append(Sensor1.Mavi_Arac)
      gelen_sari_arac_sayisi.append(Sensor2.Sari_Arac)
      giden_sari_arac_sayisi.append(Sensor1.Sari_Arac)
      gelen_yesil_arac_sayisi.append(Sensor2.Yesil_Arac)
      giden_yesil_arac_sayisi.append(Sensor1.Yesil_Arac)
      Sensor1.Algilanan_Arac_Sayisi = 0
      Sensor2.Algilanan_Arac_Sayisi = 0
      Sensor1.Algilanan_Uzun_Arac_Sayisi = 0
      Sensor2.Algilanan_Uzun_Arac_Sayisi = 0
      Sensor2.Kirmizi_Arac = 0
      Sensor1.Kirmizi_Arac   = 0 
      Sensor2.Beyaz_Arac = 0
      Sensor1.Beyaz_Arac = 0
      Sensor2.Mavi_Arac = 0
      Sensor1.Mavi_Arac = 0
      Sensor2.Sari_Arac = 0
      Sensor1.Sari_Arac = 0
      Sensor2.Yesil_Arac = 0
      Sensor1.Yesil_Arac = 0


    k=cv2.waitKey(60) & 0xff    # When you press esc, the program closes.
    if k == 27 :
        for n in gelen_arac_sayisi:
            if gelen_en_kucuk > n:
                gelen_en_kucuk = n
                gelen_index_kucuk = i
            if gelen_en_buyuk < n:
                gelen_en_buyuk = n
                gelen_index_buyuk = i
            i = i + 1
        print("Gelen En Büyük Sayı :", gelen_en_buyuk, "\n Gelen En Küçük Sayı :",gelen_en_kucuk)
        print("En Büyük index :", gelen_index_buyuk, " :" ,gelen_arac_sayisi[gelen_index_buyuk] ,"\n En Küçük İndex :",gelen_index_kucuk, ": ",gelen_arac_sayisi[gelen_index_kucuk])
        print("GELEN Araç yoğunluğunun en fazla olduğu aralık :", gecen_zaman[gelen_index_buyuk-1] ," ile " ,gecen_zaman[gelen_index_buyuk ], " arasındadır")
        for m in giden_arac_sayisi:
            if giden_en_kucuk > m:
                giden_en_kucuk = m
                giden_index_kucuk = j
            if giden_en_buyuk < m:
                giden_en_buyuk = m
                giden_index_buyuk = j
            j = j + 1
        print("Giden En Büyük Sayı :", giden_en_buyuk, "\n Giden En Küçük Sayı :",giden_en_kucuk)
        print("En Büyük index :", giden_index_buyuk, " :" ,giden_arac_sayisi[giden_index_buyuk] ,"\n En Küçük İndex :",giden_index_kucuk, ": ",giden_arac_sayisi[giden_index_kucuk])
        print("GİDEN Araç yoğunluğunun en fazla olduğu aralık :", gecen_zaman[giden_index_buyuk-1] ," ile " ,gecen_zaman[giden_index_buyuk ], " arasındadır")
        
        print(gecen_zaman)
        print(gelen_arac_sayisi)
        print(giden_arac_sayisi)   
        for i in range(0,len(gecen_zaman)): # We find the length of the array.
         planSheet.write(i+1,0,gecen_zaman[i]) # (row order, column order, value) time column stays in 0th column so I just incremented the rows

        for i in range(0,len(gelen_arac_sayisi)): #We find the length of the array.
            planSheet.write(i+1,1,gelen_arac_sayisi[i]) #  Since the incoming vehicle column remains in the 1st column, I just increased the rows

        for i in range(0,len(gelen_uzun_arac_sayisi)): #We find the length of the array.
            planSheet.write(i+1,2,gelen_uzun_arac_sayisi[i]) #  Since the incoming vehicle column remains in the 2nd column, I just increased the rows

        for i in range(0,len(giden_arac_sayisi)): #We find the length of the array.
            planSheet.write(i+1,3,giden_arac_sayisi[i])# I just incremented the rows as the outbound vehicle column stays in the 3rd column

        for i in range(0,len(giden_uzun_arac_sayisi)): #We find the length of the array.
            planSheet.write(i+1,4,giden_uzun_arac_sayisi[i])# I just increased the rows as the outgoing long vehicle column stays in the 4th column
            
        for i in range(0,len(gelen_beyaz_arac_sayisi)): 
            planSheet.write(i+1,5,gelen_beyaz_arac_sayisi[i])

        for i in range(0,len(giden_beyaz_arac_sayisi)): 
            planSheet.write(i+1,6,giden_beyaz_arac_sayisi[i])

        for i in range(0,len(gelen_kirmizi_arac_sayisi)): 
            planSheet.write(i+1,7,gelen_kirmizi_arac_sayisi[i])

        for i in range(0,len(giden_kirmizi_arac_sayisi)): 
            planSheet.write(i+1,8,giden_kirmizi_arac_sayisi[i])
        
        for i in range(0,len(gelen_mavi_arac_sayisi)): 
            planSheet.write(i+1,9,gelen_mavi_arac_sayisi[i])

        for i in range(0,len(giden_mavi_arac_sayisi)): 
            planSheet.write(i+1,10,giden_mavi_arac_sayisi[i])

        for i in range(0,len(gelen_sari_arac_sayisi)): 
            planSheet.write(i+1,11,gelen_sari_arac_sayisi[i])
        
        for i in range(0,len(giden_sari_arac_sayisi)): 
            planSheet.write(i+1,12,giden_sari_arac_sayisi[i])

        for i in range(0,len(gelen_yesil_arac_sayisi)): 
            planSheet.write(i+1,13,gelen_yesil_arac_sayisi[i])
        
        for i in range(0,len(giden_yesil_arac_sayisi)): 
            planSheet.write(i+1,14,giden_yesil_arac_sayisi[i])

            
        planWorkBook.close() 
        plt.figure(figsize=(20,10))

        plt.subplot(2,2,1)   
        plt.plot(gecen_zaman,gelen_arac_sayisi,color="r") 
        plt.xlabel("Geçen Zaman")
        plt.ylabel("Gelen Araç Sayısı")
        plt.title("Gelen Araç")

        plt.subplot(2,2,2)
        plt.plot(gecen_zaman,giden_arac_sayisi,color="blue")
        plt.xlabel("Geçen Zaman")
        plt.ylabel("Giden Araç Sayısı")
        plt.title("Giden Araç")
        plt.show()

        break

Video_Okuyucu.release()  # such as releasing the file, not keeping it permanently, closing it briefly
cv2.destroyAllWindows()   #we destroy opencv windows
