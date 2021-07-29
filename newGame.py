
import cv2
import time
import HandbewegungModul as had


pT = 0
cT = 0
Bild = cv2.VideoCapture(1)
detector=had.handDetector()
while True:
    success, img = Bild.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img)

    if len(lmList) !=0:
         print(lmList[4])
    cT = time.time()
    fps = 1 / (cT - pT)
    pT = cT
    cv2.putText(img, str(int(fps)), (5, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)