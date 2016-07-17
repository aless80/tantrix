try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import config as cfg
from sys import path
path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
from PodSixNet.Connection import ConnectionListener, connection


class waitingRoom():

    def startWaitingRoomUI(self):
        cfg.wroom = tk.Tk()
        cfg.wroom.wm_title("Tantrix - Waiting room")
        """Positions and sizes"""
        height_wroom = 310; width_wroom = 300;
        ws = cfg.wroom.winfo_screenwidth() 		#width of the screen
        hs = cfg.wroom.winfo_screenheight() 	#height of the screen
        x = 0; y = hs/2 - height_wroom/2 		#x and y coord for the Tk root window
        cfg.wroom.geometry('%dx%d+%d+%d' % (width_wroom, height_wroom, x, y))
        """Window content"""
        lbl = tk.Label(cfg.wroom, text="Welcome!", bg="cyan", name="welcome")
        ent = tk.Entry(cfg.wroom, name="ent", text = "localhost")
        ent.insert(0, "a default value")

        btn_wroom_ready = tk.Button(cfg.wroom, text="Ready", bg="cyan", name="btnReady")
        btn_wroom_ready.bind('<ButtonRelease-1>', self.buttonCallback)
        btn_wroom_solitaire = tk.Button(cfg.wroom, text="Solitaire", bg="red", name="btnSolitaire")
        btn_wroom_solitaire.bind('<ButtonRelease-1>', self.buttonCallback)
        btn_wroom_exit = tk.Button(cfg.wroom, text="Quit", bg="red", name="btnQuitWRoom")
        btn_wroom_exit.bind('<ButtonRelease-1>', self.buttonCallback)
        #self.btnQuit.bind('<ButtonRelease-1>', )
        lbl.grid(row = 0, columnspan = 3, padx=5, pady=5) #, sticky=W+E+N+S)
        ent.grid(row = 1, columnspan = 3, padx=5, pady=5)
        btn_wroom_ready.grid(row = 2, column = 0, padx=5, pady=5)
        btn_wroom_solitaire.grid(row = 2, column = 1, padx=5, pady=5)
        btn_wroom_exit.grid(row = 2, column = 2, padx=5, pady=5)
        """Start main loop in waiting room"""
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

