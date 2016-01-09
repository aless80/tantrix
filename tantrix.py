""" 
install python-dev
sudo apt-get install python-pygame
sudo apt-get install python3-pil
sudo apt-get install python3-imaging-tk
aggdraw:
get the zip here: http://effbot.org/downloads#aggdraw
In some cases I have to use 
export CFLAGS="-fpermissive"
then use the commands in the README ie:
python setup.py install

http://variable-scope.com/posts/hexagon-tilings-with-python
http://www.raywenderlich.com/1223/python-tutorial-how-to-generate-game-tiles-
with-python-imaging-library

http://www.redblobgames.com/grids/hexagons/
"""

import math
#from PIL import Image
import PIL.Image, PIL.ImageTk
from aggdraw import Draw, Brush, Pen
#import aggdraw.Draw, aggdraw.Brush, aggdraw.Pen
try: 
  import Tkinter as tk # for Python2
except Error: 
  import tkinter as tk # for Python3
import random


#OFFSET: col or q, row or r
#AXIAL HEX: q = x and r = z

'''def pixel_to_hex(x, y):
  q = x * 2/3 / HEX_SIZE
  r = (-x / 3 + math.sqrt(3)/3 * y) / HEX_SIZE
  return hex_round((q, r))  #q,r are here axial
  #return hex_round(Hex(q, r)) #q,r are here axial

  def off2cube(row,col): 
  # convert odd-q offset to cube
  x = col
  z = row - (col - (col&1)) / 2
  y = -x-z
  return (x,y,z)

  def hex_to_pixel(hex):
    x = HEX_SIZE * math.sqrt(3) * (hex[1] + hex[0]/2)
    y = HEX_SIZE * 3/2 * hex[0]
    return (x, y) #Point(x, y)

  def hex_round(h):
    return cube_to_hex(cube_round(hex_to_cube(h)))

  def cube_to_hex(cube): 
    # axial
    q = cube[0]
    r = cube[2]
    return (q, r)
  '''
def pixel_to_off(x, y):
  q = x * 2/3 / HEX_SIZE
  r = (-x / 3 + math.sqrt(3)/3 * y) / HEX_SIZE
  #print("cube_round in axial="+str(cube_round((q, -q-r, r))))
  return cube2off(cube_round((q, -q-r, r))) #Ale col works - no

def cube2off(cube):
  # convert cube to odd-q offset
  col = cube[0]
  row = cube[2] + (cube[0] - (cube[0]%2)) / 2
  return (row,col)

def hex_to_cube(h): # axial
    x = h[1]
    z = h[0]
    y = -x-z
    return (x, y, z) #return Cube(x, y, z)

def cube_round(h):
    rx = round(h[0])
    ry = round(h[1])
    rz = round(h[2])
    x_diff = abs(rx - h[0])
    y_diff = abs(ry - h[1])
    z_diff = abs(rz - h[2])
    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry
    return ((rx, ry, rz)) #return (Cube(rx, ry, rz))
    
class HexagonGenerator(object):
  """Returns a hexagon generator for hexagons of the specified size."""
  def __init__(self, edge_length):
    self.edge_length = edge_length
  @property
  def col_width(self):
    return self.edge_length * 3
  @property
  def row_height(self):
    return math.sin(math.pi / 3) * self.edge_length
  def __call__(self, row, col):
    #x = (col + 0.5 * (row % 2)) * self.col_width+21
    x = col * 0.5  * self.col_width + HEX_SIZE / 2
    y = (2 * row + (col % 2)) * self.row_height
    y -= 1 * ((col + 1) % 2) #fix even columns by one pixel
    #top left pixel
    topleft=(x + math.cos(math.radians(240)) * self.edge_length,  
             y + math.sin(math.radians(0)) * self.edge_length)
    #print("---");
    #print(topleft)
    for angle in range(0, 420, 60):
      x += math.cos(math.radians(angle)) * self.edge_length
      y += math.sin(math.radians(angle)) * self.edge_length
      #print(x,y,angle)
      yield x
      yield y
  def topleftPixel(self, row, col):
    print("---")
    x = col * 0.5  * self.col_width+20
    y = (2 * row + (col % 2)) * self.row_height
    #top left pixel
    topleft=(x + math.cos(math.radians(240)) * self.edge_length,  
      y + math.sin(math.radians(0)) * self.edge_length)
    #print(topleft)
    return topleft

class Deck(object):
  def __init__(self):
    self.undealt=range(1, 57)
    self.dealt=[]
    self.photos=[]
  '''  @property
  def dealt(self):
    return []
  '''
  def deal(self): #, *num, **keyword_parameters):
    ran = random.randrange(0, len(self.undealt))
    ran = self.undealt.pop(ran)
    self.dealt.append(ran)
    tile=tileobj(ran)
    photo = PIL.ImageTk.PhotoImage(tile)
    self.photos.append(photo)
    return (ran,photo)

class Tile(object):
  def __init__(self):
    pass
  def __call__(self, row): #getTile(row):
    tile=SPRITE.crop((3+SPRITE_WIDTH*(row-1),4, 
          SPRITE_WIDTH*(row)-2,SPRITE_HEIGHT)).resize((HEX_SIZE*2,int(HEX_HEIGHT)))
    return tile
  def placeTile(self,row,col):
    x = (HEX_SIZE * 2 - HEX_SIDE) * (col - 1)
    y = HEX_HEIGHT * (row - 1) + HEX_HEIGHT / 2 * ((col + 1) % 2)
    #y = HEX_HEIGHT * ((row - 1) + 1 / 2 * ((col + 1) % 2))
    yield HEX_SIZE + x
    yield HEX_HEIGHT / 2 + y

SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
HEX_SIZE=50
HEX_HEIGHT=math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_SIDE=math.cos(math.radians(60)) * HEX_SIZE
CANVAS_WIDTH=400
CANVAS_HEIGHT=400
ROWS=int(math.ceil(float(CANVAS_HEIGHT)/HEX_SIZE/2))+1
COLS=8

SPRITE_WIDTH=180
SPRITE_HEIGHT=156

win=False
canvas=False
hexagon_generator=False
canvasup=False
canvasdown=False
deck=False
tileobj=False

def main():
  global win, canvas, hexagon_generator, canvasup, canvasdown, deck, tileobj
  #Window and canvases
  win=tk.Tk()
  canvas=tk.Canvas(win, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, background='lightgrey')
  canvasup=tk.Canvas(win, height=HEX_HEIGHT+2, width=CANVAS_WIDTH, background='lightgrey')
  canvasdown=tk.Canvas(win, height=HEX_HEIGHT+2, width=CANVAS_WIDTH, background='lightgrey')
  #create hexagons
  hexagon_generator=HexagonGenerator(HEX_SIZE)  
  for row in range(ROWS):
    for col in range(COLS):
      pts=list(hexagon_generator(row, col))
      canvas.create_line(pts)
  #append canvas
  canvasup.grid(row=1, column=1,columnspan=1)
  canvas.grid(row=2, column=1,columnspan=1)
  canvasdown.grid(row=3, column=1,columnspan=1)
  #.pack(side = tk.TOP, expand=True, fill=tk.BOTH)
  
  #Tile and deck
  tileobj=Tile()
  deck = Deck()
  #Deal tiles  
  for i in range(1,6):
    num1,ph1=deck.deal()
    num2,ph2=deck.deal()
    temp1 = canvasup.create_image(HEX_SIZE+HEX_SIZE*2*(i-1), HEX_HEIGHT/2, image=ph1)
    temp2 = canvasdown.create_image(HEX_SIZE+HEX_SIZE*2*(i-1), HEX_HEIGHT/2, image=ph2)
  num3,photo3=deck.deal()
  tilepos3=list(tileobj.placeTile(1,2))
  temp3 = canvas.create_image(tilepos3[0], tilepos3[1], image=photo3)
  num4,photo4=deck.deal()
  tilepos4=list(tileobj.placeTile(1,1))
  temp4 = canvas.create_image(tilepos4[0], tilepos4[1], image=photo4)
  
  #Bindings
  #win.bind('<Motion>', motion)
  win.bind('<Button>', motion) #type 4
  win.bind('<B1-Motion>', motion) #drag
  #win.bind('<Return>', motion)
  #win.bind('<Key>', motion)
  win.bind('<MouseWheel>', wheel)
  win.mainloop()


def motion(event):
  print('keycode='+str(event.keycode))
  print('state='+str(event.state))
  print('type='+str(event.type))
  print('delta='+str(event.delta))
  print('')
  #event.num = mouse number, keycode, state (press, release,leave, motion,..), 
              #type (as number), delta of wheel
  x, y = event.x, event.y
  if int(event.type) == 4:
    print("pixel_to_ off="+str(pixel_to_off(x,y)))
  else :
    print('{}, {}'.format(x, y))

def wheel(event):
  print('keycode='+str(event.keycode))
  print('state='+str(event.state))
  print('type='+str(event.type))
  print('delta='+str(event.delta))
  print('')
  x, y = event.x, event.y
  print('{}, {}'.format(x, y))


def isrotation(s1,s2):
     return len(s1)==len(s2) and s1 in 2*s2

def isrot(src, dest):
  # Make sure they have the same size
  if len(src) != len(dest):
    return False

  # Rotate through the letters in src
  for ix in range(len(src)):
    # Compare the end of src with the beginning of dest
    # and the beginning of src with the end of dest
    if dest.startswith(src[ix:]) and dest.endswith(src[:ix]):
      return True

  return False


if __name__ == "__main__":
  main()
