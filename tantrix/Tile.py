import PIL.Image, PIL.ImageTk
import os.path
try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import config as cfg

class Tile(object):
    """Tile object"""
    @property
    def angle(self):
        """The object's angle"""
        return self._angle
    @angle.setter
    def angle(self, angle = 0):
        self._angle = angle
    @property
    def lock(self):
        """If the tile has been confirmed and cannot be moved (1) or not (0)"""
        return self._lock
    @lock.setter
    def lock(self, lock = False):
        self._lock = lock

    def __init__(self, num, angle = 0):
        """tile object containing a tile in PhotoImage format.
        NB: tile image is created and placed in create_at_rowcoltab"""
        """.tile property is a PhotoImage (required by Canvas' create_image) and its number"""
        units = (num - 1) % 10
        decimals = (num - 1)/ 10
        cfg.SPRITE = PIL.Image.open(os.path.join(cfg.script_dir, "../img/sprites/sprite_smaller.png"))
        tilePIL = cfg.SPRITE.crop( (cfg.SPRITE_WIDTH * units, cfg.SPRITE_HEIGHT * (decimals),
             cfg.SPRITE_WIDTH * (units + 1), cfg.SPRITE_HEIGHT * (decimals + 1)) ).resize(
            (cfg.HEX_SIZE * 2, int(cfg.HEX_HEIGHT)), PIL.Image.ANTIALIAS)
        if angle != 0:
            tilePIL = tilePIL.rotate(angle, expand = 0, resample = PIL.Image.BICUBIC) #, tags = "tile")
        self.tile = PIL.ImageTk.PhotoImage(tilePIL)
        self.basecolors = cfg.colors[num - 1]
        self.angle = angle % -360
        self.lock = False
        self.num = num #store the tile number
        self.confirm = None
        self.itemid = None

    def __str__(self):
        string = 'tile %d, %s, %d degrees, confirmed in %s: ' % (self.num, self.getColor(), self.angle, str(self.confirm))
        return string

    def getColor(self):
        """Get the current colors starting from North direction"""
        basecolor = self.basecolors
        n = self.angle/60
        return basecolor[n:] + basecolor[:n]

    def rowcolcanv_match_colors(self):
        """Return True if the tile at rowcoltab and angle1 matches the neighbors' colors"""
        """No colors matching when user is trying things"""
        return False
        #if cfg.TRYING == True:
        #    print("TRYING is True, so no colors check")
        #    return True
        """Get neighboring colors"""
        neighcolors = deck.get_neighboring_colors(rowcoltab)
        """Angle"""
        basecolor = self.getColor()
        n = angle/60
        tilecolor = basecolor[n:] + basecolor[:n]
        for nc in neighcolors:
            if tilecolor[nc[1]] != nc[0]:
                #print("neighbors: " + str(deck.get_neighboring_tiles(rowcoltab)))
                #print("tilecolor = " + str(tilecolor) + " " + str(nc[1]) + " " + nc[0])
                #NB cannot move tile one tile away because current tile is present.
                # I do not see any case in which that is what i want
                return False
        return True

    def tile_match_colors(self, rowcoltab, angle = 0):
        """Return True if the tile at rowcoltab and angle matches the neighbors' colors"""
        #No colors matching when user is trying things
        #if cfg.TRYING == True:
        #  print("TRYING is True, so no colors check")
        #  return True
        """Get neighboring colors"""
        neighcolors = cfg.deck.get_neighboring_colors(rowcoltab)
        """Angle"""
        basecolor = self.getColor()
        n = angle/60
        tilecolor = basecolor[n:] + basecolor[:n]
        for nc in neighcolors:
            if tilecolor[nc[1]] != nc[0]:
                """NB cannot move tile one tile away because current tile is present.
                   I do not see any case in which that is what I want"""
                return False
        """Lock the tile image, meaning that it is placed on a regular place on the board/tabs"""
        return True

    def create_at_rowcoltab(self, rowcoltab):
        """Create a tile image and place it on cfg.canvas. No update .positions. Return the itemid."""
        """Get the pixels"""
        x, y = cfg.board.off_to_pixel(rowcoltab)
        self.itemid = cfg.canvas.create_image(x, y, image = self.tile, tags = "a tag") #TODO this is where tile is created and placed
        self.lock = True
        #TESTING
        #find_below, itemcget
        fill1 = cfg.canvas.itemcget(cfg.stipple1, 'fill')
        fill2 = cfg.canvas.itemcget(cfg.stipple2, 'fill')
        stipple1 = cfg.canvas.itemcget(cfg.stipple1, 'stipple')
        stipple2 = cfg.canvas.itemcget(cfg.stipple2, 'stipple')
        #cfg.canvas.itemconfig(cfg.stipple1, fill = '')
        #cfg.canvas.itemconfig(cfg.stipple2, fill = 'gray', stipple = "gray12")
        cfg.canvas.tag_raise(cfg.stipple1)
        cfg.canvas.tag_raise(cfg.stipple2)

        cfg.win.update()
        return self.itemid

    def move_to_pixel(self, x, y):
        """Move an existing tile to the pixel coordinates x, y"""
        cfg.canvas.coords(self.itemid, (x, y))
