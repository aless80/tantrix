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

