__author__ = 'amarin'

import config as cfg

class DeckHelper():

    def get_index_from_tile_number(self, num):
        '''Given a tile number num find the index in deck.dealt'''
        return self.dealt.index(num)

    def get_index_from_rowcoltab(self, rowcoltab, storage = None):
        '''Given rowcoltab find the index in storage. storage can is _positions by default but you can also pass lists of rowcolnum'''
        if storage is None:
            storage2 = self._positions
        else:
            storage2 = [self.get_rowcoltab_from_rowcolnum(s) for s in storage]
        try:
            return storage2.index(tuple(rowcoltab))
        except:
            return None

    def get_confirmed_rowcolnums_in_table(self, table):
        '''Get the tiles as list of rowcoltab currently confirmed in a table, ie present in ._confirmed[0], _confirmed[1], _confirmed[2]'''
        return self._confirmed[-table]

    def get_itemid_from_rowcoltab(self, rowcoltab):
        '''Get itemid and ind of the tile in rowcoltab. This uses get_index_from_rowcoltab, ie ._positions'''
        ind = self.get_index_from_rowcoltab(rowcoltab)
        return self.itemids[ind], ind

    def get_tile_number_from_rowcoltab(self, rowcoltab):
        '''Given rowcoltab find the index in _positions and return
        the tile number in deck.dealt'''
        ind = self.get_index_from_rowcoltab(rowcoltab)
        return self.get_tile_number_from_index(ind)

    def get_rowcolnum_from_rowcoltab(self, rowcoltab):
        '''Get rowcolnum from rowcoltab by using _positions and deck.dealt'''
        num = self.get_tile_number_from_rowcoltab(rowcoltab)
        if num is None:
            return None
        return tuple([rowcoltab[0], rowcoltab[1], num])

    def get_tile_number_from_index(self, ind):
        try:
            return self.dealt[ind]
        except:
            return None

    def get_neighboring_tiles(self, row, col = False):
        '''Find the occupied tiles in ._positions that are neighbors to a hexagon on the main canvas.
        Return a list of tile indices from _positions'''
        rowcoltabs = cfg.board.get_neighboring_hexagons(row, col)
        #Find if there is a tile on rowcoltab
        neigh_ind = []

        for rowcoltab in rowcoltabs:
            ind = self.get_index_from_rowcoltab(rowcoltab)
            if ind is not None:
                neigh_ind.append(ind) #list of ind where tile is present [(0,0),..]
        return neigh_ind

    def get_neighboring_colors(self, row, col = False, color = "rgyb"):
        '''Return the neighboring colors as a list of (color, ind, n) where
        ind is the index of cfg.directions, n is the index in _positions.
        Optionally indicate in color which colors the neighbors should match.
        cfg.directions starts from north and goes clock-wise'''
        if not isinstance(row, (int, float)):
            row, col, bin = row
        neigh = self.get_neighboring_tiles(row, col)
        color_dirindex_neighIndex = []
        if len(neigh) > 0:
            for n in neigh:
                wholecolor = self.tiles[n].getColor()
                """Here get direction and right color"""
                rowcoltab = self._positions[n]
                cube = cfg.board.off_to_cube(rowcoltab[0], rowcoltab[1])
                home = cfg.board.off_to_cube(row, col)
                founddir = map(lambda c, h: c - h, cube, home)
                dirindex = cfg.directions.index(founddir)
                clr = wholecolor[(dirindex + 3) % 6]
                if clr in color:
                    color_dirindex_neighIndex.append(tuple([clr, dirindex, n]))
        return color_dirindex_neighIndex #[('b',0,43),('color',directionIndex,n)]

    def get_rowcoltab_from_rowcolnum(self, rowcolnum):
        '''Find in ._positions the rowcoltab that corresponds to the tile in rowcolnum'''
        row, col, num = rowcolnum
        for rowcoltab in self._positions:
            i = self.get_index_from_rowcoltab(rowcoltab)
            n = self.get_tile_number_from_index(i)
            if n == rowcolnum[2]:
                return tuple([rowcolnum[0], rowcolnum[1], rowcoltab[2]])
        raise UserWarning("get_rowcoltab_from_rowcolnum: Cannot find rowcoltab")

    def get_rowcoltabs_in_table(self, table):
        '''Get the tiles as list of rowcoltab currently present in a table, ie present in ._positions'''
        rowcoltabs = []
        for pos in self._positions:
            row, col, tab = pos
            if tab == table:
                rowcoltabs.append(tuple([row, col, table]))
        return rowcoltabs

    def get_tile_from_tile_number(self, num):
        '''Get the instance of Tile corresponding to a tile number'''
        ind = self.get_index_from_tile_number(num)
        return self.tiles[ind]

    def get_tile_from_rowcolnum(self, rowcoltab):
        '''Get the instance of Tile and optionally the index in _positions corresponding to a tile number'''
        ind = self.get_index_from_rowcoltab(rowcoltab)
        return self.tiles[ind]

"""TO DO

fixed: move 1 tile to main. move one tile of top to top. confirm throws error. maybe after move_automatic

fixed: drag close but just outside a tile: it will be dragged in mid air but not moved there.
        that is because motionCallback bound to cfg.canvas moves tile rectangle whereas
        mouse click sees an empty hexagon and does not use move()

Alt+Shift+F10 you can access the Run/Debug dropdown

is_confirmable runs when i rotate a tile in top. it is a waste but ok..

ideas for storage:  _positions becomes (row, col num) and I store table in another array
                    _confirmed_table etc become _confirmed[0], [1] and [2]

def tile.free_moving(self, event, itemid): itemid should be a property of the tile
"""
