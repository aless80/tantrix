def get_neighbors(self, row, col=False):
    """Find neighbors of a hexagon in the main canvas"""
    if type(row) == list or type(row) == tuple:
      row, col,bin = row
    row, col = int(row),int(col)
    #Convert to cube coordinates, then add directions to cube coordinate
    neigh = []
    cube = list(board.off_to_cube(row, col))
    for dir in directions:
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
    neigh = board.get_neighbors(row, col) #[(0,0),..]
    color_dirindex_neighIndex = []
    if len(neigh) > 0:
      for n in neigh:   #(0,0)
        wholecolor = self.tiles[n].color
        #here get direction and right color
        rowcolcanv = self.positions[n]
        cube = board.off_to_cube(rowcolcanv[0],rowcolcanv[1])
        home = board.off_to_cube(row, col)
        founddir = map(lambda dest, hom : dest-hom,cube,home)
        dirindex = directions.index(founddir)
        color = wholecolor[(dirindex + 3) % 6]
        color_dirindex_neighIndex.append(tuple([color,dirindex,n]))











  def get_neighboring_colors(self, row, col = False):
    """Return the neighboring colors as a list of (color,ind)"""
    if type(row) != int:
      row, col,bin = row
    neigh = self.get_neighbors(row, col) #[(0,0),..]
    color_dirindex_neighIndex = []
    if len(neigh) > 0:
      for n in neigh:   #(0,0)
        wholecolor = deck.tiles[n].color
        #here get direction and right color
        rowcolcanv = deck.positions[n]
        cube = self.off_to_cube(rowcolcanv[0],rowcolcanv[1])
        home = board.off_to_cube(row, col)
        founddir = map(lambda dest, hom : dest-hom,cube,home)
        dirindex = directions.index(founddir)
        color = wholecolor[(dirindex + 3) % 6]
        color_dirindex_neighIndex.append(tuple([color,dirindex,n]))
    return color_dirindex_neighIndex #[('b',1),('color',directionIndex),]