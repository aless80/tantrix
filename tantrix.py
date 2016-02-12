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
import callbacks as clb
import helpers as hp

import tkMessageBox as mb

"""
from pymouse import PyMouse
from pykeyboard import PyKeyboard
k = PyKeyboard()
m = PyMouse()
"""
#http://stackoverflow.com/questions/1917198/how-to-launch-a-python-tkinter-dialog-box-that-self-destructs
#https://www.summet.com/dmsi/html/guiProgramming.html

deck = cfg.deck
#board = False
#deck = False
hand1 = False
hand2 = False
#clicked_rowcolcanv = None
#canvases = [cfg.canvastop, cfg.canvasmain, cfg.canvasbottom]
canvases = [cfg.canvasmain]
turn = 1

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
        '''tile object containing a tile in PhotoImage format'''
        #.tile property is a PhotoImage (required by Canvas' create_image) and its number
        tilePIL = cfg.SPRITE.crop((cfg.SPRITE_WIDTH * (num - 1), 4,
             cfg.SPRITE_WIDTH * num - 2, cfg.SPRITE_HEIGHT)).resize((cfg.HEX_SIZE * 2, int(cfg.HEX_HEIGHT)))
        if angle != 0:
            tilePIL = tilePIL.rotate(angle, expand = 0)
        self.tile = PIL.ImageTk.PhotoImage(tilePIL)
        self.basecolors = cfg.colors[num - 1]
        self.angle = angle % -360
        self.lock = False

    def __str__(self):
        return 'tile colors and angle: ' +self.getColor() +' ' + str(self.angle) +' '

    def getColor(self):
        basecolor = self.basecolors
        n = self.angle/60
        return basecolor[n:] + basecolor[:n]

    def rowcolcanv_match_colors(self, rowcolcanv1,rowcolcanv2, angle1 = 0, angle2 = 0):
        '''Return True if the tile at rowcoltab and angle1 matches the neighbors' colors'''
        #No colors matching when user is trying things
        return False
        if cfg.TRYING == True:
            print("TRYING is True, so no colors check")
            return True
        #Get neighboring colors
        neighcolors = deck.get_neighboring_colors(rowcoltab)
        #Angle
        basecolor = self.getColor()
        n = angle/60
        tilecolor = basecolor[n:] + basecolor[:n]
        for nc in neighcolors:
            if tilecolor[nc[1]] != nc[0]:
              #print("neighbors: " + str(deck.get_neighboring_tiles(rowcoltab)))
              #print("tilecolor = " + str(tilecolor) + " " + str(nc[1]) + " " + nc[0])
              #NB cannot move tile one tile away because current tile is present.
              # I do not see any case in which that is what i want
              return False
        return True

    def tile_match_colors(self, rowcoltab, angle = 0):
        '''Return True if the tile at rowcoltab and angle matches the neighbors' colors'''
        #No colors matching when user is trying things
        #if cfg.TRYING == True:
        #  print("TRYING is True, so no colors check")
        #  return True
        #Get neighboring colors
        neighcolors = deck.get_neighboring_colors(rowcoltab)
        #Angle
        basecolor = self.getColor()
        n = angle/60
        tilecolor = basecolor[n:] + basecolor[:n]
        for nc in neighcolors:
            if tilecolor[nc[1]] != nc[0]:
                print("neighbors: " + str(deck.get_neighboring_tiles(rowcoltab)))
                print("tilecolor = " + str(tilecolor) + " " + str(nc[1]) + " " + nc[0])
                #NB cannot move tile one tile away because current tile is present.
                #   I do not see any case in which that is what i want
                return False
        return True

    def create_at_rowcoltab(self, rowcoltab):
        '''Create a tile image and place it on cfg.canvasmain. No update .positions. Return the itemid.'''
        #Get the pixels
        x, y = cfg.board.off_to_pixel(rowcoltab)
        itemid = cfg.canvasmain.create_image(x, y, image = self.tile, tags = "a tag")
        cfg.win.update()
        return itemid

    def move_to_rowcoltab(self, rowcoltab):
        '''Move an existing tile to rowcoltab'''
        #Get the pixels
        x, y = cfg.board.off_to_pixel(rowcoltab)
        itemid, _ = cfg.deck.get_itemid_from_rowcoltab(rowcoltab)
        cfg.canvasmain.coords(itemid, (x, y))
        cfg.win.update()

    def move_to_pixel(self, x, y, itemid):
        '''Move an existing tile to the pixel coordinates x, y'''
        cfg.canvasmain.coords(itemid, (x, y))


class Hand(object):

    def __init__(self, name):
      #Choose a color for the player
      avail_colors = cfg.PLAYERCOLORS
      ran = rndgen.randint(0, len(cfg.PLAYERCOLORS) - 1)
      #ran = randrange(0, len(cfg.PLAYERCOLORS))
      self.playercolor = cfg.PLAYERCOLORS.pop(ran)
      #todo Color the corresponding button
      self.playercolor
      self.name = name
      deck.refill_deck(self.name)

    def refill(self, tab):
      pass



class Deck(hp.DeckHelper):

    def __init__(self):
        self.tiles = []       #this contains tile in PhotoImage format
        self.itemids = []     #itemid = cfg.canvasmain.create_image()
        self.undealt =range(1, 57) #1:56
        self.dealt = [] #1:56
        self._positions = []   #(row, col, table)
        self._table = [] #(table)
        self._positions_moved = []   #(row, col, table, num)
        self._confirmed = []
        self._confirmed.append([]) #;ater do it for number of players
        self._confirmed.append([])
        self._confirmed.append([])
        #self._confirmed[0] = [] #(row, col, num)
        #self._confirmed[1] = [] #(row, col, num)
        #self._confirmed[2] = [] #(row, col, num)

    def is_occupied(self, rowcoltab):
        """Return whether an hexagon is already occupied in ._positions:
        deck.isOccupied(rowcoltab)    """
        return rowcoltab in self._positions

    def is_movable(self, rowcoltab1, rowcoltab2):
        row1, col1, table1 = rowcoltab1
        row2, col2, table2 = rowcoltab2
        #Ignore movement when:
        if self.is_occupied(rowcoltab2):
            #Return False if destination is already occupied
            print('Destination tile is occupied: ' + str(rowcoltab2))
            return False
        """if turn == 1 and rowcoltab1[2] == -2:
            print("It is player1's turn. You cannot move the opponent's tiles")
            return False
        if turn == 2 and rowcoltab[2] == -1:
            print("It is player2's turn. You cannot move the opponent's tiles")
            return False
        """
        if table1 != table2 and table1 != 0 and table2 != 0:
            print('Cannot move from top to bottom or vice versa')
            return False
        if cfg.TRYING:
            return True
        '''Movement to main table.'''
        if table2 == 0:
            #Ok if there are no tiles on table
            if len(self._confirmed[0]) == 0:
                return True
            #Check if tile matches colors
            ind1 = self.get_index_from_rowcoltab(rowcoltab1)
            tile = deck.tiles[ind1]
            #NB The following does not allow you to move the same tile one position away.
            #That should not be of any use though so ok
            if not cfg.TRYING:
                ok = tile.tile_match_colors(rowcoltab2)
                if not ok:
                    print('No color matching')
                    return ok
        elif table1 != 0 and table1 != table2:
            #Return False if trying to move from bottom to top or vice versa
            print('trying to move from bottom to top or vice versa')
            return False
        elif table1 == 0 and table2 != 0:
            #Return False if trying to move from 0 to top or bottom
            print('trying to move from .canvasmain to top or bottom')
            return False
        return True

    def is_confirmable(self):
        curr_tiles_on_table = self.get_rowcoltabs_in_table(0)
        num_curr_tiles_on_table = len(curr_tiles_on_table)
        num_curr_tiles_on_hand1 = len(self.get_rowcoltabs_in_table(-1))
        num_curr_tiles_on_hand2 = len(self.get_rowcoltabs_in_table(-2))
        confirmed_tiles_on_table = self._confirmed[0]
        num_confirmed_tiles_on_table = len(confirmed_tiles_on_table)
        if 0:
            print("num_confirmed_tiles_on_table=" + str(num_confirmed_tiles_on_table))
            print("num_curr_tiles_on_table=" + str(num_curr_tiles_on_table))
            print("num_curr_tiles_on_hand1=" + str(num_curr_tiles_on_hand1))
            print("num_curr_tiles_on_hand2=" + str(num_curr_tiles_on_hand2))
            #print("len(self._confirmed[1])=" + str(len(self._confirmed[1])))
            #print("len(self._confirmed[2])=" + str(len(self._confirmed[2])))
        msg = ""
        if turn % 2 == 1 and num_curr_tiles_on_hand2 < 6:
                msg = "It is hand1's turn, there are tiles of hand2 out"
        elif turn % 2 == 0 and num_curr_tiles_on_hand1 < 6:
                msg = "It is hand2's turn, there are tiles of hand1 out"
        elif num_curr_tiles_on_hand1 > 6 or num_curr_tiles_on_hand2 > 6:
            msg = "hand1 or hand2 have more than 6 tiles"
        elif num_curr_tiles_on_hand1 == 6 and num_curr_tiles_on_hand2 == 6:
            msg = "hand1 and hand2 have 6 tiles each"
        elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 > 11:
            msg = "no tiles from hand1 or hand2 are out2"
        elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 < 11:
            msg = "More than 1 tile from hand1 and hand2 are out"
        elif num_confirmed_tiles_on_table - num_curr_tiles_on_table == 0:
            msg = "no tiles were added to the table"
        elif num_confirmed_tiles_on_table - num_curr_tiles_on_table > 1:
            raise UserWarning("more than one tile were added to the table. I should not see this msg")
        elif num_curr_tiles_on_table - num_confirmed_tiles_on_table < 0:
            raise UserWarning("There are less tiles on table that in ._confirmed[0]. I should not see this msg")
        elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 == 11:
            if num_curr_tiles_on_table == 1:
                #only one tile on the table
                return True
            elif num_curr_tiles_on_table - num_confirmed_tiles_on_table == 1:
                #Find tile to be confirmed
                rowcoltab = [ct for ct in curr_tiles_on_table if self.get_tile_number_from_rowcoltab(ct) not in [c[2] for c in self._confirmed[0]]]
                if len(rowcoltab) != 1:
                    raise UserWarning("more than one tile were added to table in this turn. I should not see this msg")
                else:
                    rowcoltab = rowcoltab[0]
                    #check if new tile is adjacent to other tiles
                    neighboring = deck.get_neighboring_tiles(rowcoltab[0], rowcoltab[1])
                    if not neighboring:
                        return "The tile at ({},{}) is not adjacent to any other tile on the table".format(rowcoltab[0], rowcoltab[1])
                    ind = self.get_index_from_rowcoltab(rowcoltab)
                    tile = deck.tiles[ind]

                    match = tile.tile_match_colors(rowcoltab)
                    if match: #todo check when tiles are not neighbors!
                        return True
                    else:
                        msg = "The tile added at ({},{}) does not match the surrounding colors".format(rowcoltab[0],rowcoltab[1])
                        print("tile {} ind={}, rowcoltab={}".format(str(tile), str(ind), str(rowcoltab)) )
                        tile.tile_match_colors(rowcoltab)
        else:
            raise UserWarning("is_confirmable: Cannot determine if confirmable")
        if msg is not "":
            return msg
        #Raise error
        #todo: maybe make a property deck.confirmable

    def confirm_move(self):
        #print("confirm_move. cfg.TRYING="+str(cfg.TRYING))
        confirmable = self.is_confirmable()
        if confirmable != True:
            print("confirm_move: Cannot confirm this move because: " + confirmable)
            return False
        #Place first tile in the middle
        """if turn == 1:
            rowcoltab = self.get_rowcoltab_from_rowcolnum(self._positions_moved[0])
            self.move_automatic(rowcoltab, (math.floor(cfg.ROWS / 2) - 1, math.floor(cfg.COLS / 2), 0))
        """
        #Update each confirmed table (._confirmed[0], ._confirmed[1], ._confirmed[2])
        for ind, pos in enumerate(self._positions):
            row, col, tab = pos
            if tab == 0:
                num = self.get_tile_number_from_index(ind)
                rowcolnum = tuple([row, col, num])
                if rowcolnum not in self._confirmed[0]:
                    #._confirmed[0] must get one tile more
                    self._confirmed[0].append(rowcolnum)
                    #Lock the confirmed tile
                    tile = self.tiles[ind]
                    tile.lock = True
                    #._confirmed[1] or ._confirmed[2] must remove one tile
                    match = filter(lambda t : t[2] == num, [tup for tup in self._confirmed[1]])
                    if len(match) == 1:
                        self._confirmed[1].remove(match[0])
                    elif len(match) > 1:
                        raise UserWarning("confirm_move: ._confirmed[1] has more than one tile played!")
                    match = filter(lambda t : t[2] == num, [tup for tup in self._confirmed[2]])
                    if len(match) == 1:
                        self._confirmed[2].remove(match[0])
                    elif len(match) > 1:
                        raise UserWarning("confirm_move: ._confirmed[2] has more than one tile played!")
                    #todo I think I can use a break here
                    #todo new _positions_moved
                    self._positions_moved.remove(rowcolnum)
        global turn
        turn += 1
        return True

    def remove(self, row, col, table):
        rowcoltab = tuple([row, col, table])
        ind = self.get_index_from_rowcoltab(rowcoltab)
        #Delete itemid from table and .itemids
        try:
            itemid = self.itemids.pop(ind)
        except:
            print("remove: Cannot do self.itemids.pop({}) !!".format(ind))
            print("rowcoltab={}".format(str(rowcoltab)))
            print("len self.itemids=", str(len(self.itemids)))
            log()
            raise UserWarning("remove: Error!")
        #I think this is already done by move_automatic
        cfg.canvasmain.delete(itemid)
        #Update confirmed storage
        n = self.get_tile_number_from_index(ind)
        rowcolnum = tuple([row, col, n])
        if not cfg.TRYING:
            if table == 0:
                self._confirmed[0].remove(rowcolnum)
            elif table == -1:
                print("removing: _confirmed[1] and row, col, ind")
                self._confirmed[1].remove(rowcolnum)
            elif table == -2:
                self._confirmed[2].remove(rowcolnum)
        #Update _positions_moved
        if rowcolnum in self._positions_moved:
            print("removed rowcolnum {} from _positions_moved".format(rowcolnum))
            self._positions_moved.remove(rowcolnum)
        #NB: remove tile from deck dealt. leaving undealt as is
        num = deck.dealt.pop(ind)
        #Return information
        pos = self._positions.pop(ind)
        table = self._table.pop(ind)
        tile = self.tiles.pop(ind)
        return (pos, num, tile)

    def deal(self, row, col, tab, num = 'random'):
        row = int(row)
        col = int(col)
        #Random tile if num is not set
        if num =='random':
          ran = rndgen.randint(0, len(self.undealt) - 1) #0:55
        num= self.undealt.pop(ran)   #1:56
        #Get tile as PhotoImage
        tileobj = Tile(num)
        #Update storage
        rowcoltab = tuple([row, col, tab])
        temp = rowcoltab
        #temp = (cfg.COLS / 2, cfg.ROWS / 2, 0) #this makes nice automatic dealing
        self.tiles.append(tileobj)
        self.dealt.append(num)
        self._positions.append(temp)
        self._table.append(tab)
        #Place on canvasmain
        itemid = tileobj.create_at_rowcoltab(temp)
        self.itemids.append(itemid)
        #self.move_automatic(temp, rowcoltab)    #this makes nice automatic dealing
        #self._positions_moved.pop()
        #Update confirmed storage
        if 1:
            ind = self.get_index_from_rowcoltab(rowcoltab)
            n = self.get_tile_number_from_index(ind)
            rowcolnum = tuple([row, col, n])
            if tab == 0:
                self._confirmed[0].append(rowcolnum)
            elif tab == -1:
               self._confirmed[1].append(rowcolnum)
            elif tab == -2:
                self._confirmed[2].append(rowcolnum)
        #no update to ._positions_moved ? I think it gets done by the confirm button

    def move(self, rowcoltab1, rowcoltab2):
        '''Move a tile and update storage. ._positions_moved are updated'''
        _, _, tab1 = rowcoltab1
        _, _, tab2 = rowcoltab2
        if not self.is_movable(rowcoltab1, rowcoltab2):
            print("move: You cannot move the tile as it is to this hexagon")
            self.is_movable(rowcoltab1, rowcoltab2)
            return False
        itemid, ind = cfg.deck.get_itemid_from_rowcoltab(rowcoltab1)
        tilex, tiley = cfg.board.off_to_pixel(rowcoltab2)
        cfg.canvasmain.coords(itemid, (tilex, tiley))
        #Update moved storage
        num = self.dealt[ind]
        rowcolnum1 = tuple([rowcoltab1[0], rowcoltab1[1], num])
        rowcolnum2 = tuple([rowcoltab2[0], rowcoltab2[1], num])
        if rowcolnum1 in self._positions_moved:
            self._positions_moved.remove(rowcolnum1)
        #todo: also _position_moved for tiles that go to top/bottom but not on original place
        if tab2 == 0:
            self._positions_moved.append(rowcolnum2)
        elif rowcoltab2 not in cfg.deck.get_rowcoltabs_in_table(tab2):
            if rowcolnum2 not in cfg.deck.get_confirmed_rowcoltabs_in_table(tab2):
                self._positions_moved.append(rowcolnum2)
        self._positions[ind] = (rowcoltab2)
        self._table[ind] = (tab2)
        #Update window
        cfg.win.update()
        return True

    def move_automatic(self, rowcoltab1, rowcoltab2):
        '''move tile. NB: .move is used and therefore also ._positions_moved is updated'''
        itemid, ind = cfg.deck.get_itemid_from_rowcoltab(rowcoltab1)
        #tile = cfg.deck.tiles[ind]
        #Calculate coordinates, direction, distance etc
        x1, y1 = cfg.board.off_to_pixel(rowcoltab1)
        x2, y2 = cfg.board.off_to_pixel(rowcoltab2)
        dir = (float(x2 - x1), float(y2 - y1))
        distance = math.sqrt(dir[0] * dir[0] + dir[1] * dir[1])
        steps = int(math.ceil(distance / 10))
        if steps == 0:
            print("\nsteps==0!")
            print("rowcoltab1, rowcoltab2= {}, {}".format(str(rowcoltab1),str( rowcoltab2)))
            print("x1,y1, x2,y2={}".format(str((x1, y1, x2, y2))))
            print("dir={}, distance={}".format(str(dir), str(distance)))
        deltax, deltay = dir[0] / steps, dir[1] / steps
        for i in range (1, steps + 1):
            xi = x1 + round(deltax * i)
            yi = y1 + round(deltay * i)
            cfg.canvasmain.coords(itemid, (xi, yi))
            cfg.canvasmain.after(15, cfg.win.update())
        ok = self.move(rowcoltab1, rowcoltab2)
        return ok

    def rotate(self, rowcoltab):
        '''Rotate a tile if tile is not locked: spawn it, replace itemid in deck.itemids.
        Return True if successful '''
        #Find the index
        try:
            ind= self.get_index_from_rowcoltab(rowcoltab)
        except:
            print('not found: ' + str(rowcoltab) +' in')
            return
        #Check if tile is locked
        if self.tiles[ind].lock == True:
            return False
        #Spawn the rotated tile
        tile = Tile(self.dealt[ind], self.tiles[ind].angle - 60)
        #Update tiles list
        self.tiles[ind] = tile
        print("rotate: after spawn before savng in .tiles: ",str(self.tiles[ind].basecolors))
        #Place the tile
        itemid = tile.create_at_rowcoltab(rowcoltab)
        self.itemids[ind] = itemid
        return True

    def refill_deck(self, tab):
        #print("refill_deck")
        #Check how many tiles there are
        rowcoltab = self.get_rowcoltabs_in_table(tab)
        count = len(rowcoltab)
        if count == 6:
            print("There are already 6 tiles on that deck")
            return False
        """Flush existing tiles to left"""
        for i in range(0, count):
            bin, cols, bin = rowcoltab[i]
            if cols > i:
                """move tile to left by one or more places (if I move and reset tiles)"""
                ok = False
                while not ok:
                    ok = self.move_automatic((0, cols, tab), (0, i, tab))
                    if ok:
                        num = self.get_tile_number_from_rowcoltab((0, i, tab))
                        if tab == -1:
                            ind_conf = cfg.deck._confirmed[1].index((0, cols, num))
                            cfg.deck._confirmed[1][ind_conf] = (0, i, num)
                        elif tab == -2:
                            ind_conf = cfg.deck._confirmed[2].index((0, cols, num))
                            cfg.deck._confirmed[2][ind_conf] = (0, i, num)
                    else:
                        print("That might be ok. I will try again flushing")
                    if i > 6:
                        raise UserWarning("Cannot flush!")
                    #This updates _positions_moved
                    num = self.get_tile_number_from_rowcoltab(tuple([0, i, tab]))
                    try:
                        self._positions_moved.remove(tuple([0, i, num]))
                    except:
                        print(i, cols, num, self._positions_moved)
                        print("problem here!")
                    i += 1
        #Refill deck
        for i in range(count, 6):
            self.deal(0, i, tab)
        return True

    def reset(self):
        '''Reset the table by bringing unconfirmed tiles back to confirmed position. If given, rowcolnum resets those tiles'''
        while (self._positions_moved != []):
            """Get info on moved tile"""
            rowcolnum1 = self._positions_moved[-1]
            rowcoltab1 = self.get_rowcoltab_from_rowcolnum(rowcolnum1)
            """Find where tile in ._positions_moved should go,
            ie tile num rowcolnum1[2] is present in confirmed storage"""
            confirmed = [self._confirmed[1], self._confirmed[0], self._confirmed[2]]
            tab_confirmed = ['top','main','bottom']
            rowcoltab2 = [] #list of all rowcoltab that were moved
            for i, bin in enumerate(confirmed):
                for rowcolnum2 in confirmed[i]:
                    if rowcolnum2[2] == rowcolnum1[2]:
                        r, c, cv = self.get_rowcoltab_from_rowcolnum(rowcolnum2)
                        rowcoltab2.append(tuple([r, c, tab_confirmed[i]]))
                    else:
                        continue
                    break
            """Move rowcoltab1 to rowcoltab2"""
            if len(rowcoltab2) > 1:
                raise UserWarning("Deck.reset: more than one rowcolnum per tiles in confirmed positions. It should not happen")
            elif rowcoltab2:
                print("reset: moving {} to {}".format(str(rowcoltab1), str(rowcoltab2[0])))
                ok = self.move_automatic(rowcoltab1, rowcoltab2[0])
                print("reset: move_automatic ok=:",ok)
                #If tile cannot be moved because original place is occupied, move it to temporary position
                if not ok:
                    temp = (rowcoltab2[0][0], -1, rowcoltab2[0][2])
                    print("reset move_automatic to temp:",temp)
                    ok2 = self.move_automatic(rowcoltab1, temp)
                    print("reset: move_automatic ok2=:",ok2)
                    #while loop takes last tile. continues with second tile.
                    last = self._positions_moved.pop(-1)
                    self._positions_moved.insert(0, last)
            #here _position_moved has been purged
        return True

    def get_surrounding_hexagons(self, table):
        '''Return a set of rowcolnum. which are all the empty hexagons surrounding tiles on a table.
        The table is _confirmed[0] by default'''
        if table is None:
            table = self._confirmed[0]
        surr = set([])
        for t in table:
            hex = cfg.board.get_neighbors(t[0], t[1])
            [surr.add(h) for h in hex]
        print("surrounding tiles=",str(surr))
        return surr

    def check_obliged(self):
        surr = self.get_surrounding_hexagons(self._confirmed[0])
        for s in surr:
            neig_tiles = self.get_neighboring_tiles(s[0], s[1])
            if len(neig_tiles) == 3:
                print("Obliged hexagon at {},{}".format(s[0], s[1]))
                cfg.board.place_highlight(s)
                matches = self.find_matching_tiles(s)
                for m in matches:
                    cfg.board.place_highlight(m)
            elif len(neig_tiles) > 3:
                raise UserWarning("Hexagon at {},{} is surrounded by >3 tiles!".format(s[2], s[0], s[1]))

    def find_matching_tiles(self, rowcoltab):
        ind = self.get_index_from_rowcoltab(rowcoltab)
        colors = "bbr" #to do
        #find matching colors in top (todo bottom as well, or maybe all unconfirmed)
        rowcoltabs2 = self.get_rowcoltabs_in_table(-1)
        match = []
        for rowcoltab2 in rowcoltabs2:
            ind2 = self.get_index_from_rowcoltab(rowcoltab2)
            tile2 = self.tiles[ind2]
            if colors in tile2.basecolors+tile2.basecolors:
                match.append(rowcoltab2)
        return match

class Gui(clb.Callbacks):
    def __init__(self):
        global deck
        cfg.win = tk.Tk()

        if 1:
            w = cfg.CANVAS_WIDTH + 5
            h = cfg.CANVAS_HEIGHT + cfg.HEX_HEIGHT * 3
            ws = cfg.win.winfo_screenwidth()    #width of the screen
            hs = cfg.win.winfo_screenheight()   #height of the screen
            x = ws - w / 2; y = hs - h / 2      #x and y coord for the Tk root window
            cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
            w = w + 76
            x = x - 76 - 140
            cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, 600))
            #cfg.win.geometry('%dx%d+%d+%d' % (w + 76, h, 0, 600))
            #print(w, h, x, 600)
        print("x={}, xleft is {}, xright={}".format(x,2559,2214))

        from pymouse import PyMouse
        m = PyMouse()

        cfg.canvasmain = tk.Canvas(cfg.win, height = cfg.YBOTTOM + cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH,
                                   background = 'lightgrey', name = "canvasmain")


        #Create hexagons on cfg.canvasmain
        cfg.canvasmain.create_rectangle(0, cfg.YTOP, cfg.CANVAS_WIDTH, cfg.YBOTTOM,
                                        width = 2, fill = "lightgreen")
        cfg.hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
        for row in range(cfg.ROWS):
            for col in range(cfg.COLS):
                pts = list(cfg.hexagon_generator(row, col))
                cfg.canvasmain.create_line(pts, width = 2)
        #Append canvas
        cfg.canvasmain.grid(row = 1, column = 0, rowspan = 5) #,expand="-ipadx")
        #Confirm button
        btnwidth = 6
        self.btnConf = tk.Button(cfg.win, text = "Confirm\nmove", width = btnwidth,
                                 name = "btnConf", state = "disabled",
                                 relief = "flat", bg = "white", activebackground = "blue")
        self.btnConf.bind('<ButtonRelease-1>', self.buttonCallback)
        self.btnConf.grid(row = 2, column = 1, columnspan = 1)
        #Reset button
        self.btnReset = tk.Button(cfg.win, text = "Reset\ndeck", width = btnwidth,
                                  name = "btnReset", state = "disabled",
                                  relief = "flat", bg = "white", activebackground = "blue")
        self.btnReset.bind('<ButtonRelease-1>', self.buttonCallback)
        self.btnReset.grid(row = 4, column = 1, columnspan = 1)

        #Update window
        cfg.win.update()
        print(m.position()) #(2211, 636)
        print(".btnReset.winfo_width="+str(self.btnReset.winfo_width())) #76
        #cfg.win.geometry(str(cfg.canvasmain.winfo_width() + self.btnConf.winfo_width()) + "x" +
        #                 str(int(cfg.canvasmain.winfo_height() )) )
        cfg.win.update_idletasks()
        cfg.win.update()
        print(m.position())
        1


    def main(self):
        global rndgen
        rndgen = random.Random(0)
        global deck
        #global board not needed because:
        cfg.board = bd.Board()
        #Deal deck
        cfg.deck = Deck()
        deck = cfg.deck #deck is needed for other methods
        hand1 = Hand(-1)
        hand2 = Hand(-2)
        #Check for duplicates. It should never happen
        dupl = set([x for x in deck.dealt if deck.dealt.count(x) > 1])
        if len(dupl) > 0:
          raise UserWarning("Duplicates in deck.dealt!!!")
        #Bindings
        cfg.canvasmain.bind('<ButtonPress-1>', self.clickCallback) #type 4
        #<Double-Button-1>?
        cfg.canvasmain.bind('<B1-Motion>', self.motionCallback) #drag
        cfg.canvasmain.bind('<ButtonRelease-1>', self.clickCallback) #release
        cfg.canvasmain.bind('<ButtonPress-3>', self.rxclickCallback)
        cfg.canvasmain.focus_set()
        #cfg.canvasmain.bind("<1>", lambda event: cfg.canvasmain.focus_set())
        cfg.canvasmain.bind('<Key>', self.keyCallback) #cfg.deck.confirm_move()) #deck.confirm_move()
        #canvas.bind('<MouseWheel>', wheel)
        #import test as ts
        #ts.tests()


def log(msg = " "):
    print(msg)
    #print("TRYING=" + str(cfg.TRYING))
    print("cfg.deck._positions=" + str(cfg.deck._positions[0:4]))
    print("                  =" + str(cfg.deck._positions[4:8]))
    print("                  =" + str(cfg.deck._positions[8:]))
    print("cfg.deck._table=" + str(cfg.deck._table))
    print("cfg.deck._positions_moved=" + str(cfg.deck._positions_moved))
    print("cfg.deck._confirmed[0]=" + str(cfg.deck._confirmed[0]))
    print("cfg.deck._confirmed[1]=" + str(cfg.deck._confirmed[1]))
    print("cfg.deck._confirmed[2]=" + str(cfg.deck._confirmed[2]))
    print("cfg.deck.itemids=" + str(cfg.deck.itemids))
    print("cfg.deck.dealt=" + str(cfg.deck.dealt))
    print("cfg.deck.is_confirmable= " + str(cfg.deck.is_confirmable()))

if __name__ == "__main__":
    gui_instance = Gui()
    gui_instance.main()
    cfg.canvasmain.mainloop()

def test():
    if cfg.canvasmain.find_withtag(tk.CURRENT):
        #canvas.itemconfig(tk.CURRENT, fill="blue")
        cfg.canvasmain.update_idletasks()
        cfg.canvasmain.after(200)
        #canvas.itemconfig(tk.CURRENT, fill="red")
