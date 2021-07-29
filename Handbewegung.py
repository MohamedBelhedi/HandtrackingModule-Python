import mediapipe as mp
import cv2
import time
Bild=cv2.VideoCapture(1)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw= mp.solutions.drawing_utils
pT=0
cT=0


while True:
    success,img=Bild.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res=hands.process(imgRGB)
    # print(res.multi_hand_landmarks)
    if res.multi_hand_landmarks:
        for handLMS in res.multi_hand_landmarks:
            for id,lm in enumerate(handLMS.landmark):
                # print(id,lm)
                h,w,c =img.shape
                cx,cy=int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)
                if id:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
            mpDraw.draw_landmarks(img,handLMS,mpHands.HAND_CONNECTIONS)

    cT=time.time()
    fps=1/(cT-pT)
    pT=cT

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
