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
for i in range(0, len(dirs)):
	file = Button(fenetre, text=dirs[i])
	delete = Button(fenetre, text="X", command=lambda : os.remove(dirs[i]))

	file.grid(row=1, column=i)
	delete.grid(row=2, column=i)

fenetre.mainloop()
