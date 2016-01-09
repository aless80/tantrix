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

problem:
mouse events in tkinter using win, whereas exagons are in Image.new from PIL
http://stackoverflow.com/questions/18369936/how-to-open-pil-image-in-tkinter-on-canvas
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
    x = col * 0.5  * self.col_width+20
    y = (2 * row + (col % 2)) * self.row_height
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
  def deal(self):
    ran = random.randrange(0, len(self.undealt))
    print(ran)
    print(self.dealt)
    print(self.undealt)
    ran = self.undealt.pop(ran)
    print(ran)
    self.dealt.append(ran)
    print(self.dealt)
    print(self.undealt)
    tile=tileobj(ran)
    photo = PIL.ImageTk.PhotoImage(tile)
    self.photos.append(photo)
    print("len(self.photos)="+str(len(self.photos)))
    print(" ")
    return (ran,photo)


class Tile(object):
  def __init__(self):
    pass
  def __call__(self, row): #getTile(row):
    tile=SPRITE.crop((3+SPRITE_WIDTH*(row-1),4, 
          SPRITE_WIDTH*(row)-2,SPRITE_HEIGHT)).resize((RADIUS*2,int(HEX_HEIGHT)))
    return tile
  def placeTile(self,row,col):
    x = (RADIUS * 2 - HEX_SIDE) * (col - 1)
    #y = HEX_HEIGHT * (row - 1) + HEX_HEIGHT / 2 * ((col + 1) % 2)
    y = HEX_HEIGHT * ((row - 1) + 1 / 2 * ((col + 1) % 2))
    yield RADIUS + x
    yield HEX_HEIGHT / 2 + y

SPRITE = PIL.Image.open("tantrix_sprite.png")
RADIUS=40
HEX_HEIGHT=math.sin(math.radians(120)) * RADIUS * 2
HEX_SIDE=math.cos(math.radians(60)) * RADIUS
CANVAS_WIDTH=400
CANVAS_HEIGHT=400
ROWS=int(math.ceil(float(CANVAS_HEIGHT)/RADIUS/2))+1
COLS=8

SPRITE_WIDTH=180
SPRITE_HEIGHT=156

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
  hexagon_generator=HexagonGenerator(RADIUS)  
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
    temp1 = canvasup.create_image(RADIUS+RADIUS*2*(i-1), HEX_HEIGHT/2, image=ph1)
    temp2 = canvasdown.create_image(RADIUS+RADIUS*2*(i-1), HEX_HEIGHT/2, image=ph2)
  num3,photo3=deck.deal()
  tilepos3=list(tileobj.placeTile(2,3))
  temp3 = canvas.create_image(tilepos3[0], tilepos3[1], image=photo3)
  num4,photo4=deck.deal()
  tilepos4=list(tileobj.placeTile(2,2))
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
    print("pos2ind="+str(pos2ind(x,y)))
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

def pos2ind(x,y):
  indx = math.ceil(x / (2 * RADIUS - HEX_SIDE))
  #math.acos()
  horiz_pos = (x % (2 * RADIUS - HEX_SIDE))   / (2 * RADIUS - HEX_SIDE)
  vert_half = (y % HEX_HEIGHT )   / HEX_HEIGHT
  return (indx,horiz_pos,vert_half)


"""
def drawBkg():
  bkg = PIL.Image.new('RGB', (750, 750), 'cyan')
  bkgD = Draw(bkg)
  hexagon_generator = HexagonGenerator(40)
  for row in range(ROWS):
    color = row * 10, row * 20, row * 30
    for col in range(COLS):
      hexagon = hexagon_generator(row, col)
      #print(list(hexagon))
      #pts=[40,0, 60,34.64, 40,69.3, 0,69.3, -20,34.64, 0,0]
      pts=list(hexagon)
      bkgD.polygon(pts, Brush((255,255,255)))
      print(bkgD)
      #bkgD.polygon(pts, Pen((0,0,0)))
  bkgD.flush()
  return bkg

def main():
  
  window with canvas, bkg is PIL.Image with Draw ..
  draw directly on canvas using create_line!
  
  win=tk.Tk()
  canvas=tk.Canvas(win, height=752, width=752)

  #bkg2 = PIL.Image.open("tile01.png")
  bkg=drawBkg()   #PIL.Image (750, 750)
  #bkg = PIL.Image.new('RGB', (750, 750), 'red')
  
  #basewidth = 750
  #wpercent = (basewidth / float(bkg.size[0]))
  #hsize = int((float(bkg.size[1]) * float(wpercent)))
  #bkg = bkg.resize((basewidth, hsize), PIL.Image.ANTIALIAS) #(750,750)

  #make PhotImage of PIL.Image instance ..
  photo = PIL.ImageTk.PhotoImage(bkg) #move it to the right!
  #photo = tk.PhotoImage(bkg) #error
  #..put it on tk.Canvas
  item4 = canvas.create_image(photo.width()/2, photo.height()/2, image=photo)

  canvas.pack(side = tk.TOP, expand=True, fill=tk.BOTH)
  win.mainloop()
"""

if __name__ == "__main__":
  main()

"""
import Tkinter
win=tkinter.Tk()
win.geometry("300x300")

photo=tkinter.PhotoImage(file=".gif")
img=tkinter.Label(win, image=photo)

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))

win.bind('<Motion>', motion)
win.mainloop()
"""