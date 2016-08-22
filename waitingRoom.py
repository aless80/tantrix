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
from PodSixNet.Connection import connection #ConnectionListener, connection
from time import sleep
import clientListener as cll



class WaitingRoom(cll.ClientListener): #Note: extending cll.ClientListener if Gui does not extend WaitingRoom
    def __init__(self):
        self.Names = [] #["Aless","Mararie"] #TODO log names that are present so that Entry can check them
        self.tree_headers = ['Player','Status','Address','Game']
        self.quit = False   #quit program after wroom has been closed. it will be passed to Gui.quit

    def startWaitingRoomUI(self, pumpit):

        self.pumpit = True
        if 'pumpit' in locals():
            self.pumpit = pumpit
        cfg.wroom = Tk()

        # Initialize our "databases":
        #  tree_codes - the list of players codes
        #  tree_names - a parallel list of player names, in the same order as the player codes
        #  ? - a hash table mapping player code to player information
        #tree_codes = () #('Aless', 'Mararie','Mary','John','Hugo','Heleen','Joe','Casper','Kiki')
        tree_names = () #('Aless', 'Mararie','Mary','John','Hugo','Heleen','Joe','Casper','Kiki')
        tree_status = () #('Ready','Ready','Playing','Playing','Playing','Playing','Solitaire','Idle','Idle')
        tree_list = []#[('Aless', 'Ready',1),('Mararie','Ready',2),('Mary','Playing',3),('John','Playing',4),('Hugo', 'Playing',5),('Heleen', 'Playing',6),('Joe', 'Solitaire',7),('Casper', 'Idle',8),('Kiki', 'Idle',9)]
        cnamesvar = StringVar(value=tree_names)

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
        self.tree = Treeview(content, show="headings", columns=cfg.wroominstance.tree_headers, name="treeview")
        self.tree.column("#1",minwidth=100,width=120, stretch=NO)
        self.tree.column("#2",minwidth=30,width=60, stretch=NO)
        self.tree.column("#3",minwidth=30,width=50, stretch=YES)
        self.tree.column("#4",minwidth=30,width=50, stretch=YES)
        namelbl = ttk.Label(content, text="Name")
        entry_sv = StringVar()
        #entry_sv.trace("w", lambda name, index, mode, sv=entry_sv: self.changeName(sv))
        nameentry = ttk.Entry(content, bg = 'white', textvariable = entry_sv, name="nameentry")#, validatecommand=validateIt)

        lbl = ttk.Label(content, text="Send to player:")	#Label on the right
        g1 = ttk.Radiobutton(content, text=messages['invite'], variable=messagevar, value='invite')
        g2 = ttk.Radiobutton(content, text=messages['refuse'], variable=messagevar, value='refuse')
        log = Listbox(content, height=5, bg = 'white', name="logbox")#, listvariable=cmessagelog		#Listbox with messages
        #todo: ready was bound to sendMessage, quitrw to quit
        testbtn = ttk.Button(content, text='Print connections', command=self.test, default='active', width='6', name="testbtn")	#Button
        ready = ttk.Button(content, text='Ready', command=self.toggleReadyForGame, default='active', width='6', name="readybtn")	#Button
        solitaire = ttk.Button(content, text='Solitaire', command=self.solitaire, default='active', width='6', name="solitairebtn")		#Button
        quit = ttk.Button(content, text='Quit', command=self.quitWaitingRoom, default='active', width='6', name="quitbtn")					#Button
        sentlbl = ttk.Label(content, textvariable=sentmsgvar, anchor='center', name="sentlbl")			#Label appearing below button
        status = ttk.Label(content, textvariable=statusmsgvar, anchor=W, name="statuslbl")				#Label on the bottom

        #def _build_tree():
        #    for ind, col in enumerate(cfg.wroominstance.tree_headers):
        #        self.tree.heading(ind, text=col.title(),command=lambda c=col: sortby(self.tree, c, 0))#
                # adjust the column's width to the header string
                #self.tree.column(col, width=tkFont.Font().measure(col.title()))
            #import Tkinter.font as tkFont
        #    for item in tree_list:
        #        self.tree.insert('', 'end', values=item)
                # adjust column's width if necessary to fit each value
                #for ix, val in enumerate(item):
                    #col_w = tkFont.Font().measure(val)
                #if self.tree.column(selfcfg.wroominstance.tree_headers[ix],width=None)<col_w:
                    #self.tree.column(selfcfg.wroominstance.tree_headers[ix], width=col_w)
        def get_tree():
            """Get from the self.tree an item when clicked"""
            idxs = self.tree.item(self.tree.focus())
            vals = idxs['values']
            if len(idxs['values'])==0: return None
            #name = vals[0]
            #address = vals[2]
            #status = vals[1]
            #return (name, status, address, game)
            return vals
        """def sortby(tree, col, descending):
            Sort tree contents when a column header is clicked on
            # grab values to sort
            data = [(tree.set(child, col), child) \
                for child in tree.get_children('')]
            # now sort the data in place
            data.sort(reverse=descending)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)
            # switch the heading so it will sort in the opposite direction
            tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))
        """
        def showstatus(*args):
            """Called when the selection in the listbox changes;
            Update the status message on the bottom with the new information"""
            name_num_status = get_tree()
            if name_num_status is None: return
            statusmsgvar.set("Player %s (%s) has this status: %s" % name_num_status)
            sentmsgvar.set('')

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


        # Grid all the widgets
        self.tree.grid(column=0, row=0, rowspan=8, sticky=(N,S,E,W))
        self.buildTree(tree_list) #not really needed anymore..
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

        # Set event bindings
        self.tree.bind('<<TreeviewSelect>>', showstatus)
        cfg.wroom.bind('<Double-1>', sendMessage)
        cfg.wroom.bind('<Return>', sendMessage)
        nameentry.bind('<Return>', (lambda _: self.changeName(nameentry)))
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
        showstatus()

        """Start main loop for tkinter and Sixpodnet"""
        self.keepLooping = True
        if self.pumpit:
            self.mainLoopWithPump()
        else:
            self.mainLoopWithoutPump()
        return self.quit

    def test(self):
        if self.pumpit:
            self.send_to_server("test")

    def buildTree(self, tree_list):
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

        for ind, col in enumerate(self.tree_headers):
            self.tree.heading(ind, text=col.title(),command=lambda c=col: sortby(self.tree, c, 0))#
            # adjust the column's width to the header string
            #self.tree.column(col, width=tkFont.Font().measure(col.title()))
        """Convert Status and Game to a better format, then insert in Treeview"""
        convert_status = {0: "Idle", 1: "Ready", -1: "Playing", -2: "Solitaire"}
        for item in tree_list:
            item[1] = convert_status[item[1]]
            if item[3] is None: item[3] = ""
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            #import Tkinter.font as tkFont
            #for ix, val in enumerate(item):
                #col_w = tkFont.Font().measure(val)
            #if self.tree.column(selfcfg.wroominstance.tree_headers[ix],width=None)<col_w:
                #self.tree.column(selfcfg.wroominstance.tree_headers[ix], width=col_w)

    def addToMessageLog(self, listToLog):
        """Add a line to the log listbox"""
        frame = cfg.wroom.winfo_children()[0]
        logbox = frame.children['logbox']
        #children contain widgets with these names: "treeview","nameentry","logbox","readybtn","solitairebtn","quitbtn","sentlbl","statuslbl"
        for item in listToLog:
            logbox.insert(END, item)

    def searchTreeByHeader(self, val, header = 'Player'):
        """Return item in Treeview by player name"""
        val = str(val)
        #frame = cfg.wroom.winfo_children()[0]
        #tree = frame.children['treeview']
        items = self.tree.get_children()
        headerIndToSearchInto = cfg.wroominstance.tree_headers.index(header) # ['Player','Status','Address']
        for item in items:
            itemval = str(self.tree.item(item, 'values')[headerIndToSearchInto])
            if itemval.startswith(val):
                return item
        return None

    def editItemInTree(self, item, valList, headerList = ['Player']):
        """Edit an item of TreeView by its header(s)"""
        #frame = cfg.wroom.winfo_children()[0]
        #self.tree = frame.children['treeview']
        #Get the current (old) values as a list
        old_vals = self.tree.item(item)['values']
        #Create a list with the new values
        newvalues = list(old_vals)
        for ind, header in enumerate(headerList):
            #Get from headerList which index should be changed
            headerIndex = cfg.wroominstance.tree_headers.index(header)
            newvalues[headerIndex] = valList[ind]
        #Finally change the old values
        self.tree.item(item, values=newvalues)

    def removeFromTree(self, name = ''):
        #TODO: what if two players have the same name? use Entry(..,validatecommand=validateIt) to check if not already present!
        item = self.searchTreeByHeader(name, header = 'Player')
        #frame = cfg.wroom.winfo_children()[0]
        #self.tree = frame.children['treeview']
        if item is not None:
            self.tree.delete(item)

    def changeName(self, sv):
        name = sv.get()
        cfg.name = name
        self.send_to_server("name", sender = cfg.connectionID, newname=name)  #TODO

    def toggleReadyForGame(self):
        if self.pumpit:
            self.send_to_server("toggleReady")
            #Change button layout when clicked
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
        self.quit = True    #used to quit everything after wroom has been closed
        if self.pumpit:
            self.send_to_server("quit")

    def solitaire(self):
        print("solitaire")
        cfg.solitaire = True
        self.keepLooping = False
        if self.pumpit:
            self.send_to_server("solitaire")

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