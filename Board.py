import math
import PIL.Image, PIL.ImageTk
try:
  import Tkinter as tk # for Python2
except:
  import tkinter as tk # for Python3
import HexagonGenerator as hg
from config import * #todo




def print_event(event, msg= ' '):
  print(msg)
  x, y = event.x, event.y
  hex = board.pixel_to_hex(x,y)
  cube = board.pixel_to_off(x, y)
  print('cube (if in canvasmain!) = ' + str(cube))
  print('hex = ' + str(hex))
  rowcolcanv=onClickRelease(event)
  neigh= deck.get_neighbors(rowcolcanv)
  print('neigh = ' + str(neigh))
  neighcolors = deck.get_neighboring_colors(rowcolcanv)
  print('neighcolors = ' + str(neighcolors))

def buttonClick(event):
  print('buttonClick')
  #Buttons
  if event.widget._name[0:3] == "btn":
    if event.state == 272:  #release click
      if event.widget._name == "btn1":
        deck.refill_deck(canvastop)
      elif event.widget._name == "btn2":
        deck.refill_deck(canvasbottom)
      elif event.widget._name == "btnConf":
        print("Confirmed! todo")
        pass
      elif event.widget._name == "btnTry":
        global TRYING
        TRYING = not TRYING
        clr={False:"grey", True:"cyan"}
        btnTry.configure(background = clr[TRYING])
        print('widget = ' + str(event.widget))
        print("TRYING = " + str(TRYING))
    return

def clickEmptyHexagon(event):
  print_event(event,' \nclickEmptyHexagon')

def clickB3Callback(event):
  print_event(event, ' \nclickB3Callback')

def clickCallback(event):
  print('\nclickCallback')
  global clicked_rowcolcanv
  x, y = event.x, event.y
  #logs
  if 0:
    print(' widget = ' + str(event.widget))
    print(' type = ' + str(event.type))
    print(' state = ' + str(event.state))
    print(' num = ' + str(event.num))
    print(' delta =' + str(event.delta))
    print('x, y = {}, {}'.format(x, y))
    print(" x_root, y_root = ",str((event.x_root, event.y_root)))
  #with this I change to the canvas' coordinates: x = canvas.canvasx(event.x)
  #print canvas.find_closest(x, y)
  #http://epydoc.sourceforge.net/stdlib/Tkinter.Event-class.html
  #NB: move while dragging is type=6 (clickCallback) state=272
  #NB: click                  type=4 (BPress) state=16
  #NB: release click          type=5 (BRelea) state=272
  #
  if event.type == '4' and event.state == 16: #click
    rowcolcanv=onClickRelease(event)
    ind = deck.get_index_from_rowcolcanv(rowcolcanv)
    if ind is None:
      clicked_rowcolcanv = None
      return
    clicked_rowcolcanv = rowcolcanv
    #wait ..
  elif event.type == '5' and event.state == 272: #release click
    #previously clicked on empty hexagon
    if clicked_rowcolcanv is None:
      clickEmptyHexagon(event)
      return
    rowcolcanv=onClickRelease(event)  #todo here I could use simpler onClickRelease
    print('rowcolcanv=      ' + str(rowcolcanv))
    print('clicked_rowcolcanv=' + str(clicked_rowcolcanv))
    if len(rowcolcanv) == 0:
      return
    if rowcolcanv == clicked_rowcolcanv: #released on same tile => rotate it
      #Rotate
      deck.rotate(rowcolcanv)
    elif rowcolcanv != clicked_rowcolcanv: #released elsewhere => drop tile there.
      #previously clicked on empty hexagon
      if clicked_rowcolcanv is None:
        return
      #move tile if place is not occupied already:
      canvas_origin, canvas_dest = win.children[clicked_rowcolcanv[2][1:]], win.children[rowcolcanv[2][1:]]
      deck.move(clicked_rowcolcanv[0],clicked_rowcolcanv[1],canvas_origin, rowcolcanv[0],rowcolcanv[1],canvas_dest)
    #Reset the coordinates of the canvas where the button down was pressed
    clicked_rowcolcanv=None
  else :
    print('\n !event not supported \n')
  print('')

def onClickRelease(event):
  x, y = event.x, event.y
  if x <= 0 or x >= event.widget.winfo_reqwidth():
    print('x outside the original widget')
    return tuple()
  elif x < event.widget.winfo_reqwidth():
    print('x is inside the original widget')
  else:
    print('cannot be determined where x is vs original widget')
    return tuple()
  #event.x and event.y
  ytop= canvastop.winfo_reqheight()
  ymain= ytop + canvasmain.winfo_reqheight()
  ybottom=ymain + canvasbottom.winfo_reqheight()
  if str(event.widget) == ".canvastop":
    yrel = y
  elif str(event.widget) == ".canvasmain":
    yrel = y + ytop
  elif str(event.widget) == ".canvasbottom":
    yrel = y + ymain
  else:
    return tuple()
    raise UserWarning("onClickRelease: cannot determine yrel")

  if yrel <= 0 or yrel >= ybottom:
    print('x outside the original widget')
    return tuple()
  elif yrel <= ytop:
    print('x inside canvastop')
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,y))
    rowcolcanv.append(".canvastop")
  elif yrel <= ymain:
    print('x inside canvas')
    rowcolcanv = list(board.pixel_to_off(x,yrel-ytop))
    rowcolcanv.append(".canvasmain")
  elif yrel <= ybottom:
    print('x inside canvasbottom')
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,yrel-ymain))
    rowcolcanv.append(".canvasbottom")
  else:
    raise UserWarning("onClickRelease: cannot destination canvas")
    return tuple()
  return rowcolcanv

def onClick2(event):
  #Find rowcolcanv ie offset and canvas
  x, y = event.x, event.y
  if str(event.widget) == ".canvasmain":
    print("board.pixel_to_off= " + str(board.pixel_to_off(x,y))) #wrong for canvastop, eg 1.3 becomes 1,4
    rowcolcanv = list(board.pixel_to_off(x,y))
  elif str(event.widget) == ".canvastop" or str(event.widget) == ".canvasbottom":
    print("board.pixel_to_off_canvastopbottom= " + str(board.pixel_to_off_canvastopbottom(x,y)))
    rowcolcanv = list(board.pixel_to_off_canvastopbottom(x,y))
  else:
    print('\n clickCallback did not find the canvas! event.widget is :')
    print(str(event.widget))
  rowcolcanv.append(str(event.widget))
  return rowcolcanv


def isrotation(s1, s2):
     return len(s1)==len(s2) and s1 in 2*s2

def isrot(src, dest):
  # Make sure they have the same size
  #if len(src) != len(dest):
  #  return False
  # Rotate through the letters in src
  for ix in range(len(src)):
    # Compare the end of src with the beginning of dest
    # and the beginning of src with the end of dest
    if dest.startswith(src[ix:]) and dest.endswith(src[:ix]):
      return True
  return False
