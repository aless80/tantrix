import sys
import Gui
import config as cfg

##import HexagonGenerator as hg
##import Board as bd
##import callbacks as clb
##import helpers as hp
##import tkMessageBox as mb
##import waitingRoom as wr

deck = cfg.deck
def launch():
    if len(sys.argv) != 2:
        print("Usage:", sys.argv[0], "host:port")
        print("  e.g.", sys.argv[0], "localhost:31425")
        #Launch anyway
        host = "localhost"
        port = 31425
        print("Launcing with host, port = %s , %d" % (host, port))
    else:
        host, port = sys.argv[1].rsplit(":",1)
        print("Host: " + host)
        print("Port: " + str(port))
    """Call this script as with two optional arguments: python tantrix <ready> <player_name>"""
    cfg.ready = 0
    if len(sys.argv) == 3:
        cfg.ready = sys.argv[2]
    elif len(sys.argv) == 4:
        cfg.ready = sys.argv[2]
        cfg.name = sys.argv[3]

    cfg.gui_instance = Gui.Gui(host, port)
    if not cfg.gui_instance.quit:
        cfg.gui_instance.main()




if __name__ == "__main__":
    launch()

""" Dependences and notes
install python-dev
sudo apt-get install python3-pil
sudo apt-get install python3-imaging-tk

http://variable-scope.com/posts/hexagon-tilings-with-python
http://www.raywenderlich.com/1223/python-tutorial-how-to-generate-game-deck-
with-python-imaging-library

http://www.redblobgames.com/grids/hexagons/
"""