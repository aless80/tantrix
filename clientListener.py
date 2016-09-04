from PodSixNet.Connection import ConnectionListener, connection
import config as cfg
import random

class ClientListener(ConnectionListener, object):
    def __init__(self):
        cfg.connection = connection

    def connect(self, host, port):
        self.Connect((host,int(port)))

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
        print("\nReceived by " + str(cfg.name) + " for " + command + ":\n  " + str(data))
        method = getattr(self, command)
        method(data)

    def receiveChat(self, data):
        msgList = data['msgList']
        self.addToMessageLog(msgList, fg = 'black')

    def updateTreeview(self, data):
        """receive updates about the connections. Rebuild the treeview"""
        #print("\nupdateTreeview in " + str(cfg.connectionID))
        #Clear the Treeview on the wroom
        if cfg.wroominstance.tree is None:
            return #protect from error if wroom was closed
        map(self.tree.delete, self.tree.get_children())
        tree_list = data['listVal']
        self.buildTree(tree_list)

    def clientIsConnected(self, data):
        """Server confirmed to the player that they have connected"""
        cfg.connectionID = data["addr"]
        """Set the player name in the waiting room"""
        if cfg.name is not '':
            self.sendChangedName(cfg.name)
        else:
            cfg.name = data['yourname']
            self.nameentry.insert(0, cfg.name)
        """Set the player color"""
        cfg.playercolor = data["color"]
        self.colorframe.configure(bg = cfg.playercolor)

    def startgame(self, data):
        """Start a game"""
        """If server found that player colors are the same, display a dialog and set ready to idle"""
        if cfg.playercolor == data["opponentcolor"]:
            if data["changecolor"]:
                self.toggleReadyForGame()
                msg = "Attempted to start a game with " + data["opponentname"]
                msg += " but one player has to change color. Please choose different colors and get ready again"
                msgList = [msg]
                self.addToMessageLog(msgList, fg = 'cyan')
                return
        """Store information from server"""
        #self.quit = False
        cfg.player_num = data["player_num"]
        cfg.gameid = data["gameid"]
        cfg.opponentname = data["opponentname"]
        cfg.playerIsTabUp = data["playerIsTabUp"]
        cfg.wroominstance.tree = None
        cfg.opponentcolor = data["opponentcolor"]
        """Create a new random number generator"""
        cfg.rndgen = random.Random(data["seed"])
        cfg.history.append([cfg.name + " pl" + str(cfg.player_num), "Seed=" + str(data["seed"])])
        """Start the game"""
        self.keepLooping = False

    def hasquit(self, data):
        """Another player has quit the waiting room"""
        #Show alert only during game mode
        #TODO selfgameinprogress fails when somebody quits wroom.
        """if self.gameinprogress: #self is WaitingRoom
            import tkMessageBox
            tkMessageBox.showwarning("Notification", "Player has quit!")
        """
        """Remove player from tree"""
        if cfg.wroominstance.tree is None:
            return #protect from error if wroom was closed
        name = data['quitterName']
        if cfg.wroominstance.searchTreeByHeader(name, header = 'Player') is None:
            print("\n    Error in hasquit: could not find quitter from tree!")
        cfg.wroominstance.removeFromTree(name)
        """Add message to logbox"""
        quitterName = data['quitterName']
        msgList = [quitterName + " has quit"]
        self.addToMessageLog(msgList, fg = 'cyan')

    def hastoggledready(self, data):
        """Players have toggled ready. Add message to logbox"""
        player = data['player']
        ready = data['ready']
        convert_status = {0: "Idle", 1: "Ready"}
        msgList = ["%s has become %s" % (player, convert_status[ready])]
        self.addToMessageLog(msgList, fg = 'cyan')

    def hasstartedgame(self, data):
        """Players have started a game or a solitaire
        Add message to logbox"""
        gametype = data['gametype']
        player1 = data['player1']
        if gametype == 'Game':
            player2 = data['player2']
            msgList = ["New game for %s and %s" % (player1, player2)]
        else:
            msgList = ["%s has started a solitaire" % player1]
        self.addToMessageLog(msgList, fg = 'cyan')

    def refusedNewname(self, data):
        self.changeName(data['name'])

    """Methods that send to server"""
    def playConfirmedMove(self, data):
        rowcolnum = data["rowcolnum"]   #Destination [coord,coord,tile number]
        rowcoltab1 = data["rowcoltab1"] #Origin [coord,coord,tab as -1,0,-2]
        rowcoltab2 = data["rowcoltab2"] #Destination [coord,coord,tab as -1,0,-2]
        angle = data["angle"]     #angle of the tile
        ###TODO - can skip? I think so. also rowcoltab1
        turnUpDown = data['turnUpDown']
        ###
        """Correct received move with current shifts"""
        rowcoltab2 = (rowcoltab2[0] + cfg.shifts[0] * 2, rowcoltab2[1] + cfg.shifts[1], rowcoltab2[2])
        """Reset, move automatically, confirm locally"""
        cfg.deck.reset()
        cfg.deck.move_automatic(rowcoltab1, rowcoltab2, angle)
        self.buttonConfirm(send = False, force = True) #Here post_confirm increases turnUpDown
        #cfg.deck.confirm_move(send = False)

    def sendSolitaire(self):
        self.send_to_server("solitaire")
        #cfg.solitaire = True #Note: already set in waitingRoom.solitaire
        cfg.wroominstance.tree = None

    def sendChangedName(self, newname):
        self.send_to_server("name", newname = newname)

    def sendChangedColor(self, newcolor):
        self.send_to_server("color", newcolor = newcolor)

    def sendToggleReady(self):
        self.send_to_server("toggleReady")

    def sendChatToAll(self, msgList):
        self.send_to_server("chat", msgList = msgList)

    def send_to_server(self, action, **dict):
        """Allow Client to send to Server (server.ClientChannel.Network_<action>)
        Include the sender, gameid and default action"""
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

