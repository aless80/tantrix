"""
install python-dev
sudo apt-get install python3-pil
sudo apt-get install python3-imaging-tk

http://variable-scope.com/posts/hexagon-tilings-with-python
http://www.raywenderlich.com/1223/python-tutorial-how-to-generate-game-deck-
with-python-imaging-library

http://www.redblobgames.com/grids/hexagons/
"""
import Gui
import config as cfg
import HexagonGenerator as hg
import Board as bd
import callbacks as clb
import helpers as hp

import tkMessageBox as mb

"""
from pymouse import PyMouse
from pykeyboard import PyKeyboard
k = PyKeyboard()
m = PyMouse()
"""
#http://stackoverflow.com/questions/1917198/how-to-launch-a-python-tkinter-dialog-box-that-self-destructs
#https://www.summet.com/dmsi/html/guiProgramming.html

deck = cfg.deck
#board = False
#deck = False
#hand1 = False
#hand2 = False
#clicked_rowcolcanv = None
#canvases = [cfg.canvastop, cfg.canvas, cfg.canvasbottom]
#canvases = [cfg.canvas]
#cfg.turn = 1
#cfg.free = True

from PodSixNet.Connection import ConnectionListener, connection

if __name__ == "__main__":
    gui_instance = Gui.Gui()
    gui_instance.main()
    #cfg.canvas.mainloop()

    #http://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop
