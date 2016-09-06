__author__ = 'amarin'

import config as cfg
directions = [[0, 1, -1], [+1, 0, -1], [+1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0]]

class DeckHelper(object):

    def get_index_from_tile_number(self, num):
        """Given a tile number player_num find the index in deck.dealt"""
        return self.dealt.index(num)

    def get_index_from_rowcoltab(self, rowcoltab, storage = None):
        """Given rowcoltab find the index in storage. storage can is _positions by default but you can also pass lists of rowcolnum"""
        if storage is None:
            storage2 = self._positions
        else:
            storage2 = [self.get_rowcoltab_from_rowcolnum(s) for s in storage]
        try:
            return storage2.index(tuple(rowcoltab))
        except:
            return None

    def get_confirmed_rowcolnums_in_table(self, table):
        """Get the tiles as list of rowcoltab currently confirmed in a table, ie present in ._confirmed[0], _confirmed[1], _confirmed[2]"""
        return self._confirmed[-table]

    def get_itemid_from_rowcoltab(self, rowcoltab):
        """Get itemid and ind of the tile in rowcoltab. This uses get_index_from_rowcoltab, ie ._positions"""
        ind = self.get_index_from_rowcoltab(rowcoltab)
        if ind is None:
            print(">helpers.get_itemid_from_rowcoltab: ind = self.get_index_from_rowcoltab("+str(rowcoltab)+") returned None")
            print(">check self._positions:")
            print(self._positions)
        return self.itemids[ind], ind

    def get_tile_number_from_rowcoltab(self, rowcoltab):
        """Given rowcoltab find the index in _positions and return
        the tile number in deck.dealt"""
        ind = self.get_index_from_rowcoltab(rowcoltab)
        return self.get_tile_number_from_index(ind)

    def get_rowcolnum_from_rowcoltab(self, rowcoltab):
        """Get rowcolnum from rowcoltab by using _positions and deck.dealt"""
        num = self.get_tile_number_from_rowcoltab(rowcoltab)
        if num is None:
            return None
        return tuple([rowcoltab[0], rowcoltab[1], num])

    def get_tile_number_from_index(self, ind):
        try:
            #return self.dealt[ind]
            return self.tiles[ind].num
        except:
            return None

    def get_neighboring_tiles(self, row, col = False):
        """Find the occupied tiles in ._positions that are neighbors to a hexagon on the main canvas.
        Return a list of tile indices from _positions"""
        rowcoltabs = cfg.board.get_neighboring_hexagons(row, col)
        #Find if there is a tile on rowcoltab
        neigh_ind = []
        for rowcoltab in rowcoltabs:
            ind = self.get_index_from_rowcoltab(rowcoltab)
            if ind is not None:
                neigh_ind.append(ind) #list of ind where tile is present [(0,0),..]
        return neigh_ind

    def get_neighboring_colors(self, row, col = False, color = "rgyb", add_tilenum_at_rowcolnum_rot = None):
        """Return the neighboring colors as a list of (color, ind, n) where
        ind is the index of directions, n is the index in _positions.
        Optionally indicate in color which colors the neighbors should match.
        directions starts from north and goes clock-wise"""
        if not isinstance(row, (int, float)):
            row, col, bin = row
        neigh_ind = self.get_neighboring_tiles(row, col) #TODO append add_tilenum_at_rowcolnum_rot[1] if it is a neighbor
        #TODO - append add_tilenum_at_rowcolnum_rot[1] if it is a neighbor
        if add_tilenum_at_rowcolnum_rot is not None:
            added_rocoltab = add_tilenum_at_rowcolnum_rot[1]
            #added_num = add_tilenum_at_rowcolnum_rot[0]
            #added_index = self.get_index_from_rowcoltab(added_rocoltab) NO! and I might not have it. get
            if added_rocoltab in cfg.board.get_neighboring_hexagons(row, col):
                neigh_ind.append(added_rocoltab)
        #TODO end
        color_dirindex_neighIndex = []
        if len(neigh_ind) > 0:
            for nind in neigh_ind:
                wholecolor = self.tiles[nind].getColor()
                """Here get direction and right color"""
                rowcoltab = self._positions[nind]
                cube = cfg.board.off_to_cube(rowcoltab[0], rowcoltab[1])
                home = cfg.board.off_to_cube(row, col)
                founddir = map(lambda c, h: c - h, cube, home)
                dirindex = directions.index(founddir)
                clr = wholecolor[(dirindex + 3) % 6]
                if clr in color:
                    color_dirindex_neighIndex.append(tuple([clr, dirindex, nind]))
        return color_dirindex_neighIndex #[('b',0,43),('color',directionIndex,n)]

    def get_rowcoltab_from_rowcolnum(self, rowcolnum):
        """Find in ._positions the rowcoltab that corresponds to the tile in rowcolnum"""
        row, col, num = rowcolnum
        for rowcoltab in self._positions:
            i = self.get_index_from_rowcoltab(rowcoltab)
            n = self.get_tile_number_from_index(i)
            if n == rowcolnum[2]:
                return tuple([rowcolnum[0], rowcolnum[1], rowcoltab[2]])
        raise UserWarning("get_rowcoltab_from_rowcolnum: Cannot find rowcoltab")

    def get_rowcoltabs_in_table(self, table):
        """Get the tiles as list of rowcoltab currently present in a table, ie present in ._positions"""
        rowcoltabs = []
        for pos in self._positions:
            row, col, tab = pos
            if tab == table:
                rowcoltabs.append(tuple([row, col, table]))
        return rowcoltabs

    def get_tile_from_tile_number(self, num):
        """Get the instance of Tile corresponding to a tile number"""
        ind = self.get_index_from_tile_number(num)
        return self.tiles[ind]

    def get_tile_from_rowcolnum(self, rowcoltab):
        """Get the instance of Tile and optionally the index in _positions corresponding to a tile number"""
        ind = self.get_index_from_rowcoltab(rowcoltab)
        return self.tiles[ind]

    def update_stipples(self):
            """Update stipples to reflect the turn"""
            _turn = (2 - cfg.turnUpDown % 2 )
            if not cfg.solitaire and (cfg.player_num != _turn):
                cfg.canvas.itemconfig(cfg.stipple1, fill = "gray", stipple = "gray12")
                cfg.canvas.itemconfig(cfg.stipple2, fill = "gray", stipple = "gray12")
            else:
                if _turn % 2:
                    cfg.canvas.itemconfig(cfg.stipple1, fill = "")
                    cfg.canvas.itemconfig(cfg.stipple2, fill = "gray", stipple = "gray12") #gray12, gray25
                    cfg.canvas.tag_raise(cfg.stipple2) #needed?
                    cfg.canvas.tag_raise(cfg.stipple1) #needed?
                    cfg.board.message("")
                else:
                    cfg.canvas.itemconfig(cfg.stipple2, fill = "")
                    cfg.canvas.itemconfig(cfg.stipple1, fill = "gray", stipple = "gray12")
                    cfg.canvas.tag_raise(cfg.stipple1)
                    cfg.canvas.tag_raise(cfg.stipple2)
                    cfg.board.message("")