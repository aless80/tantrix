__author__ = 'amarin'

import config as cfg

class DeckHelper():

    def get_index_from_tile_number(self, num):
        '''Given a tile number num find the index in deck.dealt'''
        return self.dealt.index(num)

    def get_index_from_rowcoltab(self, rowcoltab):
        '''Given rowcoltab find the index in _positions'''
        try:
            return self._positions.index(tuple(rowcoltab))
        except:
            return None

    def get_itemid_from_rowcoltab(self, rowcoltab):
        '''Get itemid and ind of the tile in rowcoltab. This uses get_index_from_rowcoltab'''
        ind = self.get_index_from_rowcoltab(rowcoltab)
        return self.itemids[ind], ind

    def get_tile_number_from_rowcoltab(self, rowcoltab):
        '''Given rowcoltab find the index in _positions and return
        the tile number in deck.dealt'''
        ind = self.get_index_from_rowcoltab(rowcoltab)
        return self.get_tile_number_from_index(ind)

    def get_tile_number_from_index(self, ind):
        try:
            return self.dealt[ind]
        except:
            return None

    def get_neighboring_tiles(self, row, col = False):
        """Find the neighbors of a hexagon in the main canvas.
        Return a list with offset coordinates"""
        rowcoltabs = cfg.board.get_neighbors(row, col)
        #Find if there is a tile on rowcoltab
        neigh = []
        for rowcoltab in rowcoltabs:
            ind = self.get_index_from_rowcoltab(rowcoltab)
            if ind is not None:
                neigh.append(ind) #list of ind where tile is present [(0,0),..]
        return neigh

    def get_neighboring_colors(self, row, col = False):
        """Return the neighboring colors as a list of (color,ind)"""
        if type(row) != int:
            row, col,bin = row
        neigh = self.get_neighboring_tiles(row, col) #[(0,0),..]
        color_dirindex_neighIndex = []
        if len(neigh) > 0:
            for n in neigh:
                wholecolor = self.tiles[n].colors
                #Here get direction and right color
                rowcoltab = self._positions[n]
                cube = cfg.board.off_to_cube(rowcoltab[0],rowcoltab[1])
                home = cfg.board.off_to_cube(row, col)
                founddir = map(lambda dest, hom : dest-hom,cube,home)
                dirindex = cfg.directions.index(founddir)
                color = wholecolor[(dirindex + 3) % 6]
                color_dirindex_neighIndex.append(tuple([color,dirindex,n]))
        return color_dirindex_neighIndex #[('b',1),('color',directionIndex),]

    def get_rowcoltab_from_rowcolnum(self, rowcolnum):
        '''Find in ._positions the rowcoltab that corresponds to the tile in rowcolnum'''
        row, col, num = rowcolnum
        for rowcoltab in self._positions:
            i = self.get_index_from_rowcoltab(rowcoltab)
            n = self.get_tile_number_from_index(i)
            if n == rowcolnum[2]:
                return tuple([rowcolnum[0], rowcolnum[1], rowcoltab[2]])
        raise UserWarning("get_rowcoltab_from_rowcolnum: Cannot find rowcoltab")

    def get_tiles_in_table(self, table):
        '''Get the tiles as list of rowcoltab currently present in a table, ie present in ._positions'''
        rowcoltabs = []
        for pos in self._positions:
            row, col, tab = pos
            if tab == table:
                rowcoltabs.append(tuple([row, col, table]))
        return rowcoltabs

    def get_confirmed_tiles_in_table(self, table):
        '''Get the tiles as list of rowcoltab currently confirmed in a table, ie present in ._confirmed_pos_table, _confirmed_pos_hand1, _confirmed_pos_hand2'''
        if table == "main":
            return self._confirmed_pos_table
        elif table == "top":
            return self._confirmed_pos_hand1
        elif table == "bottom":
            return self._confirmed_pos_hand2
