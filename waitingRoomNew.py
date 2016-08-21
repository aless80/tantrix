#http://www.tkdocs.com/tutorial/morewidgets.html
try:
	from Tkinter import *
	import Tkinter as ttk
	#import ScrolledText as tkst
	from ttk import Treeview
except:
	#import tkinter.scrolledtext as tkst
	from tkinter import *
	from tkinter import ttk
	from ttk import Treeview


import config as cfg
from sys import path
path.insert(0, './tantrix/PodSixNet')
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

class WaitingRoom():
    def __init__(self):
        self.Names = ["Aless","Mararie"] #TODO log names that are present so that Entry can check them
        pass

    def startWaitingRoomUI(self, pumpit):
        self.pumpit = True
        if 'pumpit' in locals():
            self.pumpit = pumpit
        cfg.wroom = Tk()

        # Initialize our "databases":
        #  tree_codes - the list of players codes
        #  tree_names - a parallel list of player names, in the same order as the player codes
        #  ? - a hash table mapping player code to player information
        tree_codes = ('Aless', 'Mararie','Mary','John','Hugo','Heleen','Joe','Casper','Kiki')
        tree_names = ('Aless', 'Mararie','Mary','John','Hugo','Heleen','Joe','Casper','Kiki')
        cnamesvar = StringVar(value=tree_names)
        tree_status = ('Ready','Ready','Playing','Playing','Playing','Playing','Solitaire','Idle','Idle')
        tree_header = ['Player','Status','Player No']
        tree_list = [('Aless', 'Ready',1),('Mararie','Ready',2),('Mary','Playing',3),('John','Playing',4),('Hugo', 'Playing',5),('Heleen', 'Playing',6),('Joe', 'Solitaire',7),('Casper', 'Idle',8),('Kiki', 'Idle',9)]

        # Initialize some messages that go in log listbox
        messagelog = [] #'Joe quit', 'Mararie entered the room']
        #cmessagelog = StringVar(value=messagelog)
        # Messages we can send to other players
        messages = { 'invite':'invite to play', 'refuse':'refuse to play'}

        # State variables - By using textvariable=var in definition widget is tied to this variable
        messagevar = StringVar()
        sentmsgvar = StringVar()
        statusmsgvar = StringVar()

        # Create and grid the outer content frame
        content = ttk.Frame(cfg.wroom) #, padding=(5, 5, 12, 0)) 		#Frame in cfg.wroom
        content.grid(column=0, row=0, sticky=(N,W,E,S))
        cfg.wroom.grid_columnconfigure(0, weight=1)
        cfg.wroom.grid_rowconfigure(0, weight=1)

        # Create the different widgets; note the variables that many
        # of them are bound to, as well as the button callback.
        tree = Treeview(content, show="headings", columns=('Player', 'Status','Player No'), name="treeview")
        namelbl = ttk.Label(content, text="Name")
        entry_sv = StringVar()
        #entry_sv.trace("w", lambda name, index, mode, sv=entry_sv: self.changeName(sv))
        nameentry = ttk.Entry(content, bg = 'white', textvariable = entry_sv, name="nameentry")#, validatecommand=validateIt)
        nameentry.bind('<Return>', (lambda _: self.changeName(nameentry)))


        lbl = ttk.Label(content, text="Send to player:")	#Label on the right
        g1 = ttk.Radiobutton(content, text=messages['invite'], variable=messagevar, value='invite')
        g2 = ttk.Radiobutton(content, text=messages['refuse'], variable=messagevar, value='refuse')
        log = Listbox(content, height=5, bg = 'white', name="logbox")#, listvariable=cmessagelog		#Listbox with messages
        #todo: ready was bound to sendMessage, quitrw to quit
        testbtn = ttk.Button(content, text='Test rm', command=self.removeFromTree, default='active', width='6', name="testbtn")	#Button
        ready = ttk.Button(content, text='Ready', command=self.toggleReadyForGame, default='active', width='6', name="readybtn")	#Button
        solitaire = ttk.Button(content, text='Solitaire', command=self.solitaire, default='active', width='6', name="solitairebtn")		#Button
        quit = ttk.Button(content, text='Quit', command=self.quitWaitingRoom, default='active', width='6', name="quitbtn")					#Button
        sentlbl = ttk.Label(content, textvariable=sentmsgvar, anchor='center', name="sentlbl")			#Label appearing below button
        status = ttk.Label(content, textvariable=statusmsgvar, anchor=W, name="statuslbl")				#Label on the bottom

        def _build_tree():
            for ind, col in enumerate(tree_header):
                tree.heading(ind, text=col.title(),command=lambda c=col: sortby(tree, c, 0))#
                # adjust the column's width to the header string
                #tree.column(col, width=tkFont.Font().measure(col.title()))
            #import Tkinter.font as tkFont
            for item in tree_list:
                tree.insert('', 'end', values=item)
                # adjust column's width if necessary to fit each value
                #for ix, val in enumerate(item):
                    #col_w = tkFont.Font().measure(val)
                #if tree.column(tree_header[ix],width=None)<col_w:
                    #tree.column(tree_header[ix], width=col_w)
        def get_tree():
            """Get from the tree an item when clicked"""
            idxs = tree.item(tree.focus())
            vals = idxs['values']
            if len(idxs['values'])==0: return None
            num = vals[2]
            name = vals[0]
            status = vals[1]
            return (name, status, num)
        def sortby(tree, col, descending):
            """Sort tree contents when a column header is clicked on"""
            # grab values to sort
            data = [(tree.set(child, col), child) \
                for child in tree.get_children('')]
            # now sort the data in place
            data.sort(reverse=descending)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)
            # switch the heading so it will sort in the opposite direction
            tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

        def showstatus(*args):
            """Called when the selection in the listbox changes;
            Update the status message on the bottom with the new information"""
            name_num_status = get_tree()
            if name_num_status is None: return
            statusmsgvar.set("Player %s (%s) has this status: %s" % name_num_status)
            sentmsgvar.set('')

        ############ NEEDED?
        # Called when the user double clicks an item in the listbox, presses
        # the "Send message" button, or presses the Return key.  In case the selected
        # item is scrolled out of view, make sure it is visible.
        #
        # Figure out which player is selected, which message is selected with the
        # radiobuttons, "send to player", and provide feedback that it was sent.
        def sendMessage(*args):
            name_num_status = get_tree()
            if name_num_status is None: return
            #
            #    idx = int(idxs[0])
            #    lbox.see(idx)
            #    name = playernames[idx]
                # message sending left as an exercise to the reader
            #    sentmsgvar.set("Sent %s to %s" % (messages[message.get()], name))
            sentmsgvar.set("Sent %s to %s" % (messages[messagevar.get()], name_num_status[0]))

        def quitwr(*args):
            idxs = lbox.curselection()
            if len(idxs)==1:
                idx = int(idxs[0])
                lbox.see(idx)
                name = playernames[idx]
                # message sending left as an exercise to the reader
                sentmsgvar.set("Quit")
        ############ NEEDED END?


        # Grid all the widgets
        tree.grid(column=0, row=0, rowspan=8, sticky=(N,S,E,W))
        _build_tree()
        #lbox.grid(column=0, row=0, rowspan=8, sticky=(N,S,E,W))
        namelbl.grid(column=1, row=0, columnspan=3, sticky=(N,W), padx=5)			#name Label
        nameentry.grid(column=1, row=1, columnspan=3, sticky=(N,E,W), pady=5, padx=5)	#name Entry
        lbl.grid(column=1, row=2, columnspan=3, sticky=W, padx=10, pady=5) 		#Label "Send to player"
        g1.grid(column=1, row=3, columnspan=2, sticky=W, padx=20)		#RadioButton invite
        g2.grid(column=1, row=4, columnspan=2, sticky=W, padx=20)		#RadioButton refuse
        testbtn.grid(column=3, row=3, sticky=W, padx=20)		#Test Button
        log.grid(column=1, row=5, columnspan=3, sticky=(N,S,E,W), padx=5, pady=5) 		#Listbox with all messages
        ready.grid(column=1, row=6, sticky=(W,S))			#
        solitaire.grid(column=2, row=6, sticky=(W,S))
        quit.grid(column=3, row=6, sticky=(W,S))
        sentlbl.grid(column=1, row=7, columnspan=2, sticky=N, pady=5, padx=5)
        status.grid(column=0, row=8, columnspan=2, sticky=(W,E))
        #Configure content Frame
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(5, weight=1)

        # Set event bindings for when the selection in the listbox changes,
        # when the user double clicks the list, and when they hit the Return key
        #lbox.bind('<<ListboxSelect>>', showstatus)
        tree.bind('<<TreeviewSelect>>', showstatus)
        cfg.wroom.bind('<Double-1>', sendMessage)
        cfg.wroom.bind('<Return>', sendMessage)
        #nameentry.bind('<Double-1>', self.changeName)
        # Colorize alternating lines of the player listbox
        #for i in range(0,len(playernames),2):
        #    lbox.itemconfigure(i, background='lightblue')

        # Set the starting state of the interface, including selecting the
        # default message to send, and clearing the messages.  Select the first
        # player in the list; because the <<ListboxSelect>> event is only
        # generated when the user makes a change, we explicitly call showstatus.
        self.addToMessageLog(messagelog)
        messagevar.set('invite')
        sentmsgvar.set('')
        statusmsgvar.set('')
        #lbox.selection_set(0)
        showstatus()

        #cfg.wroom.mainloop()
        """Start main loop for tkinter and Sixpodnet"""
        self.keepLooping = True
        if self.pumpit:
            self.mainLoopWithPump()
        else:
            self.mainLoopWithoutPump()

    def addToMessageLog(self, listToLog):
        """Add a line to the log listbox"""
        frame = cfg.wroom.winfo_children()[0]
        logbox = frame.children['logbox']
        #children contain widgets with these names: "treeview","nameentry","logbox","readybtn","solitairebtn","quitbtn","sentlbl","statuslbl"
        for item in listToLog:
            logbox.insert(END, item)

    def addToTree(self, name_num_status):
        """Add a line to the log listbox"""
        frame = cfg.wroom.winfo_children()[0]
        #children contain widgets with these names: "treeview","nameentry","logbox","readybtn","solitairebtn","quitbtn","sentlbl","statuslbl"
        tree = frame.children['treeview']
        #for item in name_num_status:
        tree.insert('', 'end', values=name_num_status)

    def searchTreeByName(self, name):
        frame = cfg.wroom.winfo_children()[0]
        tree = frame.children['treeview']
        items = tree.get_children()
        for item in items:
            itemname = tree.item(item, 'values')[0]
            if itemname.startswith(name):
                return item
        return None

    def removeFromTree(self, name = 'Mararie'):
        #TODO: what if two players have the same name? use Entry(..,validatecommand=validateIt) to check if not already present!
        item = self.searchTreeByName(name)
        frame = cfg.wroom.winfo_children()[0]
        tree = frame.children['treeview']
        if item is not None:
            tree.delete(item)


    def changeName(self, sv):
        print("changeName")
        print sv.get()
        pass #TODO

    def toggleButton(self):
        #####       OLD     ######
        button = event.widget
        print(button.configure('bg'))
        if button.configure('bg')[4] == 'white':
            button.configure(bg = "green", relief='SUNKEN', activebackground="green")
        elif button.configure('bg')[4] == 'green':
            button.configure(bg = "white", relief='RAISED', activebackground="white")
        sleep(0.2)
        cfg.wroom.update()
        print(button.configure('bg'))

    def toggleReadyForGame(self):
        print("toggleReadyForGame")
        if self.pumpit:
            self.send_to_server("toggleReady", sender = cfg.connectionID, orig = "callbacks.Callbacks.toggleReadyForGame")
            cfg.connection.Pump()
            #TODO: change button background/text!
            frame = cfg.wroom.winfo_children()[0]
            readybtn = frame.children['readybtn']
            """Configure the button"""
            if readybtn.config('relief')[4]=='raised':
                readybtn.configure(relief='sunken')
                readybtn.configure(bg = 'green')
            elif readybtn.config('relief')[4]=='sunken':
                readybtn.configure(relief='raised')
                readybtn.configure(bg = '#d6d6d6')
            sleep(0.1)
            cfg.wroom.update()


    def quitWaitingRoom(self):
        print("quitWaitingRoom()")
        self.keepLooping = False
        self.quit = True    #still used?
        if self.pumpit:
            self.send_to_server("quit", orig = "callbacks.Callbacks.quitWaitingRoom")
            cfg.connection.Pump()

    def solitaire(self):
        print("solitaire")
        cfg.solitaire = True
        self.keepLooping = False
        if self.pumpit:
            self.send_to_server("solitaire", orig = "callbacks.Callbacks.solitaire")
            cfg.connection.Pump()

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