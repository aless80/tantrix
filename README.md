# Tantrix
Python code for the Tantrix game

## Launch server and two clients
cd ~/tantrix/
python ./server.py
python ./tantrix.py
python ./tantrix.py

## Description of this version
8.2 was using waitingRoom.py based on wxpython. The problem was wxpython s Mainloop, which gets stuck there without allowing Podsixnet to Pump (exchange messages with server). Using tkinter I have my own main loop, so I would have had to do the same with wxpython. 
In this version I am going back to waitingRoomOLD.py which uses tkinter, also because tkinter is usually already included in python. 
I cleaned this README file. refer to previous versions for a study on Podsixnet.

#Problems with 8.2
cfg.connection = connection was in __init__ of clientLisener. I put it in config.py and it works. there is still a bug on server side, in toggleReadyFromAddr addr is None. This come because sender sent from client is None:
	Sending to server:  {'action': 'toggleReady', 'gameid': None, 'sender': None, 'orig': 'callbacks.Callbacks.toggleReadyForGame'}

## TODO
make sure quit always quits in spite of the error
quit server gracefully if channel is already taken
quit gracefully if waitingroom gets closed?
Quit game goes back to room
decide what to do with quit and sendmessage methods in waitingRoomNew
