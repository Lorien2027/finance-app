import tkinter as tk

from tkinter import font, Canvas
from PIL import ImageTk
from utils import config_widget


class CategoryButton:
    def __init__(self, master, image, position, state='normal', text=None):
        self.text = text
        self.font = font.Font(font=('Lucida Sans', 22, 'normal'))
        self.position = tuple(position)
        self.tk_image = ImageTk.PhotoImage(image, master=master)
        self.widget = Canvas(master, width=60, height=60, bd=0, highlightthickness=0, bg='#e2ddec')
        self.widget_image = self.widget.create_image(0, 0, image=self.tk_image, anchor='nw', state=state)
        self.widget_text = self.widget.create_text(30, 30, font=self.font, text=text, state=state, justify=tk.CENTER)
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=25, pady=25)
        config_widget(self.widget)

    def change_position(self, position):
        self.position = tuple(position)
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=20, pady=20)
        config_widget(self.widget)

    def change_text(self, text):
        self.text = text
        self.widget.itemconfig(self.widget_text, text=text)

    def set_state(self, state):
        self.widget.itemconfig(self.widget_image, state=state)
        self.widget.itemconfig(self.widget_text, state=state)


class Category:
    def __init__(self, position, name):
        self.position = position
        self.name = name
        self.fields = []

    def create_field(self, amount, date, description, subcategory):
        self.fields.append({'amount': amount, 'date': date, 'description': description, 'subcategory': subcategory})

    def delete_field(self, index):
        del self.fields[index]

    def change_field(self, index, amount=None, date=None, description=None, subcategory=None):
        if index >= len(self.fields):
            return
        for key, value in zip(('amount',  'date', 'description', 'subcategory'),
                              (amount, date, description, subcategory)):
            if value is not None:
                self.fields[index][key] = value

