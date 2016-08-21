from PodSixNet.Connection import ConnectionListener, connection
import config as cfg

class ClientListener(ConnectionListener):
    def __init__(self):
        cfg.connection = connection

    def connect(self):
        self.Connect()

    def mainloop(self):
        """This is the polling loop during the game"""
        while self.running:
            """Polling loop for the client. asks the connection singleton for any new messages from the network"""
            cfg.connection.Pump()   #Polling loop for the client.
            """Server"""
            self.Pump()             #Server
            """Update the boards"""
            cfg.win.update()
            cfg.win.update_idletasks()
            #cfg.gui_instance.send_to_server
        """Notify server that this instance is quitting"""
        self.send_to_server("quit", orig = "Gui.main")
        cfg.connection.Pump()

    def Network_clientListener(self, data):
        """Listen to all messages wtih action=clientListener sent from server
        Then dispatch to the method based on the command sent"""
        #data.pop("action") #Does not preserve order
        command = data.pop('command')
        action = data.pop('action')
        print("\nReceived by " + str(cfg.connectionID1) + " for " + command + ":\n  " + str(data))
        method = getattr(self, command)
        method(data)

    def startgame(self, data):
        """Called from server.Connected"""
        self.keepLooping = False
        #self.quit = False
        cfg.player_num = data["player_num"]
        cfg.gameid = data["gameid"]

    def playConfirmedMove(self, data):
        rowcolnum = data["rowcolnum"]
        rowcoltab1 = data["rowcoltab1"]
        rowcoltab2 = data["rowcoltab2"]
        cfg.deck.reset()
        cfg.deck.move_automatic(rowcoltab1, rowcoltab2)
        self.buttonConfirm(send = False)
        #cfg.deck.confirm_move(send = False)

    #def playConfirmedMove(self, data):
    #    print("\n\nplayConfirmedMove")
    #    print(data)
    #    cfg.deck.confirm_move(send = False)

    def hasquit(self, data):
        import tkMessageBox
        tkMessageBox.showwarning("Notification", "Player has quit!")

    def disconnected(self, data):
        print("\n\n\nDisconnected from the server!")
        #TODO

    def Network_error(self, data):
        print "error:", data['error'][1]
        #TODO

    def players(sefl, data):
        """update gui element displaying the number of currently connected players"""
        [cfg.players.append(p) for p in data["addresses"] if p not in cfg.players]
        #print("Players are: {}".format(str(data["num"])))
        listtolog = ["Number of players is %s" % str(data["num"])]
        """Add a line to the log listbox"""
        cfg.wroominstance.addToMessageLog(listtolog)
        for newaddr in data['newaddr']:
            #TODO check if it exists! implement num in server, status, etc
            #TODO rm client from server's list when needed
            name_num_status = [newaddr[1],666,"Idle"]
            cfg.wroominstance.addToTree(name_num_status)

    def clientIsConnected(self, data):
        cfg.connectionID = data["addr"]
        cfg.connectionID1 = data["addr"][1]
        """Set the player name in the waiting room"""
        frame = cfg.wroom.winfo_children()[0]
        nameentry = frame.children["nameentry"]
        nameentry.insert(0, "Player " + str(cfg.connectionID[1]))

    def send_to_server(self, action, **dict):
        '''Allow Client to send to Server (server.ClientChannel.Network_<action>)'''
        data = {"action": "serverListener", "command": action, "gameid": cfg.gameid, "sender": cfg.connectionID, "orig": "Server.send_to_server"}
        """Add key-value pairs in dict to data dictionary"""
        for kw in dict:
            data[kw] = dict[kw]
        """Send data to server"""
        cfg.connection.Send(data)
        datacp = data.copy()
        datacp.pop('action')  #serverListener
        command = datacp.pop('command')
        print("\nSent for " + command + ":  " + str(data))

