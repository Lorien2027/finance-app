import tkinter as tk
import os
from tkinter import font, Canvas
from PIL import Image, ImageTk


class GroupStorage(tk.Frame):
    def __init__(self, master=None, grid_shape=(8, 8)):
        super().__init__(master=master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.grid_shape = grid_shape
        self.last_position = (0, 0)
        for i in range(self.grid_shape[0]):
            self.rowconfigure(i, weight=1)
        for i in range(self.grid_shape[1]):
            self.columnconfigure(i, weight=1)
        self._create_widgets()
        self.grid(sticky=tk.NSEW, row=0, column=0)

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
        self.original_image = Image.open(os.path.join('images', 'plus_button.png'))
        self.image = ImageTk.PhotoImage(self.original_image, master=self)

        self.plus_button = Canvas(self, width=180, height=180, bd=0, highlightthickness=0, bg='#e2ddec')
        self.plus_canvas_image = self.plus_button.create_image(90, 90, image=self.image)
        self.plus_button.grid(row=self.last_position[0], column=self.last_position[1], sticky=tk.NSEW,
                                     padx=20, pady=20)
        self.plus_button.bind("<Configure>", self._resize_callback)

        self._config_widget(self.plus_button)

    def _resize_callback(self, event):
        self.width = event.width // self.grid_shape[1]
        self.height = event.height // self.grid_shape[0]
        self.plus_button.config(width=self.width, height=self.height)

        self.image = ImageTk.PhotoImage(self.original_image.resize((event.width, event.height)))
        self.plus_button.coords(self.plus_canvas_image, event.width // 2, event.height // 2)
        self.plus_button.itemconfig(self.plus_canvas_image, image=self.image)



