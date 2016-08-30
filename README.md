# Tantrix
Python code for the Tantrix game

## Launch server and two clients
cd ~/tantrix/
python ./server.py
python ./tantrix.py
python ./tantrix.py

## Description of this version
In version 11 I ditched all methods called from waitingroom communicating with server events such as changing name, toggle ready, etc. Instead, each time these events are triggered, the server sends an update with all information about the connections (sendUpdateTreeview). 
I fixed the problem occurring when confirming a move in a game by sending the rotation of a moved tile. 
Manually closing the windows (e.g. with Alt+F4) now triggers an event so that the server knows it. 

## TODO
colors: prevent player from starting game with same color. create dialog for solitaire
alert when quitting wroom. self problem in clientListener
quit server more gracefully if channel is already taken?
Quit game goes back to room
decide what to do with quit and sendmessage methods in waitingRoomNew
rx click rotates the other way

#BUG
no turn change after single forced tile
#BUG 
1 tile, shift down, place tile next to it, it says "is not adjacent"
#BUG
1 forced tile is shown even if it leads to an impossible place because of 3 colors
	impossible_neighbor is only called in is_confirmable
	Plan: Add impossible_neighbor check to check_forced?, but I have to consider a virtual tile somehow
check_forced found a tile "s" with 3 neighs. 
for each of the tiles fitting there:
	find the possible orientations
	for each orientation:
		check=impossible_neighbor(self, rowcolnum, add_tilenum_at_rowcolnum_rot = [1, (0,0,0), 60])
		if check = False, break first for loop
	if check contains only True:
		do not add s
	else: 
		add s

Test:
cfg.deck.get_neighboring_colors((0,1,0), add_tilenum_at_rowcolnum_rot = [1, (0,0,0), 0])  #ryybrb	[('b', 0, 0)]
cfg.deck.get_neighboring_colors((0,1,0), add_tilenum_at_rowcolnum_rot = [1, (0,0,0), 60]) #bryybr	[('y', 0, 0)]



