import sys
#sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
sys.path.insert(0, './PodSixNet')
from PodSixNet.Channel import Channel
#import PodSixNet.Server
from PodSixNet.Server import Server
from time import sleep


class ClientChannel(Channel):
    """Receive messages from client. self._server refers to tantrixServer ie the instance of TantrixServer"""
    def Network(self, data):
        '''Allow Server to get recipient of .Send from Client'''
        print("\nReceiving in server.ClientChannel.Network() from player :\n  " + str(data))

    def Network_myaction(self, data):
        print("\nReceiving in server.ClientChannel.Network_myaction() from player :\n  " + str(data))

    def Network_toggleReady(self, data):
        addr = data["sender"]
        print("\nReceiving in server.ClientChannel.Network_toggleReady() from player {}:\n  {}".format(str(addr), str(data)))
        self._server.allConnections.toggleReadyFromAddr(addr)
        self._server.checkConnections()

    def Network_confirm(self, data):
        #deconsolidate all of the data from the dictionary
        rowcolnum = data["rowcolnum"]
        #player number (1 or 0)
        sender = data["sender"]
        #change the origin to this server
        data["orig"] = "server.ClientChannel.Network_confirm"
        #tells server to place line
        self._server.placeLine(rowcolnum, data, data["gameid"], sender)

    def Network_quit(self, data):
        """One player has quit"""
        print("\nReceiving in server.ClientChannel.Network_quit() from player :\n  " + str(data))
        quitter = data['sender']
        """Tell other players that one has quit. Must do it inside TantrixServer"""
        self._server.tellToQuit(data)
        """Delete the quitter from allConnections"""
        self._server.allConnections.removeConnection(quitter)


class TantrixServer(Server):
    """Send message to clients"""
    channelClass = ClientChannel  #needed!

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.gameIndex = 0
        self.allConnections = WaitingConnections()

    def checkConnections(self):
        print(self.allConnections.__str__())
        """Check if at least two players are ready"""
        players_ready = 0
        for ind in range(self.allConnections.count()):
            if self.allConnections.ready[ind] == 1:
                players_ready += 1
                tempind = ind
        if players_ready < 2: return
        """If so, initialize a game"""
        self.gameIndex += 1
        game = Game(self.allConnections.players[tempind], self.gameIndex)
        #####BUG I SEE CONFIRM SENDING TO THE WRONG PLAYER!
        for ind in range(self.allConnections.count()):
            if not self.allConnections.ready[ind]: continue
            game.addPlayer(self.allConnections.players[ind])
        """start the game"""
        for ind in range(self.allConnections.count()):
            if not self.allConnections.ready[ind]: continue
            self.allConnections.addGame(game, self.allConnections.addr[ind])
            self.allConnections.ready[ind] = -1
        print("  self.gameIndex={}, player.gameid={}, tempgame={}".format(str(self.gameIndex), str(game.gameid), str(game)))
        self.startGame()
        


    def Connected(self, player, addr):
        """self.game  contains the array .players"""
        print("\nReceiving in server.TantrixServer.Connected:")
        print("  new connection: channel = {},address = {}".format(player, addr))
        """create or edit a game""" #TODO move this once players in wroom confirm each other
        if not self.allConnections.game:
            self.gameIndex += 1
            #tempgame = Game(player,self.gameIndex) #TODO I do not want this
            #tempgame.gameid = self.gameIndex #TODO I do nto want this now.
            #print("  self.gameIndex={}, player.gameid={}, tempgame={}".format(str(self.gameIndex), str(tempgame.gameid), str(tempgame)))
            """roger that 1st client has connected. send back the client's address"""
            data0 = {"action": "roger", "addr": addr, "orig": "Server.TantrixServer.Connected"}
            self.roger(player, data0)
            self.allConnections.addConnection(player, addr, 0)
            #self.allConnections.addGame(tempgame, addr)
        else:
            #self.allConnections.game[0].addPlayer(player)
            self.allConnections.addConnection(player, addr, 0)
            #self.allConnections.addGame(self.allConnections.game[0], addr)
            """roger that 2nd client has connected. send back the client's address"""
            data1 = {"action": "roger", "addr": addr, "orig": "Server.TantrixServer.Connected"}
            self.roger(player, data1)
            #"""start game"""
            #self.startGame()
        """Send the number of players in waiting room or playing to all"""
        #note: not able to send game
        addr = [c for c in self.allConnections.addr]
        data = {"action": "players", "orig": "Server.TantrixServer.sendToAll",
                "players": addr, "num": len(addr)} #[self.allConnections.addr[c] for c in range(self.allConnections.count())]}
        for player in self.allConnections.players:
            #player.Send(data)
            self.sendToPlayer(player, data)

    def sendToPlayer(self, player, data):
        print("\nSending to client " + str(player.addr[1]) + ":\n  " + str(data))
        player.Send(data)

    def roger(self, player, data):
        """send confirmation messages to client"""
        print("\nSending to client " + str(player.addr[1]) + ":\n  " + str(data))
        player.Send(data)


    def startGame(self):
            data0 = {"action": "startgame", "player_num":1, "gameid": self.allConnections.game[0].gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 1:\n  " + str(data0))
            self.allConnections.players[0].Send(data0)
            data1 = {"action": "startgame", "player_num":2, "gameid": self.allConnections.game[1].gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 2:\n  " + str(data1))
            self.allConnections.players[1].Send(data1)

    def placeLine(self, rowcolnum, data, gameid, sender):
        game = self.allConnections.getGameFromAddr(sender)
        game.placeLine(rowcolnum, data, sender)

    def tellToQuit(self, data):
        quitter = data["sender"]
        ind = self.allConnections.addr.index(quitter)
        #p = self.allConnections.players[(ind+1)%2]
        dataAll = {"action": "hasquit", "quitter": quitter,
                   "orig": "Server.TantrixServer.tellToQuit2"}
        for i in range(self.allConnections.count()):
            if i != ind and self.allConnections.game[i] == self.allConnections.game[ind]:
                p = self.allConnections.players[i]
                print("\nSending to client {}:\n  {}".format(str(p), str(dataAll)))
                p.Send(dataAll)

class Game:
    def __init__(self, player, gameIndex):
        # whose turn (1 or 0)
        self.turn = 1
        #Storage
        self._confirmedgame = []
        #initialize the players including the one who started the game
        self.players = []
        self.addPlayer(player)
        #gameid of game
        self.gameid = gameIndex

    def addPlayer(self, player):
        if player is not None and player not in self.players:
            self.players.append(player)
        else:
            print("Game.addPlayer failed: player is None or was already added")

    def placeLine(self, rowcolnum, data, sender):
        #make sure it's their turn TODO
        if 1 or sender == self.turn + 1: #TODO
            self.turn = 0 if self.turn else 1
            #place line in game
            self._confirmedgame.append(rowcolnum)
            #send data and turn to the opponent
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

    def addConnection(self, player, addr, ready = 0, game = None):
        self.players.append(player)
        self.addr.append(addr)
        self.ready.append(ready)
        self.game.append(game)

    def addGame(self, game, addr):
        ind = self.addr.index(addr)
        self.game[ind] = game

    def removeConnection(self, addr):
        ind = self.addr.index(addr)
        self.addr.pop(ind)
        self.players.pop(ind)
        self.game.pop(ind)
        self.ready.pop(ind)

    def count(self):
        return len(self.players)

    def getIndexFromAddr(self, addr):
        return self.addr.index(addr)

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
        game = self.getGameFromAddr(addr)
        ind_sender = self.getIndexFromAddr(addr)
        opponents = []
        for ind in range(self.count()):
            if ind != ind_sender and self.game[ind] == game:
                opponents.append(self.players[ind])
        return opponents
        #return [x for i, x in enumerate(self.players) if x == player and self.addr[i] is not addr]

    def toggleReadyFromAddr(self, addr):
        try:
            ind = self.addr.index(addr)
        except:
            import inspect
            print("Unexpected error at :", inspect.stack()[0][3])
            print("addr="+ str(addr) + " is not contained in self.addr="+ str(self.addr))
            raise

        self.ready[ind] = (self.ready[ind] + 1) %2

    def __str__(self):

        string = "Connections:\n<======================\n"
        for ind in range(self.count()):
            string += "ready, addr, players, game:\n"
            string += "{}, {}, {}, {}".format(
                str(self.ready[ind]),
                str(self.addr[ind]),
                str(self.players[ind]),
                str(self.game[ind]))
        string += "\n======================>\n"
        return string

print "STARTING SERVER ON LOCALHOST"
tantrixServer = TantrixServer()  #'localhost', 1337
while True:
    tantrixServer.Pump()
    sleep(0.01)

#TODO:
#tantrixServer