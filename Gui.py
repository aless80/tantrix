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
        self.gameinprogress = True
        #global deck
        cfg.win = tk.Tk()
        cfg.win.protocol("WM_DELETE_WINDOW", self.deleteWindow)
        cfg.win.wm_title("Player %d: %s" % (cfg.player_num, cfg.name))
        #TODO do something with cfg.opponentname

        if 1:
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
            #cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, 650))
            cfg.win.geometry('%dx%d+%d+%d' % (w, cfg.YBOTTOMWINDOW, x, hs - cfg.YBOTTOMWINDOW - 125))
            #print(w, h, x, 600)
            #print("x={}, xleft is {}, xright={}".format(x,2559,2214))

        """Create cfg.canvas"""
        cfg.canvas = tk.Canvas(cfg.win, height = cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT,
            width = cfg.CANVAS_WIDTH + 76, name = "canvas")

        """Create main bkgr rectangle in cfg.canvas"""
        cfg.canvas.create_rectangle(0, cfg.YTOPMAINCANVAS, cfg.CANVAS_WIDTH, cfg.YBOTTOMMAINCANVAS,
            width = 2, fill = "#F1DCFF") #purple

        """Create hexagons on cfg.canvas"""
        cfg.hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
        for row in range(-10, cfg.ROWS + 10):
            for col in range(-10, cfg.COLS + 10):
                pts = list(cfg.hexagon_generator(row, col))
                cfg.canvas.create_line(pts, width = 2)

        """Create rectangles in cfg.canvas"""
        cfg.textwin = cfg.canvas.create_rectangle(0, 0, cfg.CANVAS_WIDTH, cfg.YTOPPL1,
                                                  width = 2, fill = "#F1DCFF", tags = "raised") #text celeste
        cfg.canvas.create_rectangle(cfg.CANVAS_WIDTH, 0, cfg.CANVAS_WIDTH + 76, cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT,
                                    width = 2, fill = "#F1DCFF", tags = "raised") ##C1F0FF right purple
        cfg.canvas.create_rectangle(0, cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YTOPMAINCANVAS,
                                    width = 2, fill = "#F1DCFF", tags = "raised") #top background purple
        cfg.pl1 = cfg.canvas.create_rectangle(0, cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YTOPMAINCANVAS,
                                              width = 2, fill = "#FEFD6C", tags = "raised") #top yellow
        cfg.canvas.create_rectangle(0, cfg.YBOTTOMMAINCANVAS, cfg.CANVAS_WIDTH, cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT,
                                    width = 2, fill = "#F1DCFF", tags = "raised") #bottom bkgr purple
        cfg.pl2 = cfg.canvas.create_rectangle(0, cfg.YBOTTOMMAINCANVAS, cfg.CANVAS_WIDTH,
                                    cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT, width = 2, fill = "#6AFF07", tags = "raised") #bottom green
        cfg.canvas.itemconfig(cfg.pl2, stipple = "gray50") #bottom green
        """Append canvas"""
        cfg.canvas.grid(row = 1, column = 0, rowspan = 5) #,expand="-ipadx")
        """Buttons"""
        btnwidth = 6
        """Confirm button"""
        self.btnConf = tk.Button(cfg.win, text = "Confirm\nmove", width = btnwidth, name = "btnConf",
                state = "disabled", relief = "flat", bg = "white", activebackground = "cyan", anchor = tk.W)
        self.btnConf.bind('<ButtonRelease-1>', self.buttonCallback)
        self.btnConf_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YTOPMAINCANVAS + cfg.HEX_SIZE * 4,
                                                       anchor = tk.NW, window = self.btnConf)
        #self.btnConf.grid(row = 2, column = 1, columnspan = 1)
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
        """Score"""
        self.btnScore = tk.Button(cfg.win, text = "Score", width = btnwidth, name = "btnScore", state = "normal",
                        relief = "flat", bg = "white", activebackground = "cyan")
        self.btnScore_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMMAINCANVAS +
                                    (cfg.YTOPMAINCANVAS - cfg.YBOTTOMMAINCANVAS) / 2 + cfg.HEX_SIZE, anchor = tk.W, window = self.btnScore)
        self.btnScore.bind('<ButtonRelease-1>', self.buttonCallback)
        """

        f = tk.Frame(cfg.win, height=32, width=32)
        f.pack_propagate(0) # don't  shrink
        #f.pack()
        f.grid(row = 1, column = 1, columnspan = 1)
        b = tk.Button(f, text="Sure!")
        b.pack(fill=tk.BOTH, expand=1)

        #self.btnConf_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YTOPMAINCANVAS + cfg.HEX_SIZE * 4, anchor = tk.NW, window = self.btnConf)
        """

        """Text widget"""
        cfg.text = cfg.canvas.create_text(0 + 5, 0, text = "", anchor = tk.NW, font = 20, tags = "raised")
        cfg.board.message()
        cfg.pl1text = cfg.canvas.create_text(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YTOPMAINCANVAS,
                                             text = "", anchor = tk.SW, font = 20)
        cfg.pl2text = cfg.canvas.create_text(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMMAINCANVAS + cfg.HEX_SIZE * 2,
                                             text = "", anchor = tk.SW, font = 20)
        """Bind arrows"""
        cfg.win.bind('<Left>', lambda event, horiz = 1: cfg.deck.shift(horiz, 0))
        cfg.win.bind('<Right>', lambda event, horiz = -1: cfg.deck.shift(horiz, 0))
        cfg.win.bind('<Down>', lambda event, vert = -1: cfg.deck.shift( 0, vert))
        cfg.win.bind('<Up>', lambda event, vert = 1: cfg.deck.shift(0, vert))
        """Update window"""
        cfg.win.update()

        #from pymouse import PyMouse
        #m = PyMouse()
        #print(m.position()) #(2211, 636)
        #print(".btnReset.winfo_width="+str(self.btnReset.winfo_width())) #76
        #cfg.win.geometry(str(cfg.canvas.winfo_width() + self.btnConf.winfo_width()) + "x" +
        #                 str(int(cfg.canvas.winfo_height() )) )
        cfg.win.update_idletasks()
        cfg.win.update()
        #print(m.position())
        #print("self.btnConf.winfo_width()={}".format(self.btnConf.winfo_width()))



    def main(self):
        global rndgen
        rndgen = random.Random(0)
        #global deck
        #global board not needed because:
        cfg.board = bd.Board()
        """Deal deck"""
        cfg.deck = Deck.Deck()
        #deck = cfg.deck #deck is needed for other methods
        cfg.hand1 = Hand.Hand(-1)
        cfg.hand2 = Hand.Hand(-2)

        """Color the buttons"""
        cfg.canvas.itemconfig(cfg.pl1, fill = cfg.hand1.playercolor[1])
        cfg.canvas.itemconfig(cfg.pl2, fill = cfg.hand2.playercolor[1])
        """Bindings"""
        cfg.canvas.bind('<ButtonPress-1>', self.clickCallback) #type 4
        #<Double-Button-1>?
        cfg.canvas.bind('<B1-Motion>', self.motionCallback) #drag
        cfg.canvas.bind('<ButtonRelease-1>', self.clickCallback) #release
        cfg.canvas.bind('<ButtonPress-3>', self.rxclickCallback)
        cfg.canvas.focus_set()
        #cfg.canvas.bind('<Key>', self.keyCallback)
        cfg.canvas.bind('r', self.keyCallback) #buttonReset)
        cfg.canvas.bind('<Return>', self.buttonConfirm)
        #cfg.canvas.bind('\x7f', self.buttonReset)
        cfg.canvas.bind('s', self.keyCallback) #buttonsScore)
        cfg.canvas.bind('<Control-Key-w>', self.buttonsQuit)
        cfg.canvas.bind('<Control-Key-q>', self.buttonsQuit)
        self.mainloop()
