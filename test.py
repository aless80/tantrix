import Tkinter as tk # for Python2
import PIL.Image, PIL.ImageTk

win = tk.Tk()
canvas = tk.Canvas(win, height = 500, width = 500)

#Create a rectangle with stipples on top of the images
rectangle = canvas.create_rectangle(0, 0, 400, 300, fill = "gray", stipple = "gray12")

#Create two images
SPRITE = PIL.Image.open("image.jpg")
imagePIL = SPRITE.resize((100, 100))
imagePI = PIL.ImageTk.PhotoImage(imagePIL)
image1 = canvas.create_image(100, 100, image = imagePI, tags = "image")
image2 = canvas.create_image(200, 200, image = imagePI, tags = "image")
images = [image1, image2]

def getImage(x, y):
    for image in images:
        curr_x, curr_y = canvas.coords(image)
        x1 = curr_x - imagePI.width()/2
        x2 = curr_x + imagePI.width()/2
        y1 = curr_y - imagePI.height()/2
        y2 = curr_y + imagePI.height()/2
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            return image
#Callback
# Here I select image1 or image2 depending on where I click, and
# drag them on the canvas. The problem is when I put the rectangle
# on top using tag_raise (see below).
def callback(event):
    id  = getImage(event.x, event.y)
    if id:
        canvas.coords(id, (event.x, event.y))

#Binding
canvas.bind("<B1-Motion>", callback)
#Place the rectangle on top of all
canvas.pack()

# This is the problem. I want to have the rectangle on top and be able to use the callback
canvas.tag_raise(rectangle)

canvas.mainloop()