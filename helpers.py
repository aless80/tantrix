__author__ = 'amarin'

import config as cfg

class DeckHelper():
    def get_index_from_tile_number(self, num):
        return self.dealt.index(num)

    def get_index_from_rowcolcanv(self, rowcolcanv):
        if type(rowcolcanv[2]) is not str:
          raise UserWarning("get_index_from_rowcolcanv: rowcolcanv should contain the canvas as string")
        try:
          return self.positions.index(tuple(rowcolcanv))
        except:
          return None

    def get_tile_number_from_rowcolcanv(self, rowcolcanv):
        ind = self.get_index_from_rowcolcanv(rowcolcanv)
        return self.get_tile_number_from_index(ind)

    def get_tile_number_from_index(self, ind):
        try:
          return self.dealt[ind]
        except:
          return None

    def get_neighboring_tiles(self, row, col=False):
        """Find the neighbors of a hexagon in the main canvas.
        Return a list with offset coordinates"""
        rowcolcanvs = cfg.board.get_neighbors(row, col)
        #Find if there is a tile on rowcolcanv
        neigh = []
        for rowcolcanv in rowcolcanvs:
          ind = self.get_index_from_rowcolcanv(rowcolcanv)
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
          for n in neigh:   #(0,0)
            wholecolor = self.tiles[n].color
            #here get direction and right color
            rowcolcanv = self.positions[n]
            cube = cfg.board.off_to_cube(rowcolcanv[0],rowcolcanv[1])
            home = cfg.board.off_to_cube(row, col)
            founddir = map(lambda dest, hom : dest-hom,cube,home)
            dirindex = cfg.directions.index(founddir)
            color = wholecolor[(dirindex + 3) % 6]
            color_dirindex_neighIndex.append(tuple([color,dirindex,n]))
        return color_dirindex_neighIndex #[('b',1),('color',directionIndex),]

    def get_rowcolcanv_from_rowcolnum(self, rowcolnum):
        '''Find in .positions the rowcolcanv that corresponds to the tile in rowcolnum'''
        row, col, num = rowcolnum
        for rowcolcanv in self.positions:
          i = self.get_index_from_rowcolcanv(rowcolcanv)
          n = self.get_tile_number_from_index(i)
          if n == rowcolnum[2]:
            #Test consistency. remove later if it never throws the error
            #they can be different! if rowcolcanv[0] != row or rowcolcanv[1] != col:
              #raise UserWarning("get_rowcolcanv_from_rowcolnum: found row col not consistent with input")
            return tuple([rowcolnum[0], rowcolnum[1], rowcolcanv[2]])
        raise UserWarning("get_rowcolcanv_from_rowcolnum: Cannot find rowcolcanv")