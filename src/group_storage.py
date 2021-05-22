import tkinter as tk
import time
from tkinter import font
from category import Category, ControlWindow, CategoryWindow, InformationWindow
from utils import config_widget


class GroupStorage(tk.Frame):
    def __init__(self, master=None, grid_shape=(6, 4)):
        super().__init__(master=master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.grid_shape = grid_shape
        self.categories = []
        self.control_frame = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self.category_frame = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self.information_frame = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self._create_widgets()

        self.grid(sticky=tk.NSEW, row=0, column=0)
        self.control_frame.grid(sticky=tk.NSEW, row=0, column=0)
        self.category_frame.grid(sticky=tk.NSEW, row=1, column=0)
        self.information_frame.grid(sticky=tk.NSEW, row=2, column=0)

        for i, weight in enumerate((1, 64, 1)):
            self.rowconfigure(i, weight=weight)
        self.columnconfigure(0, weight=1)

        for i in range(self.grid_shape[0]):
            self.category_frame.rowconfigure(i, weight=1)
        for i in range(self.grid_shape[1]):
            self.category_frame.columnconfigure(i, weight=1)

    def _create_widgets(self):
        """Create all basic widgets of the window."""
        self.control_window = ControlWindow(self.control_frame)
        self.category_window = CategoryWindow(self.category_frame,  self.grid_shape)
        self.information_window = InformationWindow(self.information_frame)

        create_button = self.category_window.create_button
        create_button.widget.tag_bind(create_button.widget_image, '<Button-1>', self._create_category)

    def _create_category(self, event):
        if not self.control_window.validate('category'):
            self.control_window.validate_error('category', message='Invalid category name')
            return
        text = self.control_window.validate_success('category')
        category = Category(self.category_window.last_pos)
        # self.category_window.show_category(text)
        self.categories.append(category)
        time.sleep(0.05)
        self.update_idletasks()
        self.update()





