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
from sys import path
path.insert(0, './tantrix/PodSixNet')
from PodSixNet.Connection import connection #ConnectionListener, connection
import clientListener as cll
import hoverInfo as hover

class pregameDialog(cll.ClientListener): #Note: extending cll.ClientListener if Gui does not extend WaitingRoom
    def __init__(self):
        self.Names = []
        self.tree_headers = ['Player','Status','Address','Game','Color']
        self.quit = False   #quit program after wroom has been closed. it will be passed to Gui.quit

    def startWaitingRoomUI(self, pumpit):
        self.pumpit = True
        if 'pumpit' in locals():
            self.pumpit = pumpit
        cfg.wroom = Tk()
        cfg.wroom.protocol("WM_DELETE_WINDOW", self.quitWaitingRoom)

        """State variables - By using textvariable=var in definition widget is tied to this variable"""
        statusmsg_sv = StringVar() #needed
        entry_sv = StringVar(value = cfg.name)
        #entry_sv.trace("w", lambda name, index, mode, sv=entry_sv: self.changeName(sv))
        chatentry_sv = StringVar(value = "Press enter to chat")

        """Create and grid the outer content frame"""
        content = ttk.Frame(cfg.wroom) #, padding=(5, 5, 12, 0)) 		#Frame in cfg.wroom
        content.grid(column = 0, row = 0, sticky = (N,W,E,S))
        cfg.wroom.grid_columnconfigure(0, weight = 1)
        cfg.wroom.grid_rowconfigure(0, weight = 1)

        """Create the different widgets; note the variables that manysome widgets are bound to"""
        self.tree = Treeview(content, show="headings", columns=cfg.wroominstance.tree_headers, name = "treeview")
        self.tree.column("#1", minwidth = 100, width = 120, stretch = NO)
        self.tree.column("#2", minwidth = 30, width = 60, stretch = NO)
        self.tree.column("#3", minwidth = 30, width = 50, stretch = YES)
        self.tree.column("#4", minwidth = 30, width = 50, stretch = YES)
        self.tree.column("#5", minwidth = 30, width = 50, stretch = YES)
        namelbl = ttk.Label(content, text="Player name")
        nameentry = ttk.Entry(content, bg = 'white', textvariable = entry_sv, name = "nameentry")#, validatecommand=validateIt)
        colorlbl = ttk.Label(content, text="Player color")
        self.colorframe = ttk.Frame(content, name = "colorframe", borderwidth = 1, relief='sunken')
        lbl = ttk.Label(content, text="Send to player:")	#Label on the right
        self.log = Listbox(content, height = 5, bg = 'white', name = "logbox")#, listvariable=cmessagelog		#Listbox with messages
        self.chatAll = ttk.Button(content, text = 'Chat to All', command = self.chatToAll, default = 'active', width = '6',name = "chat")
        self.chatentry = ttk.Entry(content, bg = 'white', foreground = 'gray', textvariable = chatentry_sv, name = "chatentry", selectforeground = 'blue')
        testbtn = ttk.Button(content, text = 'Connections', command = self.test, default = 'active', width = '6', name = "testbtn") #Button
        ready = ttk.Button(content, text = 'Ready', command = self.toggleReadyForGame, default = 'active', width = '6', name = "readybtn")	   #Button
        solitaire = ttk.Button(content, text = 'Solitaire', command = self.solitaire, default = 'active', width = '6', name = "solitairebtn")	    #Button
        quit = ttk.Button(content, text = 'Quit', command = self.quitWaitingRoom, default = 'active', width = '6', name = "quitbtn")  #Button
        status = ttk.Label(content, textvariable = statusmsg_sv, anchor = W, name = "statuslbl") #Label on the bottom

        # Grid all the widgets
        self.tree.grid(row = 0, column = 0, rowspan = 9, sticky = (N,S,E,W))
        namelbl.grid(row = 0, column = 1, columnspan = 2, sticky = (N,W), padx = 5)
        nameentry.grid(row = 1, column = 1, columnspan = 2, sticky = (N,E,W), pady = 5, padx = 5)
        colorlbl.grid(row = 0, column = 3, columnspan = 1, sticky = (N,W), padx = 5)
        self.colorframe.grid(row = 1, column = 3, columnspan = 1, sticky = (N,E,W), pady = 5, padx = 5)
        testbtn.grid(row = 3, column = 3, columnspan = 1, sticky = E, padx = 5)		#Test Button
        self.log.grid(row = 5, column = 1, columnspan = 3, sticky = (N,S,E,W), padx = 5, pady = 5)   #Listbox with all messages
        self.chatentry.grid(row = 6, column = 1, columnspan = 2, sticky = (N,E), padx = 5, pady = 5)
        self.chatAll.grid(row = 6, column = 3, columnspan = 1, sticky = (N,E), padx = 5, pady = 5)
        ready.grid(row = 7, column = 1, sticky = (W,S), padx = 5, pady = 5)			#
        solitaire.grid(row = 7, column = 2, sticky = (W,S), padx = 5, pady = 5)
        quit.grid(row = 7, column = 3, sticky = (W,S), padx = 5, pady = 5)
        status.grid(row = 9, column = 0, columnspan = 2, sticky = (W,E))

        """Configure content Frame and color Frame"""
        content.grid_columnconfigure(0, weight = 1)
        content.grid_rowconfigure(5, weight = 1)
        h = nameentry.winfo_reqheight()
        self.colorframe.configure(height = h, bg = 'red')

        """Set event bindings"""
        self.tree.bind('<<TreeviewSelect>>', showstatus)
        nameentry.bind('<Return>', (lambda _: self.changeName(nameentry)))
        cfg.wroom.bind('<Control-Key-w>', self.quitWaitingRoom)
        cfg.wroom.bind('<Control-Key-q>', self.quitWaitingRoom)
        cfg.wroom.bind('<Control-Key-r>', self.toggleReadyForGame)
        cfg.wroom.bind('<Control-Key-s>', self.solitaire)
        self.chatentry.bind("<Return>",self.chatToAll)
        def chatEntryActive(e = None):
            self.chatentry.config(foreground = 'black')
            self.chatentry.delete(0, 'end')
        def chatEntryInactive(e = None):
            print(self)
            chatentry_sv.set("Press enter to chat")
            self.chatentry.config(foreground = 'gray')
        self.chatentry.bind("<FocusIn>", lambda e: chatEntryActive(e))
        self.chatentry.bind("<FocusOut>", lambda e: chatEntryInactive(e))
        self.colorframe.bind("<ButtonRelease-1>", self.changeColor)

        """Set tooltips on widgets"""
        hover.createToolTip(namelbl, "Type in your name and press Enter")
        hover.createToolTip(nameentry, "Type in your name and press Enter")
        hover.createToolTip(testbtn, "This is just for testing")
        hover.createToolTip(ready, "Toggle ready state to play tantrix with other players")
        hover.createToolTip(solitaire, "Start a two player game on this computer")
        hover.createToolTip(quit, "Quit Tantrix")
        hover.createToolTip(self.chatentry, "Press enter to send to chat")
        hover.createToolTip(self.chatAll, "Press enter to send to chat")
        hover.createToolTip(self.colorframe, "Click to select your color")
        hover.createToolTip(colorlbl, "Your color")
        # Colorize alternating lines of the player listbox
        #for i in range(0,len(playernames),2):
        #    lbox.itemconfigure(i, background='lightblue')

        """Start main loop for tkinter and Sixpodnet"""
        self.keepLooping = True
        if self.pumpit:
            self.mainLoopWithPump()
        else:
            self.mainLoopWithoutPump()
        return self.quit

    def changeColor(self, e = None):
        current = self.colorframe.cget('bg')
        color_ind = cfg.PLAYERCOLORS.index(current) + 1
        color = cfg.PLAYERCOLORS[color_ind % 4]
        self.colorframe.configure(bg = color)
        cfg.playercolor = color
        self.sendChangedColor(color)


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
    #will fail because of .Pump of Podsixnet.
    wr = WaitingRoom()
    wr.startWaitingRoomUI(False)


if __name__ == '__main__':
    main()