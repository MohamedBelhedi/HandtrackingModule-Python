import cv2
import time
import numpy as np
import HandbewegungModul as hd
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import requests
# url='https://www.google.de'
wCam,hCam=640,480

cap=cv2.VideoCapture(1)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
cTime=0


detector=hd.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minVol=volRange[0]
maxVol=volRange[1]
volLeiste=200
vol=0
volper=0


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

        vol=np.interp(länge,[50,150],[minVol,maxVol])
        volLeiste = np.interp(länge, [50, 150], [400, 150])
        volper = np.interp(länge, [50, 150], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)

        if länge>=145:
            cv2.circle(Bild, (cx, cy), 15, (0, 233, 255), cv2.FILLED)
            time.sleep(1)
            # res1=requests.get(url)
            # res1()



    cv2.rectangle(Bild,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(Bild, (50, int(volLeiste)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(Bild, f'{int(volper)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (265, 170, 0), 3)




    cTime=time.time()
    fps= 1/(cTime-pTime)
    pTime=cTime

    cv2.putText(Bild,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("IMG",Bild)
    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()