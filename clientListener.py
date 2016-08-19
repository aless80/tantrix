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
            self.Pump()         #Server
            """Update the boards"""
            cfg.win.update()
            cfg.win.update_idletasks()
            #cfg.gui_instance.send_to_server
        """Notify server that this instance is quitting"""
        self.send_to_server("quit", orig = "Gui.main")
        cfg.connection.Pump()

    def Network_test(self, data):
        print("\nReceiving in Gui.test():  \n" + str(data))

    def Network_startgame(self, data):
        """Called from server.Connected"""
        print("\nReceiving in Gui.Network_startgame():\n  " + str(data))
        self.pumpit = False
        #self.quit = False
        cfg.player_num = data["player_num"]
        cfg.gameid = data["gameid"]

    def Network_confirm(self, data):
        print("\nReceiving in Gui.Network_confirm():  " + str(data))
        """Get attributes"""
        rowcolnum = data["rowcolnum"]
        rowcoltab1 = data["rowcoltab1"]
        rowcoltab2 = data["rowcoltab2"]
        cfg.deck.reset()
        cfg.deck.move_automatic(rowcoltab1, rowcoltab2)
        self.buttonConfirm(send = False)
        #cfg.deck.confirm_move(send = False)

    def Network_hasquit(self, data):
        print("\nReceiving in Gui.Network_haasquit():  " + str(data))
        import tkMessageBox
        tkMessageBox.showwarning("Notification", "Player has quit!")

    def Network_disconnected(self, data):
        print "disconnected from the server"
        #TODO

    def Network_error(self, data):
        print "error:", data['error'][1]
        #TODO

    def Network_numplayers(sefl, data):
        # update gui element displaying the number of currently connected players
        print("\nReceiving in Gui.Network_numplayers():  " + str(data))
        #data = {"action": "numplayers", "players": dict([(c.players, c.addr) for c in self.allConnections])}
        [cfg.players.append(p) for p in data["players"] if p not in cfg.players]
        print("Players are: {}".format(str(len(cfg.players))))

    def Network_roger(self, data):
        print("\nReceiving in Gui.Network_roger():  " + str(data))
        cfg.connectionID = data["addr"]

    def send_to_server(self, action, **dict):
        '''Allow Client to send to Server (server.ClientChannel.Network_<action>)'''
        data = {"action": action, "gameid": cfg.gameid, "sender": cfg.connectionID, "orig": "Server.send_to_server"}
        """Add key-value pairs in dict to data dictionary"""
        for kw in dict:
            data[kw] = dict[kw]
        """Send data to server"""
        print("\nSending to server:  " + str(data))
        cfg.connection.Send(data)
