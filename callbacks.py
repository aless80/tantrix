__author__ = 'Alessandro Marin'

import config as cfg
moving_tile_ind = 1 #todo I have to store the tille that was clicked!
clicked_rowcolcanv = None
clicked_ind = None

class Callbacks(object):

    def clickCallback(self, event):
      global clicked_rowcolcanv, clicked_ind
      #self.print_event(event)
      '''click'''
      if event.type == '4' and event.state == 16:
        print('\nclb.clickCallback pressed')
        rowcoltab = self.click_to_rowcolcanv(event)
        ind = cfg.deck.get_index_from_rowcolcanv(rowcoltab)
        print("clickCallback: rowcoltab, ind=" + str(rowcoltab) + str(ind))
        clicked_rowcolcanv = rowcoltab
        if ind is None:
          clicked_rowcolcanv = None
          return
        clicked_ind = ind
        '''release click'''
      elif event.type == '5' and event.state == 272:
        print('\nclb.clickCallback released')
        #previously clicked on empty hexagon
        if clicked_rowcolcanv is None:
          self.clickEmptyHexagon(event)
          return
        rowcoltab = self.click_to_rowcolcanv(event)  #todo here I could use simpler click_to_rowcolcanv
        if len(rowcoltab) == 0:
          return
        if rowcoltab == clicked_rowcolcanv: #released on same tile => rotate it
          '''Rotate'''
          cfg.deck.rotate(rowcoltab)
        elif rowcoltab != clicked_rowcolcanv: #released elsewhere => drop tile there.
          #previously clicked on empty hexagon
          #if clicked_rowcolcanv is None:
          #  return
          '''Move tile if place is not occupied already'''
          #newc
          deck_origin, deck_dest = clicked_rowcolcanv[2], rowcoltab[2]
          ok = cfg.deck.move(clicked_rowcolcanv[0], clicked_rowcolcanv[1], deck_origin,
                                   rowcoltab[0], rowcoltab[1], deck_dest)
          self.btnReset.configure(state = "active")
          #if moved is True:
          if cfg.deck.is_confirmable() is True:
            self.btnConf.configure(state = "active", bg = "cyan")
          else:
            self.btnConf.configure(state = "disabled", bg = "white")
          cfg.win.update() #this makes the color of the Confirm button white!
        #Reset the stored coordinates of the canvas where the button down was pressed
        clicked_rowcolcanv = None
        clicked_num = None
        #Delete the moving tile on win
        #cfg.win.children['moving'].destroy()

    def click_to_rowcolcanv(self, event):
      '''From mouse click return rowcoltab'''
      x, y = event.x, event.y
      if x <= 0 or x >= event.widget.winfo_reqwidth():
        print('x outside the original widget')
        return tuple()
      elif x < event.widget.winfo_reqwidth():
        print('x is inside the original widget')
      else:
        print('cannot be determined where x is vs original widget')
        return tuple()
      ybottom = cfg.canvasmain.winfo_reqheight()
      #Check y
      if y <= 0 or y >= ybottom:
        print('y outside the original widget')
        return tuple()
      elif y <= cfg.YTOP:
        print('y inside top')
        #newc   only x needed for pixel_to_off_canvastopbottom(x)
        rowcoltab = list(cfg.board.pixel_to_off_topbottom(x))
        rowcoltab.append("top")
      elif y <= cfg.YBOTTOM:
        print('y inside canvasmain')
        rowcoltab = list(cfg.board.pixel_to_off(x,y))
        rowcoltab.append("main")
      elif y <= ybottom:
        print('y inside cfg.canvasbottom')
        rowcoltab = list(cfg.board.pixel_to_off_topbottom(x))
        rowcoltab.append("bottom")
      else:
        raise UserWarning("click_to_rowcolcanv: cannot destination canvas")
        return tuple()
      return rowcoltab


    def buttonCallback(self, event):
      print('buttonCallback')
      #Buttons
      widget_name = event.widget._name
      if widget_name[0:3] == "btn":
        #release click
        if event.state == 272:
          if event.widget.cget("state") == 'disabled': return
          if widget_name == "btnConf":
            self.confirm_button()
          elif widget_name == "btnReset":
            print(self.btnReset.cget('state'))
            print("Reset!")
            status = cfg.deck.reset()
            #When reset enable/disable buttons
            if status:
              self.btnReset.configure(state = "disabled")
              self.btnConf.configure(state = "disabled")
              cfg.win.update()
        return


    def clickEmptyHexagon(self, event):
      from tantrix import log
      log()
      #self.print_event(event,' \nclickEmptyHexagon')

    def rxclickCallback(self, event):
      self.print_event(event, ' \nrxclickCallback')
      #new testing
      cfg.deck.move_ball((0, 5, "top"), (0, 6, "bottom"))
      #newc todo fix this
      cfg.win.children['moving'].destroy()

    def keyCallback(self, event):
      print("'" + str(event.char) + "' pressed")
      if event.char == '\r':
        self.confirm_button()

    def motionCallback(self, event):
      if clicked_ind is None: return
      tile = cfg.deck.tiles[clicked_ind]
      itemidold = cfg.deck.itemids[clicked_ind]
      cfg.deck.itemids.remove(itemidold)
      cfg.canvasmain.delete(itemidold) #this deletes it
      itemid = tile.free_place(event)
      cfg.deck.itemids.insert(clicked_ind, itemid)

    def confirm_button(self):
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

