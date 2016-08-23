"""
install python-dev
sudo apt-get install python3-pil
sudo apt-get install python3-imaging-tk

http://variable-scope.com/posts/hexagon-tilings-with-python
http://www.raywenderlich.com/1223/python-tutorial-how-to-generate-game-deck-
with-python-imaging-library

http://www.redblobgames.com/grids/hexagons/
"""
import sys
import Gui
import config as cfg
import HexagonGenerator as hg
import Board as bd
import callbacks as clb
import helpers as hp
import tkMessageBox as mb
import waitingRoom as wr

deck = cfg.deck

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("e.g.", sys.argv[0], "localhost:31425")
        #Launch anyway
        host = "localhost"
        port = 31425
        print("Launcing with host, port = %s , %d" % (host, port))
    else:
        host, port = sys.argv[1].split(":")

    cfg.gui_instance = Gui.Gui()
    if not cfg.gui_instance.quit:
        cfg.gui_instance.main()
    #cfg.canvas.mainloop()
