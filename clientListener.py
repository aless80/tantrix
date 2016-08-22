from PodSixNet.Connection import ConnectionListener, connection
import config as cfg

class ClientListener(ConnectionListener, object):
    def __init__(self):
        cfg.connection = connection

    def connect(self):
        self.Connect()

    def mainloop(self):
        """This is the polling loop during the game"""
        while self.gameinprogress: #Note: self is Gui instance
            """Polling loop for the client. asks the connection singleton for any new messages from the network"""
            cfg.connection.Pump()   #Polling loop for the client.
            """Server"""
            self.Pump()             #Server
            """Update the boards"""
            cfg.win.update()
            cfg.win.update_idletasks()
            #cfg.gui_instance.send_to_server
        """Notify server that this instance is quitting"""
        self.send_to_server("quit")
        cfg.connection.Pump()

    def Network_clientListener(self, data):
        """Listen to all messages wtih action=clientListener sent from server
        Then dispatch to the method based on the command sent"""
        command = data.pop('command')
        action = data.pop('action')     #"clientListener"
        print("\nReceived by " + str(cfg.connectionID1) + " for " + command + ":\n  " + str(data))
        method = getattr(self, command)
        method(data)

    def startgame(self, data):
        """Called from server.Connected"""
        self.keepLooping = False
        #self.quit = False
        cfg.player_num = data["player_num"]
        cfg.gameid = data["gameid"]
        cfg.wroominstance.tree = None



    def updateTreeview(self, data):
        print("\nupdateTreeview")
        #Clear the Treeview on the wroom
        if cfg.wroominstance.tree is None: return #protect from error if wroom was closed
        map(self.tree.delete, self.tree.get_children())
        tree_list = data['listVal']
        self.buildTree(tree_list)

    def playConfirmedMove(self, data):
        rowcolnum = data["rowcolnum"]
        rowcoltab1 = data["rowcoltab1"]
        rowcoltab2 = data["rowcoltab2"]
        cfg.deck.reset()
        cfg.deck.move_automatic(rowcoltab1, rowcoltab2)
        self.buttonConfirm(send = False)
        #cfg.deck.confirm_move(send = False)

    def hasquit(self, data):
        """Another player has quit"""
        #Show alert only during game mode
        #bug: when another player comes back from solitaire, self.gameinprogress is not present
        """#TODO fix below. self is bad
        print(">hasquit: self and super(ClientListener,self) are:")
        print(self) #waitingroom. why???
        #print(super(ClientListener,self)) #does not work
        if self.gameinprogress: #self is WaitingRoom
            import tkMessageBox
            tkMessageBox.showwarning("Notification", "Player has quit!")
        """
        """Remove player from tree"""
        if cfg.wroominstance.tree is None: return #protect from error if wroom was closed
        name = data['quitterName']
        if cfg.wroominstance.searchTreeByHeader(name, header = 'Player') is None:
            print("\n    Error in hasquit: could not find quitter from tree!")
        cfg.wroominstance.removeFromTree(name)

    def disconnected(self, data):
        print("\n\n\nDisconnected from the server!")
        #TODO

    def newPlayer(sefl, data):
        """Update gui element with a new player and display the current number of players"""
        #[cfg.players.append(p) for p in data["addresses"] if p not in cfg.players]
        newaddr = data['newaddr']
        cfg.players.append(newaddr)
        """Add a line to the log listbox"""
        listtolog = ["Number of players is %s" % str(data["total"])]
        cfg.wroominstance.addToMessageLog(listtolog)
        """Add new player"""
        for i, addr in enumerate(data['addresses']):
            name = data['names'][i]
            if cfg.wroominstance.searchTreeByHeader(name, header = 'Player') is None:
                valList = [name, "Idle", addr[1]]
                cfg.wroominstance.tree.insert('', 'end', values = valList)

    def nameChanged(sel, data):
        print("nameChanged")
        print(data)
        sender = data['sender']
        newname = data['newname']
        #"sender", "newname"
        item = cfg.wroominstance.searchTreeByHeader(sender[1], header = 'Address')
        cfg.wroominstance.editItemInTree(item, valList = [newname], headerList = ['Player'])
        print(item)
        #TODO

    def clientIsConnected(self, data):
        cfg.connectionID = data["addr"]
        cfg.connectionID1 = data["addr"][1]
        """Set the player name in the waiting room"""
        frame = cfg.wroom.winfo_children()[0]
        nameentry = frame.children["nameentry"]
        nameentry.insert(0, "Player " + str(cfg.connectionID[1]))

    def send_to_server(self, action, **dict):
        '''Allow Client to send to Server (server.ClientChannel.Network_<action>)
        Include the sender, gameid and default action'''
        data = {"action": "serverListener", "command": action, "gameid": cfg.gameid, "sender": cfg.connectionID}
        """Add key-value pairs in dict to data dictionary"""
        for kw in dict:
            data[kw] = dict[kw]
        """Send data to server"""
        cfg.connection.Send(data)
        datacp = data.copy()
        datacp.pop('action')  #serverListener
        command = datacp.pop('command')
        print("\nSent for " + command + ":  " + str(datacp))

