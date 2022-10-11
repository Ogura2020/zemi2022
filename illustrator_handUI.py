import tkinter as tk
from PIL import Image,ImageTk
import tkinter.ttk as ttk
import pyautogui as pg
import time
import cv2
import mediapipe as mp
import threading
import numpy as np   #いらないかも！確認する！
 
image_index=0
root = tk.Tk()
root.geometry("400x300")
root.resizable(False, False)  #ウィンドウサイズ固定
root.title("HAND UI")
root.configure(bg='#ECE2DB')
root.attributes("-topmost", True)  #ウィンドウを常に一番前にする
root.option_add('*font',("Yu Gothic UI Semibold",10))

canvas=tk.Canvas(root, bg='#1b1b1b')
canvas.pack()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

times_p=times_n=0.0
a=0

thresh_h = 3.5            #threshold for tangent. 3.0 corresponds to 30 < theta <60. 30度～60度の間
thresh_l = 1.0/thresh_h   #thresh_lは↑ができたら勝手に計算するので気にしなくてよし
thresh_n = 4              #threshold for the number of points in the same direction　四回45度になったら
thresh_t = 2           #2.5秒の間に指がクロスしたら

cap = cv2.VideoCapture(0)
def camera():
 global image_index
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
    if results.multi_hand_landmarks and image_index==1:
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
      if abs(yuX[4]-yuX[12])<15 and abs(yuY[4]-yuY[12])<15 and abs(yuX[4]-yuX[8])<15 and abs(yuY[4]-yuY[8])<15 and yuY[16] > yuY[13] and yuY[20] > yuY[17]:
        pg.hotkey("p")
        time.sleep(1)
        print("ペンツール")
        text['text'] = 'ペンツール'
      if yuY[8] < yuY[6] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[18] < yuY[20] and abs(yuX[4]-yuX[12])<13:
        pg.hotkey("v")
        time.sleep(1)
        print("選択ツール")
        text['text'] = '選択ツール'
      if yuY[8] < yuY[6] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[18] < yuY[20] and 15 < np.linalg.norm(yuX[4]-yuX[10]) > 25:
        pg.hotkey("v")
        time.sleep(1)
        print("ダイレクト選択ツール")
        text['text'] = 'ダイレクト選択ツール'
      if yuX[8] > yuX[6] and yuX[12] > yuY[10] and 10 < np.linalg.norm(yuX[4]-yuX[10]) > 20 and yuX[8] > yuX[16] and yuX[12] > yuX[16]:
        pg.hotkey("t")
        time.sleep(1)
        print("文字ツール")
        text['text'] = '文字ツール'
      #if yuX[8] < yuX[6] and yuX[12] < yuX[10] and yuX[16] < yuX[14] and yuX[20] < yuX[18] and yuY[4] < yuY[0]:
        #pg.hotkey("shift","]")
      #  time.sleep(1)
      #  print("前面に移動")
      #if yuX[8] < yuX[6] and yuX[12] < yuX[10] and yuX[16] < yuX[14] and yuX[20] < yuX[18] and yuY[4] > yuY[0]:
        #pg.hotkey("shift","[")
      #  time.sleep(1)
      #  print("背面に移動")
      if  yuY[8] < yuY[6] and yuY[20] < yuY[18] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[20] < yuY[12] and yuY[20] < yuY[16] and abs(yuX[4]-yuX[12])<13:
        pg.hotkey("ctrl","z")
        time.sleep(1)
        print("取り消し")
        text['text'] = '取り消しました！'
      if  yuY[8] < yuY[6] and yuY[20] < yuY[18] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[20] < yuY[12] and yuY[20] < yuY[16] and 10 < np.linalg.norm(yuX[4]-yuX[10]) > 25:
        pg.hotkey("ctrl","shift","z")
        time.sleep(1)
        print("元に戻す")
        text['text'] = 'もとに戻しました！'
      if 20 < np.linalg.norm(yuY[4]-yuY[8]) > 25 and abs(yuX[8]-yuX[12]) < 10 and abs(yuX[12]-yuX[16]) < 10 and abs(yuX[16]-yuX[20]) < 10:
        pg.hotkey("ctrl","c")
        time.sleep(1)
        print("コピー")
        text['text'] = 'コピーしました！'
      if yuY[8] < yuY[6] and yuY[12] < yuY[10] and abs(yuX[4]-yuX[14]) < 14 and yuY[16] > yuY[14] and yuY[20] > yuY[18] and 5 < np.linalg.norm(yuX[8]-yuX[12]) > 20:
        pg.hotkey("ctrl","v")
        time.sleep(1)
        print("貼り付け")
        text['text'] = '貼り付けました！'

      '''
      if abs(yuX[4]-yuX[20])<14 and abs(yuY[4]-yuY[20])<14:
        pg.hotkey("ctrl","shift","z")
        time.sleep(1)
        print("元に戻す")
      '''

      #camera_button.config(state = "normal")

img =[ImageTk.PhotoImage(file="image/button1.png"),ImageTk.PhotoImage(file="image/button2.png")]
def camera_btn():
  global image_index
  image_index= (image_index+1) % len(img)
  btn1 = tk.Button(root, image=img[image_index], bg="#ECE2DB", width=65, height=65, bd=0, relief="sunken", activebackground="#ECE2DB", command=camera_btn)
  canvas.create_window(255,150,window=btn1)  #255,60
  print("押された！",image_index)
  if image_index==1:
   thread_camera = threading.Thread(target=camera)
   thread_camera.start()
   print("On")
  elif image_index==0:
    print("OFF")
    #cap.release()
btn1 = tk.Button(root, image=img[image_index], bg="#ECE2DB", width=65,height=65, bd=0, relief="sunken", activebackground="#ECE2DB", command=camera_btn)
canvas.create_window(255,150,window=btn1)  #255,60
print(image_index)

text = tk.Message(root, text="○○を使用しました", width=200)
text.place(x = 30, y = 135) #30,45

def delete_window():
  cap.release()
  root.destroy()
root.protocol("WM_DELETE_WINDOW", delete_window)

root.mainloop()