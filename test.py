import math
import PIL.Image, PIL.ImageTk
try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import config as cfg
import Board as bd
import callbacks as clb
from pymouse import PyMouse
m = PyMouse()
from pykeyboard import PyKeyboard
k = PyKeyboard()

x0, y0 = None, None

def tests():
    global x0, y0
    sizes, xoff, yoff = cfg.win.geometry().split("+")
    w, h = sizes.split("x")
    xoff, yoff = float(xoff), float(yoff)
    w, h = float(w), float(h)
    x0 = xoff #934
    y0 = yoff


    #print("xoff=",str(xoff),"should be 2212")
    #m.move(x0, y0 + cfg.YTOP)
    #k.press_keys([k.alt_l_key, k.tab_key])

    m.move(x0, y0)
    cfg.canvas.after(1000, cfg.win.update())
    m.move(x0 + cfg.CANVAS_WIDTH, y0 + cfg.YBOTTOMMAINCANVAS)
    return
    m.move(x0 + cfg.CANVAS_WIDTH + 1, y0 + 50)

    cfg.canvas.after(500, cfg.win.update())
    #move and confirm tile from player 1
    drag((0, 0, -1), (3, 3, 0))
    k.tap_key(k.return_key)

    cfg.canvas.after(100, cfg.win.update())
    #move, rotate and confirm tile from player 2
    drag((0, 0, -2), (4, 3, 0))
    cfg.canvas.after(100, cfg.win.update())

    x, y = click((4, 3, 0))
    k.tap_key(k.return_key)

    #some time is needed!
    cfg.canvas.after(500, cfg.win.update())

    drag((0, 0, -1), (4, 2, 0))
    #cfg.canvas.after(1000, cfg.win.update())
    k.tap_key(k.return_key)
    #cfg.canvas.after(1000, cfg.win.update())
    #find all matches
    x, y = click((0, 0, 0))
    #cfg.canvas.after(100, cfg.win.update())
    #x,y = m.position()
    #m.move(x0, y0)

def drag(rowcoltab1, rowcoltab2):
    print("Test moves {} to {}".format(rowcoltab1, rowcoltab2))
    x1, y1 = cfg.board.off_to_pixel(rowcoltab1)
    x2, y2 = cfg.board.off_to_pixel(rowcoltab2)
    m.move(x0 + x1, y0 + cfg.YTOPMAINCANVAS + y1)
    m.press(x0 + x1, y0 + cfg.YTOPMAINCANVAS + y1)
    cfg.canvas.after(100, cfg.win.update())
    m.move(x0 + x2, y0 + cfg.YTOPMAINCANVAS + y2)
    cfg.canvas.after(100, cfg.win.update())
    m.release(x0 + x2, y0 + cfg.YTOPMAINCANVAS + y2)
    cfg.canvas.after(100, cfg.win.update())

def click(rowcoltab):
    print("Test clicks {} ".format(rowcoltab))
    x, y = cfg.board.off_to_pixel(rowcoltab)
    m.move(x0 + x, y0 + cfg.YTOPMAINCANVAS + y)
    m.press(x0 + x, y0 + cfg.YTOPMAINCANVAS + y, 1)
    #cfg.canvas.after(100, cfg.win.update())
    m.release(x0 + x, y0 + cfg.YTOPMAINCANVAS + y, 1)
    #m.click(x, y, 1)
    return x, y