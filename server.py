import sys
sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
import PodSixNet.Channel
import PodSixNet.Server
from time import sleep

class ClientChannel(PodSixNet.Channel.Channel):

    def Network(self, data):
        print data

    def Network_myaction(self, data):
        print("myaction:", data)


class BoxesServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)

    def Connected(self, channel, addr):
        print 'new connection: channel = ', channel


print "STARTING SERVER ON LOCALHOST"
boxesServe = BoxesServer()  #'localhost', 1337
while True:
    boxesServe.Pump()
    sleep(0.01)