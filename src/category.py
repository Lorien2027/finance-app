import tkinter as tk
import tkinter.messagebox
import os

from tkinter import font, Canvas, StringVar
from PIL import Image, ImageTk
from utils import config_widget


class ControlWindow:
    def __init__(self, master):
        self.widgets = {}
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        for name, text in zip(('category', 'amount', 'date', 'desc', 'subcategory'),
                              ('Category:', 'Amount:', 'Date:', 'Description:', 'Subcategory')):
            label = tk.Label(master, text=text, font=self.font, bg='#e2ddec', relief='flat')
            label.pack(side=tk.LEFT, fill='both', expand=True)
            var = StringVar()
            widget = tk.Entry(master, textvariable=var, relief='groove', highlightthickness=0,
                              width=10)
            widget.pack(side=tk.LEFT, fill='both', expand=True)
            self.widgets[name] = {'widget': widget, 'label': label, 'var': var}

    def validate(self, name):
        value = self.widgets[name]['var'].get()
        if name == 'category':
            return str.isprintable(value) and len(value.split())

    def validate_error(self, name, message=None):
        widget = self.widgets[name]['widget']
        widget.config(highlightthickness=3)
        widget.config(highlightcolor='#3e3362')
        widget.focus_set()
        widget.update()
        if message:
            tk.messagebox.showwarning('Error', message, parent=widget)

    def validate_success(self, name):
        widget = self.widgets[name]['widget']
        widget.config(highlightthickness=0)
        widget.master.focus_set()
        var = self.widgets[name]['var']
        value = var.get()
        var.set('')
        return value

    def get(self, name):
        return self.widgets[name]['var'].get()


class CategoryWindow:
    def __init__(self, master, grid_shape):
        self.grid_shape = grid_shape
        self.last_pos = [0, 0]
        self.create_image = Image.open(os.path.join('images', 'create_button.png'))
        self.button_image = Image.open(os.path.join('images', 'category_window.png'))

        self.create_button = Button(master, self.create_image, [0, 0])
        self.create_button.widget.bind("<Configure>", self._resize_create_callback)
        self.category_buttons = []
        for ypos in range(self.grid_shape[0]):
            buttons = []
            for xpos in range(self.grid_shape[1]):
                button = Button(master, self.button_image, [ypos, xpos])
                if not xpos and not ypos:
                    button.widget.bind("<Configure>", self._resize_button_callback)
                # button.widget.bind('<FocusOut>')
                # button.widget.bind('<FocusIn>')
                self._change_last_pos()
                buttons.append(button)
            self.category_buttons.append(buttons)

    def _show_category(self):
        pass

    def _change_last_pos(self, increase=True):
        if increase:
            self.last_pos[0] += (self.last_pos[1] == self.grid_shape[1] - 1)
            self.last_pos[1] = (self.last_pos[1] + 1) % self.grid_shape[1]

    def _resize_create_callback(self, event):
        event.width = event.height
        height = event.height // self.grid_shape[0]
        width = height
        image = self.create_image.resize((event.width, event.height))
        self._resize_image(self.create_button, image, (width, height))

    def _resize_button_callback(self, event):
        height = event.height // self.grid_shape[0]
        width = event.width // self.grid_shape[1]
        image = self.button_image.resize((event.width, event.height))
        for ypos in range(self.grid_shape[0]):
            for xpos in range(self.grid_shape[1]):
                button = self.category_buttons[ypos][xpos]
                self._resize_image(button, image, (width, height))

    @staticmethod
    def _resize_image(button, image, button_shape):
        button.widget.config(width=button_shape[0], height=button_shape[1])
        button.tk_image = ImageTk.PhotoImage(image)
        button.widget.itemconfig(button.widget_image, image=button.tk_image)


class InformationWindow:
    def __init__(self, master):
        self.widgets = {}
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        for name, text in zip(('amount', 'date', 'desc', 'subcategory'),
                              ('Amount:', 'Date:', 'Description:', 'Subcategory:')):
            widget = tk.Listbox(master,  relief='solid', highlightthickness=0, bg='#f0f4f9',
                                font=('Times', 14))
            widget.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
            self.widgets[name] = widget


class Category:
    def __init__(self, position):
        self.position = position
        self.fields = []

    def create_field(self, amount, desc, subcategory, date):
        self.fields.append({'amount': amount, 'date': date, 'subcategory': subcategory, 'desc': desc})

    def _modify_field(self, index, amount=None, date=None,  subcategory=None, desc=None):
        if index >= len(self.fields):
            return
        for key, value in zip(('amount',  'date', 'subcategory', 'desc'), (amount, date, desc, subcategory)):
            if value is not None:
                self.fields[index][key] = value


class Button:
    def __init__(self, master, image, position, text=None):
        self.font = font.Font(font=('Lucida Sans', 24, 'normal'))
        self.position = list(position.copy())
        self.tk_image = ImageTk.PhotoImage(image, master=master)
        self.widget = Canvas(master, width=60, height=60, bd=0, highlightthickness=0, bg='#e2ddec')
        self.widget_image = self.widget.create_image(0, 0, image=self.tk_image, anchor="nw")
        self.widget_text = self.widget.create_text(30, 25, font=self.font, text=text, anchor="w")
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=20, pady=20)
        config_widget(self.widget)

    def change_position(self, position):
        self.position = position.copy()
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=20, pady=20)
        config_widget(self.widget)

    def change_text(self, text):
        self.widget.itemconfig(self.widget_text, text=text)
