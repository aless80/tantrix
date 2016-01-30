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

  def pixel_to_off(self,x, y):
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
    # convert odd-q offset to cube
    x = row
    z = col - (x - (x%2)) / 2
    y = -x-z
    return (x,y,z)

  def cube_to_hex(self, hex):
    """Convert cube coordinates to axial"""
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

  def off_to_pixel(self, row, col, tab):
    '''Given row, col and canvas, return the pixel coordinates of the center
    of the corresponding hexagon'''
    """
    if canvas.find_withtag(tk.CURRENT):
        #canvas.itemconfig(tk.CURRENT, fill="blue")
        canvas.update_idletasks()
        canvas.after(200)
        canvas.itemconfig(CURRENT, fill="red")
        """
    #I need the coordinates on the canvas
    #newc
    if tab == "top":
      x = cfg.HEX_SIZE + ((cfg.HEX_SIZE * 2) * col)
      y = cfg.HEX_HEIGHT / 2
    elif tab == "bottom":
      #cfg.HEX_HEIGHT*3+
      x = cfg.HEX_SIZE + ((cfg.HEX_SIZE * 2) * col)
      y = cfg.YBOTTOM + cfg.HEX_HEIGHT / 2
    #if str(canv) == ".canvasmain":
    elif tab == "main":
      x = cfg.HEX_SIZE + (cfg.HEX_SIZE  + cfg.HEX_SIDE) * row
      y = cfg.YTOP + cfg.HEX_HEIGHT / 2 + cfg.HEX_HEIGHT * col + cfg.HEX_HEIGHT / 2 * (row % 2)
    else:
        raise UserWarning("off_to_pixel: table "+ tab +" not defined")
    yield x
    yield y

  def get_neighbors(self, row, col=False):
    """Find the neighboring hexagons in the main canvas.
    Return a list of six rowcoltab"""
    if type(row) == list or type(row) == tuple:
      row, col, bin = row
    row, col = int(row),int(col)
    #Convert to cube coordinates, then add cfg.directions to cube coordinate
    neigh = []
    cube = list(self.off_to_cube(row, col))
    for dir in cfg.directions:
      c = map(lambda x, y : x + y, cube, dir)
      off = self.cube_to_off(c)
      #Get rowcoltab
      rowcoltab = off
      rowcoltab += (".canvasmain",)
      neigh.append(rowcoltab)
    if len(neigh) != 6:
        raise UserWarning("Board.get_neighbors: Neighbors should be 6!")
    return neigh #list of six rowcoltab

  def __init__(self):
    pass