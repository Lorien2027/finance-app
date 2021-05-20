import tkinter as tk
import os
from tkinter import font, Canvas
from PIL import Image, ImageTk


class Button:
    def __init__(self, master, filepath, position):
        self.position = position.copy()
        self.original_image = Image.open(filepath)
        self.tk_image = ImageTk.PhotoImage(self.original_image, master=master)
        self.widget = Canvas(master, width=180, height=180, bd=0, highlightthickness=0, bg='#e2ddec')
        self.widget_image = self.widget.create_image(90, 90, image=self.tk_image)
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=20, pady=20)
        self._config_widget(self.widget)

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

    def change_positon(self, position):
        self.position = position.copy()
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=20, pady=20)
        self._config_widget(self.widget)


class Category:
    def __init__(self, button):
        self.button = button
        self.fields = []

    def create_field(self, amount, desc, subcategory):
        self.fields.append({'amount': amount, 'desc': desc, 'subcategory': subcategory})

    def _modify_field(self, index, amount=None, desc=None, subcategory=None):
        if index >= len(self.fields):
            return
        for key, value in zip(('amount', 'desc', 'subcategory'), (amount, desc, subcategory)):
            if value is not None:
                self.fields[index][key] = value
