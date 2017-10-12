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

def deleteWidget():
	widgets = fenetre.winfo_children()
	for j in range(0, len(widgets)):
		widgets[j].destroy() 	
	time.sleep(1)
	#refresh()

def removeFile(file):
	os.remove(file)
	deleteWidget()

def refresh():
	for i in range(0, len(dirs)):
		file = Button(fenetre, text=dirs[i], command=lambda : print("ok")).grid(row=1, column=i)
		Button(fenetre, text="X", command=lambda i=i : removeFile(dirs[i]), fg="red").grid(row=2, column=i)
 
refresh()
fenetre.mainloop()
 