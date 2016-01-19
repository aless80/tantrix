import PIL.Image
import math

#win = None
#canvasmain = None
#canvastop = None
#canvasbottom = None

colors = tuple(['ryybrb','byybrr','yrrbby','bgrbrg','rbbryy','yrbybr','rbbyry','ybbryr','rbyryb','byyrbr','yrrbyb','brryby','yrrybb','ryybbr','rggryy','yrrygg','ryygrg','gyyrgr','yrrgyg','grrygy','yggrry','gyygrr','gyyrrg','bggbrr','brrggb','grrgbb','grrbgb','rbbggr','brrgbg','rbbrgg','yggryr','gyrgry','rggyry','rgyryg','yrgygr','bggrbr','rbbgrg','gbbrgr','grbgbr','bgrbrg','rggbrb','rbgrgb','gbbyyg','ybgygb','bggyyb','yggbyb','ybbygg','bggbyy','gyygbb','bgybyg','gybgby','bggyby','byygbg','gyybgb','ybbgyg','gbbygy'])

PLAYERCOLORS = ["red","blue","yellow","green"]
#TRYING = True
SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
SPRITE_WIDTH = 180
SPRITE_HEIGHT = 156

HEX_SIZE = 30
HEX_HEIGHT = math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_SIDE = math.cos(math.radians(60)) * HEX_SIZE
COLS = 10
CANVAS_HEIGHT = HEX_HEIGHT * COLS
ROWS = int(math.ceil(float(CANVAS_HEIGHT)/HEX_SIZE/2)) + 1
CANVAS_WIDTH = HEX_SIDE+(HEX_SIZE * 2 - HEX_SIDE) * COLS
