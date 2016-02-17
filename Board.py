import math
import PIL.Image, PIL.ImageTk
try:
    import Tkinter as tk # for Python2
except:
    import tkinter as tk # for Python3
import HexagonGenerator as hg
import config as cfg

class Board(object):

    def pixel_to_off_topbottom(self, x):
        col = math.floor(float(x) / (cfg.HEX_SIZE * 2))
        return (0, col)

    def pixel_to_off(self, x, y):
        y -= cfg.YTOP
        q = x * 2/3 / cfg.HEX_SIZE
        r = (-x / 3 + math.sqrt(3)/3 * y) / cfg.HEX_SIZE
        #print("self.cube_round in cube= " +str(self.cube_round((q, -q-r, r))))
        cube = (q, -q-r, r)
        cuberound = self.cube_round(cube)
        offset = self.cube_to_off(cuberound)
        return offset

    def pixel_to_hex(self, x, y):
        q = x * 2/3 / cfg.HEX_SIZE
        r = (-x / 3 + math.sqrt(3)/3 * y) / cfg.HEX_SIZE
        #print("self.cube_round in cube= " +str(self.cube_round((q, -q-r, r))))
        return self.hex_round((q, r))
        #return self.cube_to_hex(self.cube_round((q, -q-r, r)))

    def hex_round(self, hex):
        return self.cube_to_hex(self.cube_round(self.hex_to_cube(hex)))

    def cube_to_off(self,cube):
        """Convert cube to odd-q offset"""
        row = cube[0]
        col = cube[2] + (cube[0] - (cube[0]%2)) / 2
        return (row, col)

    def off_to_cube(self, row, col):
        '''convert odd-q offset to cube'''
        x = row
        z = col - (x - (x%2)) / 2
        y = -x-z
        return (x,y,z)

    def cube_to_hex(self, hex):
        '''Convert cube coordinates to axial'''
        q = hex[0]
        r = hex[1]
        return (q, r)

    def hex_to_cube(self, h): # axial
        x = h[1]
        z = h[0]
        y = -x-z
        return (x, y, z) #return Cube(x, y, z)

    def cube_round(self, h):
        rx = round(h[0])
        ry = round(h[1])
        rz = round(h[2])
        x_diff = abs(rx - h[0])
        y_diff = abs(ry - h[1])
        z_diff = abs(rz - h[2])
        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry-rz
        elif y_diff > z_diff:
            ry = -rx-rz
        else:
            rz = -rx-ry
        return ((rx, ry, rz)) #return (Cube(rx, ry, rz))

    def off_to_pixel(self, rowcoltab):
        '''Given row, col and canvas, return the pixel coordinates of the center
        of the corresponding hexagon'''
        #I need the coordinates on the canvas
        row, col, tab = rowcoltab
        if tab == -1:
            x = cfg.HEX_SIZE + ((cfg.HEX_SIZE * 2) * col)
            y = cfg.HEX_HEIGHT / 2
        elif tab == -2:
            x = cfg.HEX_SIZE + ((cfg.HEX_SIZE * 2) * col)
            y = cfg.YBOTTOM + cfg.HEX_HEIGHT / 2
        elif tab == 0:
            x = cfg.HEX_SIZE + (cfg.HEX_SIZE  + cfg.HEX_SIDE) * row
            y = cfg.YTOP + cfg.HEX_HEIGHT / 2 + cfg.HEX_HEIGHT * col + cfg.HEX_HEIGHT / 2 * (row % 2)
        else:
            raise UserWarning("off_to_pixel: table "+ tab +" not defined")
        yield x
        yield y

    def get_neighboring_hexagons(self, row, col = False):
        '''Find the neighboring hexagons in the main canvas.
        Return a list of six rowco and its numberltab'''
        if type(row) == list or type(row) == tuple:
          row, col, bin = row
        row, col = int(row), int(col)
        #Convert to cube coordinates, then add cfg.directions to cube coordinate
        neigh = []
        cube = list(self.off_to_cube(row, col))
        for dir in cfg.directions:
            c = map(lambda x, y : x + y, cube, dir)
            off = self.cube_to_off(c)
            #Get rowcoltab
            rowcoltab = off
            rowcoltab += (0,)
            neigh.append(rowcoltab)
        if len(neigh) != 6:
            raise UserWarning("Board.get_neighboring_hexagons: Neighbors should be 6!")
        return neigh #list of six rowcoltab

    def place_highlight(self, rowcoltab):
        '''Highlight a hexagon. return its id on cfg.canvasmain'''
        pts = list(cfg.hexagon_generator(rowcoltab[0], rowcoltab[1], rowcoltab[2]))
        highid = cfg.canvasmain.create_line(pts, width = 2, fill = "red", tag = "high")
        self._highlight.append(tuple(rowcoltab))
        self._highlightids.append(highid)
        cfg.win.update()
        return highid

    def remove_all_highlights(self):
        if not len(self._highlight):
            return
        try:
            #[cfg.canvasmain.delete(item) for item in self._highlight]
            [cfg.canvasmain.delete(item) for item in self._highlightids]
            self._highlightids = []
            self._highlight = []
            cfg.win.update()
        except:
            1

    def remove_highlight(self, rowcoltab):
        '''Remove all highlighted hexagons'''
        if len(self._highlightids) == 0:
            return
        try:
            hind = self._highlight.index(rowcoltab)
        except:
            print("remove_highlight except")
            return
        hid = self._highlightids.pop(hind)
        cfg.canvasmain.delete(hid)
        #todo: to remove one particular highid, how to find it? store them and go by index?
        #highids = cfg.canvasmain.find_withtag("high")
        #for h in highids:
        #    cfg.canvasmain.delete(h)

    def __init__(self):
        self._highlight = []
        self._highlightids = []
        pass