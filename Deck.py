import math
try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import random
import config as cfg
import helpers as hp
from Tile import Tile
import tkMessageBox as mb


class Deck(hp.DeckHelper):

    def __init__(self):
        self.tiles = []       #this contains tile in PhotoImage format
        self.itemids = []     #itemid = cfg.canvas.create_image()
        self.undealt =range(1, 57) #1:56
        self.dealt = [] #1:56
        self._positions = []   #(row, col, table)
        self._table = [] #(table)
        self._positions_moved = []   #(row, col, table, num)
        self._confirmed = []
        self._confirmed.append([])  #after do it for number of players
        self._confirmed.append([])
        self._confirmed.append([])

    def is_occupied(self, rowcoltab, storage = None):
        '''Return whether an hexagon is already occupied in storage,
        which is by default ._positions'''
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
            tile = self.tiles[ind1]
            #tile, ind1 = self.get_tile_from_tile_number(rowcoltab1[2])
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
            print('trying to move from .canvas to top or bottom')
            return False
        return True

    def is_confirmable(self, show_msg = False):
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
        msg = ""
        if cfg.turn % 2 == 1 and num_curr_tiles_on_hand2 < 6:
            msg = "There are tiles of Player 2 out"
        elif cfg.turn % 2 == 0 and num_curr_tiles_on_hand1 < 6:
            msg = "There are tiles of Player 1 out"
        elif num_curr_tiles_on_hand1 > 6 or num_curr_tiles_on_hand2 > 6:
            msg = "A Player has more than 6 tiles"
        elif num_curr_tiles_on_hand1 == 6 and num_curr_tiles_on_hand2 == 6:
            msg = "No tiles were placed on the board"
            forced = self.check_forced()
            if not forced:
                matches = [self.find_matching_tiles(f, [-1 * (2 - (cfg.turn % 2))]) for f in forced]
                if len(matches):
                    msg = "No new tiles but first fill in forced spaces"
        elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 > 11:
            msg = "no tiles from hand1 or hand2 are out2"
        elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 < 11:
            msg = "More than 1 tile from hand1 and hand2 are out"
        elif num_confirmed_tiles_on_table - num_curr_tiles_on_table == 0:
            msg = "No tiles were added to the table"
        elif num_confirmed_tiles_on_table - num_curr_tiles_on_table > 1:
            raise UserWarning("more than one tile were added to the table. I should not see this msg")
        elif num_curr_tiles_on_table - num_confirmed_tiles_on_table < 0:
            raise UserWarning("There are less tiles on table that in ._confirmed[0]. I should not see this msg")
        elif num_curr_tiles_on_hand1 + num_curr_tiles_on_hand2 == 11:
            if num_curr_tiles_on_table == 1:
                #only one tile on the table
                pass
            elif num_curr_tiles_on_table - num_confirmed_tiles_on_table == 1:
                """Find tile to be confirmed"""
                for m in self._positions_moved:
                    rowcoltab = self.get_rowcoltab_from_rowcolnum(m)
                    if rowcoltab[2] == 0:
                        break
                #rowcolnum = [m for m in self._positions_moved if self.get_rowcoltab_from_rowcolnum(m)[2] == 0]
                #rowcoltab = rowcoltab[0]
                #rowcoltab = [ct for ct in curr_tiles_on_table if self.get_tile_number_from_rowcoltab(ct) not in [c[2] for c in self._confirmed[0]]]
                """Check if new tile is adjacent to other tiles"""
                neighboring = self.get_neighboring_tiles(rowcoltab[0], rowcoltab[1])
                if not neighboring:
                    return "One tile is not adjacent to any other tile"
                ind = self.get_index_from_rowcoltab(rowcoltab)
                tile = self.tiles[ind]
                #tile = self.get_tile_from_tile_number(rowcoltab[2])
                """Check if colors match"""
                match = tile.tile_match_colors(rowcoltab)
                if not match:
                    msg = "Colors do not match"
                    print("tile {}, rowcoltab={}".format(str(tile), str(rowcoltab)) )
                    tile.tile_match_colors(rowcoltab)
                else:
                    """Check matching tiles for forced spaces, and see if moved tile is between them"""
                    obliged_hexagons = self.check_forced()
                    matching = []
                    matches = [self.find_matching_tiles(o, [-1 * (2 - (cfg.turn % 2))]) for o in obliged_hexagons]
                    matching = [m for m in matches if len(m)]
                    if len(matching):
                        if rowcoltab not in obliged_hexagons:
                            msg = "Fill all forced spaces"
                    #Check if any neighbors must match three identical colors
                    if not msg:
                        if cfg.turn < 44 - 12:
                            check = self.impossible_neighbor(rowcoltab)
                            if check:
                                msg = check
                        if self.controlled_side(rowcoltab):
                            msg = "A controlled side prevents this rule"
        if show_msg:
            cfg.board.message(msg)
        if msg is not "":
            return msg
        return True

    def confirm_move(self):
        '''Confirm position of moved tile, if possible'''
        confirmable = self.is_confirmable()
        if confirmable != True:
            cfg.board.message(confirmable)
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
                '''._confirmed[0] must get one tile more'''
                self._confirmed[-moved_rowcoltab[2]].append(moved_rowcolnum)
                '''Lock the confirmed tile'''
                ind = self.get_index_from_rowcoltab(moved_rowcoltab)
                tile = self.tiles[ind]
                tile.lock = True
                '''._confirmed[1] or ._confirmed[2] must remove one tile'''
                for table in (1, 2):
                    match = filter(lambda t : t[2] == moved_rowcolnum[2], [conf_rcn for conf_rcn in self._confirmed[table]])
                    if len(match) == 1:
                        self._confirmed[table].remove(match[i])
                        break
                    elif len(match) > 1:
                        raise UserWarning("confirm_move: ._confirmed[{}] has more than one tile played!".format(str(table)))
                self._positions_moved.remove(moved_rowcolnum)
            elif moved_rowcolnum[2] in [n[2] for n in self._confirmed[-moved_rowcoltab[2]] ]:
                '''Here I reconfirmed tiles that were moved from e.g. top to top'''
                ind_to_change = [(j, v) for (j, v) in enumerate(self._confirmed[-moved_rowcoltab[2]]) if v[2] == moved_rowcolnum[2]]
                print(len(ind_to_change))
                self._confirmed[-moved_rowcoltab[2]][ind_to_change[0][0]] = moved_rowcolnum

        """if 0:
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
                    self._confirmed[-rowcoltab[2]][ind_to_change[0][0]]=rowcolnum"""
        return self.post_confirm()

    def post_confirm(self):
        '''Take care of updating turn, free, the message etc'''
        """Make sure that after the play there are no forced spaces"""
        obliged_hexagons = self.check_forced()
        matchinglistcurrent = []
        matches = [self.find_matching_tiles(o, [-1 * (2 - (cfg.turn % 2))]) for o in obliged_hexagons]
        matchinglistcurrent = [m for m in matches if len(m)]
        msg = ""
        if len(matchinglistcurrent):
            """There are matching tiles of current player fitting in forced spaces. Do nothing"""
            msg = "There are forced spaces"
            [cfg.board.place_highlight(o) for o in obliged_hexagons]
            [cfg.board.place_highlight(m) for m in matchinglistcurrent[0]]
        else:
            """No matching tiles for current player"""
            if not cfg.free:
                cfg.free = True
            else:
                """Change current player and check if there are forces matches for that player"""
                cfg.turn += 1
                matchinglistother = []
                matches = [self.find_matching_tiles(o, [-1 * (2 - (cfg.turn % 2))]) for o in obliged_hexagons]
                matchinglistother = [m for m in matches if len(m)]
                if len(matchinglistother):
                    cfg.free = False
                    cfg.board.message("There are forced spaces")
                    [cfg.board.place_highlight(o) for o in obliged_hexagons]
                    [cfg.board.place_highlight(m) for m in matchinglistother[0]]
                else:
                    cfg.free = True
        if cfg.turn % 2:
            cfg.canvas.itemconfig(cfg.pl1, stipple="")
            cfg.canvas.itemconfig(cfg.pl2, stipple="gray25")
            cfg.board.message(msg)
        else:
            cfg.canvas.itemconfig(cfg.pl2, stipple="")
            cfg.canvas.itemconfig(cfg.pl1, stipple="gray25")
            cfg.board.message(msg)
        cfg.win.update()
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
        cfg.canvas.delete(itemid)
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
        num = self.dealt.pop(ind)
        #Return information
        pos = self._positions.pop(ind)
        table = self._table.pop(ind)
        tile = self.tiles.pop(ind)
        return (pos, num, tile)

    def deal(self, row, col, tab, num = 'random'):
        row = int(row)
        col = int(col)
        #Random tile if num is not set
        global rndgen
        rndgen = random.Random(0)
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
        #Place on canvas
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
        itemid, ind = self.get_itemid_from_rowcoltab(rowcoltab1)
        tilex, tiley = cfg.board.off_to_pixel(rowcoltab2)
        cfg.canvas.coords(itemid, (tilex, tiley))
        #Update moved storage
        num = self.dealt[ind]
        rowcolnum1 = tuple([rowcoltab1[0], rowcoltab1[1], num])
        rowcolnum2 = tuple([rowcoltab2[0], rowcoltab2[1], num])
        if rowcolnum1 in self._positions_moved:
            self._positions_moved.remove(rowcolnum1)
        #todo: also _position_moved for tiles that go to top/bottom but not on original place
        if tab2 == 0:
            self._positions_moved.append(rowcolnum2)
        elif rowcoltab2 not in self.get_rowcoltabs_in_table(tab2):
            if rowcolnum2 not in self.get_confirmed_rowcolnums_in_table(tab2):
                self._positions_moved.append(rowcolnum2)
        self._positions[ind] = (rowcoltab2)
        self._table[ind] = (tab2)
        #Update window
        cfg.win.update()
        return True

    def move_automatic(self, rowcoltab1, rowcoltab2):
        '''move tile. NB: .move is used and therefore also ._positions_moved is updated'''
        itemid, ind = self.get_itemid_from_rowcoltab(rowcoltab1)
        #tile = self.tiles[ind]
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
            cfg.canvas.coords(itemid, (xi, yi))
            cfg.canvas.after(15, cfg.win.update())
        ok = self.move(rowcoltab1, rowcoltab2)
        return ok

    def rotate(self, rowcoltab):
        '''Rotate a tile if tile is not locked: spawn it, replace itemid in self.itemids.
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
        '''Refill a player's deck'''
        """Check how many tiles there are"""
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
                        ind_conf = self._confirmed[-tab].index((0, cols, num))
                        try:
                            self._confirmed[-tab][ind_conf] = (0, i, num)
                        except:
                            self.log()
                            print("self._confirmed[1].index() is not in list".format(str((0, cols, num))))
                        #if tab == -1:
                        #    ind_conf = self._confirmed[1].index((0, cols, num))
                        #    self._confirmed[1][ind_conf] = (0, i, num)
                        #elif tab == -2:
                        #    ind_conf = self._confirmed[2].index((0, cols, num))
                        #    self._confirmed[2][ind_conf] = (0, i, num)
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
        """Refill deck"""
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
            #Find if there is a tile on rowcoltabs
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
        '''Find all tiles of a table that fit in an empty hexagon. Return a list of rocolnum'''
        """Get the neighbors"""
        color_index = self.get_neighboring_colors(rowcoltab)
        if not len(color_index):
            print("find_matching_tiles: hexagon has no neighbors".format(str(rowcoltab)))
            return
        elif len(color_index) > 3 and not cfg.TRYING:
            raise UserWarning("Four neighbors!")
        """Get the colors surrounding the tile"""
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
        #num = self.get_tile_number_from_rowcoltab(rowcoltab)
        match = []
        for tab in table:
            #Get all confirmed tiles in the desired table
            confs = self.get_confirmed_rowcolnums_in_table(tab)
            for conf in confs:
                ind2 = self.get_index_from_tile_number(conf[2])
                tile2 = self.tiles[ind2]
                #tile2, ind2 = self.get_tile_from_tile_number(conf[2])
                if colors in tile2.basecolors + tile2.basecolors:
                    match.append(self._positions[ind2])
        print("find_matching_tiles gives: ",str(match))
        return match

    def impossible_neighbor(self, rowcolnum):
        neigh_rowcoltabs = cfg.board.get_neighboring_hexagons(rowcolnum)
        inmaintable = self.get_rowcoltabs_in_table(0)
        for rct in neigh_rowcoltabs:
            if rct not in inmaintable:
                colors = self.get_neighboring_colors(rct)
                if len(colors) == 3:
                    if colors[0][0] == colors[1][0] and colors[0][0] == colors[2][0]:
                        return "A neighboring tile would have to match three identical colors"
                elif len(colors) == 4:
                    return "A neighboring tile would have four neighbors"
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
        #cfg.board.remove_all_highlights()
        #cfg.board.place_highlight((rowcoltab[0], rowcoltab[1], 0), "green")
        #Take each of the one or two neighbors at a certain direction.
        for i1 in range(0, neigh_number):
            cube1 = map(lambda x, y : x + y, cube0, cfg.directions[dir_ind1[i1]])
            rowcol1 = cfg.board.cube_to_off(cube1)
            #cfg.board.place_highlight((rowcol1[0], rowcol1[1], 0), "red")

            #Find new direction to go straight
            if neigh_number == 1:
                #explore both angles
                dir_ind2n = [dir_ind1[i1] - 1, dir_ind1[i1] + 1]
            else:
                #go opposite to the other neighbor
                dir_ind2n = (dir_ind1[i1] + dir_ind1[i1] - dir_ind1[(i1 + 1) % 2] + 6) % 6
            for i2 in range(0, len(list(dir_ind2n))):
                cube2n = map(lambda x, y : x + y, cube1, cfg.directions[dir_ind2n[i2]])
                rowcol2n = cfg.board.cube_to_off(cube2n)
                #cfg.board.place_highlight((rowcol2n[0], rowcol2n[1], 0))
                if rowcol2n not in rowcol_inmain:
                    continue
                #go straight till the end but check at right angle as well
                empty2n = False
                while empty2n is False:
                    #Check tile at an angle
                    dir_indn = (dir_ind2n[i2] - dir_ind1[i1] + dir_ind2n[i2] + 6 ) % 6 #todo i think this is not always good
                    cuben = map(lambda x, y : x + y, cube2n, cfg.directions[dir_indn])
                    rowcoln = cfg.board.cube_to_off(cuben)
                    #cfg.board.place_highlight((rowcoln[0], rowcoln[1], 0), "blue")
                    if rowcoln in rowcol_inmain:
                        return True
                    #update tile to the one straight ahead. exit while loop if empty
                    cube2n = map(lambda x, y : x + y, cube2n, cfg.directions[dir_ind2n[i2]])
                    rowcol2n = cfg.board.cube_to_off(cube2n)
                    #cfg.board.place_highlight((rowcol2n[0], rowcol2n[1], 0))
                    if rowcol2n not in rowcol_inmain:
                        empty2n = True
        return False

    def score(self, color):
        #http://www.redblobgames.com/grids/hexagons/#pathfinding
        print("cfg.scores     =" + str(cfg.scores))
        print("cfg.scores_loop=" + str(cfg.scores_loop))
        if cfg.turn == 1:
            return
        """conf_rowcolnums = self._confirmed[0]    #[(3.0, 1.0, 46), (3.0, 2.0, 42)]
        rowcolnum = self._confirmed[0][0]       #(3.0, 1.0, 46)
        print("rowcoltab=" + str(rowcolnum))
        _position_ind = self.get_neighboring_tiles(rowcolnum) #7
        print(_position_ind)
        conf_rowcolnums = self.get_confirmed_rowcolnums_in_table(0) # [(3.0, 1.0, 46), (3.0, 2.0, 42)]
        print(conf_rowcolnums)
        neigh_colors = self.get_neighboring_colors((3,2,24)) #[('b', 3, 8)]
        tile = self.get_tile_from_tile_number(rowcolnum[2])
        basecolors = tile.basecolors
        angle = tile.angle
        """

        score = []
        scanned_off = []
        scanned_num = [] #later decide which one is handier
        """Find first tile in _confirmed with the color"""
        """
        find = 0
        while not find:
            rowcolnum = self._confirmed[0][find]
            tile = self.get_tile_from_tile_number(rowcolnum[2])
            clr = tile.getColor()
            if color in clr:
                find = False
                score.append(1)
                #score_loop = 0
            scanned_num.append(rowcolnum[2])
            scanned_off.append(rowcolnum[0:2])
        curr_off = rowcolnum[0:2]
        """
        conf_rowcols = [c[0:2] for c in self._confirmed[0]]
        conf_nums = [c[2] for c in self._confirmed[0]]
        """Loop on all confirmed tiles"""
        all_scanned = False
        while not all_scanned:
            scanned_number = len(map(len, scanned_off))
            if scanned_number >= len(self._confirmed[0]):
                all_scanned = True #not needed, just break?
                break
            else:
                #Find the first _confirmed that was not scanned
                while 1:
                    rowcolnum = [c for c in self._confirmed[0] if c[0:2] not in scanned_off][0]
                    tile = self.get_tile_from_tile_number(rowcolnum[2])
                    clr = tile.getColor()
                    if color in clr:
                        #find = False
                        score.append(1)
                        print("score = ", score)
                        scanned_num.append(rowcolnum[2])
                        scanned_off.append(rowcolnum[0:2])
                        curr_off = rowcolnum[0:2]
                        break
                cfg.board.place_highlight((curr_off[0], curr_off[1], 0))
            """Loop on a thread"""
            thread = True
            while thread:
                """Get the angle of the color, then follow to the adjacent tile"""
                angs = (c.find('r'),c.rfind('r'))
                ang = clr.index(color) #todo get the right angle! not always the first!
                dir = cfg.directions[ang]
                cube = cfg.board.off_to_cube(curr_off[0], curr_off[1])
                next_cube = tuple(map(lambda c, d: c + d, cube, dir))
                next_off = cfg.board.cube_to_off(next_cube)
                cfg.board.place_highlight((next_off[0], next_off[1], 0))
                #todo: be able to change direction for the first found tile!!!
                """Check if it closes the loop"""
                if next_off in scanned_off:
                    score_loop = score[-1] * 2
                    score.pop()
                    thread = False
                    cfg.board.remove_all_highlights()
                    break
                """Check if present"""
                if self.is_occupied((next_off[0], next_off[1]), conf_rowcols): #_confirmed[0] needs the num
                    curr_off = next_off
                    score[-1] += 1
                    num = self.get_tile_number_from_rowcoltab((curr_off[0], curr_off[1], 0))
                    scanned_num.append(num)
                    scanned_off.append(curr_off)
                    direction_we_came_from =
                    print("score = ", str(score))
                else:
                    thread = False
                    break

        cfg.board.remove_all_highlights()
        return score, score_loop



    def log(self, msg = " "):
        print(msg)
        #print("TRYING=" + str(cfg.TRYING))
        print(" cfg.deck._positions=" + str(self._positions[0:4]))
        print("                   =" + str(self._positions[4:8]))
        print("                   =" + str(self._positions[8:]))
        print(" cfg.deck._table=" + str(self._table))
        print(" cfg.deck._positions_moved=" + str(self._positions_moved))
        print(" cfg.deck._confirmed[0]=" + str(self._confirmed[0]))
        print(" cfg.deck._confirmed[1]=" + str(self._confirmed[1]))
        print(" cfg.deck._confirmed[2]=" + str(self._confirmed[2]))
        print(" cfg.deck.itemids=" + str(self.itemids))
        print(" cfg.deck.dealt=" + str(self.dealt))
        print(" cfg.deck.is_confirmable= " + str(self.is_confirmable(True)))
        print(" cfg.board._highlightids=" + str(cfg.board._highlightids))
        print(" cfg.board._highlight=" + str(cfg.board._highlight))
        print(" cfg.turn free=" + str((cfg.turn, cfg.free)))