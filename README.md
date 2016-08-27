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
set self.pumpit to 0 if no connection so that client won't send stuff from wroom
check host port for client. where is that gone?
alert when quitting wroom. self problem in clientListener
turns
quit server more gracefully if channel is already taken?
Quit game goes back to room
decide what to do with quit and sendmessage methods in waitingRoomNew

## BUG
after the third or so, turns do not change
## BUG
GOOD NOW? I changed (3-..) logic to (..+1) in is_confirmable: I had a forced space after a move for pl1. once I placed the tile it did not flush and I stayed with 5 tiles. turnUpDown was 4 (right, I think). Forced tile was highlighted also on opponent (good actually). I see as message on pl1: Not confirmable - It is pycharm (pl2)'s turn. I do not see error of flushing

#Problem new code: 
	player1 confirms his first tile. cllientListener.playConfirmedMove moves automatically on player2 but cannot confirm it because it has cfg.turnUpDown still to 1. For this reason i added a force argument in confirm_move
now I see non matching tile as confirmable for player2. first tile must be rotated

#Problem with change of turns: pl1 confirms and creates a forces space. pl1 fills it and confirms. pl2 still checks, before changing turns, that previous player pl1 does not have forced spaces. so somehow it blocks turn+=1
