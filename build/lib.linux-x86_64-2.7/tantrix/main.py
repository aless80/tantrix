import tantrix as tx

def main(object):
  print("inside main")
  global win, canvas, hexagon_generator, canvastop, canvasbottom, board, deck
  board=tx.Board()
  #board.createBoard()
  #Deal deck
  deck=tx.Deck()
  hand1 = tx.Hand(tx.canvastop)
  hand2 = tx.Hand(tx.canvasbottom)
  #Put deck on board
  deck.deal(1, 0, tx.canvas)
  deck.deal(2, 0, tx.canvas)
  #Check for duplicates. It should never happen
  dupl = set([x for x in tx.deck.dealt if tx.deck.dealt.count(x) > 1])
  if len(dupl)>0:
    raise UserWarning("Duplicates in deck.dealt!!!")
  #Bindings
  #win.bind('<Motion>', clickCallback)
  canvas.bind('<ButtonPress-1>', tx.clickCallback) #type 4   <Double-Button-1>?
  canvastop.bind('<ButtonPress-1>', tx.clickCallback) #type 4
  canvasbottom.bind('<ButtonPress-1>', tx.clickCallback) #type 4
  canvas.bind('<B1-Motion>', tx.clickCallback) #drag
  canvastop.bind('<B1-Motion>', tx.clickCallback) #drag
  canvasbottom.bind('<B1-Motion>', tx.clickCallback) #drag
  canvas.bind('<ButtonRelease-1>', tx.clickCallback) #release
  canvastop.bind('<ButtonRelease-1>', tx.clickCallback) #release
  canvasbottom.bind('<ButtonRelease-1>', tx.clickCallback) #release
  canvas.bind('<ButtonPress-3>', tx.clickB3Callback)
  #canvas.bind('<Return>', clickCallback)
  #canvas.bind('<Key>', clickCallback)
  #canvas.bind('<MouseWheel>', wheel)
  tx.win.mainloop()

print("main.py")
print(__name__)
if __name__ == "__main__":
  main()
