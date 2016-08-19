try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import config as cfg
from sys import path
path.insert(0, './tantrix/PodSixNet')
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

class WaitingRoom():

    def startWaitingRoomUI(self, pumpit):
        self.pumpit = True
        if 'pumpit' in locals():
            self.pumpit = pumpit
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
        btn_wroom_ready = tk.Button(cfg.wroom, text="Ready", bg="white", name="btnReady", relief=tk.RAISED, activebackground="white")
        #btn_wroom_ready.bind("<Button-1>", self.toggleButton)
        btn_wroom_ready.bind('<ButtonRelease-1>', self.toggleReadyForGame)
        btn_wroom_solitaire = tk.Button(cfg.wroom, text="Solitaire", bg="white", name="btnSolitaire")
        #btn_wroom_ready.bind("<Button-1>", self.toggleButton)
        btn_wroom_solitaire.bind('<ButtonRelease-1>', self.solitaire)
        btn_wroom_exit = tk.Button(cfg.wroom, text="Quit", bg="white", name="btnQuitWRoom")
        #btn_wroom_ready.bind("<Button-1>", self.toggleReadyForGame)
        btn_wroom_exit.bind('<ButtonRelease-1>', self.quitWaitingRoom)
        lbl.grid(row = 0, columnspan = 3, padx=5, pady=5) #, sticky=W+E+N+S)
        ent.grid(row = 1, columnspan = 3, padx=5, pady=5)
        btn_wroom_ready.grid(row = 2, column = 0, padx=5, pady=5)
        btn_wroom_solitaire.grid(row = 2, column = 1, padx=5, pady=5)
        btn_wroom_exit.grid(row = 2, column = 2, padx=5, pady=5)
        #start loop. without pumping means hat is does not use sixpodnet, eg when called from main
        self.keepLooping = True
        if self.pumpit:
            self.mainLoopWithPump()
        else:
            self.mainLoopWithoutPump()

    def mainLoopWithoutPump(self):
        """Start main loop in waiting room. Do not use Sixpodnet to connect with server"""
        while self.keepLooping: #self.keepLooping changed by callbacks below
            """Update the boards"""
            cfg.wroom.update()
            cfg.wroom.update_idletasks()
        cfg.wroom.destroy()

    def mainLoopWithPump(self):
        """Start main loop in waiting room"""
        while self.keepLooping:      #self.keepLooping changed by callbacks below
            """Update the boards"""
            cfg.wroom.update()
            cfg.wroom.update_idletasks()
            """Polling loop for the client. asks the connection singleton for any new messages from the network"""
            connection.Pump()
            """Server"""
            self.Pump()
        cfg.wroom.destroy()

    def toggleButton(self, event):
        button = event.widget
        print(button.configure('bg'))
        if button.configure('bg')[4] == 'white':
            button.configure(bg = "green", relief=tk.SUNKEN, activebackground="green")
        elif button.configure('bg')[4] == 'green':
            button.configure(bg = "white", relief=tk.RAISED, activebackground="white")
        sleep(0.2)
        cfg.wroom.update()
        print(button.configure('bg'))

    def toggleReadyForGame(self, e):
        print("toggleReadyForGame")
        if self.pumpit:
            self.send_to_server("toggleReady", sender = cfg.connectionID, orig = "callbacks.Callbacks.toggleReadyForGame")
            cfg.connection.Pump()

    def quitWaitingRoom(self, e):
        print("quitWaitingRoom()")
        self.keepLooping = False
        self.quit = True    #still used?
        if self.pumpit:
            self.send_to_server("quit", orig = "callbacks.Callbacks.quitWaitingRoom")
            cfg.connection.Pump()

    def solitaire(self, e):
        print("solitaire")
        cfg.solitaire = True
        self.keepLooping = False
        if self.pumpit:
            self.send_to_server("solitaire", orig = "callbacks.Callbacks.solitaire")
            cfg.connection.Pump()

    def __init__(self):
        pass

def main():
    #will fail because of .Pump of Podsixnet.
    wr = WaitingRoom()
    wr.startWaitingRoomUI(False)


if __name__ == '__main__':
    main()
