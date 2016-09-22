# Tantrix
Implementation of the Tantrix puzzle game in Python. 
This two player game can be played on one computer or on two clients connected to a server

## Launch tantrix on one computer
Clone the master branch and start tantrix.py with e.g.:

`python tantrix.py`

The waiting room will be shown. After choosing username and color click on the "Solitaire" button: 

![alt text](https://github.com/aless80/tantrix/tree/master/img/WaitingRoom.png "Waiting room")

In the next dialog choose the username and color for the second player and click "Start": 

![alt text](https://github.com/aless80/tantrix/blob/master/img/SolitaireDialog.png "Solitaire dialog")

The tantrix game will be started:

![alt text](https://github.com/aless80/tantrix/tree/master/img/tantrix_game.png "Tantrix")

## Launch server and two tantrix clients
Clone the master branch on both computers. One computer will need an open port to start the server:

`python server.py <host>:<port>`

Both computers start tantrix.py with:

`python tantrix.py <host>:<port>`

The default host and port are localhost and 31425, respectively. In this way server.py and tantrix.py can be run on one computer.

## 

