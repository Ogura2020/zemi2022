from os import times
from tabnanny import check
import tkinter as tk
import tkinter.ttk as ttk
import random as R
import pyautogui as pg
import time
import datetime
import cv2
import mediapipe as mp
import numpy as np
import threading

stop_flag=True
thread=None
root = tk.Tk()
root.geometry("400x300")
root.title("HAND UI")
root.configure(bg='#ECE2DB')
root.attributes("-topmost", True)
root.option_add('*font',("Yu Gothic UI Semibold",10))

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#t_p=100.0
#t_n=0.0
times_p=times_n=0.0
a=0

thresh_h = 3.5            #threshold for tangent. 3.0 corresponds to 30 < theta <60. 30度～60度の間
thresh_l = 1.0/thresh_h   #thresh_lは↑ができたら勝手に計算するので気にしなくてよし
thresh_n = 4              #threshold for the number of points in the same direction　四回45度になったら
thresh_t = 2           #2.5秒の間に指がクロスしたら

X=Y=y=0
x=-100

def angle_p(x,y,X,Y):
    if ((X-x)**2*thresh_l < (Y-y)**2 < (X-x)**2*thresh_h 
    and abs(X-x) > 10 and np.sign((X-x)*(Y-y))==-1):
        return True
    else:
        return False
    
def angle_n(x,y,X,Y):
    if ((X-x)**2*thresh_l < (Y-y)**2 < (X-x)**2*thresh_h
    and abs(X-x) > 10 and np.sign((X-x)*(Y-y))==1):
        return True
    else:
        return False

cap = cv2.VideoCapture(0)
def camera():
 global stop_flag
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
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
      X=(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
      * image_width)
      Y=(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
      * image_height)

      oX1 =hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width
      oY1 =hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height

      hiX1=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width
      hiY1=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
      hiX2=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x * image_width
      hiY2=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height
      hiX3=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * image_width
      hiY3=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height
      hiX4=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * image_width
      hiY4=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height

      naX1=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * image_width
      naY1=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
      naX3=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * image_width
      naY3=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height
      naX4=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * image_width
      naY4=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height

      kuX1=hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * image_width
      kuY1=hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height
      kuX3=hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x * image_width
      kuY3=hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height

      koX1=hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * image_width
      koY1=hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height

      if abs(oX1-hiX1)<14 and abs(oY1-hiY1)<14:
        pg.hotkey("ctrl","z")
        time.sleep(0.5)
        print("戻る")
        
      if abs(oX1-koX1)<14 and abs(oY1-koY1)<14:
        pg.hotkey("ctrl","shift","z")
        time.sleep(0.5)
        print("元に戻す")

      if abs(oX1-naX1)<8 and abs(oY1-naY1)<8:
        t_n = time.time()
        times_n += 1
        time.sleep(0.5)
        print("1回目",t_n)
        if times_n == 3:
          times_n = 0


      if 0.1 < abs(t_n - t_p) < 3 and times_n ==2:
        #pg.hotkey("t")
        #time.sleep(0.5)
        print("T")
        
      t_p = t_n

def camera_on():
  app = combobox.get()
  if app == "illustrator":
   text['text'] = '👌戻る(ctrl+z)\n元に戻る'
   #text['font'] = ('System', 16)
  elif app == "GoogleChrome":
    text['text'] = 'ああああ\nいいいいい'
  elif app == "Figma":
    text['text'] = 'uuuuu\neeee'

  global stop_flag
  global thread
  if not thread:
    thread_camera = threading.Thread(target=camera)
    stop_flag=True
    thread_camera.start()

def camera_off():
  global stop_flag
  global thread
  if thread:
    stop_flag=False
    thread_camera.join()
    thread_camera=None
  print("OFF")
  cap.release()

#test_text = tk.Label(None, text="hello World")
#test_text.pack()

camera_button = tk.Button(root, text="決 定", command=camera_on, bg="#F70B48", fg='#ffffff', width=6, font=("Yu Gothic UI Semibold",12))
camera_button.place(x = 200, y = 37.5)

camera_button2 = tk.Button(root, text="終 了", command=camera_off, bg="#F70B48", fg="#ffffff", width=6, font=("Yu Gothic UI Semibold",12))
camera_button2.place(x = 300, y = 37.5)

list = ["illustrator","GoogleChrome","Figma"]
variable = tk.StringVar()
combobox = ttk.Combobox(root, values=list, textvariable=variable, state="readonly", width=15)
combobox.place(x = 20, y = 50)

text = tk.Message(root, text="ここに選択されたアプリのショートカットジェスチャーが表示される", width=300)
text.place(x = 50, y = 180)

'''
test_box = tk.Entry(width = 40)
test_box.place(x =45, y = 100)
'''

def delete_window():
  cap.release()
  root.destroy()
root.protocol("WM_DELETE_WINDOW", delete_window)

root.mainloop()