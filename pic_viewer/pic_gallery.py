import os
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image, ImageFile
from imageGridFrame import ImageGridFrame
from data_base import DataBase

ImageFile.LOAD_TRUNCATED_IMAGES = True
        
database_src = "database.csv"

max_size = 128

root = Tk()
# set window position
w = 600 # width for the Tk root
h = 600 # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

# load database
db = DataBase(database_src)

class FilterPanel:
    def __init__(self, master, content, frame=None):
        self.filter_tags = StringVar()
        self.content = content
        self.filter_tags.trace('w', self._filter)
        self.frame = frame
        filter_ent = Entry(master, textvariable = self.filter_tags)
        filter_ent.pack(expand=False, fill=X)
        
    def _filter(self, *args):
        self.content.filter(self.filter_tags.get())
        if self.frame != None:
            self.frame._init_grid()

filter_panel = FilterPanel(root, db)
img_grid = ImageGridFrame(root, db, max_size)
filter_panel.frame = img_grid

root.mainloop()
