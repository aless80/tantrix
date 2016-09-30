# Tantrix
Implementation of the Tantrix puzzle game in Python. 
This two player game can be played on one computer or on two clients connected to a server
Link to the game rules:

[www.tantrix.com](http://www.tantrix.com/english/TantrixGameRules.html)

---

## Launch tantrix on one computer
Clone the master branch and start tantrix.py with e.g.:

`python tantrix.py`

A dialog for the "Solitaire" mode is shown. Choose the usernames and colors for the two players and click on "Start": 

![alt text](https://github.com/aless80/tantrix/blob/master/img/SolitaireDialog.png "Solitaire dialog")

The tantrix game will be started:

![alt text](https://github.com/aless80/tantrix/blob/master/img/tantrix_game_solitaire.png "Tantrix")

## Launch server and two tantrix clients
Clone the master branch on both computers. One computer will need an open port to start the server:

`python server.py <host>:<port>`

Both computers start tantrix.py with:

`python tantrix.py <host>:<port>`

The default host and port are localhost and 31425, respectively. In this way server.py and tantrix.py can be run on one computer.

---

## Commands in the game

| Command        | Function       | Button     |
| ------------- |:-------------:|:-------------:|
| Return | Confirm your move | Confirm |
| Left mouse click on a tile | Rotate tile clockwise | |
| Left mouse click on an empty space | Highlight which tiles fit in the hexagon | |
| Right mouse click on a tile | Rotate tile anti-clockwise | |
| R | Reset (bring all tiles back to original place) | Reset |
| Ctrl + W | Quit the game | Quit |
| Ctrl + Q | Quit the game | Quit |
| Up/Down/Left/Right Arrows | center the played tiles (if applicable) | |
| S | Show the score | Score |