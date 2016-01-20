import PIL.Image
import math

#win = None
#canvasmain = None
#canvastop = None
#canvasbottom = None
SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
SPRITE_WIDTH = 180
SPRITE_HEIGHT = 156

colors = tuple(['ryybrb','byybrr','yrrbby','bgrbrg','rbbryy','yrbybr','rbbyry','ybbryr','rbyryb','byyrbr','yrrbyb','brryby','yrrybb','ryybbr','rggryy','yrrygg','ryygrg','gyyrgr','yrrgyg','grrygy','yggrry','gyygrr','gyyrrg','bggbrr','brrggb','grrgbb','grrbgb','rbbggr','brrgbg','rbbrgg','yggryr','gyrgry','rggyry','rgyryg','yrgygr','bggrbr','rbbgrg','gbbrgr','grbgbr','bgrbrg','rggbrb','rbgrgb','gbbyyg','ybgygb','bggyyb','yggbyb','ybbygg','bggbyy','gyygbb','bgybyg','gybgby','bggyby','byygbg','gyybgb','ybbgyg','gbbygy'])

directions = [[0, 1, -1],[+1,0, -1],[+1, -1,0],[0, -1, 1],[-1,0, 1],[-1, 1,0] ]
PLAYERCOLORS = ["red","blue","yellow","green"]
COLS = 10


