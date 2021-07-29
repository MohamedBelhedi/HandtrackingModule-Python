import cv2
import numpy as np
import time
import os
import HandbewegungModul as hd

brushThickness=15
löschThickness=200

folderpath="Header-Files"
mylist=os.listdir(folderpath)
print(mylist)
overlaylist=[]

for imPath in mylist:
    image=cv2.imread(f'{folderpath}/{imPath}')
    overlaylist.append(image)
print(len(overlaylist))

header=overlaylist[0]
drawColor=(255,0,255)

cap=cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)


detector=hd.handDetector(detectionCon=0.5)
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)
while True:
    success,img=cap.read()
    img=cv2.flip(img,1) #Bild drehen





    #die Header Image Bilder einfügen so ....

    #find Hand Landmakrs
    img=detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList)

        #mittelfinger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        # print(fingers)

    #check finger  are up


    #if selection mode two fingers then select dont draw
        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            print("selection mode")
            #checkinfg for the click
            if y1<125:
                if 250<x1<450:
                    header=overlaylist[0]
                    drawColor=(255,0,255)
                elif 550 < x1 < 750:
                    header = overlaylist[1]
                    drawColor = (255, 0, 0)
                elif 800 < x1 < 950:
                    header = overlaylist[2]
                    drawColor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = overlaylist[3]
                    drawColor = (0, 0, 0)
        cv2.rectangle(img, (x1, y1 - 15), (x2, y2 + 15), drawColor, cv2.FILLED)


    #if drawinf mode

        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            print("drawing mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                 cv2.line(img, (xp, yp), (x1, y1), drawColor, löschThickness)
                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, löschThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)

    img[0:125,0:1280]=header
    img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    cv2.imshow("Image",img)
    cv2.imshow("Canvas",imgCanvas)

    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

