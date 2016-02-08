__author__ = 'Alessandro Marin'

import config as cfg
clicked_rowcoltab = None


from Tkinter import CURRENT
class Callbacks(object):

    def keyCallback(self, event):
        print("'" + str(event.char) + "' pressed")
        key = event.char
        if key == '\r':
            self.buttonConfirm()
        elif key =='r':
            self.buttonReset()

    def motionCallback(self, event):
        id = cfg.canvasmain.find_withtag(CURRENT)
        try:
            itemid = cfg.deck.itemids.index(id[0])
        except:
            print("Error in motionCallback. itemids=",str(cfg.deck.itemids))
            print("id[0]=",str(id[0]))
            #itemid = cfg.deck.itemids.index(id[0])
            return
        tile = cfg.deck.tiles[itemid]
        tile.move_to_pixel(event.x, event.y, id[0])
        return

    def rxclickCallback(self, event):
        self.print_event(event, ' \nrxclickCallback')


    def clickCallback(self, event):
        '''Callback for lx-button click of mouse, pressed or released'''
        #self.print_event(event)
        if event.type == '4' and event.state == 16:
            self.mousePressed(event)
        elif event.type == '5' and event.state == 272:
            if clicked_rowcoltab is None:
                #previously clicked on empty hexagon
                self.clickEmptyHexagon(event)
            else: self.mouseReleased(event)

    def buttonCallback(self, event):
        '''Callback for click on a Button on the UI'''
        print('buttonCallback')
        widget_name = event.widget._name
        if widget_name[0:3] == "btn":
        #if event.state == 272: #release click
            if event.widget.cget("state") == 'disabled': return
            if widget_name == "btnConf":
                print("\nConfirm!")
                self.buttonConfirm()
            elif widget_name == "btnReset":
                print("\nReset!")
                self.buttonReset()
            return

    def mousePressed(self, event):
        global clicked_rowcoltab
        print('\nclb.clickCallback pressed')
        rowcoltab = self.click_to_rowcolcanv(event)
        clicked_rowcoltab = rowcoltab
        #clicked_rowcoltab null when no tile there
        ind = cfg.deck.get_index_from_rowcoltab(rowcoltab)
        if ind is None:
            clicked_rowcoltab = None
            return

    def mouseReleased(self, event):
        global clicked_rowcoltab
        print('clb.clickCallback released')
        rowcoltab = self.click_to_rowcolcanv(event)  #todo could use simpler click_to_rowcolcanv
        if not rowcoltab: #This could happen when mouse is released outside window, so
            #If mouse was pressed on a tile, bring tile back to its origin.
            if clicked_rowcoltab:
                ind = cfg.deck.get_index_from_rowcoltab(clicked_rowcoltab)
                itemid = cfg.deck.itemids[ind]
                tilex, tiley = cfg.board.off_to_pixel(clicked_rowcoltab)
                cfg.canvasmain.coords(itemid, (tilex, tiley))
            return
        if rowcoltab == clicked_rowcoltab: #released on same tile => rotate it
            '''Rotate'''
            cfg.deck.rotate(rowcoltab)
        elif rowcoltab != clicked_rowcoltab: #released elsewhere => drop tile there.
            '''Move tile if place is not occupied already'''
            deck_origin, deck_dest = clicked_rowcoltab[2], rowcoltab[2]
            ok = cfg.deck.move((clicked_rowcoltab[0], clicked_rowcoltab[1], deck_origin),
                               (rowcoltab[0], rowcoltab[1], deck_dest))
            """Check if placing worked and if not put back to where it was"""
            if not ok:
                self.back_to_original_place(clicked_rowcoltab)
                return
        """Confirm and Reset buttons"""
        if cfg.deck.is_confirmable() is True:
            self.btnConf.configure(state = "active", bg = "cyan")
        else:
            self.btnConf.configure(state = "disabled", bg = "white")
        if len(cfg.deck._positions_moved) is 0:
            self.btnReset.configure(state = "disabled")
        else:
            self.btnReset.configure(state = "active")
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
        #itemid, ind = cfg.deck.get_itemid_from_rowcoltab(rowcoltab)
        #ind = cfg.deck.get_index_from_rowcoltab(rowcoltab)
        itemid, ind = cfg.deck.get_itemid_from_rowcoltab(rowcoltab)
        tile = cfg.deck.tiles[ind]
        #Cannot use move_to_rowcoltab
        tile.move_to_rowcoltab(rowcoltab) #this is not good because when movin origin can appear occupied

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

