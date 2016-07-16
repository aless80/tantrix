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
        #TODO
        print("\nReceiving in server.ClientChannel.Network_quit() from player :\n  " + str(data))
        #self.allConnections.removeConnection(data['sender'])

    def Network_confirm(self, data):
        print("--server.ClientChannel.Network_confirm()", data)
        #deconsolidate all of the data from the dictionary
        rowcolnum = data["rowcolnum"]
        #player number (1 or 0)
        sender = data["sender"]
        #id of game given by server at start of game
        self.gameid = data["gameid"]
        #change the origin to this server
        data["orig"] = "server.ClientChannel.Network_confirm"
        #tells server to place line
        self._server.placeLine(rowcolnum, data, self.gameid, sender)


class TantrixServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0
        self.allConnections = WaitingConnections()

    def DelPlayer(self, player):
        #TODO
		    print "Deleting Player" + str(player.addr)
		    del self.players[player]
		    self.SendPlayers()

    def SendPlayers(self):
		    self.SendToAll({"action": "players", "players": dict([(p.id, p.color) for p in self.players])})

    def SendToAll(self, data):
		    [p.Send(data) for p in self.players]


    def Connected(self, player, addr):
        """self.queue  contains the array .players"""
        print("\nReceiving in server.TantrixServer.Connected:")
        print("  new connection: channel = {},address = {}".format(player, addr))
        """create or edit a game queue""" #TODO move this once players in wroom confirm each other
        if self.queue is None:
            self.currentIndex += 1
            player.gameid = self.currentIndex #TODO I do nto want this
            self.queue = Game(player, self.currentIndex) #TODO I do not want this
            print("  self.currentIndex={}, player.gameid={}, self.queue={}".format(str(self.currentIndex), str(player.gameid), str(self.queue)))

        else:
            player.gameid = self.currentIndex
            self.queue.addPlayer(player)
            self.startgameForQueue()
        """roger that client has connected. send back the client's address"""
        data0 = {"action": "roger", "addr": addr, "orig": "Server.TantrixServer.Connected"}
        print("\nSending to client:\n  " + str(data0))
        self.allConnections.addConnection(player, addr, self.queue)
        player.Send(data0)
        """Send the number of players to all"""
        #note: not able to send queue
        data = {"action": "numplayers", "orig": "Server.TantrixServer.Connected",
                "players": [self.allConnections.addr[c] for c in range(self.allConnections.count())]}
        for p in self.allConnections.players:
            p.Send(data)

    def startgameForQueue(self):
            data0 = {"action": "startgame", "player_num":1, "gameid": self.queue.gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 1:\n  " + str(data0))
            self.queue.players[0].Send(data0)
            data1 = {"action": "startgame", "player_num":2, "gameid": self.queue.gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 2:\n  " + str(data1))
            self.queue.players[1].Send(data1)
            self.games.append(self.queue)
            #self.queue = None

    def placeLine(self, rowcolnum, data, gameid, sender):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeLine(rowcolnum, data, sender)


class WaitingConnections:
    def __init__(self): #, currentIndex):
        #initialize the players including the one who started the game
        self.players = []
        self.addr = []
        self.queue = []

    def addConnection(self, player, addr, queue):
        self.players.append(player)
        self.addr.append(addr)
        self.queue.append(queue)

    def removeConnection(self, addr):
        ind = self.addr.index(addr)
        self.addr.pop(ind)
        self.players.pop(ind)

    def count(self):
        return len(self.players)


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
        print("\n--placeLine")
        #make sure it's their turn TODO
        if 1 or sender == self.turn + 1: #todo
            self.turn = 0 if self.turn else 1
            #place line in game
            self._confirmedgame.append(rowcolnum)
            #send data and turn data to each player
            if sender == tantrixServe.allConnections.addr[0]: #todo: only connections in the current game!
                self.players[1].Send(data)
                print("\nSending to other player:")
                print("  " + str(data))
            elif sender == tantrixServe.allConnections.addr[1]:
                self.players[0].Send(data)
                print("\nSending to other player: ")
                print("  " + str(data))
            else:
                raise UserWarning("Exception! placeLine has sender = ", str(sender))

print "STARTING SERVER ON LOCALHOST"
tantrixServe = TantrixServer()  #'localhost', 1337
while True:
    tantrixServe.Pump()
    sleep(0.01)


"""
Problem:
I call confirm to the other client, which also sends!
"""