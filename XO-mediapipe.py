import cv2
import tkinter as tk
import threading
import mediapipe as mp
import math
import numpy as np
from mediapipe.framework.formats import landmark_pb2
from math import sqrt
import win32api
import pyautogui
from tkinter import messagebox
from tkinter import *

class handDetector():
    def __init__(self,mode=False,maxHands=1, modelComplexity=1,detectionConf=0.5,trackConf=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.modelComplex = modelComplexity
        self.detectionConf = detectionConf
        self.trackConf=trackConf
        self.mpHands = mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands, self.modelComplex,self.detectionConf,self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                     self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=True):
        xList=[]
        yList=[]
        bbox=[]
        self.lmlist=[]
        if self.results.multi_hand_landmarks:  
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                xList.append(cx)
                yList.append(cy)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),2,(255,0,0),cv2.FILLED)    
            xmin,xmax=min(xList),max(xList)
            ymin,ymax=min(yList),max(yList)
            bbox=xmin,ymin,xmax,ymax


        return self.lmlist,bbox

    def fingersUp(self):
        fingers = []
        if self.lmlist[self.tipIds[0]][1] > self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    def findDistance(self, p1, p2, img, draw=True,r=15,t=3):
        x1, y1 = self.lmlist[p1][1],self.lmlist[p1][2]
        x2, y2 = self.lmlist[p2][1],self.lmlist[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw: 
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]
    
    
window = tk.Tk()
window.geometry("600x500")
lbl = Label(window, text="Play XO", font=('Helvetica', '15'))
lbl.grid(row=0, column=0)
window.title("XO game")
turn = 1 

user1 = StringVar()
user2 = StringVar()

u1_name = Entry(window, textvariable=user1, bd=2)
u2_name = Entry(window, textvariable=user2, bd=2)

label = Label( window, text="Player 1:", font='Times 12 bold', bg='white', fg='black', height=2, width=6)
label.grid(row=1, column=0)
u1_name.grid(row=1,column=0)

label = Label( window, text="Player 2:", font='Times 12 bold', bg='white', fg='black', height=2, width=6)
label.grid(row=2, column=0)
u2_name.grid(row=2,column=0)


def clickedproccessing():
    global turn
    if turn == 1:
        turn = 2
        return "X"
    elif turn == 2:
        turn = 1
        return "O"

def clicked1():
    global turn
    if btn1["text"] == " ":  # For getting the text of a button
        btn1["text"] = clickedproccessing()
        check()


def clicked2():
    global turn
    if btn2["text"] == " ":
        btn2["text"] = clickedproccessing()
        check()


def clicked3():
    global turn
    if btn3["text"] == " ":
        btn3["text"] = clickedproccessing()
        check()


def clicked4():
    global turn
    if btn4["text"] == " ":
        btn4["text"] = clickedproccessing()
        check()


def clicked5():
    global turn
    if btn5["text"] == " ":
        btn5["text"] = clickedproccessing()
        check()


def clicked6():
    global turn
    if btn6["text"] == " ":
        btn6["text"] = clickedproccessing()
        check()


def clicked7():
    global turn
    if btn7["text"] == " ":
        btn7["text"] = clickedproccessing()
        check()


def clicked8():
    global turn
    if btn8["text"] == " ":
        btn8["text"] = clickedproccessing()
        check()


def clicked9():
    global turn
    if btn9["text"] == " ":
        btn9["text"] = clickedproccessing()
        check()


def check():
    global flag
    b1 = btn1["text"] 
    b2 = btn2["text"] 
    b3 = btn3["text"]
    b4 = btn4["text"]
    b5 = btn5["text"]
    b6 = btn6["text"]
    b7 = btn7["text"]
    b8 = btn8["text"]
    b9 = btn9["text"]
    flag += 1
    if b1 == b2 and b1 == b3 and b1 == "O" or b1 == b2 and b1 == b3 and b1 == "X":
        win(b1)
    if b4 == b5 and b4 == b6 and b4 == "O" or b4 == b5 and b4 == b6 and b4 == "X":
        win(b4)
    if b7 == b8 and b7 == b9 and b7 == "O" or b7 == b8 and b7 == b9 and b7 == "X":
        win(b7)
    if b1 == b4 and b1 == b7 and b1 == "O" or b1 == b4 and b1 == b7 and b1 == "X":
        win(b1)
    if b2 == b5 and b2 == b8 and b2 == "O" or b2 == b5 and b2 == b8 and b2 == "X":
        win(b2)
    if b3 == b6 and b3 == b9 and b3 == "O" or b3 == b6 and b3 == b9 and b3 == "X":
        win(b3)
    if b1 == b5 and b1 == b9 and b1 == "O" or b1 == b5 and b1 == b9 and b1 == "X":
        win(b1)
    if b7 == b5 and b7 == b3 and b7 == "O" or b7 == b5 and b7 == b3 and b7 == "X":
        win(b7)
    elif flag == 9:
        messagebox.showinfo("DRAW !", "DRAW")
        window.destroy()
        clear()
        
def clear():
    btn1["text"] = " "
    btn2["text"] = " "
    btn3["text"] = " "
    btn4["text"] = " "
    btn5["text"] = " "
    btn6["text"] = " "
    btn7["text"] = " "
    btn8["text"] = " "
    btn9["text"] = " "


def win(player):
    ans = "Woah-hoo !" + player + " wins !!!"
    messagebox.showinfo("WIN !!!", ans)
    messagebox.askquestion("askquestion", "Wanna Play again?")
    clear()


btn1 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'),cursor="circle", command=clicked1)
btn1.grid(column=1, row=1)
btn2 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'), cursor="circle",command=clicked2)
btn2.grid(column=2, row=1)
btn3 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'),cursor="circle", command=clicked3)
btn3.grid(column=3, row=1)
btn4 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'),cursor="circle", command=clicked4)
btn4.grid(column=1, row=2)
btn5 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'),cursor="circle", command=clicked5)
btn5.grid(column=2, row=2)
btn6 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'), cursor="circle",command=clicked6)
btn6.grid(column=3, row=2)
btn7 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'),cursor="circle", command=clicked7)
btn7.grid(column=1, row=3)
btn8 = Button(window, text=" ",bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'),cursor="circle", command=clicked8)
btn8.grid(column=2, row=3)
btn9 = Button(window, text=" ", bg="#6698FF", fg="Black", width=5, height=2, font=('Helvetica', '25'), cursor="circle",command=clicked9)
btn9.grid(column=3, row=3)
flag = 0 



def video_stream():
    wCam, hCam = 640, 480
    #width=1920, height=1080
    #wCam, hCam = 510, 340
    frameR = 100
    smoothening = 7
    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0
    drawing_canvas = np.zeros((wCam, hCam,3),np.uint8)

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = handDetector(detectionConf=0.60,maxHands=1)
    wScr, hScr = pyautogui.size()
    print(pyautogui.size())
    
    a = 0
    while True:
        a+= 1
        check, img = cap.read()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(0, 255, 255), 4)
#         cv2.line(img, (320,10), (320,600), (0, 255, 0), 4)

        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            x1,y1 = lmList[8][1:]
            x2,y2 = lmList[12][1:]
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(0, 255, 255), 4)
            cv2.putText(img,"Solo",(frameR, frameR),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3,cv2.LINE_AA)
  
        
            if fingers[1] == 1 and fingers[2] == 0:
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
                plocX, plocY = clocX, clocY
                cv2.circle(img,(x1,y1),8,(0, 255, 0),-1)
               

            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:   
                length, img, lineInfo = detector.findDistance(8, 20, img)
                pyautogui.click()

        cv2.imshow('Play XO', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows

th= threading.Thread(target=video_stream)
th.setDaemon(True)
th.start()
window.mainloop()