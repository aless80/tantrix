import sys
sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

class BoxesGame(ConnectionListener):
    def __init__(self):

        self.Connect()

    def update(self):
        connection.Pump()
        self.Pump()
