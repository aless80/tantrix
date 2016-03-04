__author__ = 'amarin'
import sys
sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')


import PodSixNet, time
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep

class MyNetworkListener(ConnectionListener):

    def __init__(self): #, host, port):
        self.Connect() #(host, port))

    def Network(self, data):
        print data

# tell the client which server to connect to
gui = MyNetworkListener()  #'localhost', 1337
while 1:
    connection.Pump()
    gui.Pump()