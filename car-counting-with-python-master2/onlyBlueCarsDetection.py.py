import cv2
import numpy as np 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import xlsxwriter

planWorkBook = xlsxwriter.Workbook('mavi.xlsx')  #name of the file to be saved
planSheet = planWorkBook.add_worksheet("sayfaAdi")
planSheet.write("A1","GECEN ZAMAN")   # Name of column 1
planSheet.write("B1","GELEN ARAC SAYISI") # Name of column 2
planSheet.write("C1","GİDEN ARAC SAYISI")  # Name of column 3


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
       self.Algılanan_Arac_Sayisi=0
       


gelen_arac_sayisi = []
giden_arac_sayisi = []
gecen_zaman = []
gelen_arac_sayisi.append(0)
giden_arac_sayisi.append(0)

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

    blue_lower = np.array([94, 80, 2],np.uint8)
    blue_upper = np.array([140, 255, 255],np.uint8)
    blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)
    #blue = cv2.bitwise_and(frame, frame, mask=blue_mask)


    blue_mask = cv2.dilate(blue_mask,kernal)
    res_blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    cv2.imshow("Blue",blue_mask)

    
# resize frame
    Kesilmis_Kare= frame
    Doldurulmus_Resim=np.zeros((Kesilmis_Kare.shape[0],Kesilmis_Kare.shape[1], 1), np.uint8)

    contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area >200):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(Doldurulmus_Resim,(x,y),(x+w,y+h),(255),thickness=cv2.FILLED)
            cv2.putText(frame,"Blue Color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,0))  

    # make morphology for frame
    Arka_Plani_Silinmis_Kare=fgbg.apply(Kesilmis_Kare)
    Arka_Plani_Silinmis_Kare=cv2.morphologyEx(Arka_Plani_Silinmis_Kare,cv2.MORPH_OPEN,kernal)
    ret,Arka_Plani_Silinmis_Kare=cv2.threshold(Arka_Plani_Silinmis_Kare,127,255,cv2.THRESH_BINARY)

    # detect moving anything
    cnts,_=cv2.findContours(Arka_Plani_Silinmis_Kare,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    Sonuc=Kesilmis_Kare.copy()
    

    # detect whether there is car via bitwise_and
    
    Sensor2_Maske_Sonuc = cv2.bitwise_or(Doldurulmus_Resim,Doldurulmus_Resim,mask=Sensor2.Maske)
    Sensor2_Beyaz_Piksel_Sayisi=np.sum(Sensor2_Maske_Sonuc==255)
    Sensor2_Oran=Sensor2_Beyaz_Piksel_Sayisi/Sensor2.Maskenin_Alanı

    Sensor1_Maske_Sonuc=cv2.bitwise_or(Doldurulmus_Resim,Doldurulmus_Resim,mask=Sensor1.Maske)
    Sensor1_Beyaz_Piksel_Sayisi=np.sum(Sensor1_Maske_Sonuc==255)
    Sensor1_Oran=Sensor1_Beyaz_Piksel_Sayisi/Sensor1.Maskenin_Alanı

    print("sensor2",Sensor2_Oran)
    print("sensor1",Sensor1_Oran)
    if (Sensor2_Oran>=0.5 and   Sensor2.Durum==False):
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor2.Durum = True
    elif (Sensor2_Oran>0.1 and Sensor2_Oran<=4 and Sensor2.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor2.Algılanan_Arac_Sayisi+=1
        Sensor2.Durum = False
    else :
        cv2.rectangle(Sonuc, (Sensor2.Koordinat1.x, Sensor2.Koordinat1.y), (Sensor2.Koordinat2.x, Sensor2.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
        
    
    if (Sensor1_Oran>=0.5 and   Sensor1.Durum==False):
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0,255, 0,), thickness=cv2.FILLED)
        Sensor1.Durum = True
    elif (Sensor1_Oran>0.1 and Sensor1_Oran<=4 and Sensor1.Durum==True) :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0,255), thickness=cv2.FILLED)
        Sensor1.Durum = False
        Sensor1.Algılanan_Arac_Sayisi+=1
    else :
        cv2.rectangle(Sonuc, (Sensor1.Koordinat1.x, Sensor1.Koordinat1.y), (Sensor1.Koordinat2.x, Sensor1.Koordinat2.y),
                      (0, 0, 255), thickness=cv2.FILLED)
    

    cv2.putText(Sonuc,str(Sensor1.Algılanan_Arac_Sayisi),(Sensor1.Koordinat1.x,150),font,2,(255,255,255))
    cv2.putText(Sonuc,str(Sensor2.Algılanan_Arac_Sayisi),(Sensor2.Koordinat1.x,150),font,2,(255,255,255))



    if now < video_bölme_bitis_zamanı :   # We've added our interval to video_bölme_bitis_zamanı and we're constantly increasing it as the time gets closer to it.
      cv2.imshow("Sonuc",Sonuc)
      now = datetime.now()
    elif video_bölme_bitis_zamanı <= now:       #%H:%M:%S
      zaman = video_bölme_bitis_zamanı.strftime("%H:%M")  #converted to datetime string type
      gecen_zaman.append(zaman)  
      video_bölme_bitis_zamanı += timedelta(seconds=aralikTOsaniye)
      gelen_arac_sayisi.append(Sensor2.Algılanan_Arac_Sayisi)
      giden_arac_sayisi.append(Sensor1.Algılanan_Arac_Sayisi)
      Sensor1.Algılanan_Arac_Sayisi = 0
      Sensor2.Algılanan_Arac_Sayisi = 0
      Sensor1.Algılanan_Uzun_Arac_Sayısı = 0
      Sensor2.Algılanan_Uzun_Arac_Sayısı = 0


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
        #print("Gelen En Büyük Sayı :", gelen_en_buyuk, "\n Gelen En Küçük Sayı :",gelen_en_kucuk)
        #print("En Büyük index :", gelen_index_buyuk, " :" ,gelen_arac_sayisi[gelen_index_buyuk] ,"\n En Küçük İndex :",gelen_index_kucuk, ": ",gelen_arac_sayisi[gelen_index_kucuk])
        print("GELEN Araç yoğunluğunun en fazla olduğu aralık :", gelen_arac_sayisi[gelen_index_buyuk])
        for m in giden_arac_sayisi:
            if giden_en_kucuk > m:
                giden_en_kucuk = m
                giden_index_kucuk = j
            if giden_en_buyuk < m:
                giden_en_buyuk = m
                giden_index_buyuk = j
            j = j + 1
        #print("Giden En Büyük Sayı :", giden_en_buyuk, "\n Giden En Küçük Sayı :",giden_en_kucuk)
        #print("En Büyük index :", giden_index_buyuk, " :" ,giden_arac_sayisi[giden_index_buyuk] ,"\n En Küçük İndex :",giden_index_kucuk, ": ",giden_arac_sayisi[giden_index_kucuk])
        print("GİDEN Araç yoğunluğunun en fazla olduğu aralık :", giden_arac_sayisi[giden_index_buyuk])
        print(gecen_zaman)
        print(gelen_arac_sayisi)
        print(giden_arac_sayisi)
        for i in range(0,len(gecen_zaman)): # We find the length of the array.
         planSheet.write(i+1,0,gecen_zaman[i]) # (row order, column order, value) time column stays in 0th column so I just incremented the rows

        for i in range(0,len(gelen_arac_sayisi)): # We find the length of the array.
            planSheet.write(i+1,1,gelen_arac_sayisi[i])  #  Since the incoming vehicle column remains in the 1st column, I just increased the rows

        for i in range(0,len(giden_arac_sayisi)): # We find the length of the array.
            planSheet.write(i+1,2,giden_arac_sayisi[i]) # I just incremented the rows as the outbound vehicle column stays in the 2nd column


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
