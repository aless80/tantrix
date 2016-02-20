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
#cfg.turn = 1
#cfg.free = True

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
                #print("neighbors: " + str(deck.get_neighboring_tiles(rowcoltab)))
                #print("tilecolor = " + str(tilecolor) + " " + str(nc[1]) + " " + nc[0])
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

    def is_occupied(self, rowcoltab, storage = None):
        '''Return whether an hexagon is already occupied in ._positions:
        deck.isOccupied(rowcoltab)'''
        if storage is None:
             storage = self._positions
        return rowcoltab in storage

    def is_movable(self, rowcoltab1, rowcoltab2):
        row1, col1, table1 = rowcoltab1
        row2, col2, table2 = rowcoltab2
        #Ignore movement when:
        if self.is_occupied(rowcoltab2):
            #Return False if destination is already occupied
            print('Destination tile is occupied: ' + str(rowcoltab2))
            return False
        """if cfg.turn == 1 and rowcoltab1[2] == -2:
            print("It is player1's cfg.turn. You cannot move the opponent's tiles")
            return False
        if cfg.turn == 2 and rowcoltab[2] == -1:
            print("It is player2's cfg.turn. You cannot move the opponent's tiles")
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
        if cfg.turn % 2 == 1 and num_curr_tiles_on_hand2 < 6:
            msg = "It is hand1's turn, there are tiles of hand2 out"
        elif cfg.turn % 2 == 0 and num_curr_tiles_on_hand1 < 6:
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
                    raise UserWarning("more than one tile were added to table in this cfg.turn. I should not see this msg")
                else:
                    rowcoltab = rowcoltab[0]
                    #Check if new tile is adjacent to other tiles
                    neighboring = deck.get_neighboring_tiles(rowcoltab[0], rowcoltab[1])
                    if not neighboring:
                        return "The tile at ({},{}) is not adjacent to any other tile on the table".format(rowcoltab[0], rowcoltab[1])
                    ind = self.get_index_from_rowcoltab(rowcoltab)
                    tile = deck.tiles[ind]
                    #Check is colors match
                    match = tile.tile_match_colors(rowcoltab)
                    if not match:
                        msg = "The tile added at ({},{}) does not match the surrounding colors".format(rowcoltab[0],rowcoltab[1])
                        print("tile {} ind={}, rowcoltab={}".format(str(tile), str(ind), str(rowcoltab)) )
                        tile.tile_match_colors(rowcoltab)
                    else:
                        #Check matching tiles for forced spaces, and see if moved tile is between them
                        obliged_hexagons = self.check_forced()
                        matching = []
                        matches = [self.find_matching_tiles(o, [-1 * (2 - (cfg.turn % 2))]) for o in obliged_hexagons]
                        matching = [m for m in matches if len(m)]
                        if len(matching): #BUG SOLVED?
                            if rowcoltab not in obliged_hexagons:
                                msg = "There are forced spaces on the table. First fill those."
                        #Check if any neighbors must match three identical colors
                        if cfg.turn < 44 - 12:
                            check = self.impossible_neighbor(rowcoltab)
                            if check:
                                msg = check
                        if self.controlled_side(rowcoltab):
                            msg = "Cannot move here, there is a controlled side."
        else:
            raise UserWarning("is_confirmable: Cannot determine if confirmable")
        if msg is not "":
            return msg
        return True
        #Raise error
        #todo: maybe make a property deck.confirmable

    def confirm_move(self):
        #print("confirm_move. cfg.TRYING="+str(cfg.TRYING))
        confirmable = self.is_confirmable()
        if confirmable != True:
            print("confirm_move: Cannot confirm this move because: " + confirmable)
            return False
        #Place first tile in the middle
        """if cfg.turn == 1:
            rowcoltab = self.get_rowcoltab_from_rowcolnum(self._positions_moved[0])
            self.move_automatic(rowcoltab, (math.floor(cfg.ROWS / 2) - 1, math.floor(cfg.COLS / 2), 0))"""

        """Update confirmed storage and _positions"""
        #Use descending loop on _positions_moved because I will remove items from it
        for i in range(len(self._positions_moved) - 1, -1, -1):
            moved_rowcolnum = self._positions_moved[i]
            moved_rowcoltab = self.get_rowcoltab_from_rowcolnum(moved_rowcolnum)
            if moved_rowcoltab[2] == 0:
                #._confirmed[0] must get one tile more
                self._confirmed[-moved_rowcoltab[2]].append(moved_rowcolnum)
                #Lock the confirmed tile
                ind = self.get_index_from_rowcoltab(moved_rowcoltab)
                tile = self.tiles[ind]
                tile.lock = True
                #._confirmed[1] or ._confirmed[2] must remove one tile
                for table in (1, 2):
                    match = filter(lambda t : t[2] == moved_rowcoltab[2], [tup for tup in self._confirmed[table]])
                    if len(match) == 1:
                        self._confirmed[table].remove(match[i])
                        break
                    elif len(match) > 1:
                        raise UserWarning("confirm_move: ._confirmed[{}] has more than one tile played!".format(str(table)))
                self._positions_moved.remove(moved_rowcolnum)
            elif moved_rowcolnum[2] in [n[2] for n in self._confirmed[-moved_rowcoltab[2]] ]:
                #Here I reconfirmed tiles that were moved from e.g. top to top
                ind_to_change = [(j, v) for (j, v) in enumerate(self._confirmed[-moved_rowcoltab[2]]) if v[2] == moved_rowcolnum[2]]
                print(len(ind_to_change))
                self._confirmed[-moved_rowcoltab[2]][ind_to_change[0][0]] = moved_rowcolnum


        if 0:
            #Update each confirmed table (._confirmed[0], ._confirmed[1], ._confirmed[2])
            for ind, rowcoltab in enumerate(self._positions):
                #row, col, tab = pos
                rowcolnum = self.get_rowcolnum_from_rowcoltab(rowcoltab)
                if rowcoltab[2] == 0:
                    if rowcolnum not in self._confirmed[-rowcoltab[2]]:
                        #._confirmed[0] must get one tile more
                        self._confirmed[-rowcoltab[2]].append(rowcolnum)
                        #Lock the confirmed tile
                        tile = self.tiles[ind]
                        tile.lock = True
                        #._confirmed[1] or ._confirmed[2] must remove one tile
                        for table in (1, 2):
                            match = filter(lambda t : t[2] == rowcolnum[2], [tup for tup in self._confirmed[table]])
                            if len(match) == 1:
                                self._confirmed[table].remove(match[0])
                                break
                            elif len(match) > 1:
                                raise UserWarning("confirm_move: ._confirmed[{}] has more than one tile played!".format(str(table)))
                        self._positions_moved.remove(rowcolnum)
                elif rowcolnum[2] in [n[2] for n in self._confirmed[-rowcoltab[2]] ]:
                    #Here I reconfirmed tiles that were moved from e.g. top to top
                    ind_to_change = [(i,v) for (i,v) in enumerate(self._confirmed[-rowcoltab[2]]) if v[2] == rowcolnum[2]]
                    self._confirmed[-rowcoltab[2]][ind_to_change[0][0]]=rowcolnum

        #Make sure that after the play there are no forced spaces
        #todo: do not change cfg.turn when a forced space is filled before the cfg.free move!
        obliged_hexagons = self.check_forced()
        matchinglistcurrent = []
        matches = [self.find_matching_tiles(o, [-1 * (2 - (cfg.turn % 2))]) for o in obliged_hexagons]
        matchinglistcurrent = [m for m in matches if len(m)]

        if len(matchinglistcurrent):
            #There are matching tiles of current player fitting in forced spaces. Do nothing
            print("There are tiles of current player fitting in forced spaces. Fine, but I will not change cfg.turn")
        else:
            #No matching tiles. If before cfg.free move only do: cfg.free=True
            #global cfg.free
            if not cfg.free:
                cfg.free = True
            else:
                #No matching tiles. If after cfg.free move change cfg.turn and set cfg.free Ture/False for other player
                #global cfg.turn
                cfg.turn += 1
                matchinglistcurrent = []
                matches = [self.find_matching_tiles(o, [-1 * (2 - (cfg.turn % 2))]) for o in obliged_hexagons]
                matchinglistcurrent = [m for m in matches if len(m)]

                if len(matchinglistcurrent):
                    cfg.free = False
                else:
                    cfg.free = True
        print(cfg.turn)
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
            self.log()
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
            if rowcolnum2 not in cfg.deck.get_confirmed_rowcolnums_in_table(tab2):
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
                        ind_conf = cfg.deck._confirmed[-tab].index((0, cols, num))
                        try:
                            cfg.deck._confirmed[-tab][ind_conf] = (0, i, num)
                        except:
                            self.log()
                            print("cfg.deck._confirmed[1].index() is not in list".format(str((0, cols, num))))
                        #if tab == -1:
                        #    ind_conf = cfg.deck._confirmed[1].index((0, cols, num))
                        #    cfg.deck._confirmed[1][ind_conf] = (0, i, num)
                        #elif tab == -2:
                        #    ind_conf = cfg.deck._confirmed[2].index((0, cols, num))
                        #    cfg.deck._confirmed[2][ind_conf] = (0, i, num)
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
            tab_confirmed = [-1, 0, -2]
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
            hex = cfg.board.get_neighboring_hexagons(t[0], t[1])
            [surr.add(h) for h in hex]
        #print("surrounding tiles=",str(surr))
        for t in table:
            rowcoltab = self.get_rowcoltab_from_rowcolnum(t)
            if rowcoltab in surr:
                surr.remove(rowcoltab)
        return surr

    def check_forced(self):
        '''Check for forced spaces on the main table. Return the hexagons rowcolnum'''
        hex_surrounding_board = self.get_surrounding_hexagons(self._confirmed[0])
        obliged_hexagons = []
        rowcoltab_in_confirmed0 = [self.get_rowcoltab_from_rowcolnum(c) for c in self._confirmed[0]]
        for s in hex_surrounding_board:
            #Get confirmed neighboring tiles
            rowcoltabs = cfg.board.get_neighboring_hexagons(s[0], s[1])
            #Find if there is a tile on rowcoltab
            confirmed_neigh_tiles = 0
            for rowcoltab in rowcoltabs:
                if rowcoltab in rowcoltab_in_confirmed0:
                    confirmed_neigh_tiles += 1
            #Count confirmed neighbouring tiles
            if confirmed_neigh_tiles == 3:
                print("Forced space at {},{}".format(s[0], s[1]))
                obliged_hexagons.append(s)
                #Get tiles matching
            elif confirmed_neigh_tiles > 3:
                raise UserWarning("Hexagon at {},{} is surrounded by >3 tiles!".format(s[2], s[0], s[1]))
        return obliged_hexagons

    def find_matching_tiles(self, rowcoltab, table = [-1, -2]):
        '''Find all tiles that fit in an empty hexagon. Return a list of rocolnum'''
        #Get the neighbors
        color_index = cfg.deck.get_neighboring_colors(rowcoltab)
        if not len(color_index):
            print("find_matching_tiles: hexagon has no neighbors".format(str(rowcoltab)))
            return
        elif len(color_index) > 3 and not cfg.TRYING:
            raise UserWarning("Four neighbors!")
        #Get the colors surrounding the tile
        colors_temp = ''
        j = 0
        for i in range(0, 6):
            if j >= len(color_index):
                colors_temp += '-'
            elif i == color_index[j][1]:
                colors_temp += color_index[j][0]
                j += 1
            else:
                colors_temp += '-'
        colors_temp *= 2
        colors_temp = colors_temp.split('-')
        colors_temp2 = [i for i in colors_temp if i is not '']
        colors = colors_temp2[1]
        #
        num = self.get_tile_number_from_rowcoltab(rowcoltab)
        match = []
        for tab in table:
            #Get all confirmed tiles in the desired table
            confs = self.get_confirmed_rowcolnums_in_table(tab)
            for conf in confs:
                ind2 = self.get_index_from_tile_number(conf[2])
                tile2 = self.tiles[ind2]
                if colors in tile2.basecolors + tile2.basecolors:
                    match.append(self._positions[ind2])
        return match

    def impossible_neighbor(self, rowcolnum):
        neigh_rowcoltabs = cfg.board.get_neighboring_hexagons(rowcolnum)
        inmaintable = self.get_rowcoltabs_in_table(0)
        for rct in neigh_rowcoltabs:
            if rct not in inmaintable:
                colors = self.get_neighboring_colors(rct)
                if len(colors) == 3:
                    if colors[0][0] == colors[1][0] and colors[0][0] == colors[2][0]:
                        return "Cannot move here otherwise a neighboring tile would have to match three identical colors"
                elif len(colors) == 4:
                    return "Cannot move here otherwise a neighboring tile would have four neighbors"
        return False

    def controlled_side(self, rowcoltab):
        rowcol_inmain = [(rcn[0], rcn[1]) for rcn in self._confirmed[0]]
        if len(rowcol_inmain) < 3:
            return False
        cube0 = cfg.board.off_to_cube(rowcoltab[0], rowcoltab[1])
        neigh = self.get_neighboring_colors(rowcoltab) #(color, ind, n)
        neigh_number = len(neigh)
        if neigh_number > 2:
            return False
        #Directions of the neighbors
        dir_ind1 = [n[1] for n in neigh]
        cfg.board.remove_all_highlights()
        cfg.board.place_highlight((rowcoltab[0], rowcoltab[1], 0), "green")
        #Take each of the one or two neighbors at a certain direction.
        for i1 in range(0, neigh_number):
            cube1 = map(lambda x, y : x + y, cube0, cfg.directions[dir_ind1[i1]])
            rowcol1 = cfg.board.cube_to_off(cube1)
            cfg.board.place_highlight((rowcol1[0], rowcol1[1], 0), "red")

            #Find new direction to go straight
            if neigh_number == 1:
                #explore both angles
                dir_ind2n = [dir_ind1[i1] - 1, dir_ind1[i1] + 1]
            else:
                #go opposite to the other neighbor
                dir_ind2n = (dir_ind1[i1] + dir_ind1[i1] - dir_ind1[(i1 + 1) % 2] + 6) % 6
            for i2 in range(0, len(dir_ind2n)):
                cube2n = map(lambda x, y : x + y, cube1, cfg.directions[dir_ind2n[i2]])
                rowcol2n = cfg.board.cube_to_off(cube2n)
                cfg.board.place_highlight((rowcol2n[0], rowcol2n[1], 0))
                if rowcol2n not in rowcol_inmain:
                    continue
                #go straight till the end but check at right angle as well
                empty2n = False
                while empty2n is False:
                    #Check tile at an angle
                    dir_indn = (dir_ind2n[i2] - dir_ind1[i1] + dir_ind2n[i2] + 6 ) % 6 #todo i think this is not always good
                    cuben = map(lambda x, y : x + y, cube2n, cfg.directions[dir_indn])
                    rowcoln = cfg.board.cube_to_off(cuben)
                    cfg.board.place_highlight((rowcoln[0], rowcoln[1], 0))
                    if rowcoln in rowcol_inmain:
                        return True
                    #update tile to the one straight ahead. exit while loop if empty
                    cube2n = map(lambda x, y : x + y, cube2n, cfg.directions[dir_ind2n[i2]])
                    rowcol2n = cfg.board.cube_to_off(cube2n)
                    cfg.board.place_highlight((rowcol2n[0], rowcol2n[1], 0))
                    if rowcol2n not in rowcol_inmain:
                        empty2n = True
        return False




    def controlled_side2(self, rowcoltab):
        rowcol_inmain = [(rcn[0], rcn[1]) for rcn in self._confirmed[0]]
        if len(rowcol_inmain) < 3:
            return False
        cube = cfg.board.off_to_cube(rowcoltab[0], rowcoltab[1])
        #For each direction in cfg.directions, define two direction at 60 and -60/300 angles
        #directions = [[0, 1, -1], [+1, 0, -1], [+1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0]]
        dir60or300 = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1],
                      [-1, 1, 0], [0, 1, -1], [1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1]]
        for i, dir in enumerate(cfg.directions):
            #Go straight. We will turn 60 degrees, see if we can go straight and if there are tiles
            empty = False
            while not empty:
                cfg.board.remove_all_highlights()
                cfg.board.place_highlight((rowcoltab[0], rowcoltab[1], 0), "green")
                cube1 = map(lambda x, y : x + y, cube, dir)
                rowcol1 = cfg.board.cube_to_off(cube1)
                cfg.board.place_highlight((rowcol1[0], rowcol1[1], 0))
                if rowcol1 not in rowcol_inmain:
                    break
                #step in same direction+-60degrees
                for j1 in (0, 1):
                    cube2 = map(lambda x, y : x + y, cube1, dir60or300[i + j1 * 6])
                    rowcol2 = cfg.board.cube_to_off(cube2)
                    cfg.board.place_highlight((rowcol2[0], rowcol2[1], 0))
                    if rowcol2 in rowcol_inmain:
                        #Find in what diretion we just went
                        lastdir = [cube2[ii] - cube1[ii] for ii in range(0,3)]
                        lastdirind = cfg.directions.index(lastdir)
                        #Here try to go straight until end.
                        empty2 = False
                        while not empty2:
                            #Go straight
                            cube3 = map(lambda x, y : x + y, cube2, lastdir)
                            rowcol3 = cfg.board.cube_to_off(cube3)
                            #cfg.board.remove_all_highlights()
                            cfg.board.place_highlight((rowcol3[0], rowcol3[1], 0))
                            if rowcol3 not in rowcol_inmain:
                                empty2 = True
                                cfg.board.remove_highlight((rowcol3[0], rowcol3[1], 0))

                                #Step in previous direction+-60 and check tile there
                                #for j2 in (lastdirind, lastdirind + 6):
                                cube_angle = map(lambda x, y : x + y, cube2, dir60or300[lastdirind + j1 * 6])
                                rowcol_angle = cfg.board.cube_to_off(cube_angle)
                                cfg.board.place_highlight((rowcol_angle[0], rowcol_angle[1], 0))
                                if rowcol_angle in rowcol_inmain:
                                    return True
                            empty2 = True
                        #empty = True
                empty = True

    def score(self, player):
        #http://www.redblobgames.com/grids/hexagons/#pathfinding
        cfg.scores
        cfg.scores_loop
        _position_ind = self.get_neighboring_tiles()
        rowcolnum = self.get_confirmed_rowcolnums_in_table(0)

    def log(self, msg = " "):
        print(msg)
        #print("TRYING=" + str(cfg.TRYING))
        print(" cfg.deck._positions=" + str(cfg.deck._positions[0:4]))
        print("                   =" + str(cfg.deck._positions[4:8]))
        print("                   =" + str(cfg.deck._positions[8:]))
        print(" cfg.deck._table=" + str(cfg.deck._table))
        print(" cfg.deck._positions_moved=" + str(cfg.deck._positions_moved))
        print(" cfg.deck._confirmed[0]=" + str(cfg.deck._confirmed[0]))
        print(" cfg.deck._confirmed[1]=" + str(cfg.deck._confirmed[1]))
        print(" cfg.deck._confirmed[2]=" + str(cfg.deck._confirmed[2]))
        print(" cfg.deck.itemids=" + str(cfg.deck.itemids))
        print(" cfg.deck.dealt=" + str(cfg.deck.dealt))
        print(" cfg.deck.is_confirmable= " + str(cfg.deck.is_confirmable()))
        print(" cfg.board._highlightids=" + str(cfg.board._highlightids))
        print(" cfg.board._highlight=" + str(cfg.board._highlight))
        print(" cfg.turn free=" + str((cfg.turn, cfg.free)))

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
            cfg.win.geometry('%dx%d' % (w, h))
            w = w + 76
            x = x - 76 - 240
            cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, 650))
            #cfg.win.geometry('%dx%d+%d+%d' % (w + 76, h, 0, 600))
            #print(w, h, x, 600)
        print("x={}, xleft is {}, xright={}".format(x,2559,2214))

        from pymouse import PyMouse
        m = PyMouse()

        cfg.canvasmain = tk.Canvas(cfg.win, height = cfg.YBOTTOM + cfg.HEX_HEIGHT,
            width = cfg.CANVAS_WIDTH, name = "canvasmain")

        #Create hexagons on cfg.canvasmain
        cfg.canvasmain.create_rectangle(0, cfg.YTOP, cfg.CANVAS_WIDTH, cfg.YBOTTOM,
                                        width = 2, fill = "#D2DFC8") #light green
        cfg.canvasmain.create_rectangle(0, 0, cfg.CANVAS_WIDTH, cfg.YTOP,
                                        width = 2, fill = "#FEFD6C") #yellow top
        cfg.canvasmain.create_rectangle(0, cfg.YBOTTOM, cfg.CANVAS_WIDTH, cfg.YBOTTOM + cfg.HEX_HEIGHT,
                                        width = 2, fill = "#6AFF07") #green bottom
        cfg.canvasmain.create_rectangle(cfg.CANVAS_WIDTH, 0, cfg.CANVAS_WIDTH + 76, cfg.YBOTTOM + cfg.HEX_HEIGHT, width = 2, fill = "#FF65D6") #green bottom
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
        import test as ts
        ts.tests()


if __name__ == "__main__":
    gui_instance = Gui()
    gui_instance.main()
    cfg.canvasmain.mainloop()