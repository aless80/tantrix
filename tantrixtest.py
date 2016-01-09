#PIL.Image in tkinter
try: import Tkinter as tk # for Python2
except Err: import tkinter as tk # for Python3
import PIL.Image
import PIL.ImageTk

win=tk.Tk()
canvas=tk.Canvas(win, height=200, width=200)

PILimage = PIL.Image.open("tile01.png")

basewidth = 150
wpercent = (basewidth / float(PILimage.size[0]))
hsize = int((float(PILimage.size[1]) * float(wpercent)))
PILimage = PILimage.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

#make PhotImage of PIL.Image instance ..
photo = PIL.ImageTk.PhotoImage(PILimage)
#..put it on tk.Canvas
item4 = canvas.create_image(100, 80, image=photo)

canvas.pack(side = tk.TOP, expand=True, fill=tk.BOTH)
win.mainloop()
"""
Hello,
I am trying to in Python 2. If you run the code below it will show two images. 

First I create a blue background with image.png pasted on it. The line bkg.show() displays it.

Then I want to paste it on a canvas of the tkinter's package. To do this, I to convert bkg to an instance 'photo' of PIL's Image.PhotoImage, and then I paste the photo on the canvas. 

However, image.png is lost. What I am doing wrong? 

Thanks

    import PIL.Image, PIL.ImageTk
    import Tkinter as tk
    
    bkg = PIL.Image.new('RGB', (750, 750), 'blue')
    tile = PIL.Image.open("image.png")
    bkg.paste(tile,(0,0))
    bkg.show()
    
    win=tk.Tk()
    photo = PIL.ImageTk.PhotoImage(bkg)
    
    canvas=tk.Canvas(win, height=800, width=800)
    canvas.create_image(0, 0, image=photo)
    canvas.pack()
    win.mainloop()
"""