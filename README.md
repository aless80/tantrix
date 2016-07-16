# Tantrix
Python code for the Tantrix game


http://www.meetup.com/Code-for-Boston/events/hcddllyvlbdb/

pymouse

## Launch server and two clients
cd ~/tantrix/
python ./server.py
python ./tantrix.py
python ./tantrix.py

##
tantrix.py launches Gui.main. In Gui there is also this definition:
	connection = EndPoint()
In Gui.main there are the game and pre-game loops:
	self.Connect()
    """This is the polling loop before starting the game"""
    self.running = False
    while not self.running: #becomes true in Gui.Network_startgame, called from server.Connected
        connection.Pump()
        self.Pump()
        sleep(0.01)
	
	"""This is the polling loop during the game"""
        while 1:
            """Polling loop for the client. asks the connection singleton for any new messages from the network"""
            connection.Pump()   #Polling loop for the client.
            """Server"""
            self.Pump()         #Server
            """Update the boards"""
            cfg.win.update()
            cfg.win.update_idletasks()


connection: a singleton instantiation of an EndPoint which will be connected to the server.
Deck, Gui and Client subclass ConnectionListener in order to have an object that will receive network events.


##Instructions from Podsixnet
This module contains two components: a singleton called 'connection' and a class called 'ConnectionListener'.

'connection' is a singleton instantiation of an EndPoint which will be connected to the server at the other end.
It's a singleton because each client should only need one of these in most multiplayer scenarios.
(If a client needs more than one connection to the server, a more complex architecture can be built out of
instantiated EndPoint()s.) The connection is based on Python's asyncore and so it should have it's polling loop
run periodically, probably once per gameloop. This just means putting
"from Connection import connection; connection.Pump()" somewhere in your top level gameloop.

Subclass ConnectionListener [Gui does that!] in order to have an object that will receive network events.
For example, you might have a GUI element which is a label saying how many players there are online.
You would declare it like 
	class NumPlayersLabel(ConnectionListener, ...):
Later you'd instantiate it 
	n = NumPlayersLabel() 
and then somewhere [I have it in the end of Gui.main] in your loop you'd have 
	n.Pump()
which asks the connection singleton if there are any new messages from the network, 
and calls the 'Network_' callbacks for each bit of new data from the server. So you'd implement a method like
	def Network_players(self, data): 
which would be called whenever a message from the server arrived which looked like 
	{"action": "players", "number": 5}.

##To do
Understand how boards start. Then create a basic inteface with n_players, start_game etc that starts the game. 
	see self.startWaitingRoomUI() and its current problem. comment it to run program as before. 
Solitaire

## Server to Client - Connect
client sends from Gui.__init__ using 
	self.Connect()
server receives using server.TantrixServer.Connected, which sends {"action": stargame} to clients
Gui.Network_startgame listens on client

channel is player. it has channel.gameid
Game contains channel
allConnections adds channel, addr, queue. I want that each channel/player gets associated with queue so i have to update the first player. does queue indicate both players?

