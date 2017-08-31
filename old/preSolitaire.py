#http://www.tkdocs.com/tutorial/morewidgets.html
try:
	from Tkinter import *
	import Tkinter as ttk
	from ttk import Treeview
except:
	from tkinter import *
	from tkinter import ttk
	from ttk import Treeview


import config as cfg
import clientListener as cll
import hoverInfo as hover
from sys import path
path.insert(0, './tantrix/PodSixNet')
from PodSixNet.Connection import connection #ConnectionListener, connection


class preSolitaire(cll.ClientListener, object): #Note: extending cll.ClientListener if Gui does not extend WaitingRoom
    def __init__(self):
        self.Names = []
        self.quit = False   #quit program after preSolitaire has been closed. it will be passed to Gui.quit

    def startpreSolitaireUI(self, pumpit):
        self.pumpit = pumpit
        cfg.wroom = Tk()
        cfg.wroom.protocol("WM_DELETE_WINDOW", self.quitpreSolitaire)
        """State variables - By using textvariable=var in definition widget is tied to this variable"""
        entry_sv = StringVar(value = cfg.name)
        entry2_sv = StringVar(value = cfg.opponentname)

        """Create and grid the outer content frame"""
        content = ttk.Frame(cfg.wroom)
        content.grid(column = 0, row = 0, sticky = (N,W,E,S))
        cfg.wroom.grid_columnconfigure(0, weight = 1)
        cfg.wroom.grid_rowconfigure(0, weight = 1)

        """Create the different widgets; note the variables that some widgets are bound to"""
        namelbl = ttk.Label(content, text="Player 1's name")
        self.nameentry = ttk.Entry(content, bg = 'white', textvariable = entry_sv, name = "nameentry")
        namelbl2 = ttk.Label(content, text="Player 2's name")
        self.nameentry2 = ttk.Entry(content, bg = 'white', textvariable = entry2_sv, name = "nameentry2")
        colorlbl = ttk.Label(content, text="Player color")
        self.colorframe = ttk.Frame(content, name = "colorframe", borderwidth = 1, relief='sunken')
        colorlbl2 = ttk.Label(content, text="Player2 color")
        self.colorframe2 = ttk.Frame(content, name = "colorframe2", borderwidth = 1, relief='sunken')
        startbtn = ttk.Button(content, text = 'Start', command = self.quitToGame, default = 'active', width = '6', name = "solitairebtn")
        quit = ttk.Button(content, text = 'Quit', command = self.quitpreSolitaire, default = 'active', width = '6', name = "quitbtn")

        """Grid all the widgets"""
        namelbl.grid(row = 0, column = 0, columnspan = 2, sticky = (N,W), padx = 5)
        colorlbl.grid(row = 0, column = 3, columnspan = 1, sticky = (N,W), padx = 5)
        self.nameentry.grid(row = 1, column = 1, columnspan = 2, sticky = (N,E,W), pady = 5, padx = 5)
        self.colorframe.grid(row = 1, column = 3, columnspan = 1, sticky = (N,E,W), pady = 5, padx = 5)
        namelbl2.grid(row = 2, column = 0, columnspan = 2, sticky = (N,W), padx = 5)
        colorlbl2.grid(row = 2, column = 3, columnspan = 1, sticky = (N,W), padx = 5)
        self.nameentry2.grid(row = 3, column = 1, columnspan = 2, sticky = (N,E,W), pady = 5, padx = 5)
        self.colorframe2.grid(row = 3, column = 3, columnspan = 1, sticky = (N,E,W), pady = 5, padx = 5)
        startbtn.grid(row = 4, column = 3, sticky = (E,S), padx = 5, pady = 5)
        quit.grid(row = 4, column = 2, sticky = (W,S), padx = 5, pady = 5)

        """Configure content Frame and color Frame"""
        content.grid_columnconfigure(0, weight = 1)
        content.grid_rowconfigure(5, weight = 1)
        h = self.nameentry.winfo_reqheight()
        self.colorframe.configure(height = h, bg = cfg.playercolor)
        self.colorframe2.configure(height = h, bg = cfg.opponentcolor)

        """Set event bindings"""
        self.nameentry.bind('<Return>', (lambda _: self.askChangeName(self.nameentry, 1)))
        self.nameentry2.bind('<Return>', (lambda _: self.askChangeName(self.nameentry2, 2)))
        self.nameentry.bind('<FocusOut>', (lambda _: self.askChangeName(self.nameentry, 1)))
        self.nameentry2.bind('<FocusOut>', (lambda _: self.askChangeName(self.nameentry2, 2)))
        cfg.wroom.bind('<Control-Key-w>', self.quitpreSolitaire)
        cfg.wroom.bind('<Control-Key-q>', self.quitpreSolitaire)
        cfg.wroom.bind('<Control-Key-s>', self.quitpreSolitaire)
        self.colorframe.bind("<ButtonRelease-1>", (lambda _: self.changeColor(1)))
        self.colorframe2.bind("<ButtonRelease-1>", (lambda _: self.changeColor(2)))

        """Set tooltips on widgets"""
        #hover.createToolTip(namelbl, "Type in your name and press Enter")
        hover.createToolTip(self.nameentry, "Type in the name for player 1")
        hover.createToolTip(self.nameentry2, "Type in the name for player 2")
        hover.createToolTip(startbtn, "Start a two player game on this computer")
        hover.createToolTip(quit, "Quit Tantrix")
        hover.createToolTip(self.colorframe, "Click to select player 1's color")
        hover.createToolTip(self.colorframe2, "Click to select player 2's color")
        #hover.createToolTip(colorlbl, "Your color")

        """Start main loop for tkinter and Sixpodnet"""
        self.keepLooping = True
        if self.pumpit:
            self.mainLoopWithPump()
        else:
            self.mainLoopWithoutPump()
        return self.quit

    def quitToGame(self,e = None):
        print("Quitting the preSolitaire dialog")
        self.keepLooping = False

    def quitpreSolitaire(self,e = None):
        print("Quitting the preSolitaire dialog")
        self.keepLooping = False
        self.quit = True    #used to quit everything after wroom has been closed
        if self.pumpit:
            self.send_to_server("quit")

    def askChangeName(self, sv, player):
        """User wants to change name. Ask server if ok"""
        def validName(newname):
            """Check that name has an allowed format"""
            """Check that name is not already taken"""
            if newname in [cfg.name, cfg.opponentname]:
                return False
            """Check that newname begins with non-numeric character"""
            import re
            if re.match('^[a-zA-Z]+', newname) is None:
                return False
            return True
        newname = sv.get()
        """Send to clients new name if valid or old name"""
        if validName(newname):
            if player == 1:
                cfg.name = newname
            elif player == 2:
                cfg.opponentname = newname
        else:
            sv.delete(0, END)
            if player == 1:
                sv.insert(0, cfg.name)
            elif player == 2:
                sv.insert(0, cfg.opponentname)
        if player == 1:
            self.sendChangedName(newname)

    def changeName(self, name):
        """Server sends the name of this player"""
        self.nameentry.delete(0, END)
        self.nameentry.insert(0, name)
        cfg.name = name

    def changeColor(self, player):
        cframe = self.colorframe if player is 1 else self.colorframe2
        current = cframe.cget('bg')
        color_ind = cfg.PLAYERCOLORS.index(current) + 1
        color = cfg.PLAYERCOLORS[color_ind % 4]
        """Skip the opponent's color"""
        cframeother = self.colorframe2 if player is 1 else self.colorframe
        other = cframeother.cget('bg')
        if color == other:
            color_ind = cfg.PLAYERCOLORS.index(color) + 1
            color = cfg.PLAYERCOLORS[color_ind % 4]
        """Set the new color on the UI and store it in cfg"""
        cframe.configure(bg = color)
        if player is 1:
          cfg.playercolor = color
        elif player is 2:
          cfg.opponentcolor = color

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

def main():
    wr = preSolitaire()
    wr.startpreSolitaireUI(False)
    pass


if __name__ == '__main__':
    main()