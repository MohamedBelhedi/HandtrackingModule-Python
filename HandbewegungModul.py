import mediapipe as mp
import cv2
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon



        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res = self.hands.process(imgRGB)
            # print(res.m ulti_hand_landmarks)
        if self.res.multi_hand_landmarks:
                for handLMS in self.res.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLMS,
                                                   self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self,img,handNo=0,draw=True):

            self.lmList=[]
            if self.res.multi_hand_landmarks:
                myHand=self.res.multi_hand_landmarks[handNo]



                for id, lm in enumerate(myHand.landmark):
                    # print(id,lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # print(id, cx, cy)
                    self.lmList.append([id,cx,cy])
                    if draw:

                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            return self.lmList

    def fingersUp(self):
        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

def main():
    pT = 0
    cT = 0
    Bild = cv2.VideoCapture(1)
    detector=handDetector()
    while True:
        success, img = Bild.read()
        img=detector.findHands(img,draw=False)
        lmList=detector.findPosition(img,draw=False)

        if len(lmList) !=0:
            print(lmList[4])
        cT = time.time()
        fps = 1 / (cT - pT)
        pT = cT
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", Bild)
        cv2.waitKey(1)


if __name__ == "main":
    main()
