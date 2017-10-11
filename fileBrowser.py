import random
import time
import threading
import os
from tkinter import *
def a():
	print("a")
fenetre = Tk()
dirs = os.listdir()
print(dirs)
fenetre.title(str(os.getcwd()))
def printThis(strc):
	print(strc)

def readFile(file):
	f = open(file, "w")
	return str(f)
for i in range(0, len(dirs)):
	file = Button(fenetre, text=dirs[i])
	Button(fenetre, text="X", command=lambda i=i : print(readFile(dirs[i]))).grid(row=2, column=i)
	file.grid(row=1, column=i)

fenetre.mainloop()
