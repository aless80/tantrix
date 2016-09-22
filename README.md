# Tantrix
Implementation of the Tantrix puzzle game in Python. 
This two player game can be played on one computer or on two clients connected to a server

## Launch tantrix on one computer
Clone the master branch and start tantrix.py with e.g.:

`python tantrix.py`

## Launch server and two tantrix clients
Clone the master branch on both computers. One computer will need an open port to start the server:

`python server.py <host>:<port>`

Both computers start tantrix.py with:

`python tantrix.py <host>:<port>`

The default host and port are localhost and 31425, respectively. In this way server.py and tantrix.py can be run on one computer.

#### Clone the master branch
git clone https://github.com/aless80/tantrix.git
#### Open

Inline-style: 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
