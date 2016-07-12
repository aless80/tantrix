import config as cfg
import sys
#sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
sys.path.insert(0, './PodSixNet')
from PodSixNet.Channel import Channel
import PodSixNet.Server
from time import sleep


class ClientChannel(Channel):

    def Network(self, data):
        '''Allow Server to get recipient of .Send from Client'''
        print("\nReceiving in server.ClientChannel.Network() from player :")
        print("  " + str(data))

    def Network_myaction(self, data):
        print("server.ClientChannel.Network_myaction", data)

    def Network_waiting(self, data):
        print("server.ClientChannel.Network_waiting")

    def Network_quit(self, data):
        print("server.ClientChannel.Network_quit")

    def Network_confirm(self, data):
        print("--server.ClientChannel.Network_confirm()", data)
        #deconsolidate all of the data from the dictionary
        rowcolnum = data["rowcolnum"]
        #player number (1 or 0)
        player_num = data["sender"]
        #id of game given by server at start of game
        self.gameid = data["gameid"]
        #change the origin to this server
        data["orig"] = "server.ClientChannel.Network_confirm"
        #tells server to place line
        self._server.placeLine(rowcolnum, data, self.gameid, player_num)


class TantrixServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0

    channelClass = ClientChannel

    def Connected(self, channel, addr):
        print("\nReceiving in server.TantrixServer.Connected:")
        print("  new connection: channel = {},address = {}".format(channel, addr))
        if self.queue is None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
            print("  self.currentIndex={}, channel.gameid={}, self.queue={}".format(str(self.currentIndex), str(channel.gameid), str(self.queue)))
        else:
            channel.gameid = self.currentIndex
            self.queue.player1 = channel
            data0 = {"action": "startgame", "player_num":1, "gameid": self.queue.gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 1:")
            print("  " + str(data0))
            self.queue.player0.Send(data0)
            data1 = {"action": "startgame", "player_num":2, "gameid": self.queue.gameid, "orig": "Server.TantrixServer.Connected"}
            print("\nSending to player 2:")
            print("  " + str(data1))
            self.queue.player1.Send(data1)
            self.games.append(self.queue)
            self.queue = None

    def placeLine(self, rowcolnum, data, gameid, player_num):
        game = [a for a in self.games if a.gameid == gameid]
        if len(game) == 1:
            game[0].placeTile(rowcolnum, data, player_num)


class Game:
    def __init__(self, player0, currentIndex):
        # whose turn (1 or 0)
        self.turn = 1
        #Storage
        self._confirmedgame = []
        #initialize the players including the one who started the game
        self.player0 = player0
        self.player1 = None
        #gameid of game
        self.gameid = currentIndex

    def placeTile(self, rowcolnum, data, player_num):
        print("\n--placeLine")
        #make sure it's their turn
        print("--player_num == self.turn  + 1, {} == {}".format(str(player_num), str(self.turn + 1)))
        if 1 or player_num == self.turn + 1:
            self.turn = 0 if self.turn else 1
            #place line in game
            self._confirmedgame.append(rowcolnum)
            #send data and turn data to each player
            if player_num == 1:
                self.player1.Send(data)
                print("\nSending to player 2:")
                print("  " + str(data))
            elif player_num == 2:
                self.player0.Send(data)
                print("\nSending to player 1: ")
                print("  " + str(data))
            else:
                raise UserWarning("placeLine has player_num = ", str(player_num))

print "STARTING SERVER ON LOCALHOST"
tantrixServe = TantrixServer()  #'localhost', 1337
while True:
    tantrixServe.Pump()
    sleep(0.01)


"""
Problem:
I call confirm to the other client, which also sends!
"""