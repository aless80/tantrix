import math
try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3

import config as cfg
import helpers as hp
from Tile import Tile
import tkMessageBox as mb
import sys
sys.path.insert(0, './tantrix/PodSixNet')
#from PodSixNet.Connection import ConnectionListener #, connection
from time import sleep

#colors for highlight_forced_and_matching
colors = list(cfg.PLAYERCOLORS)
colors.append(["yellow2", "DarkOrchid2", "magenta3", "cyan2", "green3", "firebrick", "dark violet",
                      "thistle1", "MediumPurple1", "purple1"])
forcedmove = False

#todo i put fixed tile extraction for testing
ran = 0

class Deck(hp.DeckHelper): #, ConnectionListener):

    def __init__(self):
        self.tiles = []       #this contains tile in PhotoImage format
        self.itemids = []     #itemid = cfg.canvas.create_image()
        self.undealt =range(1, 57) #1:56
        self.dealt = [] #1:56
        self._positions = []   #(row, col, table)
        self._table = [] #(table)
        self._positions_moved = []   #(row, col, table, player_num)
        self._confirmed = []
        self._confirmed.append([])  #after do it for number of players
        self._confirmed.append([])
        self._confirmed.append([])
        self._rotations = []

    def is_occupied(self, rowcoltab, storage = None):
        """Return whether an hexagon is already occupied in storage,
        which is by default ._positions"""
        if storage is None:
             storage = self._positions
        return rowcoltab in storage

    def is_movable(self, rowcoltab1, rowcoltab2):
        table1 = rowcoltab1[2]
        table2 = rowcoltab2[2]
        """Check if it goes out of the table"""
        x, y = cfg.board.off_to_pixel(rowcoltab2)
        if x > cfg.CANVAS_WIDTH:
            return False
        if table2 == 0:
            if y <= cfg.YTOPMAINCANVAS:
                return False
            elif y >= cfg.YBOTTOMMAINCANVAS:
                return False
        """Ignore movement when destination is already occupied"""
        if self.is_occupied(rowcoltab2):
            return False
        """Return False if trying to move from bottom to top or vice versa"""
        tile = self.get_tile_from_rowcolnum(rowcoltab1)
        if table2 != 0 and tile.confirm != table2:
            print('Cannot move from top to bottom or vice versa')
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
        """If two players are in a game, their turn is given by cfg.turnUpDown and cfg.player_num"""
        _turn = (2 - cfg.turnUpDown % 2 )
        if not cfg.solitaire and cfg.player_num is not _turn:
            msg = "It is %s's turn" % (cfg.opponentname)
        elif cfg.turnUpDown % 2 == 1 and num_curr_tiles_on_hand2 < 6:
            msg = "There are tiles of Player 2 out"
        elif cfg.turnUpDown % 2 == 0 and num_curr_tiles_on_hand1 < 6:
            msg = "There are tiles of Player 1 out"
        elif num_curr_tiles_on_hand1 > 6 or num_curr_tiles_on_hand2 > 6:
            msg = "A Player has more than 6 tiles"
        elif num_curr_tiles_on_hand1 == 6 and num_curr_tiles_on_hand2 == 6:
            msg = "No tiles were placed on the board"
            forced = self.check_forced()
            if not forced:
                matches = [self.find_matching_tiles(f, [-1 * (2 - (cfg.turnUpDown % 2))]) for f in forced]
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
                    matches = [self.find_matching_tiles(o, [-1 * (2 - (cfg.turnUpDown % 2))]) for o in obliged_hexagons]
                    matching = [m for m in matches if len(m)]
                    if len(matching):
                        if rowcoltab not in obliged_hexagons:
                            msg = "Fill all forced spaces"
                    """Check if any neighbors must match three identical color"""
                    if not msg:
                        if cfg.turnUpDown < 44 - 12:
                            check = self.impossible_neighbor(rowcoltab)
                            if check:
                                msg = check
                        if self.controlled_side(rowcoltab):
                            msg = "A controlled side prevents this move"
        if show_msg:
            cfg.board.message(msg)
        if msg is not "":
            return msg
        return True

    def confirm_move(self, send = True, force = False):
        """Confirm position of moved tile, if possible"""
        '''change of turn turnUpDown is done in post_confirm'''
        if force:
            confirmable = True
        else:
            confirmable = self.is_confirmable()
        if confirmable != True:
            cfg.board.message(confirmable)
            return False
        #Place first tile in the middle
        """if cfg.turnUpDown == 1:
            rowcoltab = self.get_rowcoltab_from_rowcolnum(self._positions_moved[0])
            self.move_automatic(rowcoltab, (math.floor(cfg.ROWS / 2) - 1, math.floor(cfg.COLS / 2), 0))"""
        """Update confirmed storage and _positions"""
        #Use descending loop on _positions_moved because I will remove items from it
        for i in range(len(self._positions_moved) - 1, -1, -1):
            moved_rowcolnum = self._positions_moved[i]      #Origin
            moved_rowcoltab2 = self.get_rowcoltab_from_rowcolnum(moved_rowcolnum)   #Destination
            if moved_rowcoltab2[2] == 0:
                '''._confirmed[0] must get one tile more'''
                self._confirmed[-moved_rowcoltab2[2]].append(moved_rowcolnum)
                '''._confirmed[1] or ._confirmed[2] must remove one tile'''
                for table in (1, 2):
                    match = filter(lambda t : t[2] == moved_rowcolnum[2], [conf_rcn for conf_rcn in self._confirmed[table]])
                    if len(match) == 1:
                        moved_rowcoltab1 = (match[i][0], match[i][1], -table)
                        self._confirmed[table].remove(match[i])
                        break
                    elif len(match) > 1:
                        raise UserWarning("confirm_move: ._confirmed[{}] has more than one tile played!".format(str(table)))
                """Remove confirmed from storage of unconfirmed moved tiles _positions_moved"""
                self._positions_moved.remove(moved_rowcolnum)
            elif moved_rowcolnum[2] in [n[2] for n in self._confirmed[-moved_rowcoltab2[2]] ]:
                '''Here I reconfirmed tiles that were moved from e.g. top to top'''
                ind_to_change = [(j, v) for (j, v) in enumerate(self._confirmed[-moved_rowcoltab2[2]]) if v[2] == moved_rowcolnum[2]]
                print(len(ind_to_change))
                self._confirmed[-moved_rowcoltab2[2]][ind_to_change[0][0]] = moved_rowcolnum
        """Update confirm storage in tile object"""
        ind = cfg.deck.get_index_from_tile_number(moved_rowcolnum[2])
        self.tiles[ind].confirmed = moved_rowcoltab2[2]
        """Send to server"""
        angle = self.tiles[ind].angle
        if send:
            moved_rowcolnum = (moved_rowcolnum[0] - cfg.shifts[0] * 2, moved_rowcolnum[1] - cfg.shifts[1], moved_rowcolnum[2])
            moved_rowcoltab2 = (moved_rowcoltab2[0] - cfg.shifts[0] * 2, moved_rowcoltab2[1] - cfg.shifts[1], moved_rowcoltab2[2])
            cfg.gui_instance.send_to_server("confirm", rowcolnum = moved_rowcolnum, rowcoltab1 = moved_rowcoltab1,
                                            rowcoltab2 = moved_rowcoltab2, angle = angle, turnUpDown = cfg.turnUpDown)
        """Append to history"""
        rowcoltabnumrotDest = list(moved_rowcoltab2)
        rowcoltabnumrotDest.append(moved_rowcolnum[2])
        rowcoltabnumrotDest.append(cfg.deck.tiles[ind].angle)
        action = "received: " if force else "confirmed:"
        cfg.history.append(["turn="+str(cfg.turnUpDown), cfg.name + " pl" + str(cfg.player_num),
                            "Forced: " + str(forcedmove), action, tuple(rowcoltabnumrotDest)])
        return True

    def highlight_forced_and_matching(self):
            global colors
            #define colors the first time
            if cfg.playercolor in colors:
                colors.remove(cfg.playercolor)
                colors.remove(cfg.opponentcolor)
                colors.remove(cfg.PLAYERCOLORS[cfg.PLAYERCOLORS.index(cfg.playercolor) + 4])
                colors.remove(cfg.PLAYERCOLORS[cfg.PLAYERCOLORS.index(cfg.opponentcolor) + 4])
            j = 0
            msg = ""
            obliged_hexagons = self.check_forced()
            table = [-1 * (2 - (cfg.turnUpDown % 2))]
            matches = [self.find_matching_tiles(o, table) for o in obliged_hexagons]
            matchinglistcurrent = matches
            if len(matchinglistcurrent):
                """There are matching tiles of current player fitting in forced spaces. Do nothing"""
                for i, o in enumerate(obliged_hexagons):
                    if len(matchinglistcurrent[i]):
                        msg = "There are forced spaces"
                        cfg.board.place_highlight(obliged_hexagons[i], colors[j % len(colors)])
                        for m in matchinglistcurrent[i]:
                            cfg.board.place_highlight(m, colors[j % len(colors)])
                        j += 1
            cfg.board.message(msg)
            return matchinglistcurrent

    def post_confirm(self):
        """Take care of updating turnUpDown, free, the message etc"""
        """Change current player: make sure that after the play there are no forced spaces"""
        matchinglistcurrent = self.highlight_forced_and_matching() #can be [], [[]] or [[(),()]]
        #Correct when matchinglistcurrent is [[]]
        matchinglistcurrent[:] = [x for x in matchinglistcurrent if len(x)]
        """history - match cur section"""
        matchinglistcurrentnum = list(matchinglistcurrent)
        if len(matchinglistcurrent) is not 0:
            for i, listt in enumerate(matchinglistcurrent):
                for j, rct in enumerate(listt):
                    num = cfg.deck.get_tile_number_from_rowcoltab(rct)
                    print(matchinglistcurrentnum[i][j])
                    matchinglistcurrentnum[i][j] = list(matchinglistcurrentnum[i][j])
                    matchinglistcurrentnum[i][j].append(num)
                    matchinglistcurrentnum[i][j] = tuple(matchinglistcurrentnum[i][j])
        cfg.history[-1].append("match cur:")
        cfg.history[-1].append(matchinglistcurrentnum)
        """Update turnUpDown when no matching tiles for current player"""
        if len(matchinglistcurrent) == 0:
            cfg.board.remove_all_highlights()
            global forcedmove
            if forcedmove:
                forcedmove = False
                cfg.history[-1].append("Forced becomes:" + str(forcedmove))
            else:
                """Change turn to next player because no forced tiles to place and the previous was not a forced move"""
                cfg.turnUpDown += 1
                self.update_stipples()
                """Check if there are forces matches for the opponent"""
                matchinglistother = self.highlight_forced_and_matching()
                #Correct when matchinglistcurrent is [[]] or [[(1,2,-1)],[]]
                matchinglistcurrent[:] = [x for x in matchinglistcurrent if len(x)]
                if len(matchinglistother):
                    forcedmove = True
                    cfg.board.message("There are forced spaces")
                else:
                    forcedmove = False
                """history - match opp"""
                matchinglistothernum = list(matchinglistother)
                if len(matchinglistother) is not 0:
                    for i, listt in enumerate(matchinglistother):
                        for j, rct in enumerate(listt):
                            num = cfg.deck.get_tile_number_from_rowcoltab(rct)
                            print(matchinglistothernum[i][j])
                            matchinglistothernum[i][j] = list(matchinglistothernum[i][j])
                            matchinglistothernum[i][j].append(num)
                            matchinglistothernum[i][j] = tuple(matchinglistothernum[i][j])
                cfg.history[-1].append("match opp:")
                cfg.history[-1].append(matchinglistothernum)
        else: #There is a forced tile on the current player
            forcedmove = True
            cfg.history[-1].append("Forced afterelse:" + str(forcedmove))
        cfg.win.update()
        """history"""
        cfg.history[-1].append("turn=: " + str(cfg.turnUpDown))
        return True

    def remove(self, row, col, table):
        rowcoltab = tuple([row, col, table])
        ind = self.get_index_from_rowcoltab(rowcoltab)
        """Delete itemid from table and .itemids"""
        try:
            itemid = self.itemids.pop(ind)
        except:
            print("remove: Cannot do self.itemids.pop({}) !!".format(ind))
            print("rowcoltab={}".format(str(rowcoltab)))
            print("len self.itemids=", str(len(self.itemids)))
            self.log()
            raise UserWarning("remove: Error!")
        """I think this is already done by move_automatic but ok.."""
        cfg.canvas.delete(itemid)
        """Update confirmed storage"""
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
        """Update _positions_moved"""
        if rowcolnum in self._positions_moved:
            print("removed rowcolnum {} from _positions_moved".format(rowcolnum))
            self._positions_moved.remove(rowcolnum)
        """NB: remove tile from deck dealt. leaving undealt as is"""
        num = self.dealt.pop(ind)
        """Return information"""
        pos = self._positions.pop(ind)
        table = self._table.pop(ind)
        tile = self.tiles.pop(ind)
        return (pos, num, tile)

    def deal(self, row, col, tab, num = 'random'):
        row = int(row)
        col = int(col)
        """Random tile if player_num is not set"""
        if num is 'random':
            ran = cfg.rndgen.randint(0, len(self.undealt) - 1) #0:55
        #todo I put fixed tile extraction for testing
        global ran
        ran = (ran+12) % (len(self.undealt) - 1) #DOTO RM LATER!
        num = self.undealt.pop(ran)   #1:56
        """Get tile as PhotoImage"""
        tileobj = Tile(num, angle = 0)
        """Update storage"""
        rowcoltab = tuple([row, col, tab])
        temp = rowcoltab
        #temp = (cfg.COLS / 2, cfg.ROWS / 2, 0) #this shows a nice automatic dealing
        self.tiles.append(tileobj)
        self.dealt.append(num)
        self._positions.append(temp)
        self._rotations.append(0)
        self._table.append(tab)
        """Place on canvas"""
        itemid = tileobj.create_at_rowcoltab(temp)
        self.itemids.append(itemid)
        #self.move_automatic(temp, rowcoltab)    #this shows a nice automatic dealing
        #self._positions_moved.pop()
        """Update confirmed storage"""
        ind = self.get_index_from_rowcoltab(rowcoltab)
        n = self.get_tile_number_from_index(ind)
        rowcolnum = tuple([row, col, n])
        if tab == 0:
            self._confirmed[0].append(rowcolnum)
        elif tab == -1:
            self._confirmed[1].append(rowcolnum)
        elif tab == -2:
            self._confirmed[2].append(rowcolnum)
        """Store confirmed in tile object"""
        tileobj.confirmed = tab

    def move(self, rowcoltab1, rowcoltab2, force = False):
        """Move a tile and update storage. ._positions_moved are updated.
        Return True/False if successfull"""
        _, _, tab1 = rowcoltab1
        _, _, tab2 = rowcoltab2
        if not force and not self.is_movable(rowcoltab1, rowcoltab2):
            print("move: You cannot move the tile as it is to this hexagon")
            self.is_movable(rowcoltab1, rowcoltab2)
            return False
        itemid, ind = self.get_itemid_from_rowcoltab(rowcoltab1)
        tilex, tiley = cfg.board.off_to_pixel(rowcoltab2)
        cfg.canvas.coords(itemid, (tilex, tiley))
        """Update moved storage"""
        num = self.dealt[ind]
        rowcolnum1 = tuple([rowcoltab1[0], rowcoltab1[1], num])
        rowcolnum2 = tuple([rowcoltab2[0], rowcoltab2[1], num])
        if rowcolnum1 in self._positions_moved:
            self._positions_moved.remove(rowcolnum1)
        if tab2 == 0:
            self._positions_moved.append(rowcolnum2)
        elif rowcoltab2 not in self.get_rowcoltabs_in_table(tab2):
            if rowcolnum2 not in self.get_confirmed_rowcolnums_in_table(tab2):
                self._positions_moved.append(rowcolnum2)
        self._positions[ind] = (rowcoltab2)
        self._table[ind] = (tab2)
        """Update window"""
        cfg.win.update()
        return True

    def move_automatic(self, rowcoltab1, rowcoltab2, angle = False):
        """move and rotate a tile automatically. NB: .move is used and therefore also ._positions_moved is updated"""
        itemid, ind = self.get_itemid_from_rowcoltab(rowcoltab1)
        """Rotate the tile to be moved until it matches rotation"""
        if angle is not False:
            for rot in range(6):
                if self.tiles[ind].angle == angle:
                    break
                elif rot is 6:
                    raise UserWarning("move_automatic: could not find the right rotation in 6 rotations")
                angle_temp = self.rotate(rowcoltab1, force = False)
                sleep(0.25)
                if angle_temp is False:
                    raise UserWarning("move_automatic: could not rotate the tile")
        """Calculate coordinates, direction, distance etc"""
        x1, y1 = cfg.board.off_to_pixel(rowcoltab1)
        x2, y2 = cfg.board.off_to_pixel(rowcoltab2)
        dir = (float(x2 - x1), float(y2 - y1))
        distance = math.sqrt(dir[0] * dir[0] + dir[1] * dir[1])
        steps = int(math.ceil(distance / 10))
        deltax, deltay = dir[0] / steps, dir[1] / steps
        for i in range (1, steps + 1):
            xi = x1 + round(deltax * i)
            yi = y1 + round(deltay * i)
            cfg.canvas.coords(itemid, (xi, yi))
            cfg.canvas.after(25, cfg.win.update())
        ok = self.move(rowcoltab1, rowcoltab2)
        return ok

    def rotate(self, rowcoltab, force = False, clockwise = True):
        """Rotate a tile if tile is not locked: spawn it, replace itemid in self.itemids.
        Return the angle (0 to 300) if successful, False if not"""
        """Find the index"""
        try:
            ind= self.get_index_from_rowcoltab(rowcoltab)
        except:
            print('not found: ' + str(rowcoltab) +' in')
            return False
        num = cfg.deck.get_tile_number_from_index(ind)
        if not force and num in [rcn[2] for rcn in cfg.deck._confirmed[0]]:
            return False
        """Spawn the rotated tile"""
        clockwise = 1 if clockwise else -1
        tile = Tile(self.dealt[ind], self.tiles[ind].angle - 60 * clockwise)
        """Update tiles list"""
        self.tiles[ind] = tile
        #print("rotate: after spawn before savng in .tiles: ",str(self.tiles[ind].basecolors))
        """Store rotation in storage"""
        self._rotations[ind] = tile.angle #(self._rotations[ind] + 60) % 360
        """Place the tile"""
        itemid = tile.create_at_rowcoltab(rowcoltab)
        self.itemids[ind] = itemid
        return self._rotations[ind]

    def refill_deck(self, tab):
        """Refill a player's deck"""
        """Check how many tiles there are"""
        rowcoltab = self.get_rowcoltabs_in_table(tab)
        count = len(rowcoltab)
        if count == 6:
            #print("There are already 6 tiles on deck " + str(-tab))
            return False
        """Flush existing tiles to left"""
        for i in range(0, count):
            bin, cols, bin = rowcoltab[i]
            if cols > i:
                """move tile to left by one or more places (if I move and reset tiles)"""
                ok = False
                while not ok:
                    ok = self.move_automatic((0, cols, tab), (0, i, tab), angle = False)
                    if ok:
                        num = self.get_tile_number_from_rowcoltab((0, i, tab))
                        ind_conf = self._confirmed[-tab].index((0, cols, num))
                        try:
                            self._confirmed[-tab][ind_conf] = (0, i, num)
                        except:
                            self.log()
                            print("self._confirmed[1].index() is not in list".format(str((0, cols, num))))
                        #if tab == -1:
                        #    ind_conf = self._confirmed[1].index((0, cols, player_num))
                        #    self._confirmed[1][ind_conf] = (0, i, player_num)
                        #elif tab == -2:
                        #    ind_conf = self._confirmed[2].index((0, cols, player_num))
                        #    self._confirmed[2][ind_conf] = (0, i, player_num)
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
        """Reset the table by bringing unconfirmed tiles back to confirmed position.
        Tiles are not reset to the original rotation"""
        while (self._positions_moved != []):
            """Get info on moved tile"""
            rowcolnum1 = self._positions_moved[-1]
            rowcoltab1 = self.get_rowcoltab_from_rowcolnum(rowcolnum1)
            """Find where tile in ._positions_moved should go,
            ie tile player_num rowcolnum1[2] is present in confirmed storage"""
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
                ok = self.move_automatic(rowcoltab1, rowcoltab2[0], angle = False)
                print("reset: move_automatic ok=:",ok)
                """If tile cannot be moved because original place is occupied, move it to temporary position"""
                if not ok:
                    temp = (rowcoltab2[0][0], -1, rowcoltab2[0][2])
                    print("reset move_automatic to temp:",temp)
                    ok2 = self.move_automatic(rowcoltab1, temp, angle = False)
                    print("reset: move_automatic ok2=:",ok2)
                    #while loop takes last tile. continues with second tile.
                    last = self._positions_moved.pop(-1)
                    self._positions_moved.insert(0, last)
            """here _position_moved has been purged"""
        self.highlight_forced_and_matching()
        return True

    def get_surrounding_hexagons(self, table):
        """Return a set of rowcolnum. which are all the empty hexagons surrounding tiles on a table.
        The table is _confirmed[0] by default"""
        if table is None:
            table = self._confirmed[0]
        surr = set([])
        for t in table:
            hex = cfg.board.get_neighboring_hexagons(t[0], t[1])
            [surr.add(h) for h in hex]
        for t in table:
            rowcoltab = self.get_rowcoltab_from_rowcolnum(t)
            if rowcoltab in surr:
                surr.remove(rowcoltab)
        return surr

    def check_forced(self):
        """Check for forced spaces on the main table. Return the hexagons rowcolnum"""
        hex_surrounding_board = self.get_surrounding_hexagons(self._confirmed[0])
        obliged_hexagons = []
        rowcoltab_in_confirmed0 = [self.get_rowcoltab_from_rowcolnum(c) for c in self._confirmed[0]]
        for s in hex_surrounding_board:
            """Get confirmed neighboring tiles"""
            rowcoltabs = cfg.board.get_neighboring_hexagons(s[0], s[1])
            """Find if there is a tile on rowcoltabs"""
            confirmed_neigh_tiles = 0
            for rowcoltab in rowcoltabs:
                if rowcoltab in rowcoltab_in_confirmed0:
                    confirmed_neigh_tiles += 1
            """Count if confirmed neighbouring tiles is 3"""
            if confirmed_neigh_tiles == 3:
                """Check that the possible matches do not lead to an impossible tile somewhere else!""" #TODO
                if self.impossible_neighbor(s, add_tilenum_at_rowcolnum_rot = False):
                    pass #TODO
                else:
                    print("Forced space at {},{}".format(s[0], s[1]))
                    obliged_hexagons.append(s)
                    """Get tiles matching"""
            elif confirmed_neigh_tiles > 3:
                raise UserWarning("Hexagon at {},{} is surrounded by >3 tiles!".format(s[2], s[0], s[1]))
        return obliged_hexagons

    def find_matching_tiles(self, rowcoltab, table = [-1, -2]):
        """Find all tiles of a table that fit in an empty hexagon. Return a list of rocolnum"""
        """Get the neighbors"""
        color_index = self.get_neighboring_colors(rowcoltab)
        if not len(color_index):
            #print("find_matching_tiles: hexagon has no neighbors".format(str(rowcoltab)))
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
        #player_num = self.get_tile_number_from_rowcoltab(rowcoltab)
        match = []
        for tab in table:
            """Get all confirmed tiles in the desired table"""
            confs = self.get_confirmed_rowcolnums_in_table(tab)
            for conf in confs:
                ind2 = self.get_index_from_tile_number(conf[2])
                tile2 = self.tiles[ind2]
                #tile2, ind2 = self.get_tile_from_tile_number(conf[2])
                if colors in tile2.basecolors + tile2.basecolors:
                    match.append(self._positions[ind2])
        print("find_matching_tiles gives: ",str(match))
        return match

    def impossible_neighbor(self, rowcolnum, add_tilenum_at_rowcolnum_rot = False):
        """Check is a place has impossible neighbors around it"""
        """add_tilenum_at_rowcolnum is eg [16, (0,0,0)]"""
        neigh_rowcoltabs = cfg.board.get_neighboring_hexagons(rowcolnum)
        inmaintable = self.get_rowcoltabs_in_table(0)
        #TODO
        if add_tilenum_at_rowcolnum_rot:
            inmaintable.append(add_tilenum_at_rowcolnum_rot[1]) #so that this cript will skip checking the virtual tile
        #TODO end
        for rct in neigh_rowcoltabs:
            if rct not in inmaintable:
                colors = self.get_neighboring_colors(rct, add_tilenum_at_rowcolnum_rot) #TODO
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
        """Directions of the neighbors"""
        dir_ind1 = [n[1] for n in neigh]
        """Take each of the one or two neighbors at a certain direction"""
        for i1 in range(0, neigh_number):
            cube1 = map(lambda x, y : x + y, cube0, cfg.directions[dir_ind1[i1]])
            rowcol1 = cfg.board.cube_to_off(cube1)
            """Find new direction to go straight"""
            if neigh_number == 1:
                """explore both angles"""
                dir_ind2n = [(dir_ind1[i1] - 1) % 5, (dir_ind1[i1] + 1) % 5]
            else:
                """go opposite to the other neighbor"""
                dir_ind2n = [(dir_ind1[i1] + dir_ind1[i1] - dir_ind1[(i1 + 1) % 2] + 6) % 6]
            for i2 in range(0, len(list(dir_ind2n))):
                cube2n = map(lambda x, y : x + y, cube1, cfg.directions[dir_ind2n[i2]])
                rowcol2n = cfg.board.cube_to_off(cube2n)
                if rowcol2n not in rowcol_inmain:
                    continue
                """go straight till the end but check at right angle as well"""
                empty2n = False
                while empty2n is False:
                    """Check tile at an angle"""
                    dir_indn = (dir_ind2n[i2] - dir_ind1[i1] + dir_ind2n[i2] + 6 ) % 6
                    cuben = map(lambda x, y : x + y, cube2n, cfg.directions[dir_indn])
                    rowcoln = cfg.board.cube_to_off(cuben)
                    if rowcoln in rowcol_inmain:
                        return True
                    """update tile to the one straight ahead. exit while loop if empty"""
                    cube2n = map(lambda x, y : x + y, cube2n, cfg.directions[dir_ind2n[i2]])
                    rowcol2n = cfg.board.cube_to_off(cube2n)
                    if rowcol2n not in rowcol_inmain:
                        empty2n = True
        return False

    def score(self, player):
        """Calculate the scores for a player"""
        if player == 1:
            color = cfg.hand1.playercolors[0][0]
        elif player == 2:
            color = cfg.hand2.playercolors[1][0]
        score = []
        score_loop = []
        scanned_off = []
        conf_rowcols = [c[0:2] for c in self._positions if c[2] is 0]
        """Loop on all confirmed tiles"""
        while 1:
            """See if there are unscanned tiles"""
            scanned_number = len(map(len, scanned_off))
            if scanned_number >= len(conf_rowcols):
                break
            else:
                """Find the first _confirmed that was not scanned"""
                find_first = False
                while not find_first:
                    for c in conf_rowcols: #self._confirmed[0]:
                        if c[0:2] not in scanned_off:
                            rowcolnum = c
                            break
                    scanned_off.append(rowcolnum[0:2])
                    #cfg.board.place_highlight((rowcolnum[0], rowcolnum[1], 0))
                    ind = self.get_index_from_rowcoltab((rowcolnum[0], rowcolnum[1], 0))
                    tile = self.tiles[ind]
                    clr = tile.getColor()
                    if color in clr:
                        score.append(1)
                        neighboring_colors = self.get_neighboring_colors(
                            rowcolnum[0], rowcolnum[1], color)
                        if len(neighboring_colors) == 0:
                            thread = False
                        else:
                            (neigh_color, ang, _) = neighboring_colors[0]
                            thread = True
                            curr_off = rowcolnum[0:2]
                    else:
                        thread = False
                    break
            """Loop on a thread"""
            while thread:
                """Get the angle of the color, then follow to the adjacent tile"""
                dir = cfg.directions[ang]
                cube = cfg.board.off_to_cube(curr_off[0], curr_off[1])
                next_cube = tuple(map(lambda c, d: c + d, cube, dir))
                next_off = cfg.board.cube_to_off(next_cube)
                #cfg.board.place_highlight((next_off[0], next_off[1], 0))
                """Check if it closes the loop"""
                if next_off in scanned_off:
                    score_loop.append(score.pop() * 2)
                    cfg.board.remove_all_highlights()
                    break
                """Check if present"""
                if self.is_occupied((next_off[0], next_off[1]), conf_rowcols):
                    curr_off = next_off
                    score[-1] += 1
                    ang_from = (ang + 3) % 6
                    tile = self.get_tile_from_rowcolnum((curr_off[0], curr_off[1], 0))
                    clr = tile.getColor()
                    angs = (clr.find(color), clr.rfind(color))
                    ang = angs[0]
                    if ang == ang_from:
                        ang = angs[1]
                    scanned_off.append(curr_off)
                else:
                    break
        #cfg.board.remove_all_highlights()
        """Transcribe the scores"""
        cfg.scores[player - 1] = 0
        if len(score):
            cfg.scores[player - 1] = score
            score = max(score)
        else:
            score = 0
        cfg.scores_loop[player - 1] = 0
        if len(score_loop):
            cfg.scores_loop[player - 1] = score_loop
            score_loop = max(score_loop)
        else: score_loop = 0
        #print("cfg.scores[]     =" + str(cfg.scores[player - 1]))
        #print("cfg.scores_loop[]=" + str(cfg.scores_loop[player - 1]))
        return score, score_loop

    def is_shiftable(self, horiz = 0, vert = 0):
        """Return if it is possible to do a horizontal or vertical shift of the tiles on the table"""
        if len(self._confirmed[0]) < 1:
            return False
        if horiz == 0 and vert == 0:
            #print("Zero shifts are not allowed")
            return False
        """Horizontal shift"""
        if horiz:
            rows = [p[0] for p in self._confirmed[0]]
            row_min = min(rows)
            xmin, _ = cfg.board.off_to_pixel((row_min, 0, 0))
            row_max = max(rows)
            xmax, _ = cfg.board.off_to_pixel((row_max, 0, 0))
        """Allow to move 1/-1 i.e. lx/rx"""
        if horiz == -1:
            if xmin > cfg.HEX_SIZE * 4:
                #print("Shift left: xmin is high so ok")
                return True
            elif xmin  <= cfg.HEX_SIZE * 4:
                if xmax >= cfg.CANVAS_WIDTH: # - cfg.HEX_SIZE * 2:
                    #print("Shift left: xmin is low, but xmax is high so ok")
                    return True
                else:
                    #print("Shift left: xmin is low so deny shift")
                    return False
        elif horiz == 1:
            if xmax < cfg.CANVAS_WIDTH - cfg.HEX_SIZE * 4:
                #print("Shift right: xmax is low so ok")
                return True
            elif xmax >= cfg.CANVAS_WIDTH - cfg.HEX_SIZE * 4:
                if xmin <= cfg.HEX_SIZE * 3:
                    #print("Shift right: xmax is high, but xmin is low so ok")
                    return True
                else:
                    #print("Shift right: xmax is high so deny shift")
                    return False
        """Vertical shift"""
        if vert:
            cols = [p[1] for p in self._confirmed[0]]
            col_min = min(cols)
            _, ymin = cfg.board.off_to_pixel((0, col_min, 0))
            col_max = max(cols)
            _, ymax = cfg.board.off_to_pixel((0, col_max, 0))
        """Allow to move 1/-1 i.e. up/down"""
        if vert == 1: #down
            if ymax < cfg.YBOTTOMMAINCANVAS - cfg.HEX_HEIGHT * 2:
                #print("Shift down: ymax is low so ok")
                return True
            elif ymax >= cfg.YBOTTOMMAINCANVAS - cfg.HEX_HEIGHT * 2:
                if ymin <= cfg.YTOPMAINCANVAS + cfg.HEX_SIZE:
                    #print("Shift down: ymax is high, but ymin is low so ok")
                    return True
                else:
                    #print("Shift down: ymax is high so deny shift")
                    return False
        elif vert == -1:
            if ymin > cfg.YTOPMAINCANVAS + cfg.HEX_HEIGHT * 2:
                #print("Shift up: ymin is high so ok")
                return True
            elif ymin <= cfg.YTOPMAINCANVAS + cfg.HEX_HEIGHT * 2:
                if ymax >= cfg.YBOTTOMMAINCANVAS - cfg.HEX_HEIGHT:
                    #print("Shift up: ymin is low, but ymax is high so ok")
                    return True
                else:
                    #print("Shift up: ymin is low so deny shift")
                    return False
        print("I should not come here in is_shiftable!")
        return False

    def shift(self, shift_row = 0, shift_col = 0):
        """Shift the whole board based on the current storage"""
        if shift_row:
            if not self.is_shiftable(horiz = shift_row):
                return False
        if shift_col:
            if not self.is_shiftable(vert = shift_col):
                return False
        """Store all the info that has to be used to move the tiles.
        I cannot simply move because tiles will be temporarily overlayed"""
        rowcoltabs_to_move = []
        rowcoltab_destinations = []
        rowcolnum_destinations = []
        indexes_confirmed = []
        indexes_positions = []
        itemids = [] #"""Find what has to be moved and store all information"""
        for ind, rowcoltab in enumerate(self._positions):
            if rowcoltab[2] is 0:
                indexes_positions.append(ind)
                rowcoltabs_to_move.append(rowcoltab)
                rowcolnum = self.get_rowcolnum_from_rowcoltab(rowcoltab)
                rowcoltab_dest = (rowcoltab[0] + shift_row * 2, rowcoltab[1] + shift_col, 0)
                rowcoltab_destinations.append(rowcoltab_dest)
                itemid, _ = self.get_itemid_from_rowcoltab(rowcoltab)
                itemids.append(itemid)
                """Update _confirmed storage and remove confirmed from ._positions_moved"""
                if rowcolnum in self._confirmed[0]:
                    indexes_confirmed.append(self._confirmed[0].index(rowcolnum))
                    rowcolnum_destinations.append((rowcoltab_dest[0], rowcoltab_dest[1], rowcolnum[2]))
                else:
                    indexes_confirmed.append(-666)
                    rowcolnum_destinations.append(-666)

        for i in range(0, len(rowcoltabs_to_move)):
            """Cannot use .move so move "manually" """
            tilex, tiley = cfg.board.off_to_pixel(rowcoltab_destinations[i])
            cfg.canvas.coords(itemids[i], (tilex, tiley))
            """Update _positions"""
            self._positions[indexes_positions[i]] = rowcoltab_destinations[i]
            """Update confirmed from ._positions_moved"""
            if indexes_confirmed[i] != -666:
                self._confirmed[0][indexes_confirmed[i]] = rowcolnum_destinations[i]
                #"""Remove confirmed from ._positions_moved"""
                #cfg.deck._positions_moved.remove(rowcolnum_destinations[i])
        """"Manually" shift the _positions_moved storage"""
        for i, rowcolnum in enumerate(self._positions_moved):
            self._positions_moved[i] = (rowcolnum[0] + shift_row * 2, rowcolnum[1] + shift_col, rowcolnum[2])
        """Control which tiles must stay on top"""
        #cfg.canvas.tag_raise("raised")
        for rct in self._positions:
            if rct[2] != 0:
                itid, _ = self.get_itemid_from_rowcoltab(rct)
                cfg.canvas.tag_raise(itid)
                cfg.win.update()
        """Remove highlights"""
        cfg.board.remove_all_highlights()
        self.highlight_forced_and_matching()
        """Raise stipple rectangles"""
        self.update_stipples()
        """Store shifts for sending to other client"""
        cfg.shifts[0] += shift_row
        cfg.shifts[1] += shift_col

        return True

    def log(self, msg = " "):
        print("  =======>" + msg)
        print("  cfg.TRYING=" + str(cfg.TRYING))
        print("  Player %d - %s" %(cfg.player_num, cfg.name))
        #print("TRYING=" + str(cfg.TRYING))
        print("  cfg.turnUpDown=" + str(cfg.turnUpDown))
        print("  cfg.player_num=" + str(cfg.player_num) + ", playerIsTabUp=" + str(cfg.playerIsTabUp))
        print("  cfg.name/opponentname=" + str(cfg.name) + "/" + cfg.opponentname)
        print("  cfg.deck.is_confirmable= " + str(self.is_confirmable(True)))

        print("  cfg.deck._positions=" + str(self._positions[0:4]))
        print("                   =" + str(self._positions[4:8]))
        print("                   =" + str(self._positions[8:]))
        print("  cfg.deck._table=" + str(self._table))
        print("  cfg.deck._positions_moved=" + str(self._positions_moved))
        print("  cfg.deck._rotations=" + str(self._rotations))
        print("  cfg.deck._confirmed[0]=" + str(self._confirmed[0]))
        print("  cfg.deck._confirmed[1]=" + str(self._confirmed[1]))
        print("  cfg.deck._confirmed[2]=" + str(self._confirmed[2]))
        print("  cfg.deck.itemids=" + str(self.itemids))
        for t in cfg.deck.tiles:
            print(t.confirmed)
        #print(" cfg.deck.dealt=" + str(self.dealt))
        #print(" cfg.board._highlightids=" + str(cfg.board._highlightids))
        #print(" cfg.board._highlight=" + str(cfg.board._highlight))
        #print(" cfg.turnUpDown free=" + str((cfg.turnUpDown, cfg.forcedmove)))
        print("  <=======")
