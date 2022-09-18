import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import pyautogui as pg
import time
import cv2
import mediapipe as mp
import numpy as np
import threading

def fixed_map(option):
    return [elm for elm in style.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]

stop_flag=True
thread=None
root = tk.Tk()
root.geometry("400x300")
root.resizable(False, False)  #ウィンドウサイズ固定
root.title("HAND UI")
root.configure(bg='#ECE2DB')
root.attributes("-topmost", True)  #ウィンドウを常に一番前にする
root.option_add('*font',("Yu Gothic UI Semibold",10))

style = ttk.Style()
style.configure("Treeview.Heading", font=("Yu Gothic UI Semibold", 10))
style.configure("Treeview", font=("",11))
style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

canvas=tk.Canvas(width=400,height=300, bg='#ECE2DB')
canvas.pack()
#画像を用意
photo1=tk.PhotoImage(file='image/ok_sign1.png')
#画像を描画(中点x,中点y,画像)
canvas.create_image(50,50,image=photo1)

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
        pg.hotkey("ctrl","s")
        time.sleep(1)
        print("保存")
      if abs(yuX[4]-yuX[12])<15 and abs(yuY[4]-yuY[12])<15 and abs(yuX[4]-yuX[8])<15 and abs(yuY[4]-yuY[8])<15 and yuY[16] > yuY[13] and yuY[20] > yuY[17]:
        pg.hotkey("p")
        time.sleep(1)
        print("ペンツール")
      if yuY[8] < yuY[6] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[18] < yuY[20] and abs(yuX[4]-yuX[12])<13:
        #pg.hotkey("v")
        time.sleep(1)
        print("選択ツール")
      if yuY[8] < yuY[6] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[18] < yuY[20] and 15 < np.linalg.norm(yuX[4]-yuX[10]) > 25:
        #pg.hotkey("v")
        time.sleep(1)
        print("ダイレクト選択ツール")
      if yuX[8] > yuX[6] and yuX[12] > yuY[10] and 10 < np.linalg.norm(yuX[4]-yuX[10]) > 20 and yuX[8] > yuX[16] and yuX[12] > yuX[16]:
        #pg.hotkey("t")
        time.sleep(1)
        print("文字ツール")
      #if yuX[8] < yuX[6] and yuX[12] < yuX[10] and yuX[16] < yuX[14] and yuX[20] < yuX[18] and yuY[4] < yuY[0]:
        #pg.hotkey("shift","]")
      #  time.sleep(1)
      #  print("前面に移動")
      #if yuX[8] < yuX[6] and yuX[12] < yuX[10] and yuX[16] < yuX[14] and yuX[20] < yuX[18] and yuY[4] > yuY[0]:
        #pg.hotkey("shift","[")
      #  time.sleep(1)
      #  print("背面に移動")
      if  yuY[8] < yuY[6] and yuY[20] < yuY[18] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[20] < yuY[12] and yuY[20] < yuY[16] and abs(yuX[4]-yuX[12])<13:
        #pg.hotkey("ctrl","z")
        time.sleep(1)
        print("取り消し")
      if  yuY[8] < yuY[6] and yuY[20] < yuY[18] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[20] < yuY[12] and yuY[20] < yuY[16] and 10 < np.linalg.norm(yuX[4]-yuX[10]) > 25:
        #pg.hotkey("ctrl","shift","z")
        time.sleep(1)
        print("元に戻す")
      if 20 < np.linalg.norm(yuY[4]-yuY[8]) > 25 and abs(yuX[8]-yuX[12]) < 10 and abs(yuX[12]-yuX[16]) < 10 and abs(yuX[16]-yuX[20]) < 10:
        #pg.hotkey("ctrl","c")
        time.sleep(1)
        print("コピー")
      if yuY[8] < yuY[6] and yuY[12] < yuY[10] and abs(yuX[4]-yuX[14]) < 14 and yuY[16] > yuY[14] and yuY[20] > yuY[18] and 5 < np.linalg.norm(yuX[8]-yuX[12]) > 20:
        #pg.hotkey("ctrl","v")
        time.sleep(1)
        print("貼り付け")

      '''
      if abs(yuX[4]-yuX[20])<14 and abs(yuY[4]-yuY[20])<14:
        pg.hotkey("ctrl","shift","z")
        time.sleep(1)
        print("元に戻す")
      '''
      if abs(yuX[4]-yuX[12])<12 and abs(yuY[4]-yuY[12])<12 and abs(yuX[4]-yuX[16])<12 and abs(yuY[4]-yuY[16])<12:
        t_n = time.time()
        times_n += 1
        time.sleep(0.1)
        print("1回目",t_n)
        if times_n == 2:
          times_n = 0


      if 0.1 < abs(t_n - t_p) < 1 and times_n ==1:
        #pg.hotkey("t")
        #time.sleep(0.5)
        print("T")
        
      t_p = t_n

      #camera_button.config(state = "normal")

def camera_on():
  global stop_flag
  global thread
  if not thread:
    #camera_button.config(state = "disabled")
    thread_camera = threading.Thread(target=camera)
    stop_flag=True
    thread_camera.start()
  print("On")

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

camera_button2 = tk.Button(root, text="停 止", command=camera_off, bg="#F70B48", fg="#ffffff", width=6, font=("Yu Gothic UI Semibold",12))
camera_button2.place(x = 300, y = 37.5)

column = ('a', 'b', 'c')
tree = ttk.Treeview(root, columns=column)
tree.column('#0', width=0, stretch='no')
tree.column('a', anchor='w', width=100)
tree.column('b', anchor='center', width=100)
tree.column('c',  anchor='w', width=100)
tree.heading('#0', text='')
tree.heading('a', text='機能', anchor='w')
tree.heading('b', text='ジェスチャー', anchor='w')
tree.heading('c', text='コマンド', anchor='w')
tree.insert(parent='', index='end', values=('a', '👌', 'ctrl + z'))
tree.place(x=20, y=100)
  

'''
text = tk.Message(root, text="ここに選択されたアプリのショートカットジェスチャーが表示される", width=300)
text.place(x = 50, y = 180)
test_box = tk.Entry(width = 40)
test_box.place(x =45, y = 100)
'''

def delete_window():
  cap.release()
  root.destroy()
root.protocol("WM_DELETE_WINDOW", delete_window)

root.mainloop()