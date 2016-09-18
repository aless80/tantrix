try:
    import Tkinter as tk # for Python2
    from ttk import Treeview
except:
    import tkinter as tk # for Python3
    from ttk import Treeview
import random
import config as cfg
import HexagonGenerator as hg
import Board as bd
import callbacks as clb
import Hand
import math
import Deck as Deck
import waitingRoom as wr
import preSolitaire as ds
import hoverInfo as hover

from sys import path
path.insert(0, './PodSixNet')
import clientListener as cll
#from PodSixNet.Connection import ConnectionListener, connection

class Gui(clb.Callbacks, cll.ClientListener, object):
    #Note on inheritance: add wr.WaitingRoom if WaitingRoom does not extend cll.ClientListener
    #cll.ClientListener is extended here and also by waitingroom
    def __init__(self, host, port):
        self.quit = False
        self.connect(host, port)
        cfg.gameinprogress = False
        cfg.opponentname = "Player2"
        """Waiting room: instantiate it and start it"""
        cfg.wroominstance = wr.WaitingRoom()
        self.quit = cfg.wroominstance.startWaitingRoomUI(True)
        if self.quit:
            return

        cfg.deck = Deck.Deck()
        """Initialize deck. Needed to call one of its methods"""
        self.startGameUI()

    def startGameUI(self):
        """Determine attributes from player"""
        """Configurations for solitaire vs online game"""
        if cfg.solitaire:
            cfg.player_num = 1
            self.turn = True
            """Open a new window for choosing the name and color for the second player"""
            cfg.opponentcolor = 'red' if (cfg.playercolor != 'red') else 'blue'
            dial = ds.preSolitaire()
            dial.startpreSolitaireUI(True)
            wintitle = "%s vs %s" % (cfg.name, cfg.opponentname)
        else:
            print("Starting board for player " + str(cfg.player_num) + " " + str(cfg.name))
            if cfg.player_num == 1:
                self.turn = True
            else:
                self.turn = False
            wintitle = "Player %d: %s" % (cfg.player_num, cfg.name)

        cfg.gameinprogress = True
        self.win = tk.Tk()
        self.win.protocol("WM_DELETE_WINDOW", self.deleteWindow)
        self.win.wm_title(wintitle)
        self.win.minsize(int(cfg.HEX_COS + (cfg.HEX_SIZE * 2 - cfg.HEX_COS) * 8 + 76),
                         int(math.ceil(cfg.HEX_HEIGHT * 4) + cfg.YTOPPL1 + cfg.HEX_HEIGHT * 1.5 + cfg.HEX_HEIGHT))
        self.win.maxsize(int(cfg.HEX_COS + (cfg.HEX_SIZE * 2 - cfg.HEX_COS) * (cfg.ROWS + 30)),
                         int(math.ceil(cfg.HEX_HEIGHT * (cfg.COLS + 18)) + cfg.YTOPPL1 + cfg.HEX_HEIGHT * 1.5 + cfg.HEX_HEIGHT))
        #Set the window size and get its geometry to dynamically set the positions of its widgets
        win_width = cfg.BOARD_WIDTH + 76 #76 is the width of the buttons on the right
        win_height = cfg.YBOTTOMBOARD + cfg.HEX_HEIGHT
        self.win.geometry('%dx%d+%d+%d' % (win_width, win_height, 0, 0))
        """Create self.canvas"""
        self.canvas = tk.Canvas(self.win, height = 0, width = 0, name = "canvas")
        """Create main bkgr rectangle in self.canvas"""
        bg_color = "#F1DCFF"
        self.backgroundID = self.canvas.create_rectangle(0, 0, 0, 0,
                                    width = 2, fill = bg_color) #pink-purple
        """Create hexagons on self.canvas"""
        def create_hexagons():
            cfg.hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
            for row in range(-10, cfg.ROWS + 30):
                for col in range(-10, cfg.COLS + 18):
                    pts = list(cfg.hexagon_generator(row, col))
                    self.canvas.create_line(pts, width = 2)
        create_hexagons()
        """Append canvas on self.win"""
        #self.canvas.grid(row = 1, column = 0, rowspan = 5)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        """Create rectangles to place over self.canvas"""
        #Tiles player 1 on top
        self.textwin1 = self.canvas.create_rectangle(0, 0, 0, 0, width = 2, fill = bg_color, tags = "raised")
        color = cfg.PLAYERCOLORS.index(cfg.playercolor) if cfg.player_num == 1 else cfg.PLAYERCOLORS.index(cfg.opponentcolor)
        color = cfg.PLAYERCOLORS[color + 4]
        self.backgroundTopID = self.canvas.create_rectangle(0, 0, 0, 0, width = 2, fill = color, tags = "raised") #cover the canvas with background for the top tiles
        self.stipple1 = self.canvas.create_rectangle(0, 0, 0, 0, width = 0, tags = "stipple", fill = "") #"#FEFD6C" top yellow
        #Tiles player 2 on bottom
        color = cfg.PLAYERCOLORS.index(cfg.playercolor) if cfg.player_num == 2 else cfg.PLAYERCOLORS.index(cfg.opponentcolor)
        color = cfg.PLAYERCOLORS[color + 4]
        self.backgroundBottomID = self.canvas.create_rectangle(0, 0, 0, 0, width = 2, fill = color, tags = "raised") #cover the canvas with background for the bottom tiles
        self.stipple2 = self.canvas.create_rectangle(0, 0, 0, 0, width = 0, tags = "stipple", fill = "gray", stipple = "gray12")
        self.textwin2 = self.canvas.create_rectangle(0, 0, 0, 0, width = 2, fill = bg_color, tags = "raised")
        #cover canvas on the right
        self.backgroundRightID = self.canvas.create_rectangle(0, 0, 0, 0, width = 2, fill = bg_color, tags = "raised")
        """Buttons"""
        btnwidth = 6
        """Confirm button"""
        self.btnConf = tk.Button(self.win, text = "Confirm\nmove", width = btnwidth, name = "btnConf",
                state = "disabled", relief = "flat", bg = "white", activebackground = "cyan", anchor = tk.W)
        self.btnConf.bind('<ButtonRelease-1>', self.buttonCallback)
        self.btnConf_window = self.canvas.create_window(0, 0, anchor = tk.NW, window = self.btnConf)
        """Reset button"""
        self.btnReset = tk.Button(self.win, text = "Reset\ndeck", width = btnwidth, name = "btnReset", state = "disabled",
                        relief = "flat", bg = "white", activebackground = "cyan")
        self.btnReset_window = self.canvas.create_window(0, 0, anchor = tk.SW, window = self.btnReset)
        self.btnReset.bind('<ButtonRelease-1>', self.buttonCallback)
        """Quit button"""
        self.btnQuit = tk.Button(self.win, text = "Quit", width = btnwidth, name = "btnQuit",
                        relief = "flat", bg = "white", activebackground = "red")
        self.btnQuit_window = self.canvas.create_window(0, 0, anchor = tk.SW, window = self.btnQuit)
        self.btnQuit.bind('<ButtonRelease-1>', self.buttonCallback)
        """Score button"""
        self.btnScore = tk.Button(self.win, text = "Score", width = btnwidth, name = "btnScore", state = "normal",
                        relief = "flat", bg = "white", activebackground = "cyan")
        self.btnScore_window = self.canvas.create_window(1, 1, anchor = tk.W, window = self.btnScore)
        self.btnScore.bind('<ButtonRelease-1>', self.buttonCallback)
        """Text widgets: messages and scores"""
        self.text1 = self.canvas.create_text(0 + 5, 0, text = "", anchor = tk.NW, font = 15, tags = "raised")
        self.text2 = self.canvas.create_text(0, 0, text = "", anchor = tk.SW, font = 15, tags = "raised")
        """Chat"""
        #cfg.chat = tk.Listbox(self.canvas, height = 5, bg = 'white', name = "logbox")#, listvariable=cmessagelog		#Listbox with messages
        #cfg.chatentry = tk.Entry(self.canvas, bg = 'white', foreground = 'gray', textvariable = chatentry_sv, name = "chatentry", selectforeground = 'blue')
        #cfg.chat.grid(row = 5, column = 1, columnspan = 3, sticky = (N,S,E,W), padx = 5, pady = 5)   #Listbox with all messages
        """Store widgets and widget items"""
        cfg.win = self.win
        cfg.canvas = self.canvas
        cfg.textwin1 = self.textwin1
        cfg.stipple1 = self.stipple1
        cfg.stipple2 = self.stipple2
        cfg.textwin2 = self.textwin2
        cfg.text1 = self.text1
        cfg.text2 = self.text2
        #cfg.board = self.board

        cfg.board.message()
        def configure(event):
            """Callback to handle resizing of the main window"""
            win_width, win_height = event.width, event.height
            """Update coordinates used by UI elements"""
            cfg.BOARD_WIDTH = win_width - 76
            cfg.YTOPBOARD = cfg.YTOPPL1 + cfg.HEX_HEIGHT + cfg.BUFFER
            cfg.BOARD_HEIGHT = win_height - (cfg.HEX_HEIGHT * 2.5 + cfg.YTOPPL1 - cfg.BUFFER * 2) - 2 - cfg.HEX_HEIGHT / 4#NEW #2 is ~ the Tk window border
            cfg.YBOTTOMWINDOW = cfg.BOARD_HEIGHT + cfg.HEX_HEIGHT * 2.5 + cfg.YTOPPL1 - cfg.BUFFER * 2# - cfg.HEX_HEIGHT / 2
            #YBOTTOMWINDOW = YBOTTOMBOARD + HEX_HEIGHT + YTOPPL1
            cfg.YBOTTOMBOARD = cfg.YBOTTOMWINDOW - cfg.HEX_HEIGHT
            cfg.YBOTTOMPL2 = cfg.YBOTTOMWINDOW - cfg.YTOPPL1
            """Positions of canvas and all canvas items"""
            self.canvas.config(height = win_width, width = win_height)
            self.canvas.coords(self.backgroundID, 0, cfg.YTOPBOARD, cfg.BOARD_WIDTH, cfg.YBOTTOMBOARD)
            self.canvas.coords(self.textwin1, 0, 0, cfg.BOARD_WIDTH, cfg.YTOPPL1)
            self.canvas.coords(self.backgroundTopID, 0, cfg.YTOPPL1, cfg.BOARD_WIDTH, cfg.YTOPBOARD)
            self.canvas.coords(self.stipple1, 0, cfg.YTOPPL1, cfg.BOARD_WIDTH, cfg.YTOPBOARD)
            self.canvas.coords(self.backgroundBottomID, 0, cfg.YBOTTOMBOARD - cfg.YTOPPL1, cfg.BOARD_WIDTH, win_height - cfg.YTOPPL1)
            self.canvas.coords(self.stipple2, 0, cfg.YBOTTOMBOARD - cfg.YTOPPL1, cfg.BOARD_WIDTH, win_height - cfg.YTOPPL1)
            self.canvas.coords(self.textwin2, 0, cfg.YBOTTOMPL2, cfg.BOARD_WIDTH, cfg.YBOTTOMWINDOW)
            self.canvas.coords(self.backgroundRightID, cfg.BOARD_WIDTH, 0, win_width, win_height)
            self.canvas.coords(self.text2, 0 + 5, cfg.YBOTTOMWINDOW - cfg.YTOPPL1)
            """Positions of the buttons"""
            self.canvas.coords(self.btnConf_window, cfg.BOARD_WIDTH + cfg.BUFFER * 2, cfg.YTOPBOARD + cfg.HEX_SIZE * 2)
            self.canvas.coords(self.btnReset_window, cfg.BOARD_WIDTH + cfg.BUFFER * 2, cfg.YTOPBOARD + cfg.HEX_SIZE * 8)#cfg.YBOTTOMBOARD - cfg.HEX_SIZE * 4)
            self.canvas.coords(self.btnQuit_window, cfg.BOARD_WIDTH + cfg.BUFFER * 2, #cfg.YBOTTOMBOARD +
                               #(cfg.YTOPBOARD - cfg.YBOTTOMBOARD) / 2 - cfg.HEX_SIZE)
                               cfg.YBOTTOMBOARD - cfg.HEX_SIZE * 2)
            self.canvas.coords(self.btnScore_window, cfg.BOARD_WIDTH + cfg.BUFFER * 2,
                               #cfg.YBOTTOMBOARD + (cfg.YTOPBOARD - cfg.YBOTTOMBOARD) / 2 + cfg.HEX_SIZE)
                               cfg.YBOTTOMBOARD - cfg.HEX_SIZE * 8)
            #self.canvas.create_rectangle(0, cfg.YTOPBOARD + cfg.HEX_SIZE, 1000, cfg.YTOPBOARD + cfg.HEX_SIZE * 3, fill="red")
            #self.canvas.create_rectangle(0, cfg.YBOTTOMBOARD - cfg.HEX_SIZE * 4, 1000, cfg.YBOTTOMBOARD - cfg.HEX_SIZE * 8, fill="red")
            """Positions of the tiles"""
            cfg.deck.expand()
            """Update window"""
            self.win.update()


        self.canvas.bind("<Configure>", configure)
        """Set the sizes and positions of canvas, widgets and widget items. Create a bogus event to feed in configure"""
        class Event(object):
            pass
        event = Event()
        event.width = win_width
        event.height = win_height
        configure(event)

        """Bind arrows that move the table"""
        self.win.bind('<Left>', lambda event, horiz = 1: cfg.deck.shift(shift_row = horiz))
        self.win.bind('<Right>', lambda event, horiz = -1: cfg.deck.shift(shift_row = horiz))
        self.win.bind('<Down>', lambda event, vert = -1: cfg.deck.shift(shift_col = vert))
        self.win.bind('<Up>', lambda event, vert = 1: cfg.deck.shift(shift_col = vert))
        """Set tooltips on widgets"""
        hover.createToolTip(self.btnQuit, "Quit tantrix")
        hover.createToolTip(self.btnScore, "Show the score as longest line + closed line")
        hover.createToolTip(self.btnReset, "Bring back the moved tiles")
        hover.createToolTip(self.btnConf, "Confirm your move. If the button is disable, something is wrong with your move")
        """Update window"""
        self.win.update()
        self.win.update_idletasks()
        self.win.update()


    def main(self):
        cfg.board = bd.Board()
        #Note: this goes to the first method of Deck, refill_deck
        cfg.hand1 = Hand.Hand(-1)
        cfg.hand2 = Hand.Hand(-2)
        """Set stipples right"""
        cfg.deck.update_stipples()
        """Bindings"""
        self.canvas.bind('<ButtonPress-1>', self.clickCallback) #type 4
        self.canvas.bind('<ButtonPress-3>', self.clickCallback) #type 4
        self.canvas.bind('<B1-Motion>', self.motionCallback) #drag
        self.canvas.bind('<ButtonRelease-1>', self.clickCallback) #release
        self.canvas.bind('<ButtonRelease-3>', self.clickCallback)
        self.canvas.focus_set()
        #self.canvas.bind('<Key>', self.keyCallback)
        self.canvas.bind('r', self.keyCallback)
        self.canvas.bind('<Return>', self.buttonConfirm)
        self.canvas.bind('s', self.keyCallback)
        self.canvas.bind('<Control-Key-w>', self.buttonsQuit)
        self.canvas.bind('<Control-Key-q>', self.buttonsQuit)
        def printHistory(e):
            for h in cfg.history:
                print(h)
        self.canvas.bind('h', printHistory)
        """Start main loop"""
        self.mainloop()
