import os
import psutil
import keyboard
import threading
import datetime
import time
from  sys import exit
from pynput.keyboard import Key, Listener
from PIL import ImageGrab;
import cv2
import numpy as np
from pyautogui import press, typewrite, hotkey



def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

c = 1
def spam():
	global c
	for i in range(0, 100):
		typewrite(str(c)+"x"+str(i)+"="+str(i*c))
		keyboard.press('space')
		keyboard.press('enter')
	c += 1; 

''' while (c < 100):
	spam()
 '''
setInterval(spam, 0.1)
 
 