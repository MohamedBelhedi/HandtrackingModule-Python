import cv2
import time
import numpy as np
import HandbewegungModul as hd
import math
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys




wCam,hCam=640,480

cap=cv2.VideoCapture(1)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
cTime=0


detector=hd.handDetector(detectionCon=0.7)



while True:

    success,Bild=cap.read()
    Bild=detector.findHands(Bild)
    lmList=detector.findPosition(Bild,draw=False)
    if len(lmList)!=0:
        print(f'Deine Hand{lmList[0],lmList[8]}')
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(Bild,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(Bild, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(Bild,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(Bild,(cx,cy),15,(255,0,255),cv2.FILLED)
        länge=math.hypot(x2-x1,y2-y1)
        print(länge)


        #Hand Range 50-400
        #volume Range -64-0



        if länge>=145:
            cv2.circle(Bild, (cx, cy), 15, (0, 233, 255), cv2.FILLED)

            chromdriver_path = "C:\Development\chromedriver.exe"

            driver = webdriver.Chrome(chromdriver_path)
            driver.get("https://youtube.com/")
            time.sleep(10)
            youtube=driver.delete_all_cookies()
            # youtube = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button')
            youtube = driver.find_element_by_xpath('//*[@id="search"]')
            youtube.send_keys('Sponge Bob Deutsch')
            youtube = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
            youtube.click()
            time.sleep(3)
            youtube = driver.find_element_by_xpath('//*[@id="video-title"]/yt-formatted-string')
            youtube.click()
            time.sleep(8)
            youtube = driver.find_element_by_xpath('//*[@id="skip-button:x"]/span/button')
            youtube.click()



            # res1=requests.get(url)
            # res1()







    cTime=time.time()
    fps= 1/(cTime-pTime)
    pTime=cTime

    cv2.putText(Bild,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("IMG",Bild)
    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()






# time.sleep(3)
# youtube= driver.find_element_by_xpath('//*[@id="search"]')
# youtube.send_keys('Balti Ya hasra')
# youtube= driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
# youtube.click()
# time.sleep(3)
# youtube= driver.find_element_by_xpath('//*[@id="video-title"]/yt-formatted-string')
# youtube.click()
# time.sleep(8)
# youtube=driver.find_element_by_xpath('//*[@id="skip-button:x"]/span/button')
# youtube.click()
