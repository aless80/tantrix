import sys
#sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
sys.path.insert(0, './PodSixNet')
from PodSixNet.Channel import Channel
#import PodSixNet.Server
from PodSixNet.Server import Server
from time import sleep


class ClientChannel(Channel):
    """Receive messages from client.
    NB: self._server refers to tantrixServer ie the instance of TantrixServer"""
    def Network_serverListener(self, data):
        command = data.pop('command')
        data.pop('action')
        print("\nReceiving for " + command + ":\n  " + str(data))
        method = getattr(self, command)
        method(data)

    def test(self, data):
        """Print the remaining connections"""
        print("\n" + str(self._server.allConnections))
        self._server.sendUpdateTreeview()

    def chat(self, msgList):
        print("\nchat:")
        print(msgList)

    def solitaire(self, data):
        """Mark players who are going solitaire in allConnections"""
        for ind in range(self._server.allConnections.count()):
            if not self._server.allConnections.addr[ind] == data['sender']:
                continue
            else:
                self._server.allConnections.ready[ind] = -2
                self._server.allConnections.ready[ind] = -2
        self._server.sendUpdateTreeview()

    def toggleReady(self, data):
        addr = data["sender"]
        #print("\nReceiving in server.ClientChannel.Network_toggleReady() from player {}:\n  {}".format(str(addr), str(data)))
        self._server.allConnections.toggleReadyFromAddr(addr)
        self._server.checkConnections()
        self._server.sendUpdateTreeview()
        """Print the remaining connections"""
        print("\n" + str(self._server.allConnections))
        #TODO send to all players that player has toggled ready
        #self._server.sendToPlayer

    def confirm(self, data):
        #deconsolidate all of the data from the dictionary
        rowcolnum = data["rowcolnum"]
        #player number (1 or 0)
        sender = data["sender"]
        #tells server to place line
        data['action'] = "clientListener"
        data['command'] = "playConfirmedMove"
        self._server.placeMove(rowcolnum, data, data["gameid"], sender)

    def name(self, data):
        """Name changed"""
        sender = data["sender"]
        newname = data["newname"]
        self._server.updateName(sender, newname)

    def quit(self, data):
        """One player has quit"""
        quitter = data['sender']
        """Tell other players that one has quit. Must do it inside TantrixServer"""
        self._server.tellToQuit(data)
        """Delete the quitter from allConnections"""
        self._server.allConnections.removeConnection(quitter)
        #"""Print the remaining connections"""
        #print("\n" + str(self._server.allConnections))
        self._server.sendUpdateTreeview()
      


class TantrixServer(Server):
    """Send message to clients"""
    channelClass = ClientChannel  #needed!

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.gameIndex = 0
        self.allConnections = WaitingConnections()




    def sendUpdateTreeview(self):
        listVal = self.allConnections.getAsList()
        data = {"action": "clientListener", "command": "updateTreeview", "listVal": listVal}
        self.sendToAllWRoom(data)



    def checkConnections(self):
        """Check if there are 2 connection ready. in that case start the games"""
        print("\n" + str(self.allConnections))
        """Check if at least two players are ready"""
        players_ready = 0
        ind_game = []
        for ind in range(self.allConnections.count()):
            if self.allConnections.ready[ind] == 1:
                players_ready += 1
                tempind = ind
                ind_game.append(ind)
        #TODO: currently the first two players who are ready will start the game
        if players_ready < 2:
            return
        else:
            self.sendStartgame(ind_game)

    def sendStartgame(self, ind_game):
        """Initialize a game with two players"""
        self.gameIndex += 1  #TODO Needed? I think so
        game = Game(self.allConnections.players[ind_game[0]], self.gameIndex)
        """Add all players to game"""
        game.addPlayer(self.allConnections.players[ind_game[1]])
        """Start the game. Add game to both connections (self.allConnections.game), set ready = -1"""
        for ind in ind_game:
            self.allConnections.addGame(game, self.allConnections.addr[ind])
            self.allConnections.ready[ind] = -1
        self.doSendStartingGame(ind_game)


    def Connected(self, player, addr):
        """self.game  contains the array .players"""
        print("\nReceiving in server.TantrixServer.Connected:")
        print("  new connection: channel = {},address = {}".format(player, addr))
        """Create or edit a game""" #TODO move this once players in wroom confirm each other
        if not self.allConnections.game:
            self.gameIndex += 1
        name = "Player" + str(addr[1])
        self.allConnections.addConnection(player, addr, 0, name = name)
        """Send confirmation that client has connected. send back the client's address"""
        data = {"action": "clientListener", "command": "clientIsConnected", "addr": addr}
        self.sendToPlayer(player, data)
        """Send an update to Treeview"""
        self.sendUpdateTreeview()

    def sendToAllWRoom(self, data):
        """Send to all players that are in wroom, ie are not playing"""
        [self.sendToPlayer(self.allConnections.players[ind], data) for ind in range(self.allConnections.count()) if self.allConnections.ready >= 0]

    def sendToPlayer(self, player, data):
        player.Send(data)
        #Print to terminal
        datacp = data.copy() #so that I can edit it
        name = self.allConnections.getNameFromPlayer(player)
        datacp.pop('action')
        command = datacp.pop('command')
        print("\nSent to " + name + " for " + command + ":  " + str(datacp))
        #TODO merge with clientIsConnected?

    def doSendStartingGame(self, ind_game):
        playernames = [self.allConnections.name[j] for j in ind_game]
        for i, ind in enumerate(ind_game):
            """Get the opponent's name"""
            playernamescp = list(playernames)
            playernamescp.pop(i) #because there are two players
            opponentname = playernamescp[0]
            """Send stargame"""
            data = {"action": "clientListener", "command": "startgame", "player_num": i+1, #edited cfg.player_num in tantrix11.1. it was i
                 "gameid": self.allConnections.game[ind].gameid, "opponentname": opponentname, "playerIsTabUp": i==0}
            self.sendToPlayer(self.allConnections.players[ind], data)

    def placeMove(self, rowcolnum, data, gameid, sender): #TODO gameid not needed as argument
        game = self.allConnections.getGameFromAddr(sender)
        #data['turnUpDown'] = data['turnUpDown'] + 1
        game.placeLine(rowcolnum, data, sender)

    def tellToQuit(self, data):
        quitter = data["sender"]
        ind = self.allConnections.addr.index(quitter)
        dataAll = {"action": "clientListener", "command": "hasquit", "quitter": quitter,
                   "quitterName": self.allConnections.name[ind]}
        for i in range(self.allConnections.count()):
            if i != ind and self.allConnections.game[i] == self.allConnections.game[ind]:
                p = self.allConnections.players[i]
                a = self.allConnections.addr[i]
                n = self.allConnections.name[i]
                print("\nSending to client {}:\n  {}".format(n, str(dataAll)))
                p.Send(dataAll)

    def updateName(self, sender, newname):
        '''for ind in range(self.allConnections.count()):
            datanew = {"action": "clientListener", "command": "nameChanged",
                 "sender": sender, "newname": newname}
            name = self.allConnections.name[ind]
            print("\n-Sent to " + name + " for " + "nameChanged" + ":  " + str(datanew)) #todo improve all these prints
            self.allConnections.players[ind].Send(datanew)
            tantrixServer.Pump()
        '''
        """Edit name stored in allConnection"""
        index = self.allConnections.getIndexFromAddr(sender)
        self.allConnections.name[index] = newname
        """Send update to all in Waiting Room"""
        self.sendUpdateTreeview()

class Game:
    def __init__(self, player, gameIndex):
        # whose turnUpDown (1 or 0)
        self.turn = 1
        #Storage
        self._confirmedgame = []
        #initialize the players including the one who started the game
        self.players = []
        self.addPlayer(player)
        #gameid of game
        self.gameid = gameIndex

    def __str__(self):
        string= str(self.gameid)
        return string

    def addPlayer(self, player):
        if player is not None and player not in self.players:
            self.players.append(player)
        else:
            print("Game.addPlayer failed: player is None or was already added")

    def placeLine(self, rowcolnum, data, sender):
        #make sure it's their turnUpDown TODO
        turnUpDown = data['turnUpDown']
        if self.turn is not turnUpDown:
            print("       \n\n>>>>>>>>>>placeLine: self.turn is not data['turnUpDown']: {}~={}".format(self.turn, turnUpDown))
        self.turn += 1
        data['turnUpDown'] =self.turn
        print("       \n\n>>>>>>>>self.turnUpDown="+str(self.turn) + "\n\n")
        ####
        if 1 or sender == self.turn + 1: #TODO
            self.turn = 0 if self.turn else 1
            #place line in game
            self._confirmedgame.append(rowcolnum)
            #send data and turnUpDown to the opponent
            #TODO mv everythiong to TantrixServer
            opponents = tantrixServer.allConnections.getOpponentsFromAddress(sender)
            for o in opponents:
                print("\nSending to other player:\n  " + str(data))
                o.Send(data)

class WaitingConnections:
    def __init__(self):
        """Initialize the players"""
        self.players = []
        self.addr = []
        self.game = []
        self.ready = []
        self.name = []

    def getAsList(self):
        """Return the connections as list for Treeview in wroom eg:
        [('Alessandro', 0, 43932, None),('Mararie', -1, 2, 1), ..] """
        return [list([self.name[ind], self.ready[ind], self.addr[ind][1], str(self.game[ind])]) for ind in range(self.count())]


    def addConnection(self, player, addr, ready = 0, game = None, name = "unknown"):
        self.players.append(player)
        self.addr.append(addr)
        self.ready.append(ready)
        self.game.append(game)
        self.name.append(name)

    def addGame(self, game, addr):
        ind = self.addr.index(addr)
        self.game[ind] = game

    def removeConnection(self, addr):
        ind = self.addr.index(addr)
        self.addr.pop(ind)
        self.players.pop(ind)
        self.game.pop(ind)
        self.ready.pop(ind)
        self.name.pop(ind)

    def count(self):
        return len(self.players)

    def getIndexFromAddr(self, addr):
        return self.addr.index(addr)

    def getGameFromPlayer(self, player):
        ind = self.players.index(player)
        return self.game[ind]

    def getNameFromPlayer(self, player):
        ind = self.players.index(player)
        return self.name[ind]

    def getGameFromAddr(self, addr):
        ind = self.addr.index(addr)
        return self.game[ind]

    def getPlayerFromAddr(self, addr):
        ind = self.addr.index(addr)
        return self.players[ind]

    def getOpponentsFromAddress(self, addr):
        """Given a player, return a list of players in the game"""
        game = self.getGameFromAddr(addr)
        ind_sender = self.getIndexFromAddr(addr)
        opponents = []
        for ind in range(self.count()):
            if ind != ind_sender and self.game[ind] == game:
                opponents.append(self.players[ind])
        return opponents
        #return [x for i, x in enumerate(self.players) if x == player and self.addr[i] is not addr]

    def toggleReadyFromAddr(self, addr):
        """Toggle ready flag"""
        try:
            ind = self.addr.index(addr)
        except:
            import inspect
            print("Unexpected error at :", inspect.stack()[0][3])
            print("addr="+ str(addr) + " is not contained in self.addr="+ str(self.addr))
            raise
        self.ready[ind] = (self.ready[ind] + 1) %2

    def __str__(self):
        string = "Connections:\n<======================"
        string += "\nname, ready, addr, players, game:\n"
        for ind in range(self.count()):
            string += "{}, {}, {}, {}, {}\n".format(
                str(self.name[ind]),
                str(self.ready[ind]),
                str(self.addr[ind]),
                str(self.players[ind]),
                str(self.game[ind]))
        string += "======================>\n"
        return string

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
    #Launch anyway
    host = "localhost"
    port = 31425
    print("Launcing with host, port = %s , %d" % (host, port))
else:
    host, port = sys.argv[1].split(":")

print("STARTING SERVER ON LOCALHOST")
tantrixServer = TantrixServer(localaddr=(host, int(port)))  #'localhost', 1337
while True:
    tantrixServer.Pump()
    sleep(0.01)

