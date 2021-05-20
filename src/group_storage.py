import tkinter as tk
import os
from tkinter import font, Canvas
from PIL import Image, ImageTk
from category import Category, Button


class GroupStorage(tk.Frame):
    def __init__(self, master=None, grid_shape=(12, 4)):
        super().__init__(master=master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.grid_shape = grid_shape
        self.last_pos = [0, 0]
        self.categories = []
        self.grid(sticky=tk.NSEW, row=0, column=0)
        for i in range(self.grid_shape[0]):
            self.rowconfigure(i, weight=1)
        for i in range(self.grid_shape[1]):
            self.columnconfigure(i, weight=1)
        self._create_widgets()

    @staticmethod
    def _config_widget(widget):
        """
        Configure the columns and rows of the widget grid.

        :param widget: tk.Frame
        """
        for column in range(widget.grid_size()[0]):
            widget.columnconfigure(column, weight=1)
        for row in range(widget.grid_size()[1]):
            widget.rowconfigure(row, weight=1)

    def _create_widgets(self):
        """Create all basic widgets of the window."""
        self.create_button = Button(self, os.path.join('images', 'create_button.png'), self.last_pos)
        self.create_button.widget.bind("<Configure>", self._resize_callback(self.create_button, use_height=True))
        self.create_button.widget.tag_bind(self.create_button.widget_image, '<Button-1>', self._create_category)
        self._change_last_pos()

    def _change_last_pos(self, increase=True):
        if increase:
            self.last_pos[0] += (self.last_pos[1] == self.grid_shape[1] - 1)
            self.last_pos[1] = (self.last_pos[1] + 1) % self.grid_shape[1]

    def _resize_callback(self, button, use_height=False):
        def resize(event):
            height = event.height // self.grid_shape[0]
            if use_height:
                width = height
                event.width = event.height
            else:
                width = event.width // self.grid_shape[1]
            button.widget.config(width=width, height=height)

            button.image = ImageTk.PhotoImage(button.original_image.resize((event.width, event.height)))
            button.widget.coords(button.widget_image, event.width // 2, event.height // 2)
            button.widget.itemconfig(button.widget_image, image=button.image)
        return resize

    def _create_category(self, event):
        button = Button(self, os.path.join('images', 'category_window.png'), self.create_button.position)
        button.widget.bind("<Configure>", self._resize_callback(button))
        self.create_button.change_positon(self.last_pos)
        self._change_last_pos()
        category = Category(button=button)
        self.categories.append(category)



