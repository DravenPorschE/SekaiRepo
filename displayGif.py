from tkinter import *
from PIL import Image, ImageTk

root = Tk()

# Load the GIF using PIL
image = Image.open("animation.gif")

# Convert to PhotoImage for tkinter
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
label = Label(root, image=photo)
label.pack()

root.mainloop()