import sys
#sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
sys.path.insert(0, './PodSixNet')
from PodSixNet.Channel import Channel
#import PodSixNet.Server
from PodSixNet.Server import Server
from time import sleep


class ClientChannel(Channel):

    def Network(self, data):
        '''Allow Server to get recipient of .Send from Client'''
        print("\nReceiving in server.ClientChannel.Network() from player :\n  " + str(data))

    def Network_myaction(self, data):
        print("\nReceiving in server.ClientChannel.Network_myaction() from player :\n  " + str(data))

    def Network_waiting(self, data):
        print("\nReceiving in server.ClientChannel.Network_waiting() from player :\n  " + str(data))

    def Network_quit(self, data):
        """One player has quitted"""
        print("\nReceiving in server.ClientChannel.Network_quit() from player :\n  " + str(data))
        player = data['sender']
        #queue = tantrixServer.allConnections.getGameFromPlayer(player)
        opponents = tantrixServer.allConnections.getOpponentsFromAddress(player)
        tantrixServer.allConnections.removeConnection(player)
        #TODO tell the other player to quit
        if len(opponents): #checking is not necessary
            self._server.tellToQuit(opponents, data)



    def Network_confirm(self, data):
        print("--server.ClientChannel.Network_confirm()", data)
        #deconsolidate all of the data from the dictionary
        rowcolnum = data["rowcolnum"]
        #player number (1 or 0)
        sender = data["sender"]
        #id of game given by server at start of game
        #self.gameid = data["gameid"]
        #change the origin to this server
        data["orig"] = "server.ClientChannel.Network_confirm"
        #tells server to place line
        self._server.placeLine(rowcolnum, data, data["gameid"], sender)



class TantrixServer(Server):
    channelClass = ClientChannel  #needed!

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        #self.games = []
        #self.game = None
        self.currentIndex = 0
        self.allConnections = WaitingConnections()

    def tellToQuit(self, opponents, data):
        #TODO opponents is list of players
        quitter = data["sender"]
        dataAll = {"action": "hasquit", "quitter": quitter,
                   #"gameid": self.allConnections.getGameFromPlayer(opponents[0]).gameid,
                   "orig": "Server.TantrixServer.tellToQuit"}
        for p in opponents:
            print("\nSending to client {}:\n  {}".format(str(p), str(dataAll)))
            p.Send(dataAll)

    def SendToAll(self, data):
		    #[p.Send(data) for p in self.players]
        1

    def Connected(self, player, addr):
        """self.game  contains the array .players"""
        print("\nReceiving in server.TantrixServer.Connected:")
        print("  new connection: channel = {},address = {}".format(player, addr))
        """create or edit a game""" #TODO move this once players in wroom confirm each other
        if not self.allConnections.game:
            self.currentIndex += 1
            tempqueue = Game(player, self.currentIndex) #TODO I do not want this
            tempqueue.gameid = self.currentIndex #TODO I do nto want this now.
            print("  self.currentIndex={}, player.gameid={}, tempqueue={}".format(str(self.currentIndex), str(tempqueue.gameid), str(tempqueue)))
            """roger that 1st client has connected. send back the client's address"""
            data0 = {"action": "roger", "addr": addr, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to client:\n  " + str(data0))
            self.allConnections.addConnection(player, addr, tempqueue)
            player.Send(data0)
        else:
            self.allConnections.addConnection(player, addr, self.allConnections.game[0])
            """roger that 2nd client has connected. send back the client's address"""
            data1 = {"action": "roger", "addr": addr, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to client:\n  " + str(data1))
            player.Send(data1)
            """start game"""
            self.startgameForQueue()
        """Send the number of players to all"""
        #note: not able to send game
        data = {"action": "numplayers", "orig": "Server.TantrixServer.Connected",
                "players": [self.allConnections.addr[c] for c in range(self.allConnections.count())]}
        for p in self.allConnections.players:
            p.Send(data)

    def startgameForQueue(self):
            data0 = {"action": "startgame", "player_num":1, "gameid": self.allConnections.game[0].gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 1:\n  " + str(data0))
            self.allConnections.players[0].Send(data0)
            data1 = {"action": "startgame", "player_num":2, "gameid": self.allConnections.game[1].gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 2:\n  " + str(data1))
            self.allConnections.players[1].Send(data1)

    def placeLine(self, rowcolnum, data, gameid, sender):
        game = self.allConnections.getGameFromAddr(sender)
        game.placeLine(rowcolnum, data, sender)


class WaitingConnections:
    def __init__(self): #, currentIndex):
        #initialize the players including the one who started the game
        self.players = []
        self.addr = []
        self.game = []

    def addConnection(self, player, addr, game):
        self.players.append(player)
        self.addr.append(addr)
        self.game.append(game)

    def removeConnection(self, addr):
        ind = self.addr.index(addr)
        self.addr.pop(ind)
        self.players.pop(ind)
        self.game.pop(ind)

    def count(self):
        return len(self.players)

    def getGameFromPlayer(self, player):
        ind = self.players.index(player)
        return self.game[ind]

    def getGameFromAddr(self, addr):
        ind = self.addr.index(addr)
        return self.game[ind]

    def getPlayerFromAddr(self, addr):
        ind = self.addr.index(addr)
        return self.players[ind]

    def getOpponentsFromAddress(self, addr):
        """Given a player, return a list of players in the game"""
        player = self.getPlayerFromAddr(addr)
        return [x for i, x in enumerate(self.players) if x == player and self.addr[i] is not addr]

    def __str__(self):
        for ind in range(self.count):
            print("{},{},{}".format(str(self.players[ind]), str(self.addr[ind]), str(self.game[ind])))


class Game:
    def __init__(self, player, currentIndex):
        # whose turn (1 or 0)
        self.turn = 1
        #Storage
        self._confirmedgame = []
        #initialize the players including the one who started the game
        self.players = []
        self.players.append(player)
        #gameid of game
        self.gameid = currentIndex

    def addPlayer(self, player):
        self.players.append(player)

    def placeLine(self, rowcolnum, data, sender):
        #make sure it's their turn TODO
        if 1 or sender == self.turn + 1: #todo
            self.turn = 0 if self.turn else 1
            #place line in game
            self._confirmedgame.append(rowcolnum)
            #send data and turn data to each player
            if sender == tantrixServer.allConnections.addr[0]: #todo: only connections in the current game!
                self.players[1].Send(data)
                print("\nSending to other player:")
                print("  " + str(data))
            elif sender == tantrixServer.allConnections.addr[1]:
                self.players[0].Send(data)
                print("\nSending to other player: ")
                print("  " + str(data))
            else:
                raise UserWarning("Exception! placeLine has sender = ", str(sender))

print "STARTING SERVER ON LOCALHOST"
tantrixServer = TantrixServer()  #'localhost', 1337
while True:
    tantrixServer.Pump()
    sleep(0.01)

#TODO:
#tantrixServer