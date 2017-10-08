import pyscreenshot as ImageGrab
from pynput.mouse import Button, Controller

mouse = Controller()

def redClick():
    im=ImageGrab.grab(bbox=(100,100,600,600)) # X1,Y1,X2,Y2
    #im.show()
    for i in range(0, 500):
        for j in range(0, 500):
            r,g,b = im.getpixel((i,j))
            print(r,g,b)
            if (r == 255 and g == 0 and b == 0):
                mouse.position = (100+i, 100+j)
                mouse.press(Button.left)
                mouse.release(Button.left)
                redClick()
                return;
    return;
if __name__ == "__main__":
    redClick()

