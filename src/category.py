import tkinter as tk
import os
from tkinter import font, Canvas, StringVar
from PIL import Image, ImageTk


class Button:
    def __init__(self, master, filepath, position, text=None):
        self.font = font.Font(font=('Lucida Sans', 24, 'normal'))
        self.position = position.copy()
        self.original_image = Image.open(filepath)
        self.tk_image = ImageTk.PhotoImage(self.original_image, master=master)
        self.widget = Canvas(master, width=180, height=180, bd=0, highlightthickness=0, bg='#e2ddec')
        self.widget_image = self.widget.create_image(0, 0, image=self.tk_image, anchor="nw")
        self.widget_text = self.widget.create_text(30, 25, font=self.font, text=text, anchor="w")
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=20, pady=20)
        self._config_widget(self.widget)

    def change_position(self, position):
        self.position = position.copy()
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


class ControlWindow:
    def __init__(self, master):
        self.widgets = {}
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        for name, text in zip(('category', 'amount', 'desc', 'subcategory'),
                              ('Category:', 'Amount:', 'Description:', 'Subcategory')):
            label = tk.Label(master, text=text, font=self.font, bg='#e2ddec', relief='flat', highlightthickness=0)
            label.pack(side=tk.LEFT, fill="both")
            var = StringVar()
            widget = tk.Entry(master, textvariable=var, highlightthickness=0)
            widget.pack(side=tk.LEFT, fill="both")
            self.widgets[name] = {'widget': widget, 'label': label, 'var': var}


    def validate(self, name):
        value = self.widgets[name]['var'].get()
        if name == 'category':
            return str.isprintable(value) and len(value)

    def get(self, name):
        return self.widgets[name]['var'].get()

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
