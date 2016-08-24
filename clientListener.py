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

    """Methods that listen to server"""
    def Network_clientListener(self, data):
        """Listen to all messages wtih action=clientListener sent from server
        Then dispatch to the method based on the command sent"""
        command = data.pop('command')
        action = data.pop('action')     #"clientListener"
        print("\nReceived by " + str(cfg.connectionID1) + " for " + command + ":\n  " + str(data))
        method = getattr(self, command)
        method(data)

    def updateTreeview(self, data):
        print("\nupdateTreeview in " + str(cfg.connectionID))
        #Clear the Treeview on the wroom
        if cfg.wroominstance.tree is None:
            return #protect from error if wroom was closed
        map(self.tree.delete, self.tree.get_children())
        tree_list = data['listVal']
        self.buildTree(tree_list)

    def clientIsConnected(self, data):
        """Server confirmed to the player that they have connected"""
        cfg.connectionID = data["addr"]
        cfg.connectionID1 = data["addr"][1]
        """Set the player name in the waiting room"""
        frame = cfg.wroom.winfo_children()[0]
        nameentry = frame.children["nameentry"]
        if cfg.name is not '':
            self.sendChangedName(cfg.name)
        else:
            cfg.name = "Player" + str(cfg.connectionID[1])
            nameentry.insert(0, cfg.name)

    def startgame(self, data):
        """Called from server.Connected"""
        self.keepLooping = False
        #self.quit = False
        cfg.player_num = data["player_num"]
        cfg.gameid = data["gameid"]
        cfg.opponentname = data["opponentname"]
        cfg.wroominstance.tree = None

    def hasquit(self, data):
        """Another player has quit"""
        #Show alert only during game mode
        if self.gameinprogress: #self is WaitingRoom
            import tkMessageBox
            tkMessageBox.showwarning("Notification", "Player has quit!")
        """Remove player from tree"""
        if cfg.wroominstance.tree is None:
            return #protect from error if wroom was closed
        name = data['quitterName']
        if cfg.wroominstance.searchTreeByHeader(name, header = 'Player') is None:
            print("\n    Error in hasquit: could not find quitter from tree!")
        cfg.wroominstance.removeFromTree(name)


    """Methods that send to server"""
    def playConfirmedMove(self, data):
        rowcolnum = data["rowcolnum"]   #Destination [coord,coord,tile number]
        rowcoltab1 = data["rowcoltab1"] #Origin [coord,coord,tab as -1,0,-2]
        rowcoltab2 = data["rowcoltab2"] #Destination [coord,coord,tab as -1,0,-2]
        rotation = data["rotation"]     #rotation of tile
        ###TODO
        turnUpDown = data['turnUpDown']
        print("\n\n       >>>>>>> cfg.turn now becomes " + str(turnUpDown))
        ###
        cfg.deck.reset()
        cfg.deck.move_automatic(rowcoltab1, rowcoltab2, rotation)
        self.buttonConfirm(send = False) #Here post_confirm increases turnUpDown
        #cfg.deck.confirm_move(send = False)

    def sendSolitaire(self):
        self.send_to_server("solitaire")
        #cfg.solitaire = True #Note: already set in waitingRoom.solitaire
        cfg.wroominstance.tree = None

    def sendChangedName(self, newname):
        self.send_to_server("name", newname = newname)

    def sendToggleReady(self):
        self.send_to_server("toggleReady")

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

