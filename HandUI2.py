import tkinter as tk
from PIL import ImageTk
import pyautogui as pg
import time
import cv2
import mediapipe as mp
import threading
import numpy as np
 
image_index=0
root = tk.Tk()
root.geometry("400x900")
root.minsize(400, 140)
root.maxsize(400, 900)
#root.resizable(False, False)  #ウィンドウサイズ固定
root.title("HAND UI")
root.configure(bg='#ECE2DB')
root.iconphoto(False, ImageTk.PhotoImage(file="icon2.png"))
root.attributes("-topmost", True)  #ウィンドウを常に一番前にする
root.option_add('*font',("Yu Gothic UI Semibold",12))

canvas=tk.Canvas(root, bg='#ECE2DB', width=400,height=1000)
canvas.pack()
photo1=tk.PhotoImage(file='gesture.png')
canvas.create_image(195,500,image=photo1)

mp_hands = mp.solutions.hands

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
    results = hands.process(image)
    
    yuX = []
    yuY = []
    if results.multi_hand_landmarks and image_index==1:
      for hand_landmarks in results.multi_hand_landmarks:
       for i in range(21):
         yuX.append(hand_landmarks.landmark[i].x * image_width)
         yuY.append(hand_landmarks.landmark[i].y * image_height)
         #print(hand_landmarks.landmark[4])
      
      if abs(yuX[4]-yuX[8])<14 and abs(yuY[4]-yuY[8])<14 and yuY[12] < yuY[8] and yuY[16] < yuY[8] and yuY[20] < yuY[8]:
        pg.hotkey("ctrl","s")
        print("保存")
        text['text'] = '保存しました！'
        time.sleep(1)
      if abs(yuX[4]-yuX[12])<40 and abs(yuY[4]-yuY[12])<15 and abs(yuX[4]-yuX[8])<40 and abs(yuY[4]-yuY[8])<15 and yuY[16] > yuY[14] and yuY[20] > yuY[18]:
        pg.hotkey("p")
        print("ペンツール")
        text['text'] = 'ペンツール'
        time.sleep(1)
      if yuY[8] < yuY[6] and yuY[4] < yuY[12] and yuY[4] < yuY[16] and yuY[4] < yuY[20] and abs(yuX[4]-yuX[12])<15:
        pg.hotkey("v")
        print("選択ツール")
        text['text'] = '選択ツール'
        time.sleep(1)
      if yuY[8] < yuY[6] and yuY[4] < yuY[12] and yuY[4] < yuY[16] and yuY[4] < yuY[20] and 18 < np.linalg.norm(yuX[4]-yuX[8]) > 25 and abs(yuY[12]-yuY[16]) < 15 and abs(yuY[16]-yuY[20]) < 15:
        pg.hotkey("a")
        print("ダイレクト選択ツール")
        text['text'] = 'ダイレクト選択ツール'
        time.sleep(1)
      if yuX[8] > yuX[6] and yuX[12] > yuX[10] and yuX[8] > yuX[16] and yuX[8] > yuX[20] and yuX[12] > yuX[16] and yuX[12] > yuX[20] and yuY[3] < yuY[5]:
        pg.hotkey("t")
        print("文字ツール")
        text['text'] = '文字ツール'
        time.sleep(1)
      if  yuY[8] < yuY[6] and yuY[20] < yuY[18] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[20] < yuY[12] and yuY[20] < yuY[16] and abs(yuX[4]-yuX[12])<13:
        pg.hotkey("ctrl","z")
        print("取り消し")
        text['text'] = '取り消しました！'
        time.sleep(1)
      if  yuY[8] < yuY[6] and yuY[20] < yuY[18] and yuY[8] < yuY[12] and yuY[8] < yuY[16] and yuY[20] < yuY[12] and yuY[20] < yuY[16] and 10 < np.linalg.norm(yuX[4]-yuX[10]) > 25:
        pg.hotkey("ctrl","shift","z")
        print("元に戻す")
        text['text'] = 'もとに戻しました！'
        time.sleep(1)
      if 30 < np.linalg.norm(yuY[4]-yuY[8]) < 55 and abs(yuX[8]-yuX[12]) < 10 and abs(yuX[12]-yuX[16]) < 10 and abs(yuX[16]-yuX[20]) < 10 and yuY[8] < yuY[4]:
        pg.hotkey("ctrl","c")
        print("コピー")
        text['text'] = 'コピーしました！'
        time.sleep(1)
      if yuY[8] < yuY[6] and yuY[12] < yuY[10] and abs(yuX[4]-yuX[14]) < 14 and yuY[16] > yuY[14] and yuY[20] > yuY[18] and 5 < np.linalg.norm(yuX[8]-yuX[12]) > 20:
        pg.hotkey("ctrl","v")
        print("貼り付け")
        text['text'] = '貼り付けました！'
        time.sleep(1)
      if yuY[4] > yuY[16] and abs(yuY[4]-yuY[13])<16 and abs(yuX[4]-yuX[13])<16 and yuY[4] > yuY[8] and yuY[4] > yuY[12] and yuY[4] > yuY[16] and yuY[4] > yuY[20]:
        pg.keyDown("alt")
        print("拡大・縮小")
        text['text'] = '拡大・縮小'
        time.sleep(1)
      else :
        pg.keyUp("alt")
        #print("解除")


#カメラ切り替えボタン
img =[ImageTk.PhotoImage(file="button1.png"),ImageTk.PhotoImage(file="button2.png")]
def camera_btn():
  global image_index
  image_index= (image_index+1) % len(img)
  btn1 = tk.Button(root, image=img[image_index], bg="#ECE2DB", width=90, height=90, bd=0, relief="sunken", activebackground="#ECE2DB", command=camera_btn)
  canvas.create_window(300,70,window=btn1)
  print("押された！",image_index)
  if image_index==1:
   thread_camera = threading.Thread(target=camera)
   thread_camera.start()
   print("On")
  elif image_index==0:
    print("OFF")
btn1 = tk.Button(root, image=img[image_index], bg="#ECE2DB", width=90,height=90, bd=0, relief="sunken", activebackground="#ECE2DB", command=camera_btn)
canvas.create_window(300,70,window=btn1)  
print(image_index)

text = tk.Message(root, text="○○を使用しました", width=200,bg="#ffffff")
text.place(x = 40, y = 55) #30,45

def delete_window():
  cap.release()
  root.destroy()
root.protocol("WM_DELETE_WINDOW", delete_window)

root.mainloop()