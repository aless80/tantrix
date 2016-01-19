import PIL.Image
import math

win = False
canvasmain = False
canvastop = False
canvasbottom = False

PLAYERCOLORS = ["red","blue","yellow","green"]
TRYING = False
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
