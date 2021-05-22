import tkinter as tk
import tkinter.messagebox
import os

from functools import partial
from math import isnan
from tkinter import font, Canvas, StringVar
from PIL import Image, ImageTk
from utils import config_widget


class ControlWindow:
    def __init__(self, master):
        self.widgets = {}
        self.label_font = font.Font(font=('Lucida Sans', 13, 'normal'))
        self.widget_font = font.Font(font=('Lucida Sans', 12, 'normal'))
        for idx, name in enumerate(('category', 'amount', 'date', 'description', 'subcategory')):
            state = 'disabled' if idx else 'normal'
            label = tk.Label(master, text=name.capitalize() + ':', font=self.label_font, bg='#e2ddec', relief='flat',
                             state=state)
            label.pack(side=tk.LEFT, fill='both', expand=True)
            var = StringVar()
            widget = tk.Entry(master, textvariable=var, relief='groove', highlightthickness=0,
                              width=14, font=self.widget_font, state=state)
            widget.pack(side=tk.LEFT, fill='both', expand=True)
            widget.bind('<FocusOut>', partial(self._remove_focus, name))
            widget.bind('<Button-1>', partial(self._set_focus, name))
            self.widgets[name] = {'widget': widget, 'label': label, 'var': var}

    def validate(self, name):
        value = self.widgets[name]['var'].get()
        value = ' '.join(value.split())
        self.widgets[name]['var'].set(value)
        if name in ('category', 'date', 'description', 'subcategory'):
            return str.isprintable(value) and (name != 'category' or len(value))
        elif name == 'amount':
            try:
                value = float(value)
            except ValueError:
                return False
            return not isnan(value)
        else:
            raise KeyError

    def validate_error(self, name, message=None):
        widget = self.widgets[name]['widget']
        widget.focus_set()
        widget.update()
        widget.focus_set()
        widget.config(highlightthickness=3)
        widget.config(highlightcolor='#3e3362')
        widget.update()
        if message:
            tk.messagebox.showwarning('Error', message, parent=widget)

    def _set_focus(self, name, *args):
        widget = self.widgets[name]['widget']
        widget.focus_set()
        widget.update()

    def _remove_focus(self, name, *args):
        widget = self.widgets[name]['widget']
        widget.config(highlightthickness=0)
        widget.master.focus_set()

    def validate_success(self, name):
        self._remove_focus(name)
        var = self.widgets[name]['var']
        value = var.get()
        var.set('')
        return value if name != 'amount' else float(value)

    def get(self, name):
        return self.widgets[name]['var'].get()

    def set_state(self, state):
        for name in self.widgets:
            for widget_name, widget in self.widgets[name].items():
                if widget_name != 'var':
                    widget.config(state=state)
                    widget.config(state=state)


class CategoryWindow:
    def __init__(self, master, grid_shape):
        self.grid_shape = grid_shape
        self.last_pos = (0, 0)
        self.create_image = Image.open(os.path.join('images', 'create_button.png'))
        self.button_image = Image.open(os.path.join('images', 'category_window.png'))
        self.buttons = {}
        for ypos in range(self.grid_shape[0]):
            for xpos in range(self.grid_shape[1]):
                button = Button(master, self.button_image, (ypos, xpos), state='hidden')
                if not xpos and not ypos:
                    button.widget.bind("<Configure>", self._resize_button_callback)
                self.buttons[(ypos, xpos)] = button
        self.create_button = Button(master, self.create_image, (0, 0))
        self.create_button.widget.bind("<Configure>", self._resize_create_callback)

    def show_category(self, text):
        button = self.buttons[self.last_pos]
        button.set_state('normal')
        button.change_text(text)
        self._change_last_pos()
        self.create_button.change_position(self.last_pos)

    def bind(self, name, callback):
        for ypos in range(self.grid_shape[0]):
            for xpos in range(self.grid_shape[1]):
                button = self.buttons[(ypos, xpos)]
                button.widget.bind(name, callback(button))

    def _change_last_pos(self, increase=True):
        last_pos = list(self.last_pos)
        if increase:
            last_pos[0] += (last_pos[1] == self.grid_shape[1] - 1)
            last_pos[1] = (last_pos[1] + 1) % self.grid_shape[1]
        self.last_pos = tuple(last_pos)

    def _resize_create_callback(self, event):
        event.width = event.height
        image = self.create_image.resize((event.width, event.height))
        self._resize_image(self.create_button, image, (event.width, event.height))

    def _resize_button_callback(self, event):
        image = self.button_image.resize((event.width, event.height))
        for ypos in range(self.grid_shape[0]):
            for xpos in range(self.grid_shape[1]):
                button = self.buttons[(ypos, xpos)]
                self._resize_image(button, image, (event.width, event.height))

    @staticmethod
    def _resize_image(button, image, shape):
        button.widget.config(width=shape[0], height=shape[1])
        button.tk_image = ImageTk.PhotoImage(image)
        button.widget.itemconfig(button.widget_image, image=button.tk_image)
        button.widget.coords(button.widget_text, shape[0] // 2, shape[1] // 2)


class InformationWindow:
    def __init__(self, master):
        self.label_font = font.Font(font=('Lucida Sans', 13, 'normal'))
        self.widget_font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.control_frame = tk.Frame(master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.information_frame = tk.Frame(master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.control_frame.grid(sticky=tk.NSEW, row=0, column=0)
        self.information_frame.grid(sticky=tk.NSEW, row=0, column=1)
        state = 'disabled'

        self.control_var = StringVar()
        self.control_label = tk.Label(self.control_frame, textvariable=self.control_var, font=self.label_font,
                                      bg='#e2ddec', relief='flat', state=state)
        self.control_label.grid(row=0, column=0)
        self.control_widgets = {}
        for i, (name, text) in enumerate(zip(('add', 'change', 'remove', 'delete'),
                                             ('Add field', 'Change field', 'Remove field', 'Detele Category'))):
            widget = tk.Button(self.control_frame, text=text, font=self.label_font, highlightbackground='#e2ddec',
                               relief='solid', width=10, state=state)
            widget.grid(row=i+1, column=0)
            self.control_widgets[name] = {'widget': widget}

        self.list_widgets = {}
        for i, name in enumerate(('amount', 'date', 'description', 'subcategory')):
            label = tk.Label(self.information_frame, text=name.capitalize(), font=self.label_font, bg='#e2ddec',
                             relief='flat', state=state)
            label.grid(row=0, column=i)
            widget = tk.Listbox(self.information_frame,  relief='solid', highlightthickness=0, bg='#f0f4f9',
                                font=self.widget_font, width=25, height=5, state=state)
            widget.grid(row=1, column=i, padx=5, pady=5)
            self.list_widgets[name] = {'widget': widget, 'label': label, 'length': 0}

        config_widget(master)
        config_widget(self.control_frame)
        config_widget(self.information_frame)

    def update_list(self, fields, delete_list=False):
        if isinstance(fields, dict):
            fields = [fields]
        for name in self.list_widgets:
            widget = self.list_widgets[name]
            if delete_list:
                widget['widget'].delete(0, tk.END)
                widget['length'] = 0
            for idx, field in enumerate(fields, start=widget['length']):
                widget['widget'].insert(tk.END, f'{idx}: {field[name]}')
            widget['length'] += len(fields)

    def bind(self, button_name, bind_name, callback):
        self.control_widgets[button_name]['widget'].bind(bind_name, callback)

    def set_state(self, state):
        for widgets in (self.list_widgets, self.control_widgets):
            for name in widgets:
                for widget_name, widget in widgets[name].items():
                    if widget_name != 'length':
                        widget.config(state=state)
                        widget.config(state=state)


class Category:
    def __init__(self, position):
        self.position = position
        self.fields = []

    def create_field(self, amount, date, description, subcategory):
        self.fields.append({'amount': amount, 'date': date, 'description': description, 'subcategory': subcategory})

    def _modify_field(self, index, amount=None, date=None, description=None, subcategory=None):
        if index >= len(self.fields):
            return
        for key, value in zip(('amount',  'date', 'description', 'subcategory'),
                              (amount, description, date, subcategory)):
            if value is not None:
                self.fields[index][key] = value


class Button:
    def __init__(self, master, image, position, state='normal', text=None):
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
        self.widget.itemconfig(self.widget_text, text=text)

    def set_state(self, state):
        self.widget.itemconfig(self.widget_image, state=state)
        self.widget.itemconfig(self.widget_text, state=state)
