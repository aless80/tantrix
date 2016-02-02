__author__ = 'Alessandro Marin'

import config as cfg
clicked_rowcoltab = None
clicked_ind = None

class Callbacks(object):

    def keyCallback(self, event):
      print("'" + str(event.char) + "' pressed")
      if event.char == '\r':
        self.buttonConfirm()

    def motionCallback(self, event):
      if clicked_ind is None: return
      tile = cfg.deck.tiles[clicked_ind]
      itemidold = cfg.deck.itemids[clicked_ind]
      cfg.deck.itemids.remove(itemidold)
      cfg.canvasmain.delete(itemidold) #this deletes it
      itemid = tile.free_place(event)
      cfg.deck.itemids.insert(clicked_ind, itemid)

    def rxclickCallback(self, event):
      #self.print_event(event, ' \nrxclickCallback')
      if len(cfg.deck._positions_moved)==0:
        cfg.deck.free_move((0, 0, "top"), (0, 0, "main"))
      else:
        cfg.deck.free_move((0, 0, "main"), (0, 0, "top"))
      #newc todo fix this

    def clickCallback(self, event):
      #self.print_event(event)
      '''click'''
      if event.type == '4' and event.state == 16:
        self.mousePressed(event)
      elif event.type == '5' and event.state == 272:
        if clicked_rowcoltab is None:
          #previously clicked on empty hexagon
          self.clickEmptyHexagon(event)
        else: self.mouseReleased(event)

    def buttonCallback(self, event):
      print('buttonCallback')
      #Buttons
      widget_name = event.widget._name
      if widget_name[0:3] == "btn":
        #release click
        if event.state == 272:
          if event.widget.cget("state") == 'disabled': return
          if widget_name == "btnConf":
            print("\nConfirm!")
            self.buttonConfirm()
          elif widget_name == "btnReset":
            print("\nReset!")
            self.buttonReset()
        return

    def mousePressed(self, event):
        global clicked_rowcoltab, clicked_ind
        print('\nclb.clickCallback pressed')
        rowcoltab = self.click_to_rowcolcanv(event)
        ind = cfg.deck.get_index_from_rowcoltab(rowcoltab)
        clicked_rowcoltab = rowcoltab
        if ind is None:
          clicked_rowcoltab = None
          return
        clicked_ind = ind
        '''release click'''

    def mouseReleased(self, event):
        global clicked_rowcoltab, clicked_ind
        print('clb.clickCallback released')
        rowcoltab = self.click_to_rowcolcanv(event)  #todo could use simpler click_to_rowcolcanv
        if not rowcoltab: #This could happen when mouse is released outside window, so
          #If mouse was pressed on a tile, bring tile back to its origin.
          if clicked_rowcoltab: self.back_to_original_place(clicked_rowcoltab)
          return
        if rowcoltab == clicked_rowcoltab: #released on same tile => rotate it
          '''Rotate'''
          cfg.deck.rotate(rowcoltab)
        elif rowcoltab != clicked_rowcoltab: #released elsewhere => drop tile there.
          '''Move tile if place is not occupied already'''
          deck_origin, deck_dest = clicked_rowcoltab[2], rowcoltab[2]
          ok = cfg.deck.move(clicked_rowcoltab[0], clicked_rowcoltab[1], deck_origin,
                                   rowcoltab[0], rowcoltab[1], deck_dest)
          #check here if  placeing worked and if not put back to where it was!
          if not ok:
            #todo problem: remove the freely moved tile
            self.back_to_original_place(clicked_rowcoltab)
            return
          self.btnReset.configure(state = "active")
          #if moved is True:
          if cfg.deck.is_confirmable() is True:
            self.btnConf.configure(state = "active", bg = "cyan")
          else:
            self.btnConf.configure(state = "disabled", bg = "white")
          cfg.win.update() #this makes the color of the Confirm button white!
        #Reset the stored coordinates of the canvas where the button down was pressed
        clicked_rowcoltab = None

    def click_to_rowcolcanv(self, event):
      '''From mouse click return rowcoltab'''
      x, y = event.x, event.y
      if x <= 0 or x >= event.widget.winfo_reqwidth():
        print('x outside the original widget')
        return tuple()
      elif x < event.widget.winfo_reqwidth():
        #print('x is inside the original widget')
        pass
      else:
        print('cannot be determined where x is vs original widget')
        return tuple()
      """Check y"""
      ybottom = cfg.canvasmain.winfo_reqheight()
      if y <= 0 or y >= ybottom:
        print('y outside the original widget')
        return tuple()
      elif y <= cfg.YTOP:
        #print('y inside top')
        #newc   only x needed for pixel_to_off_canvastopbottom(x)
        rowcoltab = list(cfg.board.pixel_to_off_topbottom(x))
        rowcoltab.append("top")
      elif y <= cfg.YBOTTOM:
        #print('y inside canvasmain')
        rowcoltab = list(cfg.board.pixel_to_off(x,y))
        rowcoltab.append("main")
      elif y <= ybottom:
        #print('y inside cfg.canvasbottom')
        rowcoltab = list(cfg.board.pixel_to_off_topbottom(x))
        rowcoltab.append("bottom")
      else:
        raise UserWarning("click_to_rowcolcanv: cannot destination canvas")
        return tuple()
      return rowcoltab

    def clickEmptyHexagon(self, event):
      from tantrix import log
      log()
      #self.print_event(event,' \nclickEmptyHexagon')

    def buttonConfirm(self):
        print("Confirm clicked ")
        global TRYING
        #cfg.TRYING = False
        status = cfg.deck.confirm_move()
        #top.after(1000, top.destroy)
        #msg = tkMessageBox.showwarning("Cannot action",
        #    "Cannot confirm \n(%s)" % status)
        #cfg.win.after(1000, msg.destroy())
        print("cfg.deck.confirm_move successful: " + str(status))
        cfg.TRYING = True
        #When confirmed enable/disable buttons
        if not status: return
        self.btnReset.configure(state = "disabled")
        self.btnConf.configure(state = "disabled")
        cfg.deck.refill_deck("top")
        cfg.deck.refill_deck("bottom") #in the future I will have to refill only one
        cfg.win.update()
        #Refill todo

    def buttonReset(self):
        status = cfg.deck.reset()
        #When reset enable/disable buttons
        if status:
          self.btnReset.configure(state = "disabled")
          self.btnConf.configure(state = "disabled")
          cfg.win.update()

    def back_to_original_place(self, rowcoltab):
        ind = cfg.deck.get_index_from_rowcoltab(rowcoltab)
        itemid = cfg.deck.tiles[ind].place(rowcoltab)
        #Update storage
        tile = cfg.deck.tiles[ind]
        num = cfg.deck.get_tile_number_from_index(ind)
        cfg.deck.update_storage(clicked_rowcoltab[0], clicked_rowcoltab[1], clicked_rowcoltab[2], tile, num, itemid)

    def print_event(self, event, msg= ' '):
        print(msg)
        x, y = event.x, event.y
        hex = cfg.board.pixel_to_hex(x,y)
        cube = cfg.board.pixel_to_off(x, y)
        print(' widget = ' + str(event.widget))
        print(' type = ' + str(event.type))
        print(' state = ' + str(event.state))
        print(' num = ' + str(event.num))
        print(' delta =' + str(event.delta))
        print('x, y = {}, {}'.format(x, y))
        print(" x_root, y_root = ",str((event.x_root, event.y_root)))
        print('offset (if in cfg.canvasmain!) = ' + str(cube))
        print('hex = ' + str(hex))
        rowcoltab=self.click_to_rowcolcanv(event)
        neigh= cfg.deck.get_neighboring_tiles(rowcoltab)
        print('neigh = ' + str(neigh))
        neighcolors = cfg.deck.get_neighboring_colors(rowcoltab)
        print('neighcolors = ' + str(neighcolors))

