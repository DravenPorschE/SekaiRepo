from tkinter import *
from PIL import Image, ImageTk

root = Tk()
# Set fixed screen size
screen_width = 480
screen_height = 320
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, False)
root.configure(bg="white")

# Load the GIF using PIL
image = Image.open("animation.gif")

# Convert to PhotoImage for tkinter
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
label = Label(root, image=photo)
label.pack()

root.mainloop()