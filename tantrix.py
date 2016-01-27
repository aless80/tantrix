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
import tkMessageBox
import random
import config as cfg
import HexagonGenerator as hg
import Board as bd
import callbacks as clb
import helpers as hp
#TRYING = True
#board = cfg.board
deck = cfg.deck
#board = False
#deck = False
hand1 = False
hand2 = False
#clicked_rowcolcanv = None
canvases = [cfg.canvastop, cfg.canvasmain, cfg.canvasbottom]
turn = 0

class Tile():
  '''Tile object'''
  @property
  def angle(self):
    '''The object's angle'''
    return self._angle
  @angle.setter
  def angle(self, angle = 0):
    self._angle = angle
  @property
  def lock(self):
    '''If the tile has been confirmed and cannot be moved (1) or not (0)'''
    return self._lock
  @lock.setter
  def lock(self, lock = False):
    self._lock = lock

  def __init__(self, num, angle = 0):
    """tile object containing a tile in PhotoImage format"""
    #new global board
    #.tile property is a PhotoImage (required by Canvas' create_image) and its number
    tilePIL = cfg.SPRITE.crop((cfg.SPRITE_WIDTH * (num - 1), 4,
           cfg.SPRITE_WIDTH * num - 2, cfg.SPRITE_HEIGHT)).resize((cfg.HEX_SIZE * 2, int(cfg.HEX_HEIGHT)))
    if angle != 0:
      tilePIL = tilePIL.rotate(angle, expand = 0)
    self.tile = PIL.ImageTk.PhotoImage(tilePIL)
    self.color = cfg.colors[num - 1]
    self.angle = angle
    self.lock = False

  def __str__(self):
    return 'tile color and angle: ' +self.getColor() +' ' + str(self.angle) +' '

  def getColor(self):
    basecolor = self.color
    n = self.angle/60
    return basecolor[n:] + basecolor[:n]

  def rowcolcanv_match_colors(self, rowcolcanv1,rowcolcanv2, angle1 = 0, angle2 = 0):
    '''Return True if the tile at rowcolcanv and angle1 matches the neighbors' colors'''
    #No color matching when user is trying things
    return False
    if cfg.TRYING == True:
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
        #print("neighbors: " + str(deck.get_neighboring_tiles(rowcolcanv)))
        #print("tilecolor = " + str(tilecolor) + " " + str(nc[1]) + " " + nc[0])
        #NB cannot move tile one tile away because current tile is present. I do not see any case in which that is what i want
        return False
    return True

  def tile_match_colors(self, rowcolcanv, angle = 0):
    '''Return True if the tile at rowcolcanv and angle matches the neighbors' colors'''
    #No color matching when user is trying things
    #if cfg.TRYING == True:
    #  print("TRYING is True, so no color check")
    #  return True
    #Get neighboring colors
    neighcolors = deck.get_neighboring_colors(rowcolcanv)
    #Angle
    basecolor = self.getColor()
    n = angle/60
    tilecolor = basecolor[n:] + basecolor[:n]
    for nc in neighcolors:
      if tilecolor[nc[1]] != nc[0]:
        print("neighbors: " + str(deck.get_neighboring_tiles(rowcolcanv)))
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
  def __init__(self, canv):
    #Choose a color for the player
    avail_colors = cfg.PLAYERCOLORS
    ran = rndgen.randint(0, len(cfg.PLAYERCOLORS) - 1)
    #ran = randrange(0, len(cfg.PLAYERCOLORS))
    self.playercolor = cfg.PLAYERCOLORS.pop(ran)
    #todo Color the corresponding button
    self.playercolor
    deck.refill_deck(canv)
  def refill(self, canv):
    pass



class Deck(hp.DeckHelper):
  def __init__(self):
    self.tiles = []       #this contains tile in PhotoImage format
    self.itemids = []     #itemid = canvas.create_image()
    self.undealt =range(1, 57) #1:56
    self.dealt = [] #1:56
    self.positions = []   #(row, col, str(canvas))
    self._positions_moved = []   #(row, col, str(canvas), num) #new
    self._confirmed_pos_table = [] #(row, col, num)
    self._confirmed_pos_hand1 = [] #(row, col, num)
    self._confirmed_pos_hand2 = [] #(row, col, num)

  def get_tiles_in_canvas(self, canvas):
    count = 0
    rows = []
    cols = []
    #canvases = [cfg.canvastop, cfg.canvasmain, cfg.canvasbottom]

    for pos in self.positions:
      r, q, c = pos
      if str(c) == str(canvas):
        rows.append(r)
        cols.append(q)
        count +=1
    yield count
    yield rows
    yield cols

  def remove(self, row, col, canvas):
    rowcolcanv = tuple([row, col, str(canvas)])
    ind = self.get_index_from_rowcolcanv(rowcolcanv)
    #Delete itemid from canvas and .itemids
    itemid = self.itemids.pop(ind)
    if type(canvas) is str:
      canvas = cfg.win.children[canvas[1:]]
    canvas.delete(itemid)
    #Update properties
    #Update confirmed storage
    #if not cfg.TRYING:
      #ind = self.get_index_from_rowcolcanv(rowcolcanv) #not needed here
    n = self.get_tile_number_from_index(ind)
    rowcolnum = tuple([row, col, n])
    if not cfg.TRYING:
      if str(canvas) == ".canvasmain":
        self._confirmed_pos_table.remove(rowcolnum)
      elif str(canvas) == ".canvastop":
        print("removing: _confirmed_pos_hand1 and row, col, ind")
        self._confirmed_pos_hand1.remove(rowcolnum)
      elif str(canvas) == ".canvasbottom":
        self._confirmed_pos_hand2.remove(rowcolnum)
    #Update _positions_moved new
    if rowcolnum in self._positions_moved:
      print("todo: removed rowcolnum from _positions_moved")
      self._positions_moved.remove(rowcolnum)
    #NB: remove tile from deck dealt. leaving undealt as is
    num = deck.dealt.pop(ind)
    #Return information
    pos = self.positions.pop(ind)
    tile = self.tiles.pop(ind)
    return (pos,num,tile)

  def is_occupied(self, rowcolcanv):
    """Return whether an hexagon is already occupied:
    deck.isOccupied(rowcolcanv)    """
    return rowcolcanv in self.positions

  def is_movable(self, row1, col1, canvas1, row2, col2, canvas2):
    #Ignore movement when:
    if self.is_occupied((row2, col2, str(canvas2))):
      #Return False if destination is already occupied
      print('Destination tile is occupied: ' + str((row2, col2, str(canvas2))))
      return False
    if cfg.TRYING:
      return True
    if canvas2 == cfg.canvasmain:
      #Movement to main canvas.
      #Ok if there are no tiles on canvas
      if ".canvasmain" not in [p[2] for p in self._positions_moved]: #todo: later on maybe check turn
                                # or something that is populated when the first tile is placed
        return True
      #Check if tile matches colors
      ind1 = self.get_index_from_rowcolcanv((row1, col1, str(canvas1)))
      tile = deck.tiles[ind1]
      #NB The following does not allow you to move the same tile one position away.
      #That should not be of any use though so ok
      if not cfg.TRYING:
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

  def is_confirmable(self):
    curr_tiles_on_table = self.get_tiles_in_canvas(cfg.canvasmain)
    num_curr_tiles_on_table = len(curr_tiles_on_table)
    num_curr_tiles_on_hand1 = len(self.get_tiles_in_canvas(cfg.canvastop))
    num_curr_tiles_on_hand2 = len(self.get_tiles_in_canvas(cfg.canvasbottom ))
    confirmed_tiles_on_table = self._confirmed_pos_table
    num_confirmed_tiles_on_table = len(confirmed_tiles_on_table)
    if 0:
      print("num_confirmed_tiles_on_table=" + str(num_confirmed_tiles_on_table))
      print("num_curr_tiles_on_table=" + str(num_curr_tiles_on_table))
      print("len(._confirmed_pos_hand1)=" + str(len(self._confirmed_pos_hand1)))
      print("num_curr_tiles_on_hand1=" + str(num_curr_tiles_on_hand1))
      print("len(._confirmed_pos_hand2)=" + str(len(self._confirmed_pos_hand2)))
      print("num_curr_tiles_on_hand2=" + str(num_curr_tiles_on_hand2))
    msg = ""
    if num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 > 11:
      msg = "no tiles from hand1 or hand2 are out"
    elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 < 11:
      msg = "More than 1 tile from hand1 and hand2 are out"
    elif num_confirmed_tiles_on_table - num_curr_tiles_on_table == 0:
      msg = "no tiles were added to the table"
    elif num_confirmed_tiles_on_table - num_curr_tiles_on_table > 1:
      raise UserWarning("more than one tile were added to the table. I should not see this msg")
    elif num_curr_tiles_on_table - num_confirmed_tiles_on_table < 0:
      raise UserWarning("There are less tiles on table that in ._confirmed_pos_table. I should not see this msg")
    elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 == 11:
      if num_curr_tiles_on_table == 1:
        #only one tile on the table
        return True
      elif num_curr_tiles_on_table - num_confirmed_tiles_on_table == 1:
        #Find tile to be confirmed
        rowcolcanv = [ct for ct in curr_tiles_on_table if self.get_tile_number_from_rowcolcanv(ct) not in [c[2] for c in self._confirmed_pos_table]]
        if len(rowcolcanv) != 1:
          raise UserWarning("more than one tile were added to table in this turn. I should not see this msg")
        else:
          rowcolcanv = rowcolcanv[0]
          #check if new tile is adjacent to other tiles
          neighboring = deck.get_neighboring_tiles(rowcolcanv[0], rowcolcanv[1])
          if not neighboring:
            return "The tile at ({},{}) is not adjacent to any other tile on the table".format(rowcolcanv[0], rowcolcanv[1])
          ind = self.get_index_from_rowcolcanv(rowcolcanv)
          tile = deck.tiles[ind]
          match = tile.tile_match_colors(rowcolcanv)
          if match: #todo check when tiles are not neighbors!
            return True
          else:
            msg = "The tile added at ({},{}) does not match the surrounding colors".format(rowcolcanv[0],rowcolcanv[1])
    else:
      raise UserWarning("is_confirmable: Cannot determine if confirmable")
    if msg is not "":
      return msg
    #Raise error
    #todo: maybe make a property deck.confirmable

  def deal(self, row, col, canv, num='random'):
    row = int(row)
    col = int(col)
    #Random tile if num is not set
    if num =='random':
      ran = rndgen.randint(0, len(self.undealt) - 1) #0:55
    num= self.undealt.pop(ran)   #1:56
    #Get tile as PhotoImage
    tileobj = Tile(num)
    tile = tileobj.tile
    #Store tile instance
    self.tiles.append(tileobj)
    #Place on canvas
    itemid = tileobj.place(row, col, canv,tile)
    self.itemids.append(itemid)
    #store dealt/undealt tile numbers
    self.dealt.append(num)
    rowcolcanv = tuple([row, col, str(canv)])
    self.positions.append(rowcolcanv)
    #Update confirmed storage
    if 1: #not cfg.TRYING:
      ind = self.get_index_from_rowcolcanv(rowcolcanv) #I could use len(self.positions) - 1
      n = self.get_tile_number_from_index(ind)
      rowcolnum = tuple([row, col, n])
      if str(canv) == ".canvasmain":
        self._confirmed_pos_table.append(rowcolnum)
      elif str(canv) == ".canvastop":
        self._confirmed_pos_hand1.append(rowcolnum)
      elif str(canv) == ".canvasbottom":
        self._confirmed_pos_hand2.append(rowcolnum)
    #new: no update to ._positions_moved ?

  def move(self, row1, col1, canvas1, row2, col2, canvas2):
    if not self.is_movable(row1, col1, canvas1, row2, col2, canvas2):
      print("You cannot move the tile as it is to this hexagon")
      return False
    #Remove tile. properties get updated
    (posold, num, tile)= self.remove(row1, col1, canvas1)
    #Place tile on new place
    itemid = tile.place(row2, col2, canvas2, tile.tile)
    #Update storage
    rowcolcanv2 = tuple([row2, col2, str(canvas2)])
    self.tiles.append(tile)
    self.dealt.append(num) #before _confirmed_pos_table/_confirmed_pos_hand1!
    self.positions.append(rowcolcanv2)
    self.itemids.append(itemid)
    #new
    #todo what to do if it was moved before and it gets put back to hand?
    if tuple([row2, col2, num]) in self._positions_moved:
      self._positions_moved.remove(tuple([row2, col2, num]))
    self._positions_moved.append(tuple([row2, col2, num]))
    #Update confirmed storage after the rest fo the storage
    if not cfg.TRYING:
      ind = self.get_index_from_rowcolcanv(rowcolcanv2) #I could use len(self.positions) - 1
      n = num #self.get_tile_number_from_index(ind)
      rowcolnum = tuple([row2, col2, n])
      if str(canvas2) == ".canvasmain":
        self._confirmed_pos_table.append(rowcolnum)
      elif str(canvas2) == ".canvastop":
        self._confirmed_pos_hand1.append(rowcolnum)
      elif str(canvas2) == ".canvasbottom":
        self._confirmed_pos_hand2.append(rowcolnum)
    #Update buttons
    #move to callback! self.btnReset.configure(state="active")
    #Update window
    cfg.win.update()
    return True

  def rotate(self, rowcolcanv):
    #global cfg.win
    #Find the index
    try:
      ind= self.get_index_from_rowcolcanv(rowcolcanv)
      #print('found at ' + str(ind))
    except:
      print('not found: ' + str(rowcolcanv) +' in')
      return
    #Check if tile is locked
    if self.tiles[ind].lock == True:
      return False
    #Check if color would match todo: still useful here?
    if not cfg.TRYING:
      if str(rowcolcanv[2]) == ".canvasmain":
        if not self.tiles[ind].tile_match_colors(rowcolcanv, -60):
          print("You cannot rotate the tile")
          raise UserWarning("Should I be able to see this message, ever?")
          return
    #Spawn the rotated tile
    tile = Tile(self.dealt[ind], self.tiles[ind].angle - 60)
    #Update tiles list
    self.tiles[ind] = tile
    #Place the tile
    canvas = cfg.win.children[rowcolcanv[2][1:]]
    itemid = tile.place(rowcolcanv[0],rowcolcanv[1],canvas,tile.tile)
    self.itemids[ind] = itemid
    return True

  def refill_deck(self, canv):
    print("refill_deck")
    #Check how many tiles there are
    rowcolcanv = self.get_tiles_in_canvas(canv)
    count = len(rowcolcanv)
    if count == 6:
      print("There are already 6 tiles on that canvas")
      return False
    #Flush existing tiles to left
    for i in range(0, count):
      bin, cols, bin = rowcolcanv[i]
      if cols > i:
        deck.move(0, cols, canv, 0, i, canv)
        #problem: this updates _positions_moved
        num = self.get_tile_number_from_rowcolcanv(tuple([0, i, str(canv)]))
        try:
          self._positions_moved.remove(tuple([0, i, num]))
        except:
          print(i, cols, num, self._positions_moved)
          print("problem here!")
    #Refill deck
    for i in range(count, 6):
      self.deal(0, i, canv)
    return True

  def reset(self):
    print("Reset table")
    #new
    for rowcolnum1 in self._positions_moved:
      #Get canvas of origin
      rowcolcanv1 = self.get_rowcolcanv_from_rowcolnum(rowcolnum1)
      #todo: use list of canvases somewhere else? make dictionary with its string?
      canvases = [cfg.canvastop, cfg.canvasmain, cfg.canvasbottom]
      confirmed = [self._confirmed_pos_hand1, self._confirmed_pos_table, self._confirmed_pos_hand2]
      rowcolcanv2 = [] #list of all rowcolcanv that were moved
      for i, canv in enumerate(canvases):
        for rowcolnum2 in confirmed[i]:
          if rowcolnum2[2] == rowcolnum1[2]:
            r, c, cv = self.get_rowcolcanv_from_rowcolnum(rowcolnum2)
            rowcolcanv2.append(tuple([r, c, canvases[i]]))
      counter = 0
      if len(rowcolcanv2) > 1:
        raise UserWarning("Deck.reset: found more than one rowcolnum per tiles in confirmed positions. It should not happen")
      elif rowcolcanv2: #bug this is num!
        #Finally move
        counter += 1
        row2, col2, canv2 = rowcolcanv2[0]
        self.move(rowcolcanv1[0], rowcolcanv1[1], rowcolcanv1[2], row2, col2, canv2)
        return True
    if counter > len(self._positions_moved):
      raise UserWarning("Deck.reset: found more than one rowcolnum per tiles in confirmed positions. It should not happen")

  def get_tiles_in_canvas(self, canvasID):
    '''Get the tiles as list of rowcolcanv currently present in a canvas, ie present in .positions'''
    canvasID = str(canvasID)
    rowcolcanvs = []
    for pos in deck.positions:
      row, col, canv = pos
      if canv == canvasID:
        rowcolcanvs.append(tuple([row, col, canvasID]))
    return rowcolcanvs

  def confirm_move(self):
    print("confirm_move. cfg.TRYING="+str(cfg.TRYING))
    #if cfg.TRYING:
    #  print("Confirm this move because cfg.TRYING is: " + str(cfg.TRYING))
    #  return False #status False prevents Reset to get disabled
    confirmable = self.is_confirmable()
    if confirmable != True:
      print("confirm_move: Cannot confirm this move because: " + confirmable)
      return False
    #Update each confirmed table (._confirmed_pos_table, ._confirmed_pos_hand1, ._confirmed_pos_hand2)
    for ind, pos in enumerate(self.positions):
      row, col, canv = pos
      if canv == ".canvasmain":
        num = deck.get_tile_number_from_index(ind)
        rowcolnum = tuple([row, col, num])
        if rowcolnum not in self._confirmed_pos_table:
          #._confirmed_pos_table must get one tile more
          self._confirmed_pos_table.append(rowcolnum)
          #Lock the confirmed tile
          tile = self.tiles[ind]
          tile.lock = True
          #._confirmed_pos_hand1 or ._confirmed_pos_hand2 must remove one tile
          match = filter(lambda t : t[2] == num, [tup for tup in self._confirmed_pos_hand1])
          if len(match) == 1:
            self._confirmed_pos_hand1.remove(match[0])
          elif len(match) > 1:
            raise UserWarning("confirm_move: ._confirmed_pos_hand1 has more than one tile played!")
          match = filter(lambda t : t[2] == num, [tup for tup in self._confirmed_pos_hand2])
          if len(match) == 1:
            self._confirmed_pos_hand2.remove(match[0])
          elif len(match) > 1:
            raise UserWarning("confirm_move: ._confirmed_pos_hand2 has more than one tile played!")
          #todo I think I can use a break here
          #todo new _positions_moved
          self._positions_moved.remove(rowcolnum)
    return True


class Gui(clb.Callbacks):
  def __init__(self):
      global hexagon_generator, deck
      #global self.btn1, self.btn2, self.btnConf, self.btnReset
      cfg.win = tk.Tk()
      cfg.canvasmain = tk.Canvas(cfg.win, height= cfg.CANVAS_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey', name="canvasmain")
      cfg.canvastop = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name="canvastop")
      cfg.canvasbottom = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name="canvasbottom")
      w = cfg.CANVAS_WIDTH + 5
      h = cfg.CANVAS_HEIGHT + cfg.HEX_HEIGHT * 2 + 5
      ws = cfg.win.winfo_screenwidth()    #width of the screen
      hs = cfg.win.winfo_screenheight()   #height of the screen
      x = ws - w / 2; y = hs - h / 2      #x and y coord for the Tk root window
      cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
      #Create hexagons on main canvas
      hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
      for row in range(cfg.ROWS):
        for col in range(cfg.COLS):
          pts = list(hexagon_generator(row, col))
          cfg.canvasmain.create_line(pts, width =2)
      #Append canvases
      cfg.canvastop.grid(row = 0, column = 0) #,expand="-in")
      cfg.canvasmain.grid(row = 1, column = 0, rowspan = 5) #,expand="-ipadx")
      cfg.canvasbottom.grid(row = 6, column = 0) #,expand="-padx")
      #Button1
      self.btn1 = tk.Button(cfg.win, width=6, text="Refill\nhand", bg="yellow",
                       name = "btn1", state = "disabled")
      #Add cfg.canvastop to tags, so button click will be processed by cfg.canvastop!
      #bindtags = list(self.btn1.bindtags())
      #bindtags.insert(1, cfg.canvastop)
      #self.btn1.bindtags(tuple(bindtags))
      self.btn1.bind('<ButtonRelease-1>', self.buttonCallback)
      self.btn1.grid(row=0, column=1,columnspan=1)
      #Button2
      self.btn2 = tk.Button(cfg.win, width=6, text="Refill\nhand", bg="red",
                       name = "btn2", state = "disabled")
      self.btn2.bind('<ButtonRelease-1>', self.buttonCallback)
      self.btn2.grid(row=6, column=1,columnspan=1)
      #Confirm button
      self.btnConf = tk.Button(cfg.win, text="Confirm\nmove", bg="cyan", width=6, name = "btnConf", state="disabled")
      self.btnConf.bind('<ButtonRelease-1>', self.buttonCallback)
      self.btnConf.grid(row=2, column=1, columnspan=1)
      #Reset button
      self.btnReset = tk.Button(cfg.win, text="Reset\ndeck", bg="cyan",
                        width=6, name = "btnReset", state="disabled")
      self.btnReset.bind('<ButtonRelease-1>', self.buttonCallback)
      self.btnReset.grid(row=4, column=1,columnspan=1)
      #cfg.TRYING button
      clr={False : "lightgrey", True : "cyan"}
      #Update window
      cfg.win.update()
      cfg.win.winfo_height() #update before asking size!
      heighttop = int(max(self.btn1.winfo_height(), cfg.canvastop.winfo_height()))
      cfg.win.geometry(str(cfg.canvasmain.winfo_width() + 100) + "x" + str(int(cfg.canvasmain.winfo_height() + heighttop * 2)))
      cfg.win.update()
      cfg.win.update()

  def main(self):
    #global self.btn1, self.btn2, self.btnConf, self.btnReset, canvases
    global rndgen
    rndgen = random.Random(0)   #seed
    global deck
    #global board not needed because:
    cfg.board = bd.Board()
    #Deal deck
    cfg.deck = Deck()
    deck = cfg.deck #deck is needed for other methods
    hand1 = Hand(cfg.canvastop)
    hand2 = Hand(cfg.canvasbottom)
    #Check for duplicates. It should never happen
    dupl = set([x for x in deck.dealt if deck.dealt.count(x) > 1])
    if len(dupl) > 0:
      raise UserWarning("Duplicates in deck.dealt!!!")
    #Bindings
    cfg.canvasmain.bind('<ButtonPress-1>', self.clickCallback) #type 4
    #<Double-Button-1>?
    cfg.canvastop.bind('<ButtonPress-1>', self.clickCallback) #type 4
    cfg.canvasbottom.bind('<ButtonPress-1>', self.clickCallback) #type 4
    cfg.canvasmain.bind('<B1-Motion>', self.motionCallback) #drag
    cfg.canvastop.bind('<B1-Motion>', self.motionCallback) #drag
    cfg.canvasbottom.bind('<B1-Motion>', self.motionCallback) #drag
    cfg.canvasmain.bind('<ButtonRelease-1>', self.clickCallback) #release
    cfg.canvastop.bind('<ButtonRelease-1>', self.clickCallback) #release
    cfg.canvasbottom.bind('<ButtonRelease-1>', self.clickCallback) #release
    cfg.canvasmain.bind('<ButtonPress-3>', self.rxclickCallback)
    cfg.canvasmain.focus_set()
    #cfg.canvasmain.bind("<1>", lambda event: cfg.canvasmain.focus_set())
    #cfg.canvasmain.bind('<Return>', cfg.deck.confirm_move()) #deck.confirm_move()
    cfg.canvasmain.bind('<Key>', self.keyCallback) #cfg.deck.confirm_move()) #deck.confirm_move()
    #canvas.bind('<Key>', self.clickCallback)
    #canvas.bind('<MouseWheel>', wheel)

def log():
    print("TRYING=" + str(cfg.TRYING))
    print("cfg.deck.is_confirmable= " + str(cfg.deck.is_confirmable()))
    print("cfg.deck.positions=" + str(cfg.deck.positions[0:4]))
    print("                  =" + str(cfg.deck.positions[4:8]))
    print("                  =" + str(cfg.deck.positions[8:]))
    print("cfg.deck._positions_moved=" + str(cfg.deck._positions_moved))
    print("cfg.deck._confirmed_pos_table=" + str(cfg.deck._confirmed_pos_table))
    print("cfg.deck._confirmed_pos_hand1=" + str(cfg.deck._confirmed_pos_hand1))
    print("cfg.deck._confirmed_pos_hand2=" + str(cfg.deck._confirmed_pos_hand2))
    print("cfg.deck.dealt="+str(cfg.deck.dealt))

if __name__ == "__main__":
  gui_instance = Gui()
  gui_instance.main()
  cfg.canvasmain.mainloop()

"""TO DO
confirm first:
  ? reset does not work
"""

def move_ball(self):
        deltax = randint(0,5)
        deltay = randint(0,5)
        self.canvas.move(self.ball, deltax, deltay)
        self.canvas.after(50, self.move_ball)

def test():
  if cfg.canvasmain.find_withtag(tk.CURRENT):
    #canvas.itemconfig(tk.CURRENT, fill="blue")
    cfg.canvasmain.update_idletasks()
    cfg.canvasmain.after(200)
    #canvas.itemconfig(tk.CURRENT, fill="red")
