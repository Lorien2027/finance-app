import tkinter as tk
import os
import time
from tkinter import font, Canvas
from PIL import Image, ImageTk
from category import Category, Button, ControlWindow


class GroupStorage(tk.Frame):
    def __init__(self, master=None, grid_shape=(12, 4)):
        super().__init__(master=master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.grid_shape = grid_shape
        self.last_pos = [1, 0]
        self.categories = []
        self.grid(sticky=tk.NSEW, row=0, column=0)

        self.control_window = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self.control_window.grid(sticky=tk.NSEW, row=0, column=0)
        self.main_window = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self.main_window.grid(sticky=tk.NSEW, row=1, column=0)
        self._create_widgets()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=64)
        self.columnconfigure(0, weight=1)

        for i in range(1):
            self.control_window.rowconfigure(i, weight=1)
        for i in range(4):
            self.control_window.columnconfigure(i, weight=1)

        for i in range(self.grid_shape[0]):
            self.main_window.rowconfigure(i, weight=1)
        for i in range(self.grid_shape[1]):
            self.main_window.columnconfigure(i, weight=1)



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
        self.create_button = Button(self.main_window, os.path.join('images', 'create_button.png'), self.last_pos)
        self.create_button.widget.bind("<Configure>", self._resize_callback(self.create_button, use_height=True))
        self.create_button.widget.tag_bind(self.create_button.widget_image, '<Button-1>', self._create_category)
        self.control_widget = ControlWindow(self.control_window)
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
            button.widget.itemconfig(button.widget_image, image=button.image)
        return resize

    def _create_category(self, event):
        if not self.control_widget.validate('category'):
            self.control_widget.validate_error('category', message='Invalid category name')
            return
        text = self.control_widget.validate_success('category')
        button = Button(self.main_window, os.path.join('images', 'category_window.png'), self.create_button.position,
                        text=text)
        button.widget.bind("<Configure>", self._resize_callback(button))
        self.create_button.change_position(self.last_pos)
        self._change_last_pos()
        category = Category(button=button)
        self.categories.append(category)
        time.sleep(0.05)
        self.update_idletasks()
        self.update()


