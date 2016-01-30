__author__ = 'Alessandro Marin'

import config as cfg
moving_tile_ind = 1 #todo I have to store the tille that was clicked!
clicked_rowcolcanv = None

class Callbacks(object):

    def clickCallback(self, event):
      print('\nclb.clickCallback')
      global clicked_rowcolcanv
      x, y = event.x, event.y
      #self.print_event(event)
      #with this I change to the canvas' coordinates: x = canvas.canvasx(event.x)
      #print canvas.find_closest(x, y)
      #http://epydoc.sourceforge.net/stdlib/Tkinter.Event-class.html
      #NB: move while dragging is type=6 (clb.clickCallback) state=272
      #NB: click                  type=4 (BPress) state=16
      #NB: release click          type=5 (BRelea) state=272
      #
      '''click'''
      if event.type == '4' and event.state == 16:
        rowcolcanv = self.click_to_rowcolcanv(event)
        ind = cfg.deck.get_index_from_rowcolcanv(rowcolcanv)
        print("clickCallback: rowcolcanv, ind=" + str(rowcolcanv) + str(ind))
        #new
        clicked_rowcolcanv = rowcolcanv
        #
        if ind is None:
          clicked_rowcolcanv = None
          return
        clicked_rowcolcanv = rowcolcanv
        '''release click'''
      elif event.type == '5' and event.state == 272:
        #previously clicked on empty hexagon
        if clicked_rowcolcanv is None:
          self.clickEmptyHexagon(event)
          return
        rowcolcanv = self.click_to_rowcolcanv(event)  #todo here I could use simpler click_to_rowcolcanv
        if len(rowcolcanv) == 0:
          return
        if rowcolcanv == clicked_rowcolcanv: #released on same tile => rotate it
          '''Rotate'''
          cfg.deck.rotate(rowcolcanv)
        elif rowcolcanv != clicked_rowcolcanv: #released elsewhere => drop tile there.
          #previously clicked on empty hexagon
          #if clicked_rowcolcanv is None:
          #  return
          '''Move tile if place is not occupied already'''
          #newc
          deck_origin, deck_dest = clicked_rowcolcanv[2], rowcolcanv[2]
          moved_ok = cfg.deck.move(clicked_rowcolcanv[0], clicked_rowcolcanv[1], deck_origin,
                                   rowcolcanv[0], rowcolcanv[1], deck_dest)
          #Delete the moving tile on win
          cfg.win.children['moving'].destroy()
          self.btnReset.configure(state="active")
          #if moved is True:
          if cfg.deck.is_confirmable() is True:
            self.btnConf.configure(state = "active", bg = "cyan")
          else:
            self.btnConf.configure(state = "disabled", bg = "white")
          cfg.win.update() #this makes the color of the Confirm button white!
        #Reset the stored coordinates of the canvas where the button down was pressed
        clicked_rowcolcanv=None
      else:
        pass
        #print('\n !event not supported \n')

    def click_to_rowcolcanv(self, event):
      '''From mouse click return rowcolcanv'''
      x, y = event.x, event.y
      if x <= 0 or x >= event.widget.winfo_reqwidth():
        print('x outside the original widget')
        return tuple()
      elif x < event.widget.winfo_reqwidth():
        print('x is inside the original widget')
      else:
        print('cannot be determined where x is vs original widget')
        return tuple()
      #ytop = cfg.CANVAS_HEIGHT #cfg.canvastop.winfo_reqheight()
      #ymain = ytop + cfg.canvasmain.winfo_reqheight()
      #ybottom = ymain #+ cfg.canvasbottom.winfo_reqheight()
      '''
      if str(event.widget) == "top":
        yrel = y
      elif str(event.widget) == ".canvasmain":
        yrel = y + ytop
      elif str(event.widget) == "bottom":
        yrel = y + ymain
      else:
        return tuple()
        raise UserWarning("click_to_rowcolcanv: cannot determine yrel")
      '''
      ybottom = cfg.canvasmain.winfo_reqheight()
      #Check y
      if y <= 0 or y >= ybottom:
        print('y outside the original widget')
        return tuple()
      elif y <= cfg.YTOP:
        print('y inside top')
        #newc   only x needed for pixel_to_off_canvastopbottom(x)
        rowcolcanv = list(cfg.board.pixel_to_off_topbottom(x))
        rowcolcanv.append("top")
      elif y <= cfg.YBOTTOM:
        print('y inside canvasmain')
        rowcolcanv = list(cfg.board.pixel_to_off(x,y))
        rowcolcanv.append(".canvasmain")
      elif y <= ybottom:
        print('y inside cfg.canvasbottom')
        rowcolcanv = list(cfg.board.pixel_to_off_topbottom(x))
        rowcolcanv.append("bottom")
      else:
        raise UserWarning("click_to_rowcolcanv: cannot destination canvas")
        return tuple()
      return rowcolcanv


    def buttonCallback(self, event):
      print('buttonCallback')
      #Buttons
      widget_name = event.widget._name
      if widget_name[0:3] == "btn":
        #release click
        if event.state == 272:
          if widget_name == "btnConf":
            self.confirm_button()
          elif widget_name == "btnReset":
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
      ind = cfg.deck.get_index_from_rowcolcanv(clicked_rowcolcanv)
      cfg.deck.free_move(ind, event)

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
        rowcolcanv=self.click_to_rowcolcanv(event)
        neigh= cfg.deck.get_neighboring_tiles(rowcolcanv)
        print('neigh = ' + str(neigh))
        neighcolors = cfg.deck.get_neighboring_colors(rowcolcanv)
        print('neighcolors = ' + str(neighcolors))

