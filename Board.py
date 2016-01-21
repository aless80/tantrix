import math
import PIL.Image, PIL.ImageTk
try:
  import Tkinter as tk # for Python2
except:
  import tkinter as tk # for Python3
import HexagonGenerator as hg
import config as cfg

class Board(object):
  def pixel_to_off_canvastopbottom(self, x, y):
    col = math.floor(float(x) / (cfg.HEX_SIZE * 2))
    return (0, col)
  def pixel_to_off(self,x, y):
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
  def __init__(self):
  #  pass
  #def __call__(self):
    #global cfg.win, cfg.canvasmain, cfg.canvastop, cfg.canvasbottom, \
    global hexagon_generator, board, deck
    global btn1, btn2, btnConf, btnReset
    cfg.win = tk.Tk()
    cfg.canvasmain = tk.Canvas(cfg.win, height= cfg.CANVAS_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey', name="canvasmain")
    #cfg.canvasmain = tk.Canvas(cfg.win, height= 310, width = cfg.CANVAS_WIDTH, background='lightgrey', name="canvasmain")
    cfg.canvastop = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name="canvastop")
    cfg.canvasbottom = tk.Canvas(cfg.win, height= cfg.HEX_HEIGHT, width = cfg.CANVAS_WIDTH, background='lightgrey',name="canvasbottom")
    w = cfg.CANVAS_WIDTH + 5
    h = cfg.CANVAS_HEIGHT + cfg.HEX_HEIGHT * 2 + 5
    ws = cfg.win.winfo_screenwidth()    #width of the screen
    hs = cfg.win.winfo_screenheight()       #height of the screen
    x = ws - w / 2; y = hs - h / 2    #x and y coord for the Tk root window
    cfg.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #Create hexagons on main canvas
    hexagon_generator = hg.HexagonGenerator(cfg.HEX_SIZE)
    for row in range(cfg.ROWS):
      for col in range(cfg.COLS):
        pts = list(hexagon_generator(row, col))
        cfg.canvasmain.create_line(pts, width =2)
    #Append canvases
    cfg.canvastop.grid(row = 0, column = 0)#,expand="-in")
    cfg.canvasmain.grid(row = 1, column = 0, rowspan = 5)#,expand="-ipadx")
    cfg.canvasbottom.grid(row = 6, column = 0)#,expand="-padx")
    #Button1
    btn1 = tk.Button(cfg.win, width=6, text="Refill\nhand",  bg="yellow", name = "btn1")
    #Add cfg.canvastop to tags, so button click will be processed by cfg.canvastop!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, cfg.canvastop)
    #btn1.bindtags(tuple(bindtags))
    btn1.bind('<ButtonRelease-1>', buttonClick)
    btn1.grid(row=0, column=1,columnspan=1)
    #Button2
    btn2 = tk.Button(cfg.win, width=6, text="Refill\nhand",  bg="red", name = "btn2") #, height=int(round(cfg.HEX_HEIGHT))-1
    #Add canvasbpttom to tags, so button click will be processed by cfg.canvasbottom!
    #bindtags = list(btn1.bindtags())
    #bindtags.insert(1, cfg.canvasbottom)
    #btn2.bindtags(tuple(bindtags))
    btn2.bind('<ButtonRelease-1>', buttonClick)
    btn2.grid(row=6, column=1,columnspan=1)
    #Confirm button
    btnConf = tk.Button(cfg.win, text="Confirm\nmove",  bg="cyan",
                      width=6, name = "btnConf") #padx=5,
    btnConf.bind('<ButtonRelease-1>', buttonClick)
    btnConf.grid(row=2, column=1, columnspan=1)
    #Reset button
    btnReset = tk.Button(cfg.win, text="Reset\ndeck",  bg="cyan",
                      width=6, name = "btnReset")
    btnReset.bind('<ButtonRelease-1>', buttonClick)
    btnReset.grid(row=4, column=1,columnspan=1)
    #TRYING button
    clr={False:"lightgrey", True:"cyan"}
    '''btnTry = tk.Button(cfg.win, width=6, text="Try\nthings",  bg=clr[TRYING], name = "btnTry")
    btnTry.bind('<ButtonRelease-1>', buttonClick)
    btnTry.grid(row=3, column=1,columnspan=1)
    #btnTry(state="disabled")'''
    #Update window
    cfg.win.update()
    cfg.win.winfo_height() #update before asking size!
    cfg.win.geometry(str(cfg.canvasmain.winfo_width() + 100) + "x" + str(int(round(cfg.CANVAS_HEIGHT + 2 * cfg.HEX_HEIGHT))))
    cfg.win.update()




def buttonClick(event):
  print('buttonClick')
  #Buttons
  widget_name = event.widget._name
  if widget_name[0:3] == "btn":
    if event.state == 272:  #release click
      if widget_name == "btn1":
        deck.refill_deck(cfg.canvastop)
      elif widget_name == "btn2":
        deck.refill_deck(cfg.canvasbottom)
      elif widget_name == "btnConf":
        print("Confirm clicked ")
        global TRYING
        TRYING = False
        print("TRYING = " + str(TRYING))
        status=deck.process_move()
        print("deck.process_move successful:" + str(status))
        TRYING = True
        print("TRYING = " + str(TRYING))
        #disable the reset button
        btnReset.configure(state="disabled")
      elif widget_name == "btnReset":
        print("Reset!")
        deck.reset()
    return
