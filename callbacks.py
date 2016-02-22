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
        id = cfg.canvas.find_withtag(CURRENT)
        if clicked_rowcoltab is None:
            #otherwise tile - it is a rectangle - can be moved when clicking just outside its hexagon.
            return
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
        '''Callback for rx-button click of mouse, pressed or released'''
        #self.print_event(event, ' \nrxclickCallback')
        #Highlight
        #print(cfg.canvas.winfo_children()) #does not work. it should
        rowcoltab = self.click_to_rowcoltab(event)
        #check forced spaces
        obliged_hexagons = cfg.deck.check_forced()

    def clickCallback(self, event):
        '''Callback for lx-button click of mouse, pressed or released'''
        #self.print_event(event)
        #Remove all highlights
        cfg.board.remove_all_highlights()
        if event.type == '4' and event.state == 16:
            self.mousePressed(event)
        elif event.type == '5' and event.state == 272:
            if clicked_rowcoltab is None:
                #previously clicked on empty hexagon
                self.clickEmptyHexagon(event)
            else:
                self.mouseReleased(event)

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

    def buttonReset(self):
        cfg.board.remove_all_highlights()
        status = cfg.deck.reset()
        #When reset enable/disable buttons
        if status:
          self.btnReset.configure(state = "disabled")
          self.btnConf.configure(state = "disabled")
          cfg.win.update()

    def mousePressed(self, event):
        global clicked_rowcoltab
        print('\nclb.clickCallback pressed')
        clicked_rowcoltab = self.click_to_rowcoltab(event)
        #clicked_rowcoltab null when no tile there
        ind = cfg.deck.get_index_from_rowcoltab(clicked_rowcoltab)
        if ind is None:
            clicked_rowcoltab = None
            return

    def mouseReleased(self, event):
        global clicked_rowcoltab
        print('clb.clickCallback released')
        rowcoltab = self.click_to_rowcoltab(event)  #todo could use simpler click_to_rowcolcanv
        if not rowcoltab: #This could happen when mouse is released outside window, so
            #If mouse was pressed on a tile, bring tile back to its origin.
            if clicked_rowcoltab:
                ind = cfg.deck.get_index_from_rowcoltab(clicked_rowcoltab)
                itemid = cfg.deck.itemids[ind]
                x, y = cfg.board.off_to_pixel(clicked_rowcoltab)
                cfg.canvas.coords(itemid, (x, y))
            return
        if rowcoltab == clicked_rowcoltab: #released on same tile => rotate it
            '''Rotate'''
            n = cfg.deck.get_index_from_rowcoltab(rowcoltab)
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
        """Reset the stored coordinates of the canvas where the button down was pressed"""
        clicked_rowcoltab = None
        """Confirm and Reset buttons"""
        if cfg.deck.is_confirmable(True) is True:
            self.btnConf.configure(state = "normal", relief="raised", bg = "cyan")
        else:
            self.btnConf.configure(state = "disabled", relief="flat")
        if len(cfg.deck._positions_moved) is not 0:
            self.btnReset.configure(state = "normal", relief="raised", bg = "cyan")
        else:
            self.btnReset.configure(state = "disabled", relief="flat")

    def click_to_rowcoltab(self, event):
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
        ybottom = cfg.canvas.winfo_reqheight()
        if y <= 0 or y >= ybottom:
            print('y outside the original widget')
            return tuple()
        elif y <= cfg.YTOPCANVAS:
            #print('y inside top')
            rowcoltab = list(cfg.board.pixel_to_off_topbottom(x))
            rowcoltab.append(-1)
        elif y <= cfg.YBOTTOMCANVAS:
            #print('y inside canvas')
            rowcoltab = list(cfg.board.pixel_to_off(x, y))
            rowcoltab.append(0)
        elif y <= ybottom:
            #print('y inside cfg.canvasbottom')
            rowcoltab = list(cfg.board.pixel_to_off_topbottom(x))
            rowcoltab.append(-2)
        else:
            raise UserWarning("click_to_rowcolcanv: cannot destination canvas")
            return tuple()
        return rowcoltab

    def clickEmptyHexagon(self, event):
        rowcoltab = self.click_to_rowcoltab(event)
        cfg.deck.log(str(rowcoltab))
        neigh = cfg.deck.get_neighboring_tiles(rowcoltab)
        if len(neigh):
            cfg.board.place_highlight(rowcoltab)
            """find and highlight all matches"""
            matches = cfg.deck.find_matching_tiles(rowcoltab)
            for m in matches:
                cfg.board.place_highlight(m)
                cfg.win.update()

    def buttonConfirm(self):
        print("Confirm clicked ")
        global TRYING
        cfg.board.remove_all_highlights()
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
        cfg.deck.refill_deck(-1)
        cfg.deck.refill_deck(-2)
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
        print('offset (if in cfg.canvas!) = ' + str(cube))
        print('hex = ' + str(hex))
        rowcoltab=self.click_to_rowcoltab(event)
        neigh= cfg.deck.get_neighboring_tiles(rowcoltab)
        print('neigh = ' + str(neigh))
        neighcolors = cfg.deck.get_neighboring_colors(rowcoltab)
        print('neighcolors = ' + str(neighcolors))

