import config as cfg
import sys
sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):

    def Network(self, data):
        print("server.ClientChannel.Network()")
        print(data)

    def Network_myaction(self, data):
        print("server.ClientChannel.Network_myaction()", data)

    def Network_place(self, data):
        #deconsolidate all of the data from the dictionary

        #horizontal or vertical?
        hv = data["is_horizontal"]
        #x of placed line
        x = data["x"]

        #y of placed line
        y = data["y"]

        #player number (1 or 0)
        num=data["num"]

        #id of game given by server at start of game
        self.gameid = data["gameid"]

        #tells server to place line
        self._server.placeLine(hv, x, y, data, self.gameid, num)

class BoxesServer(PodSixNet.Server.Server):
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex = 0

    channelClass = ClientChannel

    def Connected(self, channel, addr):
        print 'new connection: channel = ', channel
        if self.queue == None:
            self.currentIndex += 1
            channel.gameid = self.currentIndex
            self.queue = Game(channel, self.currentIndex)
            print("self.currentIndex={}, channel.gameid={}, self.queue={}".format(str(self.currentIndex), str(channel.gameid),str(self.queue)))
        else:
            channel.gameid = self.currentIndex
            self.queue.player1 = channel
            self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue = None

    def placeLine(self, is_h, x, y, data, gameid, num):
        game = [a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].placeLine(is_h, x, y, data, num)


class Game:
    def __init__(self, player0, currentIndex):
        # whose turn (1 or 0)
        self.turn = 0
        #owner map
        self.owner = [[False for x in range(6)] for y in range(6)]
        # Seven lines in each direction to make a six by six grid.
        self.boardh = [[False for x in range(6)] for y in range(7)]
        self.boardv = [[False for x in range(7)] for y in range(6)]
        #initialize the players including the one who started the game
        self.player0 = player0
        self.player1 = None
        #gameid of game
        self.gameid = currentIndex

        def placeLine(self, is_h, x, y, data, num):
            #make sure it's their turn
            if num==self.turn:
                self.turn = 0 if self.turn else 1
                #place line in game
                if is_h:
                    self.boardh[y][x] = True
                else:
                    self.boardv[y][x] = True
                #send data and turn data to each player
                self.player0.Send(data)
                self.player1.Send(data)

print "STARTING SERVER ON LOCALHOST"
boxesServe = BoxesServer()  #'localhost', 1337
print(boxesServe)
while True:
    boxesServe.Pump()
    sleep(0.01)