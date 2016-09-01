try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import random
import config as cfg
import HexagonGenerator as hg
import Board as bd
import callbacks as clb
import Hand
#hand1 = False
#hand2 = False
import Deck as Deck
import waitingRoom as wr
import hoverInfo as hover

from sys import path
path.insert(0, './PodSixNet')
import clientListener as cll
#from PodSixNet.Connection import ConnectionListener, connection

class Gui(clb.Callbacks, cll.ClientListener):
    #Note on inheritance: add wr.WaitingRoom if WaitingRoom does not extend cll.ClientListener
    #cll.ClientListener is extended here and also by waitingroom
    def __init__(self, host, port):
        self.quit = False
        self.connect(host, port)
        self.gameinprogress = False

        cfg.wroominstance = wr.WaitingRoom()
        self.quit = cfg.wroominstance.startWaitingRoomUI(True)
        if self.quit:
            return
        self.startGameUI()

    def startGameUI(self):
        """Determine attributes from player"""
        if not cfg.solitaire:
            print("Starting board for player " + str(cfg.player_num) + " " + str(cfg.name))
            if cfg.player_num == 1:
                self.turn = True
            else:
                self.turn = False
        else:
            cfg.player_num = 1
            self.turn = True
            """Chose the color for the second player to red or blue""" #TODO open a dialog instead
            color_ind = cfg.PLAYERCOLORS.index(cfg.playercolor) + 1
            cfg.opponentcolor = 'red' if (cfg.playercolor != 'red') else 'blue'

        self.gameinprogress = True
        cfg.win = tk.Tk()
        cfg.win.protocol("WM_DELETE_WINDOW", self.deleteWindow)
        cfg.win.wm_title("Player %d: %s" % (cfg.player_num, cfg.name))
        #TODO do something with cfg.opponentname

        if 0:
            w = cfg.CANVAS_WIDTH + 5
            ws = cfg.win.winfo_screenwidth()    #width of the screen
            hs = cfg.win.winfo_screenheight()   #height of the screen
            #Get the x and y coord for the Tk root window
            x = ws - w / 2 - (cfg.player_num - 0) * w;  #Note: edited cfg.player_num in tantrix 11.1. it was -1
            y = hs - cfg.YBOTTOMWINDOW / 2
            cfg.win.geometry('%dx%d' % (w, cfg.YBOTTOMWINDOW))
            w = w + 76
            x = x - 76 - 150
            #cfg.win.geometry('%dx%d+%d+%d' % (w + 76, h, 0, 600))
            cfg.win.geometry('%dx%d+%d+%d' % (w, cfg.YBOTTOMWINDOW, x, hs - cfg.YBOTTOMWINDOW - 125))

        """Create cfg.canvas"""
        cfg.canvas = tk.Canvas(cfg.win, height = cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT,
            width = cfg.CANVAS_WIDTH + 76, name = "canvas")
        """Create main bkgr rectangle in cfg.canvas"""
        bg_color = "#F1DCFF"
        cfg.canvas.create_rectangle(0, cfg.YTOPMAINCANVAS, cfg.CANVAS_WIDTH, cfg.YBOTTOMMAINCANVAS,
            width = 2, fill = bg_color) #pink-purple
        """Create hexagons on cfg.canvas"""
        cfg.hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
        for row in range(-10, cfg.ROWS + 10):
            for col in range(-10, cfg.COLS + 10):
                pts = list(cfg.hexagon_generator(row, col))
                cfg.canvas.create_line(pts, width = 2)
        """Create rectangles to place over cfg.canvas"""
        cfg.textwin1 = cfg.canvas.create_rectangle(0, 0, cfg.CANVAS_WIDTH, cfg.YTOPPL1,
                            width = 2, fill = bg_color, tags = "raised")
        cfg.canvas.create_rectangle(cfg.CANVAS_WIDTH, 0, cfg.CANVAS_WIDTH + 76, cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT,
                            width = 2, fill = bg_color, tags = "raised") #cover canvas on the right
        #Tiles player 1 on top
        cfg.canvas.create_rectangle(0, cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YTOPMAINCANVAS,
                            width = 2, fill = cfg.playercolor, tags = "raised") #cover the canvas with background for the top tiles

        #TODO trying this but it shows an ugly thing at startup
        #stippleCanvas1 = tk.Canvas(cfg.win, height = cfg.YTOPMAINCANVAS - cfg.YTOPPL1, width = cfg.CANVAS_WIDTH)
        #cfg.stipple1 = stippleCanvas1.create_rectangle(0, cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YTOPMAINCANVAS,
        #                width = 0, tags = "stipple", fill = "") #"#FEFD6C" top yellow
        cfg.stipple1 = cfg.canvas.create_rectangle(0, cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YTOPMAINCANVAS,
                        width = 0, tags = "stipple", fill = "") #"#FEFD6C" top yellow

        #Tiles player 2 on bottom
        cfg.canvas.create_rectangle(0, cfg.YBOTTOMMAINCANVAS - cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT - cfg.YTOPPL1,
                            width = 2, fill = cfg.opponentcolor, tags = "raised") #cover the canvas with background for the bottom tiles
        cfg.stipple2 = cfg.canvas.create_rectangle(0, cfg.YBOTTOMMAINCANVAS - cfg.YTOPPL1, cfg.CANVAS_WIDTH,
                        cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT - cfg.YTOPPL1,
                        width = 0, tags = "stipple", fill = "gray", stipple = "gray12")
        cfg.textwin2 = cfg.canvas.create_rectangle(0, cfg.YBOTTOMPL2,
                            cfg.CANVAS_WIDTH, cfg.YBOTTOMWINDOW, #cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT,
                            width = 2, fill = bg_color, tags = "raised")
        """Append canvas on cfg.win"""
        cfg.canvas.grid(row = 1, column = 0, rowspan = 5) #,expand="-ipadx")
        #TODO stippleCanvas1.grid(row = 3, column = 0, rowspan = 5)
        """Buttons"""
        btnwidth = 6
        """Confirm button"""
        self.btnConf = tk.Button(cfg.win, text = "Confirm\nmove", width = btnwidth, name = "btnConf",
                state = "disabled", relief = "flat", bg = "white", activebackground = "cyan", anchor = tk.W)
        self.btnConf.bind('<ButtonRelease-1>', self.buttonCallback)
        self.btnConf_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YTOPMAINCANVAS + cfg.HEX_SIZE * 4,
                                                       anchor = tk.NW, window = self.btnConf)
        """Reset button"""
        self.btnReset = tk.Button(cfg.win, text = "Reset\ndeck", width = btnwidth, name = "btnReset", state = "disabled",
                        relief = "flat", bg = "white", activebackground = "cyan")
        self.btnReset_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2,
                                    cfg.YBOTTOMMAINCANVAS - cfg.HEX_SIZE * 4, anchor = tk.SW, window = self.btnReset)
        self.btnReset.bind('<ButtonRelease-1>', self.buttonCallback)
        """Quit button"""
        self.btnQuit = tk.Button(cfg.win, text = "Quit", width = btnwidth, name = "btnQuit",
                        relief = "flat", bg = "white", activebackground = "red")
        self.btnQuit_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMMAINCANVAS +
                                    (cfg.YTOPMAINCANVAS - cfg.YBOTTOMMAINCANVAS) / 2 - cfg.HEX_SIZE, anchor = tk.SW, window = self.btnQuit)
        self.btnQuit.bind('<ButtonRelease-1>', self.buttonCallback)
        """Score button"""
        self.btnScore = tk.Button(cfg.win, text = "Score", width = btnwidth, name = "btnScore", state = "normal",
                        relief = "flat", bg = "white", activebackground = "cyan")
        self.btnScore_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMMAINCANVAS +
                                    (cfg.YTOPMAINCANVAS - cfg.YBOTTOMMAINCANVAS) / 2 + cfg.HEX_SIZE, anchor = tk.W, window = self.btnScore)
        self.btnScore.bind('<ButtonRelease-1>', self.buttonCallback)
        """Text widgets: messages and scores"""
        cfg.text1 = cfg.canvas.create_text(0 + 5, 0, text = "", anchor = tk.NW, font = 15, tags = "raised")
        cfg.text2 = cfg.canvas.create_text(0 + 5, cfg.YBOTTOMWINDOW - cfg.YTOPPL1 , text = "", anchor = tk.SW, font = 15, tags = "raised")
        cfg.board.message()
        cfg.score1 = cfg.canvas.create_text(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YTOPMAINCANVAS,
                                             text = "", anchor = tk.SW, font = 20)
        cfg.score2 = cfg.canvas.create_text(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMPL2,
                                             text = "", anchor = tk.SW, font = 20)
        """Bind arrows that move the table"""
        cfg.win.bind('<Left>', lambda event, horiz = 1: cfg.deck.shift(shift_row = horiz))
        cfg.win.bind('<Right>', lambda event, horiz = -1: cfg.deck.shift(shift_row = horiz))
        cfg.win.bind('<Down>', lambda event, vert = -1: cfg.deck.shift(shift_col = vert))
        cfg.win.bind('<Up>', lambda event, vert = 1: cfg.deck.shift(shift_col = vert))
        """Set tooltips on widgets"""
        hover.createToolTip(self.btnQuit, "Quit tantrix")
        hover.createToolTip(self.btnScore, "Show the score as longest line + closed line")
        hover.createToolTip(self.btnReset, "Bring back the moved tiles")
        hover.createToolTip(self.btnConf, "Confirm your move. If the button is disable, something is wrong with your move")
        """Update window"""
        cfg.win.update()
        cfg.win.update_idletasks()
        cfg.win.update()


    def main(self):
        global rndgen
        rndgen = random.Random(0)
        cfg.board = bd.Board()
        """Deal deck"""
        cfg.deck = Deck.Deck()
        #deck = cfg.deck #deck is needed for other methods
        cfg.hand1 = Hand.Hand(-1)
        cfg.hand2 = Hand.Hand(-2)
        """Set stipples right"""
        cfg.deck.update_stipples()

        """Bindings"""
        cfg.canvas.bind('<ButtonPress-1>', self.clickCallback) #type 4
        cfg.canvas.bind('<ButtonPress-3>', self.clickCallback) #type 4
        #<Double-Button-1>?
        cfg.canvas.bind('<B1-Motion>', self.motionCallback) #drag
        #cfg.canvas.bind_class("tile", "<B1-Motion>", self.motionCallback)
        cfg.canvas.bind('<ButtonRelease-1>', self.clickCallback) #release
        cfg.canvas.bind('<ButtonRelease-3>', self.clickCallback)
        cfg.canvas.focus_set()
        #cfg.canvas.bind('<Key>', self.keyCallback)
        cfg.canvas.bind('r', self.keyCallback) #buttonReset)
        cfg.canvas.bind('<Return>', self.buttonConfirm)
        #cfg.canvas.bind('\x7f', self.buttonReset)
        cfg.canvas.bind('s', self.keyCallback) #buttonsScore)
        cfg.canvas.bind('<Control-Key-w>', self.buttonsQuit)
        cfg.canvas.bind('<Control-Key-q>', self.buttonsQuit)

        """Start main loop"""
        self.mainloop()
