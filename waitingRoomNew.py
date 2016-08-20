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

    def startWaitingRoomUI(self, pumpit):
        self.pumpit = True
        if 'pumpit' in locals():
            self.pumpit = pumpit
        #cfg.wroom = tk.Tk()


        cfg.wroom = Tk()

        # Initialize our "databases":
        #  - the list of players codes
        #  - a parallel list of player names, in the same order as the player codes
        #  - a hash table mapping player code to player information
        playercodes = ('ar', 'au', 'be', 'br', 'ca', 'cn', 'dk', 'fi', 'fr', 'gr', 'in', 'it', 'jp', 'mx', 'nl', 'no', 'es', 'se', 'ch')
        playernames = ('Argentina', 'Australia', 'Belgium', 'Brazil', 'Canada', 'China', 'Denmark', \
                'Finland', 'France', 'Greece', 'India', 'Italy', 'Japan', 'Mexico', 'Netherlands', 'Norway', 'Spain', \
                'Sweden', 'Switzerland')
        cnames = StringVar(value=playernames)
        player_info = {'ar':41000000, 'au':21179211, 'be':10584534, 'br':185971537, \
                'ca':33148682, 'cn':1323128240, 'dk':5457415, 'fi':5302000, 'fr':64102140, 'gr':11147000, \
                'in':1131043000, 'it':59206382, 'jp':127718000, 'mx':106535000, 'nl':16402414, \
                'no':4738085, 'es':45116894, 'se':9174082, 'ch':7508700}

        messagelog = ('Joe quit', 'Mararie entered the room')
        cmessagelog = StringVar(value=messagelog)
        # Messages we can send
        messages = { 'invite':'invite to play', 'refuse':'refuse to play'}

        # State variables
        gift = StringVar()
        sentmsg = StringVar()
        statusmsg = StringVar()

        # Called when the selection in the listbox changes; figure out
        # which player is currently selected, and then lookup its player
        # code, and from that, its population.  Update the status message
        # with the new population.  As well, clear the message about the
        # gift being sent, so it doesn't stick around after we start doing
        # other things.
        def showPopulation(*args):
            idxs = lbox.curselection()
            if len(idxs)==1:
                idx = int(idxs[0])
                code = playercodes[idx]
                name = playernames[idx]
                popn = player_info[code]
                statusmsg.set("Player %s (%s) has this info: %d" % (name, code, popn))
            sentmsg.set('')

        # Called when the user double clicks an item in the listbox, presses
        # the "Send Gift" button, or presses the Return key.  In case the selected
        # item is scrolled out of view, make sure it is visible.
        #
        # Figure out which player is selected, which gift is selected with the
        # radiobuttons, "send the gift", and provide feedback that it was sent.
        def sendGift(*args):
            idxs = lbox.curselection()
            if len(idxs)==1:
                idx = int(idxs[0])
                lbox.see(idx)
                name = playernames[idx]
                # Gift sending left as an exercise to the reader
                sentmsg.set("Sent %s to %s" % (messages[gift.get()], name))

        def quit(*args):
            idxs = lbox.curselection()
            if len(idxs)==1:
                idx = int(idxs[0])
                lbox.see(idx)
                name = playernames[idx]
                # Gift sending left as an exercise to the reader
                sentmsg.set("Quit")

        # Create and grid the outer content frame
        content = ttk.Frame(cfg.wroom) #, padding=(5, 5, 12, 0)) 		#Frame in cfg.wroom
        content.grid(column=0, row=0, sticky=(N,W,E,S))
        cfg.wroom.grid_columnconfigure(0, weight=1)
        cfg.wroom.grid_rowconfigure(0, weight=1)

        # Create the different widgets; note the variables that many
        # of them are bound to, as well as the button callback.
        # Note we're using the StringVar() 'cnames', constructed from 'playernames'
        lbox = Listbox(content, listvariable=cnames, height=5, bg = 'white')		#Listbox in content frame on the left
        namelbl = ttk.Label(content, text="Name")
        name = ttk.Entry(content, bg = 'white')
        name.insert(0, "Player 1")
        lbl = ttk.Label(content, text="Send to player:")	#Label on the right
        g1 = ttk.Radiobutton(content, text=messages['invite'], variable=gift, value='invite')
        g2 = ttk.Radiobutton(content, text=messages['refuse'], variable=gift, value='refuse')
        log = Listbox(content, listvariable=cmessagelog, height=5, bg = 'white')		#Listbox with messages
        ready = ttk.Button(content, text='Ready', command=sendGift, default='active', width='6')			#Button
        solitaire = ttk.Button(content, text='Solitaire', command=sendGift, default='active', width='6')		#Button
        quit = ttk.Button(content, text='Quit', command=quit, default='active', width='6')					#Button
        sentlbl = ttk.Label(content, textvariable=sentmsg, anchor='center')			#Label appearing below button
        status = ttk.Label(content, textvariable=statusmsg, anchor=W)				#Label on the bottom

        # Try treeview



        tree_header = ['Player', 'Status','Player No']
        tree = Treeview(content, show="headings", columns=('Player', 'Status','Player No'))

        tree_list = [('Aless', 'Ready',1),('Mararie','Ready',2),('Mary','Playing',3),('John','Playing',4),('Hugo', 'Playing',5),('Heleen', 'Playing',6),('Joe', 'Solitaire',7),('Casper', 'Idle',8),('Kiki', 'Idle',9)]

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

        def sortby(tree, col, descending):
            """sort tree contents when a column header is clicked on"""
            # grab values to sort
            data = [(tree.set(child, col), child) \
                for child in tree.get_children('')]
            # if the data to be sorted is numeric change to float
            #data =  change_numeric(data)
            # now sort the data in place
            data.sort(reverse=descending)
            for ix, item in enumerate(data):
                tree.move(item[1], '', ix)
            # switch the heading so it will sort in the opposite direction
            tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

        # Grid all the widgets
        tree.grid(column=0, row=0, rowspan=8, sticky=(N,S,E,W))
        _build_tree()

        #lbox.grid(column=0, row=0, rowspan=8, sticky=(N,S,E,W))
        namelbl.grid(column=1, row=0, columnspan=3, sticky=(N,W), padx=5)			#name Label
        name.grid(column=1, row=1, columnspan=3, sticky=(N,E,W), pady=5, padx=5)	#name Entry
        lbl.grid(column=1, row=2, columnspan=3, sticky=W, padx=10, pady=5) 		#Label "Send to player"
        g1.grid(column=1, row=3, columnspan=3, sticky=W, padx=20)		#RadioButton invite
        g2.grid(column=1, row=4, columnspan=3, sticky=W, padx=20)		#RadioButton refuse
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
        lbox.bind('<<ListboxSelect>>', showPopulation)
        lbox.bind('<Double-1>', sendGift)
        cfg.wroom.bind('<Return>', sendGift)

        # Colorize alternating lines of the player listbox
        for i in range(0,len(playernames),2):
            lbox.itemconfigure(i, background='lightblue')

        # Set the starting state of the interface, including selecting the
        # default gift to send, and clearing the messages.  Select the first
        # player in the list; because the <<ListboxSelect>> event is only
        # generated when the user makes a change, we explicitly call showPopulation.
        gift.set('invite')
        sentmsg.set('')
        statusmsg.set('')
        lbox.selection_set(0)
        showPopulation()

        #cfg.wroom.mainloop()
        """Start main loop for tkinter and Sixpodnet"""
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
            button.configure(bg = "green", relief='SUNKEN', activebackground="green")
        elif button.configure('bg')[4] == 'green':
            button.configure(bg = "white", relief='RAISED', activebackground="white")
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