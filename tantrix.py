"""
install python-dev
sudo apt-get install python3-pil
sudo apt-get install python3-imaging-tk
aggdraw:
get the zip here: http://effbot.org/downloads#aggdraw
In some cases I have to use
export CFLAGS="-fpermissive"
then use the commands in the README ie:
python setup.py install

http://variable-scope.com/posts/hexagon-tilings-with-python
http://www.raywenderlich.com/1223/python-tutorial-how-to-generate-game-deck-
with-python-imaging-library

http://www.redblobgames.com/grids/hexagons/
"""
import math
import PIL.Image, PIL.ImageTk
#import aggdraw.Draw, aggdraw.Brush, aggdraw.Pen
try:
  import Tkinter as tk # for Python2
except:
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

class Board(object):
  def __init__(self):
    pass
  def pixel_to_off_canvastopbottom(self,x, y):
    col=math.ceil(float(x) / (HEX_SIZE * 2))
    return (1,col)
  def pixel_to_off(self,x, y):
    q = x * 2/3 / HEX_SIZE
    r = (-x / 3 + math.sqrt(3)/3 * y) / HEX_SIZE
    #print("self.cube_round in axial="+str(self.cube_round((q, -q-r, r))))
    return self.cube2off(self.cube_round((q, -q-r, r)))

  def cube2off(self,cube):
    '''convert cube to odd-q offset'''
    col = cube[0] + 1
    row = cube[2] + (cube[0] - (cube[0]%2)) / 2 + 1
    return (row,col)

  def hex_to_cube(self,h): # axial
      x = h[1]
      z = h[0]
      y = -x-z
      return (x, y, z) #return Cube(x, y, z)

  def cube_round(self,h):
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
  def createBoard(self):
    global win, canvas, hexagon_generator, canvastop, canvasbottom, board, deck
    win=tk.Tk()
    canvas=tk.Canvas(win, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, background='lightgrey')
    canvastop=tk.Canvas(win, height=HEX_HEIGHT, width=CANVAS_WIDTH, background='lightgrey')
    canvasbottom=tk.Canvas(win, height=HEX_HEIGHT, width=CANVAS_WIDTH, background='lightgrey')
    w=CANVAS_WIDTH+5
    h=CANVAS_HEIGHT+HEX_HEIGHT*2+5
    ws=win.winfo_screenwidth()    #width of the screen
    hs=win.winfo_screenheight()       #height of the screen
    x=ws-w/2; y=hs-h/2    #x and y coord for the Tk root window
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Create hexagons on main canvas
    hexagon_generator=HexagonGenerator(HEX_SIZE)
    for row in range(ROWS):
      for col in range(COLS):
        pts=list(hexagon_generator(row, col))
        canvas.create_line(pts,width=2)
    #Append canvases
    #canvastop.grid(row=1, column=1,columnspan=1,expand=1)
    #canvas.grid(row=2, column=1,columnspan=1,expand=1)
    #canvasbottom.grid(row=3, column=1,columnspan=1,expand=1)
    canvastop.pack(fill='both',expand=1,side='top')
    canvas.pack(fill='both',expand=1)
    canvasbottom.pack(fill='both',expand=1,side='bottom')

class Tile(object):
  def __init__(self, num, angle=0):
    """tile object containing a tile in PhotoImage format"""
    global board
    #tile is a PhotoImage (required by Canvas' create_image) and its number
    tilePIL=SPRITE.crop((3+SPRITE_WIDTH*(num-1),4,
           SPRITE_WIDTH*(num)-2,SPRITE_HEIGHT)).resize((HEX_SIZE*2,int(HEX_HEIGHT)))
    if angle != 0:
      tilePIL=tilePIL.rotate(angle, expand=0)
    self.tile = PIL.ImageTk.PhotoImage(tilePIL)
    self.color = colors[num-1]
    self.angle = angle
  def getColor(self):
    basecolor=self.color
    n=self.angle/60
    return basecolor[n:] + basecolor[:n]
  def __str__(self):
    return 'tile color and angle: '+self.getColor()+' '+str(self.angle)+' '
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
    canvasID=str(canvas)
    if canvasID.endswith(str(canvastop)): #top canvas
      #print('\ntop:   '+str(canvas))
      x = HEX_SIZE + ((HEX_SIZE * 2) * (col - 1))
      y = HEX_HEIGHT / 2
    elif canvasID.endswith(str(canvasbottom)): #bottom canvas
      #print('\nbottom:'+str(canvas))
      x = HEX_SIZE + ((HEX_SIZE * 2) * (col - 1))
      y = HEX_HEIGHT / 2
    else: #main canvas
      #print('\nmain  :'+str(canvas))
      x = HEX_SIZE + ((HEX_SIZE * 2 - HEX_SIDE) * (col - 1))
      y = HEX_HEIGHT / 2 + (HEX_HEIGHT * (row - 1) + HEX_HEIGHT / 2 * ((col + 1) % 2))
    #print(x,y)
    yield x
    yield y
    yield canvasID

  def place(self,row,col,canvas,tile):
    '''Place image from tile instance on canvas. No update .positions. Return the itemid.'''
    #Get the pixels
    tilex,tiley,canvasID=self.tilePixels(row,col,canvas)
    itemid=canvas.create_image(tilex, tiley, image=tile)
    #Update positions - not needed!
    #Update window
    win.update()
    return itemid
 
class Deck(object):
  def __init__(self):
    self.tiles=[]       #this contains tile in PhotoImage format
    self.positions=[]   #(row,col,str(canvas))
    self.itemids=[]     #itemid=canvas.create_image()
    self.undealt=range(1, 57) #1:56
    self.dealt=[]
  #def __call__(self, ran):
  def getIndexFromTileNumber(self,num):
    return self.dealt.index(num)
  def getIndexFromRowColCanv(self,rowcolcanv):
    ind=deck.positions.index(tuple(rowcolcanv))
    return ind
  def getTileNumberFromRowColCanv(self,rowcolcanv):
    pass #self.getTileNumberFromIndex(self.getIndexFromRowColCanv(rowcolcanv))
  def getTileNumberFromIndex(self,ind):
    pass #self.dealt[ind]

  def remove(self,row,col,canvas):
    ind=self.getIndexFromRowColCanv((row,col,str(canvas)))
    itemid=self.itemids[ind]
    #Delete it
    canvas.delete(itemid)
    #Update properties
    pos=self.positions.pop(ind)
    tileobj=self.tiles.pop(ind)
    self.itemids.pop(ind)
    #NB: remove tile from deck dealt. leaving undealt as is
    num=deck.dealt.pop(ind)
    return (pos,num,tileobj)
    
  def move(self,row1,col1,canvas1,row2,col2,canvas2):
    #Return if destination is already occupied
    if (row2,col2,str(canvas2)) in deck.positions:
      return 0
    ind=self.getIndexFromRowColCanv((row1,col1,str(canvas1)))    
    #Remove tile. properties get updated
    (posold,num,tileobj)=self.remove(row1,col1,canvas1)
    #Place tile on new place    
    itemid=tileobj.place(row2,col2,canvas2,tileobj.tile)
    #Update storage
    self.tiles.append(tileobj)
    self.positions.append((row2,col2,str(canvas2)))
    self.itemids.append(itemid)
    deck.dealt.append(num)
    #Update window
    win.update()
    return 1

  def rotate(self,rowcolcanv):
    global win
    #Find the index
    try:
      ind=self.getIndexFromRowColCanv(tuple(rowcolcanv))
      print('found at '+str(ind))
    except:
      print('not found: '+str(rowcolcanv)+' in')
      print(deck.positions)
      return
    #Spawn the rotated tile
    tileobj=Tile(deck.dealt[ind], self.tiles[ind].angle-60)
    tile=tileobj.tile    
    #Update tiles list
    self.tiles[ind]=tileobj
    #Place the tile
    canvas=win.children[rowcolcanv[2][1:]]
    itemid=tileobj.place(rowcolcanv[0],rowcolcanv[1],canvas,tile)
    self.itemids[ind]=itemid
    print(tileobj)

  def deal(self,row,col,canvas,num='random'):
    #Random tile if num is not set
    if num =='random':
      ran = random.randrange(0, len(self.undealt)) #0:55
    num=self.undealt.pop(ran)   #1:56
    #Get tile as PhotoImage
    tileobj=Tile(num)
    tile=tileobj.tile
    #Store tile instance
    self.tiles.append(tileobj)
    #Place on canvas
    itemid=tileobj.place(row,col,canvas,tile)
    #print('itemid='+str(itemid))
    self.itemids.append(itemid)
    #store dealt/undealt tile numbers
    self.dealt.append(num)
    self.positions.append((row,col,str(canvas)))


SPRITE = PIL.Image.open("./img/tantrix_sprite.png")
SPRITE_WIDTH=180
SPRITE_HEIGHT=156

HEX_SIZE=30
HEX_HEIGHT=math.sin(math.radians(120)) * HEX_SIZE * 2
HEX_SIDE=math.cos(math.radians(60)) * HEX_SIZE
CANVAS_WIDTH=HEX_SIDE+(HEX_SIZE * 2 - HEX_SIDE) * 8
CANVAS_HEIGHT=HEX_HEIGHT * 6
ROWS=int(math.ceil(float(CANVAS_HEIGHT)/HEX_SIZE/2))+1
COLS=12

colors=tuple(['ryybrb','byybrr','yrrbby','bgrbrg','rbbryy','yrbybr','rbbyry','ybbryr','rbyryb','byyrbr','yrrbyb','brryby','yrrybb','ryybbr','rggryy','yrrygg','ryygrg','gyyrgr','yrrgyg','grrygy','yggrry','gyygrr','gyyrrg','bggbrr','brrggb','grrgbb','grrbgb','rbbggr','brrgbg','rbbrgg','yggryr','gyrgry','rggyry','rgyryg','yrgygr','bggrbr','rbbgrg','gbbrgr','grbgbr','bgrbrg','rggbrb','rbgrgb','gbbyyg','ybgygb','bggyyb','yggbyb','ybbygg','bggbyy','gyygbb','bgybyg','gybgby','bggyby','byygbg','gyybgb','ybbgyg','gbbygy'])
win=False
canvas=False
hexagon_generator=False
canvastop=False
canvasbottom=False
board=False
deck=False
click_rowcolcanv=[]

def main():
  global win, canvas, hexagon_generator, canvastop, canvasbottom, board, deck
  board=Board()
  board.createBoard()
  #Deck
  deck=Deck()
  #Deal deck

  
  for i in range(1,6):
    deck.deal(1,i,canvastop)
    deck.deal(1,i,canvasbottom)
    #canvasbottom.create_image(tilex2, tiley2, image=tile2)
  #Put deck on board
  #canvas.create_image(tilex4, tiley4, image=tile4)
  deck.deal(1,2,canvas)
  deck.deal(3,3,canvas)
  #print("deck.positions="+str(deck.positions))
  #Check for duplicates. It should never happen
  dupl=set([x for x in deck.dealt if deck.dealt.count(x) > 1])
  if len(dupl)>0:
    raise UserWarning("Duplicates in deck.dealt!!!")
  #Bindings
  #win.bind('<Motion>', clickCallback)
  canvas.bind('<Button>', clickCallback) #type 4
  canvastop.bind('<Button>', clickCallback) #type 4
  canvasbottom.bind('<Button>', clickCallback) #type 4
  canvas.bind('<B1-Motion>', clickCallback) #drag
  canvastop.bind('<B1-Motion>', clickCallback) #drag
  canvasbottom.bind('<B1-Motion>', clickCallback) #drag
  canvas.bind('<ButtonRelease-1>', clickCallback) #release
  canvastop.bind('<ButtonRelease-1>', clickCallback) #release
  canvasbottom.bind('<ButtonRelease-1>', clickCallback) #release
  #canvas.bind('<Return>', clickCallback)
  #canvas.bind('<Key>', clickCallback)
  #canvas.bind('<MouseWheel>', wheel)
  win.mainloop()

def clickCallback(event):
  global click_rowcolcanv
  x, y = event.x, event.y
  #Logs
  if str(canvas)==str(event.widget):
    test=' main'
  elif str(canvastop)==str(event.widget):
    test=' top'
  elif str(canvasbottom)==str(event.widget):
    test=' botton'
  #logs
  if 0:
    print(' widget='+str(event.widget) + test)
    print(' type='+str(event.type))
    print(' state='+str(event.state))
    print(' num='+str(event.num))
    print(' delta='+str(event.delta))
    print('{}, {}='.format(x, y))
    print(" x_root, y_root=",str((event.x_root, event.y_root)))
  #with this I change to the canvas' coordinates: x = canvas.canvasx(event.x)
  #print canvas.find_closest(x, y)
  #
  #event.num = mouse number, state (press=16, release272,leave, clickCallback,..),
  #http://epydoc.sourceforge.net/stdlib/Tkinter.Event-class.html
  #NB: move while dragging is type=6 (clickCallback) state=272
  #NB: click                  type=4 (BPress) state=16
  #NB: release click          type=5 (BRelea) state=272
  if int(event.type) == 4 and int(event.state) == 16: #click
    rowcolcanv=onClickRelease(event)
    click_rowcolcanv=rowcolcanv
    #wait ..
  elif int(event.type) == 5 and int(event.state) == 272: #release click
    rowcolcanv=onClickRelease(event)  #todo here I could use simpler onClickRelease
    print('rowcolcanv=      '+str(rowcolcanv))
    print('click_rowcolcanv='+str(click_rowcolcanv))
    if len(rowcolcanv)==0:
      return
    if rowcolcanv==click_rowcolcanv: #released on same tile => rotate it
      #Rotate
      deck.rotate(rowcolcanv)
    elif rowcolcanv!=click_rowcolcanv: #released elsewhere => drop tile there.
      #move tile if place is not occupied already:
      canvas_origin, canvas_dest = win.children[click_rowcolcanv[2][1:]], win.children[rowcolcanv[2][1:]]
      deck.move(click_rowcolcanv[0],click_rowcolcanv[1],canvas_origin, rowcolcanv[0],rowcolcanv[1],canvas_dest)
    #Reset the coordinates of the canvas where the button down was pressed
    click_rowcolcanv=[]
  else :
    print('\n !event not supported \n')
  print('')

def onClickRelease(event):
  x, y = event.x, event.y
  if x <= 0 or x >= event.widget.winfo_reqwidth():
    print('x outside the original widget')
    return tuple()
  elif x < event.widget.winfo_reqwidth():
    print('x is inside the original widget')
  else:
    print('cannot be determined where x is vs original widget')
    return tuple()
  #event.x and event.y
  ytop=canvastop.winfo_reqheight()
  ymain=ytop+canvas.winfo_reqheight()
  ybottom=ymain+canvasbottom.winfo_reqheight()
  if str(event.widget)==str(canvastop):
    yrel=y
  elif str(event.widget)==str(canvas):
    yrel=y+ytop
  elif str(event.widget)==str(canvasbottom):
    yrel=y+ymain
  else: 
    raise UserWarning("onClickRelease: cannot determine yrel")
    return tuple()
  
  if yrel<=0 or yrel>=ybottom:
    print('x outside the original widget')
    return tuple()
  elif yrel<=ytop:
    print('x inside canvastop')
    rowcolcanv=list(board.pixel_to_off_canvastopbottom(x,y))
    rowcolcanv.append(str(canvastop))
  elif yrel<=ymain:
    print('x inside canvas')
    rowcolcanv=list(board.pixel_to_off(x,yrel-ytop))
    rowcolcanv.append(str(canvas))
  elif yrel<=ybottom:
    print('x inside canvasbottom')
    rowcolcanv=list(board.pixel_to_off_canvastopbottom(x,yrel-ymain))
    rowcolcanv.append(str(canvasbottom))
  else: 
    raise UserWarning("onClickRelease: cannot destination canvas")
    return tuple()
  return rowcolcanv

def onClick2(event):
  #Find rowcolcanv ie offset and canvas
  x, y = event.x, event.y
  if str(event.widget) == str(canvas):
    print("board.pixel_to_off="+str(board.pixel_to_off(x,y))) #wrong for canvastop, eg 1.3 becomes 1,4
    rowcolcanv=list(board.pixel_to_off(x,y))
  elif str(canvastop)==str(event.widget) or str(canvasbottom)==str(event.widget):
    print("board.pixel_to_off_canvastopbottom="+str(board.pixel_to_off_canvastopbottom(x,y)))
    rowcolcanv=list(board.pixel_to_off_canvastopbottom(x,y))
  else:
    print('\n clickCallback did not find the canvas! event.widget is :')
    print(str(event.widget))
  rowcolcanv.append(str(event.widget))
  return rowcolcanv


def isrotation(s1,s2):
     return len(s1)==len(s2) and s1 in 2*s2

def isrot(src, dest):
  # Make sure they have the same size
  #if len(src) != len(dest):
  #  return False
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
cannot drag from top (or bottom) to main canvas. the problem is in onClickRelease because  event.widget is still top canvas. 
coordinates however indicate that i released outside the top canvas, so maybe use that x,y=(68, 352)

"""
