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
from Deck import Deck


class Gui(clb.Callbacks):
    def __init__(self):
        global deck
        cfg.win = tk.Tk()

        if 1:
            w = cfg.CANVAS_WIDTH + 5
            h = cfg.YBOTTOMWINDOW
            ws = cfg.win.winfo_screenwidth()    #width of the screen
            hs = cfg.win.winfo_screenheight()   #height of the screen
            x = ws - w / 2; y = hs - h / 2      #x and y coord for the Tk root window
            cfg.win.geometry('%dx%d' % (w, h))
            w = w + 76
            x = x - 76 - 150
            #cfg.win.geometry('%dx%d+%d+%d' % (w + 76, h, 0, 600))
            #cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, 650))
            cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, hs - h - 125))
            #print(w, h, x, 600)
        print("x={}, xleft is {}, xright={}".format(x,2559,2214))

        """Create cfg.canvas"""
        cfg.canvas = tk.Canvas(cfg.win, height = cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT,
            width = cfg.CANVAS_WIDTH + 76, name = "canvas")

        """Create main rectangle in cfg.canvas"""
        cfg.canvas.create_rectangle(0, cfg.YTOPMAINCANVAS, cfg.CANVAS_WIDTH, cfg.YBOTTOMMAINCANVAS,
            width = 2, fill = "#F1DCFF") #celeste

        """Create hexagons on cfg.canvas"""
        cfg.hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
        for row in range(-10, cfg.ROWS + 10):
            for col in range(-10, cfg.COLS + 10):
                pts = list(cfg.hexagon_generator(row, col))
                cfg.canvas.create_line(pts, width = 2)

        """Create rectangles in cfg.canvas"""
        cfg.textwin = cfg.canvas.create_rectangle(0, 0, cfg.CANVAS_WIDTH, cfg.YTOPPL1, width = 2, fill = "#F1DCFF") #text celeste
        cfg.canvas.create_rectangle(cfg.CANVAS_WIDTH, 0, cfg.CANVAS_WIDTH + 76, cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT, width = 2, fill = "#F1DCFF") ##C1F0FF right celeste
        cfg.canvas.create_rectangle(0, cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YTOPMAINCANVAS, width = 2, fill = "#F1DCFF") #top background celeste
        cfg.pl1 = cfg.canvas.create_rectangle(0, cfg.YTOPPL1, cfg.CANVAS_WIDTH, cfg.YTOPMAINCANVAS, width = 2, fill = "#FEFD6C", tags="pl1") #top yellow
        cfg.canvas.create_rectangle(0, cfg.YBOTTOMMAINCANVAS, cfg.CANVAS_WIDTH, cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT, width = 2, fill = "#F1DCFF", tags="pl1") #bottom bkgr celeste
        cfg.pl2 = cfg.canvas.create_rectangle(0, cfg.YBOTTOMMAINCANVAS, cfg.CANVAS_WIDTH, cfg.YBOTTOMMAINCANVAS + cfg.HEX_HEIGHT, width = 2, fill = "#6AFF07") #bottom green
        cfg.canvas.itemconfig(cfg.pl2, stipple="gray50") #bottom green
        """Append canvas"""
        cfg.canvas.grid(row = 1, column = 0, rowspan = 5) #,expand="-ipadx")
        """Buttons"""
        btnwidth = 6
        self.btnConf = tk.Button(cfg.win, text = "Confirm\nmove", width = btnwidth, name = "btnConf",
                state = "disabled", relief = "flat", bg = "white", activebackground = "cyan", anchor = tk.W)
        self.btnConf.bind('<ButtonRelease-1>', self.buttonCallback)
        self.btnConf_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YTOPMAINCANVAS + cfg.HEX_SIZE * 4, anchor = tk.NW, window = self.btnConf)
        #self.btnConf.grid(row = 2, column = 1, columnspan = 1)
        #Reset button
        self.btnReset = tk.Button(cfg.win, text = "Reset\ndeck", width = btnwidth, name = "btnReset", state = "disabled",
                        relief = "flat", bg = "white", activebackground = "cyan")
        self.btnReset_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMMAINCANVAS - cfg.HEX_SIZE * 4, anchor = tk.SW, window = self.btnReset)
        self.btnReset.bind('<ButtonRelease-1>', self.buttonCallback)

        self.btnScore = tk.Button(cfg.win, text = "Score", width = btnwidth, name = "btnScore", state = "normal",
                        relief = "flat", bg = "white", activebackground = "cyan")
        self.btnScore_window = cfg.canvas.create_window(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMMAINCANVAS + (cfg.YTOPMAINCANVAS - cfg.YBOTTOMMAINCANVAS) / 2, anchor = tk.W, window = self.btnScore)
        self.btnScore.bind('<ButtonRelease-1>', self.buttonCallback)
        """Text widget"""
        cfg.text = cfg.canvas.create_text(0 + 5, 0, text = "", anchor=tk.NW, font = 20) #cfg.YBOTTOM + cfg.HEX_HEIGHT
        cfg.board.message()
        cfg.pl1text = cfg.canvas.create_text(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YTOPMAINCANVAS, text = "", anchor=tk.SW, font = 20)
        cfg.pl2text = cfg.canvas.create_text(cfg.CANVAS_WIDTH + cfg.BUFFER * 2, cfg.YBOTTOMMAINCANVAS + cfg.HEX_SIZE * 2, text = "", anchor=tk.SW, font = 20)
        """Update window"""
        cfg.win.update()

        from pymouse import PyMouse
        m = PyMouse()
        print(m.position()) #(2211, 636)
        print(".btnReset.winfo_width="+str(self.btnReset.winfo_width())) #76
        #cfg.win.geometry(str(cfg.canvas.winfo_width() + self.btnConf.winfo_width()) + "x" +
        #                 str(int(cfg.canvas.winfo_height() )) )
        cfg.win.update_idletasks()
        cfg.win.update()
        print(m.position())
        print("self.btnConf.winfo_width()={}".format(self.btnConf.winfo_width()))


    def main(self):
        global rndgen
        rndgen = random.Random(0)
        global deck
        #global board not needed because:
        cfg.board = bd.Board()
        """Deal deck"""
        cfg.deck = Deck()
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
        #cfg.canvas.bind("<1>", lambda event: cfg.canvas.focus_set())
        cfg.canvas.bind('<Key>', self.keyCallback) #cfg.deck.confirm_move()) #deck.confirm_move()
        #canvas.bind('<MouseWheel>', wheel)
        import test as ts
        ts.tests()
