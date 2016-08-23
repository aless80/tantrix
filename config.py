import PIL.Image
import math

win = None
canvas = None
wroom = None
wroominstance = None

#SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
import os.path

script_dir = os.path.dirname(os.path.abspath(__file__))
SPRITE  = PIL.Image.open(os.path.join(script_dir, "./img/sprite_smaller.png"))
#SPRITE = PIL.Image.open("./img/sprite_smaller.png")
#SPRITE_WIDTH = 180
#SPRITE_HEIGHT = 156
SPRITE_WIDTH = 2004 / 2
SPRITE_HEIGHT = 1736 / 2

hexagon_generator = None
"rbryby 4th, not rbrgbg"
colors = tuple(['ryybrb','byybrr','yrrbby','byrbry','rbbryy','yrbybr','rbbyry','ybbryr','rbyryb','byyrbr','yrrbyb','brryby','yrrybb','ryybbr','rggryy','yrrygg','ryygrg','gyyrgr','yrrgyg','grrygy','yggrry','gyygrr','gyyrrg','bggbrr','brrggb','grrgbb','grrbgb','rbbggr','brrgbg','rbbrgg','yggryr','gyrgry','rggyry','rgyryg','yrgygr','bggrbr','rbbgrg','gbbrgr','grbgbr','bgrbrg','rggbrb','rbgrgb','gbbyyg','ybgygb','bggyyb','yggbyb','ybbygg','bggbyy','gyygbb','bgybyg','gybgby','bggyby','byygbg','gyybgb','ybbgyg','gbbygy'])

directions = [[0, 1, -1], [+1, 0, -1], [+1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0]]
PLAYERCOLORS = [["red", "orange"], ["blue", "#C1F0FF"], ["yellow", "#FEF760"], ["green", "lightgreen"]]
COLS = 10

HEX_SIZE = 15
HEX_HEIGHT = math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_COS = math.cos(math.radians(60)) * HEX_SIZE
BUFFER = 1
YTOPPL1 = 20
YTOPMAINCANVAS = HEX_HEIGHT + YTOPPL1 + BUFFER
CANVAS_HEIGHT = math.ceil(HEX_HEIGHT * COLS)
YBOTTOMMAINCANVAS = CANVAS_HEIGHT + HEX_HEIGHT * 1.5 + YTOPPL1 + BUFFER * 2
YBOTTOMWINDOW = YBOTTOMMAINCANVAS + HEX_SIZE * 2
ROWS = int(math.ceil(float(CANVAS_HEIGHT) / HEX_SIZE / 2)) + 1
CANVAS_WIDTH = HEX_COS + (HEX_SIZE * 2 - HEX_COS) * COLS




import Board as bd
board = bd.Board()

TRYING = True
#board = False
deck = False
hand1 = False
hand2 = False
turnUpDown = 1
free = True
scores = [0, 0]
scores_loop = [0, 0]

gui_instance = None
gameid = None
player_num = None
name = ""
opponentname = "" #TODO

from PodSixNet.Connection import ConnectionListener, connection
connection = connection

connectionID = None   #eg ('127.0.0.1', 35240)
connectionID1 = None  #for brevity, eg 35240
players = []
queue = None
solitaire = False