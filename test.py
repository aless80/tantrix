import Tkinter as tk # for Python2
import PIL.Image, PIL.ImageTk

win = tk.Tk()
#Create a canvas
canvas = tk.Canvas(win, height = 500, width = 500)

#Create a rectangle on the right of the canvas
rect = canvas.create_rectangle(250, 0, 500, 250, width = 2, fill = "red")

#Create ovals
canvas.create_oval(200, 100, 300, 200, fill = "blue", tags = "mytag")
canvas.create_oval(100, 200, 300, 250, fill = "yellow", tags = "mytag")
#Place the canvas
canvas.pack()

#Raise the rectangle on the right of the canvas
canvas.tag_raise(rect)

#
def callback(event):
	print(event)

def callback2(event):
	print("callback2")
	print(event)

canvas.bind_class("mytag", "<B1-Motion>", callback)

canvas.bind("<B1-Motion>", callback2)
#new_tags = widg.bindtags() + ("mytag",)
#widg.bindtags(new_tags)

canvas.mainloop()
