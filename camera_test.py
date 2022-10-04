from re import I
import tkinter as tk
from PIL import Image,ImageTk
import tkinter.ttk as ttk
import pyautogui as pg
import time
import cv2
import mediapipe as mp
import numpy as np      #いらないかも！確認する！
import threading

i=0
root = tk.Tk()
root.geometry("400x300")
root.resizable(False, False)  #ウィンドウサイズ固定
root.title("HAND UI")
root.configure(bg='#ECE2DB')
root.attributes("-topmost", True)  #ウィンドウを常に一番前にする
root.option_add('*font',("Yu Gothic UI Semibold",10))

canvas=tk.Canvas(root, bg='#1b1b1b')
canvas.pack()

event = threading.Event()

mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
def camera():
 with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    image_height, image_width, c = image.shape
    
    if not success:
      print("Ignoring empty camera frame.")
      break
    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    #image.flags.writeable = False
    results = hands.process(image)

    #image.flags.writeable = True
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    yuX = []
    yuY = []
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
       for i in range(21):
         yuX.append(hand_landmarks.landmark[i].x * image_width)
         yuY.append(hand_landmarks.landmark[i].y * image_height)
         #print(hand_landmarks.landmark[4])
      X=(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)
      Y=(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)
      
      if abs(yuX[4]-yuX[8])<14 and abs(yuY[4]-yuY[8])<14 and yuY[12] < yuY[8]:
        #pg.hotkey("ctrl","s")
        time.sleep(1)
        print("保存")
        text['text'] = '保存しました！'

img =[ImageTk.PhotoImage(file="image/button1.png"),ImageTk.PhotoImage(file="image/button2.png")]
def camera_btn():
  global i
  i= (i+1) % len(img)
  btn1 = tk.Button(root, image=img[i], bg="#ECE2DB", width=65, height=65, bd=0, relief="sunken", activebackground="#ECE2DB", command=camera_btn)
  canvas.create_window(255,150,window=btn1)  #255,60
  print("押された！",i)
  if i==1:
   thread_camera = threading.Thread(target=camera)
   thread_camera.start()
   print("On")
  elif i==0:
    print("OFF")
    cap.release()
btn1 = tk.Button(root, image=img[i], bg="#ECE2DB", width=65,height=65, bd=0, relief="sunken", activebackground="#ECE2DB", command=camera_btn)
canvas.create_window(255,150,window=btn1)  #255,60
print(i)
'''
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
def camera():
 #app = combobox.get()
 global stop_flag
 stop_flag = True
 t_p=100.0
 t_n=0.0
 times_n = 0
 with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    image_height, image_width, c = image.shape
    
    if not success:
      print("Ignoring empty camera frame.")
      break
    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    #image.flags.writeable = False
    results = hands.process(image)

    #image.flags.writeable = True
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    yuX = []
    yuY = []
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
       for i in range(21):
         yuX.append(hand_landmarks.landmark[i].x * image_width)
         yuY.append(hand_landmarks.landmark[i].y * image_height)
         #print(hand_landmarks.landmark[4])
      X=(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)
      Y=(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)

      if abs(yuX[4]-yuX[8])<14 and abs(yuY[4]-yuY[8])<14 and yuY[12] < yuY[8]:
        #pg.hotkey("ctrl","s")
        time.sleep(1)
        print("保存")
        text['text'] = '保存しました！'

'''

text = tk.Message(root, text="○○を使用しました", width=200)
text.place(x = 30, y = 135) #30,45

def delete_window():
  cap.release()
  root.destroy()
root.protocol("WM_DELETE_WINDOW", delete_window)

root.mainloop()