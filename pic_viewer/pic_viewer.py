from doctest import master
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

class PicViewer:
    def __init__(self, master, width, height, db, img_size, ptr=0):
        master.update()
        self.root = Toplevel()
        # set window position
        # w = 678 # width for the Tk root
        # h = 542 # height for the Tk root
        self.width = width
        self.height = height
        
        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        # x = (ws/2) - (self.width/2)
        # y = (hs/2) - (self.height/2)
        x = master.winfo_x() + 36
        y = master.winfo_y() + 36

        # set the dimensions of the screen 
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        
        # init database
        self.db = db
        self.ptr = ptr
        
        # init image and description
        self.img_size = img_size

        self.img_panel = Label(self.root, image=PhotoImage(), width = self.img_size, height = self.img_size)
        self.img_panel.place(x=0, y=0)
        self.txt_panel = Text(self.root, wrap='word')
        self.txt_panel.place(x=self.img_size + 8, y=60, \
                        width=self.width - self.img_size - 16, height=self.height-60)

        self.btn_next = ttk.Button(self.root, text="Next", command=self.next_pic)
        self.btn_next.place(x=self.img_size + 8, y=0)
        self.btn_prev = ttk.Button(self.root, text="Prev", command=self.prev_pic)
        self.btn_prev.place(x=self.img_size + 8, y=30)

        self.load_image()

        def on_closing():
            self.safe_dscr()
            self.root.destroy()
                
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()
        
    def load_image(self):
        height = self.img_size
        width = self.img_size
        src = self.db.filtered[self.ptr]
        image1 = Image.open(src)

        # ratio = image1.width / image1.height
        ratio = image1.height / image1.width

        if ratio < 1:
            height = int(self.img_size * ratio)
            width = int(self.img_size)
        elif ratio > 1:
            ratio = 1 / ratio
            height = int(self.img_size)
            width = int(self.img_size * ratio)
        
        image1 = image1.resize((width, height), Image.Resampling.LANCZOS)
        print(image1.width, image1.height, ratio)
        test = ImageTk.PhotoImage(image1, master=self.root)
        self.img_panel.configure(image = test)
        self.img_panel.image = test
        self.txt_panel.delete(1.0, 'end')
        self.txt_panel.insert('end', self.db.db[self.db.filtered[self.ptr]])

    def safe_dscr(self):
        self.db.db[self.db.filtered[self.ptr]] = self.txt_panel.get(1.0, 'end')

    def next_pic(self):
        self.safe_dscr()
        if self.ptr < len(self.db.filtered)-1:
            self.ptr += 1
            self.load_image()

    def prev_pic(self):
        self.safe_dscr()
        if self.ptr > 0:
            self.ptr -= 1
            self.load_image()