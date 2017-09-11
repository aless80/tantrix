#from Tkinter import *

import argparse
p = argparse.ArgumentParser(description='Show a notification in tkinter.')
p.add_argument ('string', metavar = 'string', type = str, help = 'The message')
p.add_argument ('position', metavar = 'position', type = str, help = 'The position', default = "300x310+100+100")
args = p.parse_args()

print(args.string)
print(args.position)


import tkMessageBox

tkMessageBox.showwarning("Notification", args.string)