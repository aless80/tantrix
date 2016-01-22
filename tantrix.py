"""
install python-dev
sudo apt-get install python3-pil
sudo apt-get install python3-imaging-tk

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
import config as cfg
import HexagonGenerator as hg
import Board as bd

'''
class Board(object):
  def pixel_to_off_canvastopbottom(self, x, y):
    col = math.floor(float(x) / (cfg.HEX_SIZE * 2))
    return (0, col)
  def pixel_to_off(self,x, y):
    q = x * 2/3 / cfg.HEX_SIZE
    r = (-x / 3 + math.sqrt(3)/3 * y) / cfg.HEX_SIZE
    #print("self.cube_round in cube= " +str(self.cube_round((q, -q-r, r))))
    cube = (q, -q-r, r)
    cuberound = self.cube_round(cube)
    offset = self.cube_to_off(cuberound)
    return offset
  def pixel_to_hex(self, x, y):
    q = x * 2/3 / cfg.HEX_SIZE
    r = (-x / 3 + math.sqrt(3)/3 * y) / cfg.HEX_SIZE
    #print("self.cube_round in cube= " +str(self.cube_round((q, -q-r, r))))
    return self.hex_round((q, r))
    #return self.cube_to_hex(self.cube_round((q, -q-r, r)))
  def hex_round(self, hex):
    return self.cube_to_hex(self.cube_round(self.hex_to_cube(hex)))
  def cube_to_off(self,cube):
    """Convert cube to odd-q offset"""
    row = cube[0]
    col = cube[2] + (cube[0] - (cube[0]%2)) / 2
    return (row, col)
  def off_to_cube(self, row, col):
    # convert odd-q offset to cube
    x = row
    z = col - (x - (x%2)) / 2
    y = -x-z
    return (x,y,z)
  def cube_to_hex(self, hex):
    """Convert cube coordinates to axial"""
    q = hex[0]
    r = hex[1]
    return (q, r)
  def hex_to_cube(self, h): # axial
      x = h[1]
      z = h[0]
      y = -x-z
      return (x, y, z) #return Cube(x, y, z)
  def cube_round(self, h):
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
  def __init__(self):
  #  pass
  #def __call__(self):
    global cfg.win, cfg.canvasmain, cfg.canvastop, cfg.canvasbottom, hexagon_generator, board, deck
    global btn1, btn2, btnConf, btnReset
    cfg.win = tk.Tk()
    cfg.canvasmain = tk.Canvas(cfg.win, height= cfg.CANVAS_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey', name=".canvasmain")
    cfg.canvastop = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name=".canvastop")
    cfg.canvasbottom = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name=".canvasbottom")
    w = cfg.CANVAS_WIDTH + 5
    h = cfg.CANVAS_HEIGHT + cfg.HEX_HEIGHT * 2 + 5
    ws = cfg.win.winfo_screenwidth()    #width of the screen
    hs = cfg.win.winfo_screenheight()       #height of the screen
    x = ws - w / 2; y = hs - h / 2    #x and y coord for the Tk root window
    cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Create hexagons on main canvas
    hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
    for row in range(cfg.ROWS):
      for col in range(cfg.COLS):
        pts = list(hexagon_generator(row, col))
        cfg.canvasmain.create_line(pts, width =2)
    #Append canvases
    cfg.canvastop.grid(row = 0, column = 0)#,expand="-in")
    cfg.canvasmain.grid(row = 1, column = 0, rowspan = 5)#,expand="-ipadx")
    cfg.canvasbottom.grid(row = 6, column = 0)#,expand="-padx")
    #Button1
    btn1 = tk.Button(cfg.win, width=6, text="Refill\nhand",  bg="yellow", name = "btn1")
    #Add cfg.canvastop to tags, so button click will be processed by cfg.canvastop!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, cfg.canvastop)
    #btn1.bindtags(tuple(bindtags))
    btn1.bind('<ButtonRelease-1>', buttonClick)
    btn1.grid(row=0, column=1,columnspan=1)
    #Button2
    btn2 = tk.Button(cfg.win, width=6, text="Refill\nhand",  bg="red", name = "btn2") #, height=int(round(cfg.HEX_HEIGHT))-1
    #Add canvasbpttom to tags, so button click will be processed by cfg.canvasbottom!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, cfg.canvasbottom)
    #btn2.bindtags(tuple(bindtags))
    btn2.bind('<ButtonRelease-1>', buttonClick)
    btn2.grid(row=6, column=1,columnspan=1)
    #Confirm button
    btnConf = tk.Button(cfg.win, text="Confirm\nmove",  bg="cyan",
                      width=6, name = "btnConf") #padx=5,
    btnConf.bind('<ButtonRelease-1>', buttonClick)
    btnConf.grid(row=2, column=1, columnspan=1)
    #Reset button
    btnReset= tk.Button(cfg.win, text="Reset\ndeck",  bg="cyan",
                      width=6, name = "btnReset")
    btnReset.bind('<ButtonRelease-1>', buttonClick)
    btnReset.grid(row=4, column=1,columnspan=1)
    #Update window
    cfg.win.update()
    cfg.win.winfo_height() #update before asking size!
    cfg.win.geometry(str(cfg.canvasmain.winfo_width() + 100) + "x" + str(int(round(cfg.CANVAS_HEIGHT + 2 * cfg.HEX_HEIGHT))))
    cfg.win.update()
'''


class Deck(object):
  def __init__(self):
    self.tiles = []       #this contains tile in PhotoImage format
    self.positions = []   #(row, col,str(canvas))
    self.itemids = []     #itemid = canvas.create_image()
    self.undealt =range(1, 57) #1:56
    self.dealt = [] #1:56
    self.positionstable = [] #(row, col, num)
    self.positionshand1 = [] #(row, col, num)
    self.positionshand2 = [] #(row, col, num)
  def get_index_from_tile_number(self, num):
    return self.dealt.index(num)
  def get_index_from_rowcolcanv(self, rowcolcanv):
    try:
      return self.positions.index(tuple(rowcolcanv))
    except:
      return None
  def get_tile_number_from_rowcolcanv(self, rowcolcanv, notimplemented):
    pass #self.getTileNumberFromIndex(self.get_index_from_rowcolcanv(rowcolcanv))
  def get_tile_number_from_index(self, ind):
    try:
      return self.dealt[ind]
    except:
      return None

  def get_neighbors(self, row, col=False):
    """Find neighbors of a hexagon in the main canvas"""
    if type(row) == list or type(row) == tuple:
      row, col,bin = row
    row, col = int(row),int(col)
    #Convert to cube coordinates, then add cfg.directions to cube coordinate
    neigh = []
    cube = list(board.off_to_cube(row, col))
    for dir in cfg.directions:
      c = map(lambda x, y : x + y, cube, dir)
      off = board.cube_to_off(c)
      #Get rowcolcanv
      rowcolcanv = off
      rowcolcanv += (".canvasmain",)
      #Find if there is a tile on rowcolcanv
      ind = self.get_index_from_rowcolcanv(rowcolcanv)
      if ind is not None:
        neigh.append(ind)
    return neigh #list of ind where tile is present [(0,0),..]
  def get_neighboring_colors(self, row, col = False):
    """Return the neighboring colors as a list of (color,ind)"""
    if type(row) != int:
      row, col,bin = row
    neigh = self.get_neighbors(row, col) #[(0,0),..]
    color_dirindex_neighIndex = []
    if len(neigh) > 0:
      for n in neigh:   #(0,0)
        wholecolor = self.tiles[n].color
        #here get direction and right color
        rowcolcanv = self.positions[n]
        cube = board.off_to_cube(rowcolcanv[0],rowcolcanv[1])
        home = board.off_to_cube(row, col)
        founddir = map(lambda dest, hom : dest-hom,cube,home)
        dirindex = cfg.directions.index(founddir)
        color = wholecolor[(dirindex + 3) % 6]
        color_dirindex_neighIndex.append(tuple([color,dirindex,n]))
    return color_dirindex_neighIndex #[('b',1),('color',directionIndex),]

  def remove(self, row, col, canvas):
    rowcolcanv = tuple([row, col, str(canvas)])
    ind = self.get_index_from_rowcolcanv(rowcolcanv)
    itemid = self.itemids[ind]
    #Delete it
    canvas.delete(itemid)
    #Update properties
    #Update confirmed storage
    if not TRYING:
      #ind = self.get_index_from_rowcolcanv(rowcolcanv) #not needed here
      n = self.get_tile_number_from_index(ind)
      rowcolnum = tuple([row, col, n])
      if str(canvas) == ".canvasmain":
        self.positionstable.remove(rowcolnum)
      elif str(canvas) == ".canvastop":
        print("removing: positionshand1 and row, col, ind")
        self.positionshand1.remove(rowcolnum)
      elif str(canvas) == ".canvasbottom":
        self.positionshand2.remove(rowcolnum)
    #
    pos = self.positions.pop(ind)
    tile = self.tiles.pop(ind)
    self.itemids.pop(ind)
    #NB: remove tile from deck dealt. leaving undealt as is
    num = deck.dealt.pop(ind)
    return (pos,num,tile)
  def is_occupied(self, rowcolcanv):
    """Return whether an hexagon is already occupied:
    deck.isOccupied(rowcolcanv)    """
    return rowcolcanv in self.positions
  def movable(self, row1, col1, canvas1, row2, col2, canvas2):
    if TRYING:
      return True
    #Ignore movement when:
    if self.is_occupied((row2, col2, str(canvas2))):
      #Return False if destination is already occupied
      print('Destination tile is occupied: ' + str((row2, col2, str(canvas2))))
      return False
    if canvas2 == cfg.canvasmain:
      #Movement to main canvas.
      #Ok if there are no tiles on canvas
      if ".canvasmain" not in [p[2] for p in self.positions]: #todo: later on maybe check score
                                # or something that is populated when the first tile is placed
        return True
      #Check if tile matches colors
      ind1 = self.get_index_from_rowcolcanv((row1, col1, str(canvas1)))
      tile = deck.tiles[ind1]
      #NB The following does not allow you to move the same tile one position away.
      #That should not be of any use though so ok
      ok = tile.tile_match_colors(tuple([row2, col2, str(canvas2)]))
      if not ok:
        print('No color matching')
        return ok
    elif canvas1 != cfg.canvasmain and canvas1 != canvas2:
      #Return False if trying to move from bottom to top or vice versa
      print('trying to move from bottom to top or vice versa')
      return False
    elif canvas1 == cfg.canvasmain and canvas2 != cfg.canvasmain:
      #Return False if trying to move from cfg.canvasmain to top or bottom
      print('trying to move from cfg.canvasmain to top or bottom')
      return False
    return True

  def move(self, row1, col1, canvas1, row2, col2, canvas2):
    if not self.movable(row1, col1, canvas1, row2, col2, canvas2):
      print("You cannot move the tile as it is to this hexagon")
      return 0
    #Remove tile. properties get updated
    (posold, num, tile)= self.remove(row1, col1, canvas1)
    #Place tile on new place
    itemid = tile.place(row2, col2, canvas2, tile.tile)
    #Update storage
    rowcolcanv2 = tuple([row2, col2, str(canvas2)])
    self.tiles.append(tile)
    self.dealt.append(num) #before positionstable/positionshand1!
    self.positions.append(rowcolcanv2)
    self.itemids.append(itemid)
    #Update confirmed storage after the rest fo the storage
    if not TRYING:
      ind = self.get_index_from_rowcolcanv(rowcolcanv2) #I could use len(self.positions) - 1
      n = num #self.get_tile_number_from_index(ind)
      rowcolnum = tuple([row2, col2, n])
      if str(canvas2) == ".canvasmain":
        self.positionstable.append(rowcolnum)
      elif str(canvas2) == ".canvastop":
        self.positionshand1.append(rowcolnum)
      elif str(canvas2) == ".canvasbottom":
        self.positionshand2.append(rowcolnum)
    #Update buttons
    btnReset.configure(state="active")
    #Update window
    cfg.win.update()
    return 1
  def rotate(self, rowcolcanv):
    #global cfg.win
    #Find the index
    try:
      ind= self.get_index_from_rowcolcanv(rowcolcanv)
      print('found at ' + str(ind))
    except:
      print('not found: ' + str(rowcolcanv) +' in')
      print(self.positions)
      return
    #Check if color would match
    if str(rowcolcanv[2]) == ".canvasmain":
      if not self.tiles[ind].tile_match_colors(rowcolcanv, -60):
        print("You cannot rotate the tile")
        return
    #Spawn the rotated tile
    tile = Tile(self.dealt[ind], self.tiles[ind].angle - 60)
    #Update tiles list
    self.tiles[ind] = tile
    #Place the tile
    canvas = cfg.win.children[rowcolcanv[2][1:]]
    itemid = tile.place(rowcolcanv[0],rowcolcanv[1],canvas,tile.tile)
    self.itemids[ind] = itemid
    print(tile)
  def deal(self, row, col, canv, num='random'):
    row = int(row)
    col = int(col)
    #Random tile if num is not set
    if num =='random':
      ran = random.randrange(0, len(self.undealt)) #0:55
    num= self.undealt.pop(ran)   #1:56
    #Get tile as PhotoImage
    tileobj = Tile(num)
    tile = tileobj.tile
    #Store tile instance
    self.tiles.append(tileobj)
    #Place on canvas
    itemid = tileobj.place(row, col, canv,tile)
    #print('itemid=' + str(itemid))
    self.itemids.append(itemid)
    #store dealt/undealt tile numbers
    self.dealt.append(num)
    rowcolcanv = tuple([row, col, str(canv)])
    self.positions.append(rowcolcanv)
    #Update confirmed storage
    if 1: #not TRYING:
      ind = self.get_index_from_rowcolcanv(rowcolcanv) #I could use len(self.positions) - 1
      n = self.get_tile_number_from_index(ind)
      rowcolnum = tuple([row, col, n])
      if str(canv) == ".canvasmain":
        self.positionstable.append(rowcolnum)
      elif str(canv) == ".canvastop":
        self.positionshand1.append(rowcolnum)
      elif str(canv) == ".canvasbottom":
        self.positionshand2.append(rowcolnum)

  def get_tiles_in_deck(self, canvas):
    count = 0
    rows = []
    cols = []
    for pos in self.positions:
      r, q, c = pos
      if str(c) == str(canvas):
        rows.append(r)
        cols.append(q)
        count +=1
    yield count
    yield rows
    yield cols

  def refill_deck(self, canv):
    #Check how many tiles there are
    count, row, cols = self.get_tiles_in_deck(canv)
    if count == 6:
      return 0
    #Flush existing tiles to left
    for i in range(0, len(cols)):
      if cols[i] > i:
        deck.move(0, cols[i], canv, 0, i, canv)
    #Refill deck
    for i in range(count, 6):
      self.deal(0, i, canv)
    return 1
  
  def reset(self):
    print("Reset table")
    def reposition(table, canvas): #todo: canv is a waste
      '''Move the tiles back to the positions in table (e.g. positionstable and positionshand1/2)'''
      #use tile number: .positionstable thinks it is in a different canvas than .positions
      for rowcolnum in table: #(row, col, num)
        #get current ind of
        row2, col2, num = rowcolnum
        ind = self.get_index_from_tile_number(num)
        #get current rowcolcanv from ind
        rowcolcanv1 = self.positions[ind]
        if rowcolcanv1 != tuple([row2, col2, str(canvas)]):
          row1, col1, canvasID1 = rowcolcanv1 #todo canvas1 must not be string
          canvas1 = cfg.win.children[canvasID1[1:]]
          self.move(row1, col1, canvas1, row2, col2, canvas)
    #positionstable references the tiles on the table. Put tiles back there
    reposition(self.positionstable, cfg.canvasmain)
    #positionshand1 and 2 reference the tiles on the players' hands. Put them back there
    reposition(self.positionshand1, cfg.canvastop)
    reposition(self.positionshand2, cfg.canvasbottom)

  def get_tiles_in_canvas(self, canvasID):
    '''Get the tiles as list of rowcolcanv currently present in a canvas, ie present in .positions'''
    canvasID = str(canvasID)
    rowcolcanvs = []
    for pos in deck.positions:
      row, col, canv = pos
      if canv == canvasID:
        rowcolcanvs.append(tuple([row, col, canvasID]))
    return rowcolcanvs

  def is_confirmable(self):
    curr_tiles_on_table = len(self.get_tiles_in_canvas(cfg.canvasmain))
    curr_tiles_on_hand1 = len(self.get_tiles_in_canvas(cfg.canvastop))
    curr_tiles_on_hand2 = len(self.get_tiles_in_canvas(cfg.canvasbottom ))
    tiles_on_table = len(self.positionstable)
    if 0:
      print("tiles_on_table=" + str(tiles_on_table))
      print("curr_tiles_on_table=" + str(curr_tiles_on_table))
      print("len(.positionshand1)=" + str(len(self.positionshand1)))
      print("curr_tiles_on_hand1=" + str(curr_tiles_on_hand1))
      print("len(.positionshand2)=" + str(len(self.positionshand2)))
      print("curr_tiles_on_hand2=" + str(curr_tiles_on_hand2))

    if curr_tiles_on_hand1 + curr_tiles_on_hand2 > 11:
      print("no tiles from hand1 or hand2 are out")
    elif curr_tiles_on_hand1 + curr_tiles_on_hand2 < 11:
      print("More than 1 tile from hand1 and hand2 are out")
    elif tiles_on_table - curr_tiles_on_table == 0:
      print("no tiles were added to the table")
    elif tiles_on_table - curr_tiles_on_table > 1:
      raise UserWarning("more than one tile were added to the table. I should not see this msg")
    elif curr_tiles_on_table - tiles_on_table < 0:
      raise UserWarning("How come there are less tiles on table that in .positionstable?")
    #Return True
    elif curr_tiles_on_table - tiles_on_table == 1 and curr_tiles_on_hand1 + curr_tiles_on_hand2 == 11:
      return True
    else:
      raise UserWarning("is_confirmable: Cannot determine if confirmable")
      return False
    #Raise error

  def process_move(self):
    if TRYING:
      return False
    print("process_move. TRYING="+str(TRYING))
    if not self.is_confirmable():
      print("Cannot confirm this move. Reset the table and move only one tile from your hand")
    #Update each confirmed table (.positionstable, .positionshand1, .positionshand2)

    for ind, pos in enumerate(self.positions):
      row, col, canv = pos
      if canv == ".canvasmain":
        num = deck.get_tile_number_from_index(ind)
        rowcolnum = tuple([row, col, num])
        if rowcolnum not in self.positionstable:
          #.positionstable must get one tile more
          self.positionstable.append(rowcolnum)
          #.positionshand1 or .positionshand2 must remove one tile

          match = filter(lambda t : t[2] == num, [tup for tup in self.positionshand1])
          if len(match) == 1:
            self.positionshand1.remove(match[0])
          elif len(match) > 1:
            raise UserWarning("process_move: .positionshand1 has more than one tile played!")

          match = filter(lambda t : t[2] == num, [tup for tup in self.positionshand2])
          if len(match) == 1:
            self.positionshand2.remove(match[0])
          elif len(match) > 1:
            raise UserWarning("process_move: .positionshand2 has more than one tile played!")

          #todo I think I can use a break here
    print(self.positionstable)
    print(self.positionshand1)
    print(self.positionshand2)
    return True

class Tile(object):
  def __init__(self, num, angle=0):
    """tile object containing a tile in PhotoImage format"""
    global board
    #.tile property is a PhotoImage (required by Canvas' create_image) and its number
    tilePIL = cfg.SPRITE.crop((cfg.SPRITE_WIDTH * (num - 1), 4,
           cfg.SPRITE_WIDTH * num - 2, cfg.SPRITE_HEIGHT)).resize((cfg.HEX_SIZE * 2, int(cfg.HEX_HEIGHT)))
    if angle != 0:
      tilePIL = tilePIL.rotate(angle, expand = 0)
    self.tile = PIL.ImageTk.PhotoImage(tilePIL)
    self.color = cfg.colors[num-1]
    self.angle = angle
  #def __str__(self):
  #  return 'tile color and angle: ' +self.getColor() +' ' + str(self.angle) +' '
  def getColor(self):
    basecolor = self.color
    n = self.angle/60
    return basecolor[n:] + basecolor[:n]

  def tile_match_colors(self, rowcolcanv, angle=0):
    #No color matching when user is trying things
    if TRYING == True:
      print("TRYING is True, so no color check")
      return True
    #Get neighboring colors
    neighcolors = deck.get_neighboring_colors(rowcolcanv)
    #Angle
    basecolor = self.getColor()
    n = angle/60
    tilecolor = basecolor[n:] + basecolor[:n]
    for nc in neighcolors:
      if tilecolor[nc[1]] != nc[0]:
        print("neighbors: " + str(deck.get_neighbors(rowcolcanv)))
        print("tilecolor = " + str(tilecolor) + " " + str(nc[1]) + " " + nc[0])
        #NB cannot move tile one tile away because current tile is present. I do not see any case in which that is what i want
        return False
    return True

  def tile_pixels(self, row, col, canv):
    """Given row, col and canvas, return the pixel coordinates of the center
    of the corresponding hexagon

    if canvas.find_withtag(tk.CURRENT):
        #canvas.itemconfig(tk.CURRENT, fill="blue")
        canvas.update_idletasks()
        canvas.after(200)
        canvas.itemconfig(CURRENT, fill="red")
        """
    #I need the coordinates on the canvas
    if str(canv) == ".canvasmain":
      x = cfg.HEX_SIZE + (cfg.HEX_SIZE  + cfg.HEX_SIDE) * row
      y = cfg.HEX_HEIGHT / 2 + cfg.HEX_HEIGHT * col + cfg.HEX_HEIGHT / 2 * (row % 2)
    else: #bottom or top canvases
      x = cfg.HEX_SIZE + ((cfg.HEX_SIZE * 2) * col)
      y = cfg.HEX_HEIGHT / 2
    yield x
    yield y

  def place(self, row, col, canv,tile):
    """Place image from tile instance on canvas. No update .positions. Return the itemid."""
    #Get the pixels
    tilex,tiley = self.tile_pixels(row, col, canv)
    itemid = canv.create_image(tilex, tiley, image = tile)
    #Update positions - not needed!
    #Update window
    cfg.win.update()
    return itemid


class Hand(object):
  def __init__(self,canv):
    #Choose a color for the player
    avail_colors = cfg.PLAYERCOLORS
    ran = random.randrange(0, len(cfg.PLAYERCOLORS))
    self.playercolor = cfg.PLAYERCOLORS.pop(ran)
    #todo Color the corresponding button
    self.playercolor

    for i in range(0, 6): #todo maybe use the new refill_deck
      deck.deal(0, i, canv)
  def refill(self, canv):
    pass


TRYING = True

#todo Move these globals to Hexagon generator?
'''cfg.HEX_SIZE = 30
cfg.HEX_HEIGHT = math.sin(math.radians(120)) * cfg.HEX_SIZE * 2
cfg.HEX_SIDE = math.cos(math.radians(60)) * cfg.HEX_SIZE
#COLS = 10
cfg.CANVAS_HEIGHT = cfg.HEX_HEIGHT * cfg.COLS
cfg.ROWS = int(math.ceil(float(cfg.CANVAS_HEIGHT)/cfg.HEX_SIZE/2)) + 1
cfg.CANVAS_WIDTH = cfg.HEX_SIDE+(cfg.HEX_SIZE * 2 - cfg.HEX_SIDE) * cfg.COLS
'''
#directions = [[0, 1, -1],[+1,0, -1],[+1, -1,0],[0, -1, 1],[-1,0, 1],[-1, 1,0] ]
#hexagon_generator = False
#cfg.win = False
#cfg.canvasmain = False
#cfg.canvastop = False
#cfg.canvasbottom = False
board = False
deck = False
hand1 = False
hand2 = False
clicked_rowcolcanv = None

#btnTry = False

def main():
  #todo global canvas* are not needed
  #global cfg.win, cfg.canvasmain, cfg.canvastop, cfg.canvasbottom
  global btn1, btn2, btnConf, btnReset
  global board, deck
  board = bd.Board()
  #Deal deck
  deck = Deck()
  hand1 = Hand(cfg.canvastop)
  hand2 = Hand(cfg.canvasbottom)
  #Check for duplicates. It should never happen
  dupl = set([x for x in deck.dealt if deck.dealt.count(x) > 1])
  if len(dupl) > 0:
    raise UserWarning("Duplicates in deck.dealt!!!")
  #Bindings
  cfg.canvasmain.bind('<ButtonPress-1>', clickCallback) #type 4
  #<Double-Button-1>?
  cfg.canvastop.bind('<ButtonPress-1>', clickCallback) #type 4
  cfg.canvasbottom.bind('<ButtonPress-1>', clickCallback) #type 4
  cfg.canvasmain.bind('<B1-Motion>', motionCallback) #drag
  cfg.canvastop.bind('<B1-Motion>', motionCallback) #drag
  cfg.canvasbottom.bind('<B1-Motion>', motionCallback) #drag
  cfg.canvasmain.bind('<ButtonRelease-1>', clickCallback) #release
  cfg.canvastop.bind('<ButtonRelease-1>', clickCallback) #release
  cfg.canvasbottom.bind('<ButtonRelease-1>', clickCallback) #release
  cfg.canvasmain.bind('<ButtonPress-3>', clickB3Callback)
  #canvas.bind('<Return>', clickCallback)
  #canvas.bind('<Key>', clickCallback)
  #canvas.bind('<MouseWheel>', wheel)
  cfg.win.mainloop()

def motionCallback(event):
  print_event(event)
  rowcolcanv=onClickRelease(event)
  #ind = deck.get_index_from_rowcolcanv(rowcolcanv)
  #free_move(moving_tile_ind, event)


moving_tile_ind = 1 #todo I have to store the tille that was clicked!

def free_move(ind, event):
  x, y = event.x, event.y
  x_root, y_root = event.x_root, event.y_root
  tile = deck.tiles[ind]
  canvastop.delete(deck.itemids[ind])
  #itemid = canvastop.create_image(x, y, image = tile.tile)
  img=tk.Label(win, image=tile.tile, name="img")
  img.place(x=event.x - tile.tile.width() / 2, y=event.y - tile.tile.height() / 2, height=tile.tile.height(), width=tile.tile.width())
  #Update window
  win.update()


def buttonClick(event):
  print('buttonClick')
  #Buttons
  widget_name = event.widget._name
  if widget_name[0:3] == "btn":
    if event.state == 272:  #release click
      if widget_name == "btn1":
        deck.refill_deck(cfg.canvastop)
      elif widget_name == "btn2":
        deck.refill_deck(cfg.canvasbottom)
      elif widget_name == "btnConf":
        print("Confirm clicked ")
        global TRYING
        TRYING = False
        print("TRYING = " + str(TRYING))
        status=deck.process_move()
        print("deck.process_move successful:" + str(status))
        TRYING = True
        print("TRYING = " + str(TRYING))
        #disable the reset button
        bd.btnReset.configure(state="disabled")
      elif widget_name == "btnReset":
        print("Reset!")
        deck.reset()
    return

def clickEmptyHexagon(event):
  log()
  #print_event(event,' \nclickEmptyHexagon')

def clickB3Callback(event):
  print_event(event, ' \nclickB3Callback')

def clickCallback(event):
  print('\nclickCallback')
  global clicked_rowcolcanv
  x, y = event.x, event.y
  print_event(event)
  #with this I change to the canvas' coordinates: x = canvas.canvasx(event.x)
  #print canvas.find_closest(x, y)
  #http://epydoc.sourceforge.net/stdlib/Tkinter.Event-class.html
  #NB: move while dragging is type=6 (clickCallback) state=272
  #NB: click                  type=4 (BPress) state=16
  #NB: release click          type=5 (BRelea) state=272
  #
  if event.type == '4' and event.state == 16: #click
    rowcolcanv=onClickRelease(event)
    ind = deck.get_index_from_rowcolcanv(rowcolcanv)
    if ind is None:
      clicked_rowcolcanv = None
      return
    clicked_rowcolcanv = rowcolcanv
    #wait ..
  elif event.type == '5' and event.state == 272: #release click
    #previously clicked on empty hexagon
    if clicked_rowcolcanv is None:
      clickEmptyHexagon(event)
      return
    rowcolcanv=onClickRelease(event)  #todo here I could use simpler onClickRelease
    print('rowcolcanv=      ' + str(rowcolcanv))
    print('clicked_rowcolcanv=' + str(clicked_rowcolcanv))
    if len(rowcolcanv) == 0:
      return
    if rowcolcanv == clicked_rowcolcanv: #released on same tile => rotate it
      #Rotate
      deck.rotate(rowcolcanv)
    elif rowcolcanv != clicked_rowcolcanv: #released elsewhere => drop tile there.
      #previously clicked on empty hexagon
      if clicked_rowcolcanv is None:
        return
      #move tile if place is not occupied already:
      canvas_origin, canvas_dest = cfg.win.children[clicked_rowcolcanv[2][1:]], cfg.win.children[rowcolcanv[2][1:]]
      deck.move(clicked_rowcolcanv[0],clicked_rowcolcanv[1],canvas_origin, rowcolcanv[0],rowcolcanv[1],canvas_dest)
    #Reset the coordinates of the canvas where the button down was pressed
    clicked_rowcolcanv=None
  else :
    pass
    #print('\n !event not supported \n')

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
  ytop= cfg.canvastop.winfo_reqheight()
  ymain= ytop + cfg.canvasmain.winfo_reqheight()
  ybottom=ymain + cfg.canvasbottom.winfo_reqheight()
  if str(event.widget) == ".canvastop":
    yrel = y
  elif str(event.widget) == ".canvasmain":
    yrel = y + ytop
  elif str(event.widget) == ".canvasbottom":
    yrel = y + ymain
  else:
    return tuple()
    raise UserWarning("onClickRelease: cannot determine yrel")
  #Check y
  if yrel <= 0 or yrel >= ybottom:
    print('x outside the original widget')
    return tuple()
  elif yrel <= ytop:
    print('x inside cfg.canvastop')
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,y))
    rowcolcanv.append(".canvastop")
  elif yrel <= ymain:
    print('x inside canvas')
    rowcolcanv = list(board.pixel_to_off(x,yrel-ytop))
    rowcolcanv.append(".canvasmain")
  elif yrel <= ybottom:
    print('x inside cfg.canvasbottom')
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,yrel-ymain))
    rowcolcanv.append(".canvasbottom")
  else:
    raise UserWarning("onClickRelease: cannot destination canvas")
    return tuple()
  return rowcolcanv


def buttonClick(event):
  print('buttonClick')
  #Buttons
  widget_name = event.widget._name
  if widget_name[0:3] == "btn":
    if event.state == 272:  #release click
      if widget_name == "btn1":
        deck.refill_deck(cfg.canvastop)
      elif widget_name == "btn2":
        deck.refill_deck(cfg.canvasbottom)
      elif widget_name == "btnConf":
        print("Confirm clicked ")
        global TRYING
        TRYING = False
        print("TRYING = " + str(TRYING))
        status=deck.process_move()
        print("deck.process_move successful:" + str(status))
        TRYING = True
        print("TRYING = " + str(TRYING))
        #disable the reset button
        btnReset.configure(state="disabled")
      elif widget_name == "btnReset":
        print("Reset!")
        deck.reset()
    return


def test():
  if cfg.canvasmain.find_withtag(tk.CURRENT):
    #canvas.itemconfig(tk.CURRENT, fill="blue")
    cfg.canvasmain.update_idletasks()
    cfg.canvasmain.after(200)
    #canvas.itemconfig(tk.CURRENT, fill="red")

def print_event(event, msg= ' '):
  print(msg)
  x, y = event.x, event.y
  hex = board.pixel_to_hex(x,y)
  cube = board.pixel_to_off(x, y)
  print(' widget = ' + str(event.widget))
  print(' type = ' + str(event.type))
  print(' state = ' + str(event.state))
  print(' num = ' + str(event.num))
  print(' delta =' + str(event.delta))
  print('x, y = {}, {}'.format(x, y))
  print(" x_root, y_root = ",str((event.x_root, event.y_root)))
  print('offset (if in cfg.canvasmain!) = ' + str(cube))
  print('hex = ' + str(hex))
  rowcolcanv=onClickRelease(event)
  neigh= deck.get_neighbors(rowcolcanv)
  print('neigh = ' + str(neigh))
  neighcolors = deck.get_neighboring_colors(rowcolcanv)
  print('neighcolors = ' + str(neighcolors))

def log():
  print("TRYING=" + str(TRYING))
  print("deck.positions=" + str(deck.positions))
  print("deck.positionstable=" + str(deck.positionstable))
  print("deck.positionshand1=" + str(deck.positionshand1))
  print("deck.positionshand2=" + str(deck.positionshand2))
  print("deck.dealt="+str(deck.dealt))



def initialize_board():
  #  pass
  #def __call__(self):
    #global cfg.win, cfg.canvasmain, cfg.canvastop, cfg.canvasbottom, \
    global hexagon_generator, board, deck
    global btn1, btn2, btnConf, btnReset
    cfg.win = tk.Tk()
    cfg.canvasmain = tk.Canvas(cfg.win, height= cfg.CANVAS_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey', name="canvasmain")
    #cfg.canvasmain = tk.Canvas(cfg.win, height= 310, width = cfg.CANVAS_WIDTH, background='lightgrey', name="canvasmain")
    cfg.canvastop = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name="canvastop")
    cfg.canvasbottom = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name="canvasbottom")
    w = cfg.CANVAS_WIDTH + 5
    h = cfg.CANVAS_HEIGHT + cfg.HEX_HEIGHT * 2 + 5
    ws = cfg.win.winfo_screenwidth()    #width of the screen
    hs = cfg.win.winfo_screenheight()       #height of the screen
    x = ws - w / 2; y = hs - h / 2    #x and y coord for the Tk root window
    cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Create hexagons on main canvas
    hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
    for row in range(cfg.ROWS):
      for col in range(cfg.COLS):
        pts = list(hexagon_generator(row, col))
        cfg.canvasmain.create_line(pts, width =2)
    #Append canvases
    cfg.canvastop.grid(row = 0, column = 0)#,expand="-in")
    cfg.canvasmain.grid(row = 1, column = 0, rowspan = 5)#,expand="-ipadx")
    cfg.canvasbottom.grid(row = 6, column = 0)#,expand="-padx")
    #Button1
    btn1 = tk.Button(cfg.win, width=6, text="Refill\nhand",  bg="yellow", name = "btn1")
    #Add cfg.canvastop to tags, so button click will be processed by cfg.canvastop!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, cfg.canvastop)
    #btn1.bindtags(tuple(bindtags))
    btn1.bind('<ButtonRelease-1>', buttonClick)
    btn1.grid(row=0, column=1,columnspan=1)
    #Button2
    btn2 = tk.Button(cfg.win, width=6, text="Refill\nhand",  bg="red", name = "btn2") #, height=int(round(cfg.HEX_HEIGHT))-1
    #Add canvasbpttom to tags, so button click will be processed by cfg.canvasbottom!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, cfg.canvasbottom)
    #btn2.bindtags(tuple(bindtags))
    btn2.bind('<ButtonRelease-1>', buttonClick)
    btn2.grid(row=6, column=1,columnspan=1)
    #Confirm button
    btnConf = tk.Button(cfg.win, text="Confirm\nmove",  bg="cyan",
                      width=6, name = "btnConf") #padx=5,
    btnConf.bind('<ButtonRelease-1>', buttonClick)
    btnConf.grid(row=2, column=1, columnspan=1)
    #Reset button
    btnReset = tk.Button(cfg.win, text="Reset\ndeck",  bg="cyan",
                      width=6, name = "btnReset")
    btnReset.bind('<ButtonRelease-1>', buttonClick)
    btnReset.grid(row=4, column=1,columnspan=1)
    #TRYING button
    clr={False:"lightgrey", True:"cyan"}
    '''btnTry = tk.Button(cfg.win, width=6, text="Try\nthings",  bg=clr[TRYING], name = "btnTry")
    btnTry.bind('<ButtonRelease-1>', buttonClick)
    btnTry.grid(row=3, column=1,columnspan=1)
    #btnTry(state="disabled")'''
    #Update window
    cfg.win.update()
    cfg.win.winfo_height() #update before asking size!
    cfg.win.geometry(str(cfg.canvasmain.winfo_width() + 100) + "x" + str(int(round(cfg.CANVAS_HEIGHT + 2 * cfg.HEX_HEIGHT))))
    cfg.win.update()

if __name__ == "__main__":
  initialize_board()
  main()
"""TO DO
refill only when TRYING is False

btnReset.configure(state="enabled")

start turn with free movements. when clicking confim check that it is confirmable, switch to TRYING=False, process the stuff, switch to TRYING=True again for the next turn.

"""
