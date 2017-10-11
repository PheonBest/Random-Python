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

def removeFile(file):
	os.remove(file)
	refresh();

def refresh():
	for i in range(0, len(dirs)):
		file = Button(fenetre, text=dirs[i])
		Button(fenetre, text="X", command=lambda i=i : removeFile(dirs[i]), fg="red").grid(row=2, column=i)
		file.grid(row=1, column=i)
refresh()
fenetre.mainloop()
