  def movable(self, row1, col1, canvas1, row2, col2, canvas2):
    if TRYING:
      return True
    #Ignore movement when:
    if deck.is_occupied((row2, col2, str(canvas2))):
      #Return False if destination is already occupied
      print('Destination tile is occupied: ' + str((row2, col2, str(canvas2))))
      return False
    if canvas2 == canvasmain:
      #Movement to main canvas.
      #Ok if there are no tiles on canvas
      if ".canvasmain" not in [p[2] for p in deck.positions]: #todo: later on maybe check score
                                # or something that is populated when the first tile is placed
        return True
      #Check if tile matches colors
      ind1 = deck.get_index((row1, col1, str(canvas1)))
      tile = deck.tiles[ind1]
      #NB The following does not allow you to move the same tile one position away.
      #That should not be of any use though so ok
      ok = tile.tile_match_colors(tuple([row2, col2, str(canvas2)]))
      if not ok:
        print('No color matching')
        return ok
    elif canvas1 != canvasmain and canvas1 != canvas2:
      #Return False if trying to move from bottom to top or vice versa
      print('trying to move from bottom to top or vice versa')
      return False
    elif canvas1 == canvasmain and canvas2 != canvasmain:
      #Return False if trying to move from canvasmain to top or bottom
      print('trying to move from canvasmain to top or bottom')
      return False
    return True
  
    def move(self, row1, col1, canvas1, row2, col2, canvas2):
    if not deck.movable(row1, col1, canvas1, row2, col2, canvas2):
      print("You cannot move the tile as it is to this hexagon")
      return 0
    #Remove tile. properties get updated
    (posold,num,tile)= deck.remove(row1,col1,canvas1)
    #Place tile on new place
    itemid = tile.place(row2,col2,canvas2,tile.tile)
    #Update storage
    deck.tiles.append(tile)
    deck.positions.append((row2,col2,str(canvas2)))
    deck.itemids.append(itemid)
    deck.dealt.append(num)
    #Update window
    win.update()
    return 1