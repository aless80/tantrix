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

import sys
sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep


class Gui(clb.Callbacks, ConnectionListener):

    def startWaitingRoomUI(self):
        cfg.wroom = tk.Tk()
        cfg.wroom.wm_title("Tantrix - Waiting room")
        """Positions and sizes"""
        height_wroom = 310; width_wroom = 300;
        ws = cfg.wroom.winfo_screenwidth() 		#width of the screen
        hs = cfg.wroom.winfo_screenheight() 	#height of the screen
        x = ws/2 - width_wroom/2; y = hs/2 - height_wroom/2 		#x and y coord for the Tk root window
        cfg.wroom.geometry('%dx%d+%d+%d' % (width_wroom, height_wroom, x, y))
        """Window content"""
        lbl = tk.Label(cfg.wroom, text="Welcome!", bg="cyan", name="welcome")
        ent = tk.Entry(cfg.wroom, name="ent", text = "localhost")
        ent.insert(0, "a default value")

        btn_wroom_start = tk.Button(cfg.wroom, text="Start", bg="cyan", name="btnWaitGame")
        btn_wroom_start.bind('<ButtonRelease-1>', self.buttonCallback)
        btn_wroom_exit = tk.Button(cfg.wroom, text="Quit", bg="red", name="btnQuitWRoom")
        btn_wroom_exit.bind('<ButtonRelease-1>', self.buttonCallback)
        #self.btnQuit.bind('<ButtonRelease-1>', )
        lbl.pack()
        ent.pack()
        btn_wroom_start.pack()
        btn_wroom_exit.pack()
        """Start main loop"""
        self.wroom = True
        while self.wroom: #self.wroom changed by callbacks
            """Update the boards"""
            cfg.wroom.update()
            cfg.wroom.update_idletasks()
            """Polling loop for the client. asks the connection singleton for any new messages from the network"""
            connection.Pump()
            """Server"""
            self.Pump()
        cfg.wroom.destroy()

    def startGameUI(self):
        """Determine attributes from player"""
        print("Starting board for player "+str(cfg.player_num))
        if cfg.player_num == 1:
            self.turn = True
        else:
            self.turn = False

        #global deck
        cfg.win = tk.Tk()
        cfg.win.wm_title("Player " + str(cfg.player_num))

        if 1:
            w = cfg.CANVAS_WIDTH + 5
            ws = cfg.win.winfo_screenwidth()    #width of the screen
            hs = cfg.win.winfo_screenheight()   #height of the screen
            x = ws - w / 2 - (cfg.player_num - 1) * w; y = hs - cfg.YBOTTOMWINDOW / 2      #x and y coord for the Tk root window
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
        #cfg.canvas.bind("<1>", lambda event: cfg.canvas.focus_set())
        cfg.canvas.bind('<Key>', self.keyCallback) #cfg.deck.confirm_move()) #deck.confirm_move()
        #canvas.bind('<MouseWheel>', wheel)
        import test as ts
        ts.tests()
        """This is the polling loop during the game"""
        while self.running:
            """Polling loop for the client. asks the connection singleton for any new messages from the network"""
            connection.Pump()   #Polling loop for the client.
            """Server"""
            self.Pump()         #Server
            """Update the boards"""
            cfg.win.update()
            cfg.win.update_idletasks()

    def Network_startgame(self, data):
        """Called from server.Connected"""
        print("\nReceiving in Gui.Network_startgame():")
        print("  " + str(data))
        self.wroom = False
        self.quit = False
        self.running = True
        cfg.player_num = data["player_num"]
        cfg.gameid = data["gameid"]

    def Network_confirm(self, data):
        print("\nReceiving in Gui.Network_confirm():")
        print("  " + str(data))
        """Get attributes"""
        rowcolnum = data["rowcolnum"]
        rowcoltab1 = data["rowcoltab1"]
        rowcoltab2 = data["rowcoltab2"]
        cfg.deck.reset()
        cfg.deck.move_automatic(rowcoltab1, rowcoltab2)
        self.buttonConfirm(send = False)
        #cfg.deck.confirm_move(send = False)

    def Network_disconnected(self, data):
        print "disconnected from the server"
        #TODO
    
    def Network_error(self, data):
        print "error:", data['error'][1]
        #TODO

    def Network_numplayers(data):
        # update gui element displaying the number of currently connected players
        print data['players']
        #TODO - on server implement something like channel.Send({"action": "numplayers", "players": 10})
        #       probably cfg.gui_instance.send_to_server(

    def send_to_server(self, action, **dict):
        '''Allow Client to send to Server (server.ClientChannel.Network_<action>)'''
        data = {"action": action, "gameid": cfg.gameid, "sender": cfg.player_num, "orig": "Server.send_to_server"}
        """Add key-value pairs in dict to data dictionary"""
        for kw in dict:
            data[kw] = dict[kw]
        """Send data to server"""
        print("\nSending to server:")
        print("  " + str(data))
        connection.Send(data)

    def __init__(self):
        self.Connect()
        #TODO the problem is that when server sees two clients it says startgame and I think window is not there yet
        self.quit = 0
        self.startWaitingRoomUI()
        if self.quit:
            return
        """This is the polling loop before starting the game"""
        """self.running = False
        while not self.running:  #becomes true in Gui.Network_startgame, called from server.Connected
            connection.Pump()
            self.Pump()
            sleep(0.01)
        """
        self.startGameUI()