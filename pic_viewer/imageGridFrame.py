from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image, ImageFile
from pic_viewer import PicViewer

class ImageGridFrame:
    def __init__(self, master, content, img_size):
        self.master = master
        self.frame = Frame(self.master)
        self.frame.pack(expand=True, fill=BOTH)
        self.ptr = 0
        self.file_ptr = 0
        self.db = content
        self.img_buf = {}
        self.img_size = img_size
        self._init_grid()
        self.frame.bind_all("<MouseWheel>", self._on_mousewheel)
        self.frame.bind("<Configure>", self._init_grid)

    def _init_grid(self, event=None):
        self.ptr = 0
        self.master.update()
        self.width = self.frame.winfo_width()
        self.height = self.frame.winfo_height()
        print(self.width, self.height)
        self.x_count = self.width // self.img_size
        self.y_count = self.height // self.img_size
        print(self.x_count, self.y_count)
        self.btns = {}
        for each in self.frame.winfo_children():
            each.destroy()
        for x in range(self.x_count):
            for y in range(self.y_count):
                img = PhotoImage()
                btn = Button(self.frame, image=img, width=self.img_size, height=self.img_size)
                btn.grid(column=x, row=y)
                self.btns[(x, y)] = btn
        self.update_content()

    def _on_mousewheel(self, event):
        direction = int(-1*(event.delta/120))
        print(self.ptr)
        self.ptr = max(0, min(self.ptr + direction*self.x_count, len(self.db.filtered)))
        self.update_content()

    def set_idx(self, i):
        pic_viewer = PicViewer(self.master, 768, 600, self.db, 512, i)

    def update_button(self, j, i, img):
        x = j % self.x_count
        y = j // self.x_count
        btn = self.btns[(x, y)]
        btn.configure(image = img, command = lambda: self.set_idx(i))
        
    def disable_button(self, j):
        x = j % self.x_count
        y = j // self.x_count
        btn = self.btns[(x, y)]
        # print("disable button", x, y)
        btn.configure(image = PhotoImage(), command = lambda: None)

    def update_content(self):
        count = self.x_count * self.y_count

        for j, i in enumerate(range(self.ptr, self.ptr + count)):
            if i >= len(self.db.filtered):
                self.disable_button(j)
                continue
            key = self.db.filtered[i]
            if key in self.img_buf:
                # print("Image found in buffer")
                test = self.img_buf[key]
                self.update_button(j, i, test)
        
            else:
                height = self.img_size
                width = self.img_size
                image1 = Image.open(key)

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
                test = ImageTk.PhotoImage(image1)
                self.img_buf[key] = test
                self.update_button(j, i, test)
