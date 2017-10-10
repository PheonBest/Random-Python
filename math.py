import random  
import time
import threading
import os
from tkinter import * 

fenetre = Tk()
dirs = os.listdir()
fenetre.title(str(os.getcwd()))
for i in range(0 ,len(dirs)):
	file = Button(fenetre, text=dirs[i]) 
	exit = Button(fenetre, text="X")

	file.grid(row=1, column=i)
	exit.grid(row=2, column=i)
fenetre.mainloop()