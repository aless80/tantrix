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
#from aggdraw import Draw, Brush, Pen
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
def pixel_to_off_canvastopbottom(x, y):
  col=math.ceil(float(x) / (HEX_SIZE * 2))
  return (1,col)
def pixel_to_off(x, y):
  q = x * 2/3 / HEX_SIZE
  r = (-x / 3 + math.sqrt(3)/3 * y) / HEX_SIZE
  #print("cube_round in axial="+str(cube_round((q, -q-r, r))))
  return cube2off(cube_round((q, -q-r, r)))

def cube2off(cube):
  # convert cube to odd-q offset
  col = cube[0] + 1
  row = cube[2] + (cube[0] - (cube[0]%2)) / 2 + 1
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
  def __call__(self, row, col, offset=(0,0)):
    x = offset[0] + col * 0.5  * self.col_width + HEX_SIZE / 2
    y = offset[1] + (2 * row + (col % 2)) * self.row_height
    y -= 1 * ((col + 1) % 2) #fix even columns by one pixel
    for angle in range(0, 420, 60):
      x += math.cos(math.radians(angle)) * self.edge_length
      y += math.sin(math.radians(angle)) * self.edge_length
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


class Tiles(object):
  def __init__(self):
    self.positions=[]
    self.photos=[]
    self.undealt=range(1, 57)
    self.dealt=[]
    self.angle=[]
  #def __call__(self, ran):
  
  def getTileNumberFromIndex(self,ind):
    pass #self.dealt[ind]
  def getIndexFromTileNumber(self,num):
    return self.dealt.index(num)
  def getIndexFromRowColCanv(self,rowcolcanv):
    ind=tiles.positions.index(tuple(rowcolcanv))
    return ind
  def getTileNumberFromRowColCanv(self,rowcolcanv):
    pass #self.getTileNumberFromIndex(self.getIndexFromRowColCanv(rowcolcanv))
  def tile_spawner(self, num, angle=0):
    """return a tile in PhotoImage format"""
    print('num is:' +str(num))
    global deck
    #tile is a PhotoImage (required by Canvas' create_image) and its number
    tilePIL=SPRITE.crop((3+SPRITE_WIDTH*(num-1),4,
           SPRITE_WIDTH*(num)-2,SPRITE_HEIGHT)).resize((HEX_SIZE*2,int(HEX_HEIGHT)))
    if angle != 0:
      angle+=self.angle[self.getIndexFromTileNumber(num)]
      tilePIL=tilePIL.rotate(angle, expand=0)
    tile = PIL.ImageTk.PhotoImage(tilePIL)
    return tile

  def tilePixels(self,row,col,canvas):
    '''
    if canvas.find_withtag(CURRENT):
        #canvas.itemconfig(CURRENT, fill="blue")
        canvas.update_idletasks()
        canvas.after(200)
        canvas.itemconfig(CURRENT, fill="red")
        '''
    #I need the coordinates on the canvas
    #get the window's canvases: win.children .values() and .keys()
    #get the canvas widget from its path name: win.children[str(canvas)[1:]]
    canvasID=str(canvas)
    if canvasID.endswith(str(canvastop)): #top canvas
      #print('\ntop:   '+str(canvas))
      x = HEX_SIZE + ((HEX_SIZE * 2) * (col - 1))
      y = HEX_HEIGHT / 2
    elif canvasID.endswith(str(canvasbottom)): #bottom canvas
      #print('\nbottom:'+str(canvas))
      x = HEX_SIZE + ((HEX_SIZE * 2) * (col - 1))
      y = HEX_HEIGHT / 2
    else: #main canvas #problem: win.children are not ordered!!!
      #print('\nmain  :'+str(canvas))
      x = HEX_SIZE + ((HEX_SIZE * 2 - HEX_SIDE) * (col - 1))
      y = HEX_HEIGHT / 2 + (HEX_HEIGHT * (row - 1) + HEX_HEIGHT / 2 * ((col + 1) % 2))
    #self.positions.append((row,col,canvasID))
    #print(x,y)
    yield x
    yield y
    yield canvasID

  def move(self,row1,col1,canvas1,row2,col2,canvas2):
    ind=self.getIndexFromRowColCanv((row1,col1,str(canvas1)))
    #cannot use this because place gets ind itself.. self.place(self,row2,col2,canvas2,tile)
    print('move positions before and after at ind='+str(ind))
    print(self.positions[ind])
    self.positions[ind]=(row2,col2,str(canvas))
    print(self.positions[ind])
    #todo: must kill original tile! that is a canvas.create_image
    #test if I can use self.photos[ind] instead of tile_spawner:
    #tile=self.photos[ind]
    oldtile=self.photos.pop(ind)
    tile=self.tile_spawner(tiles.dealt[ind],self.angle[ind])
    tilex,tiley,canvasID=tiles.tilePixels(row2,col2,canvas2)
    canvas.create_image(tilex, tiley, image=tile)

    tilex,tiley,canvasID=tiles.tilePixels(row2,col2,canvas2)
    if canvas1 == canvas2:
      pass
      #canvas1.coords(<MYTILE>, (tilex,tiley))
    else: #destroy and recreate tile
      pass

    #Update window
    win.update()

  def place(self,row,col,canvas,tile):
    #Place on canvas
    tilex,tiley,canvasID=tiles.tilePixels(row,col,canvas)
    canvas.create_image(tilex, tiley, image=tile)
    #Update positions
    ind=self.getIndexFromRowColCanv((row,col,str(canvas)))
    print("ind: " + str(ind))
    self.positions[ind]=(row,col,str(canvas))
    #Update window
    win.update()

  def deal(self,row,col,canvas,num='random'):
    #Random tile if num is not set
    if num =='random':
      ran = random.randrange(1, len(self.undealt))
    num=self.undealt.pop(ran)
    #Get tile as PhotoImage
    tile=self.tile_spawner(num)
    #Store tile-PhotoImage
    self.photos.append(tile)
    #Place on canvas
    tilex,tiley,canvasID=tiles.tilePixels(row,col,canvas)
    id=canvas.create_image(tilex, tiley, image=tile)
    print('id='+str(id))
    #store dealt/undealt tile numbers
    self.dealt.append(num)
    self.positions.append((row,col,str(canvas)))
    self.angle.append(0)

  def rotate(self,rowcolcanv):
    global win
    try:
      ind=self.getIndexFromRowColCanv(tuple(rowcolcanv))
      print('found at '+str(ind))
    except:
      print('not found: '+str(rowcolcanv)+' in')
      print(tiles.positions)
      return
    tile=self.tile_spawner(tiles.dealt[ind],-60)
    #Update angle
    self.angle[ind]-=60
    #Store image
    tiles.photos[ind]=tile
    #Place it
    (row,col,canvasid)=tiles.positions[ind]
    can=win.children[canvasid[1:]]
    tiles.place(row,col,can,tile)

class Deck(object):
  def __init__(self):
    pass
  def createBoard(self):
    global win, canvas, hexagon_generator, canvastop, canvasbottom, deck, tiles
    win=tk.Tk()
    canvas=tk.Canvas(win, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, background='lightgrey')
    canvastop=tk.Canvas(win, height=HEX_HEIGHT, width=CANVAS_WIDTH, background='lightgrey')
    canvasbottom=tk.Canvas(win, height=HEX_HEIGHT, width=CANVAS_WIDTH, background='lightgrey')
    w=CANVAS_WIDTH+5
    h=CANVAS_HEIGHT+HEX_HEIGHT*2+5
    ws=win.winfo_screenwidth() 		#width of the screen
    hs=win.winfo_screenheight() 	    #height of the screen
    x=ws-w/2; y=hs-h/2 		#x and y coord for the Tk root window
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Create hexagons on main canvas
    hexagon_generator=HexagonGenerator(HEX_SIZE)
    for row in range(ROWS):
      for col in range(COLS):
        pts=list(hexagon_generator(row, col))
        canvas.create_line(pts,width=2)
    #Append canvases
    canvastop.grid(row=1, column=1,columnspan=1)
    canvas.grid(row=2, column=1,columnspan=1)


SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
HEX_SIZE=30
HEX_HEIGHT=math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_SIDE=math.cos(math.radians(60)) * HEX_SIZE
CANVAS_WIDTH=HEX_SIDE+(HEX_SIZE * 2 - HEX_SIDE) * 8
CANVAS_HEIGHT=HEX_HEIGHT * 6
ROWS=int(math.ceil(float(CANVAS_HEIGHT)/HEX_SIZE/2))+1
COLS=12

SPRITE_WIDTH=180
SPRITE_HEIGHT=156

win=False
canvas=False
hexagon_generator=False
canvastop=False
canvasbottom=False
deck=False
tiles=False

def main():
  global win, canvas, hexagon_generator, canvastop, canvasbottom, deck, tiles
  deck=Deck()
  deck.createBoard()
  #Window and canvases
  canvasbottom.grid(row=3, column=1,columnspan=1)
  #Tiles and deck
  tiles=Tiles()
  #Deal tiles
  for i in range(1,6):
    tiles.deal(1,i,canvastop)
    tiles.deal(1,i,canvasbottom)
    #canvasbottom.create_image(tilex2, tiley2, image=tile2)
  #Put tiles on board
  #canvas.create_image(tilex4, tiley4, image=tile4)
  tiles.deal(3,3,canvas)
  tiles.deal(1,2,canvas)
  print("tiles.positions="+str(tiles.positions))

  #Bindings
  #win.bind('<Motion>', motion)
  canvas.bind('<Button>', motion) #type 4
  canvastop.bind('<Button>', motion) #type 4
  canvasbottom.bind('<Button>', motion) #type 4
  canvas.bind('<B1-Motion>', motion) #drag
  canvastop.bind('<B1-Motion>', motion) #drag
  canvasbottom.bind('<B1-Motion>', motion) #drag
  canvas.bind('<ButtonRelease-1>', motion) #release
  canvastop.bind('<ButtonRelease-1>', motion) #release
  canvasbottom.bind('<ButtonRelease-1>', motion) #release
  #canvas.bind('<Return>', motion)
  #canvas.bind('<Key>', motion)
  canvas.bind('<MouseWheel>', wheel)

  win.mainloop()

click_rowcolcanv=[]
def motion(event):
  #Logs
  #print(' keycode='+str(event.keycode))
  #print(' keysym='+str(event.keysym))
  if str(canvas)==str(event.widget):
    test=' main'
  elif str(canvastop)==str(event.widget):
    test=' top'
  elif str(canvasbottom)==str(event.widget):
    test=' botton'
  print(' widget='+str(event.widget) + test)
  print(' type='+str(event.type))
  print(' state='+str(event.state))
  print(' num='+str(event.num))
  print(' delta='+str(event.delta))
  x, y = event.x, event.y
  print(" x,y="+str((x,y)))
  print(" x_root, y_root=",str((event.x_root, event.y_root)))
  #with this I change to the canvas' coordinates: x = canvas.canvasx(event.x)
  #print canvas.find_closest(x, y)
  #
  #event.num = mouse number, state (press=16, release272,leave, motion,..),
  #http://epydoc.sourceforge.net/stdlib/Tkinter.Event-class.html
  #NB: move while dragging is type=6 (motion) state=272
  #NB: click                  type=4 (BPress) state=16
  #NB: release click          type=5 (BRelea) state=272

  if int(event.type) == 4 and int(event.state) == 16: #click
    rowcolcanv=onClick(event)
    global click_rowcolcanv
    click_rowcolcanv=rowcolcanv
    #wait ..
  elif int(event.type) == 5 and int(event.state) == 272: #release click
    rowcolcanv=onClick(event)
    if rowcolcanv==click_rowcolcanv: #released on same tile => rotate it
      tiles.rotate(rowcolcanv)
      click_rowcolcanv=[]
    elif rowcolcanv!=click_rowcolcanv: #released elsewhere. check and drop tile
      ind=tiles.getIndexFromRowColCanv(click_rowcolcanv)
      tile=tiles.photos[ind]
      canvas_origin = win.children[click_rowcolcanv[2][1:]]
      canvas_dest =   win.children[rowcolcanv[2][1:]]
      tiles.move(click_rowcolcanv[0],click_rowcolcanv[1],canvas_origin,rowcolcanv[0],rowcolcanv[1],canvas_dest)
      click_rowcolcanv=[]
  else :
    print('\n !!event not supported!! \n')
    print('{}, {}'.format(x, y))
  print('')

def wheel(event):
  pass

def onClick(event):
    #Find rowcolcanv ie offset and canvas
    x, y = event.x, event.y
    if str(event.widget) == str(canvas):
      print("pixel_to_off="+str(pixel_to_off(x,y))) #wrong for canvastop, eg 1.3 becomes 1,4
      rowcolcanv=list(pixel_to_off(x,y))
    elif str(canvastop)==str(event.widget) or str(canvasbottom)==str(event.widget):
      print("pixel_to_off_canvastopbottom="+str(pixel_to_off_canvastopbottom(x,y)))
      rowcolcanv=list(pixel_to_off_canvastopbottom(x,y))
    else:
      print('\n motion did not find the canvas! event.widget is :')
      print(str(event.widget))
    rowcolcanv.append(str(event.widget))
    return rowcolcanv


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

"""TO DO
distinguish drag vs click to rotate
maybe find position on click, and on release rotate if it is close
"""
