import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        print data
 
class BoxesServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
 
    def Connected(self, channel, addr):
        print 'new connection:', channel
 
print "STARTING SERVER ON LOCALHOST"
boxesServe=BoxesServer()
while True:
    boxesServe.Pump()
    sleep(0.01)