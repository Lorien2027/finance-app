import tkinter as tk
from tkinter import font
from category import Category, ControlWindow, CategoryWindow, InformationWindow


class GroupStorage(tk.Frame):
    def __init__(self, master=None, grid_shape=(6, 4)):
        super().__init__(master=master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.grid_shape = grid_shape
        self.categories = {}
        self.control_frame = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self.category_frame = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self.information_frame = tk.Frame(self, relief='ridge', bg='#e2ddec', takefocus=1)
        self._create_widgets()

        self.grid(sticky=tk.NSEW, row=0, column=0)
        self.control_frame.grid(sticky=tk.NSEW, row=0, column=0)
        self.category_frame.grid(sticky=tk.NSEW, row=1, column=0, rowspan=grid_shape[0])
        self.information_frame.grid(sticky=tk.NSEW, row=5, column=0)

        for i in range(3):
            self.rowconfigure(i, weight=1)
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
        self.category_window.bind('<Button-1>', self._set_active)

    def _set_active(self, button):
        def config(event):
            self.information_window.bind('add', '<Button-1>', self._update_category(button.position))
            self.information_window.update_list(self.categories[button.position].fields, delete_list=True)
        return config

    def _update_category(self, button_id):
        def update(event):
            text = {}
            for name in ('amount', 'date', 'description', 'subcategory'):
                if not self.control_window.validate(name):
                    self.control_window.validate_error(name, message=f'Invalid {name} field')
                    return
                text[name] = self.control_window.validate_success(name)
            self.categories[button_id].create_field(**text)
            self.information_window.update_list(text)
        return update

    def _create_category(self, event):
        if not self.control_window.validate('category'):
            self.control_window.validate_error('category', message='Invalid category name')
            return
        text = self.control_window.validate_success('category')
        last_pos = self.category_window.last_pos
        category = Category(last_pos)
        self.categories[last_pos] = category
        self.category_window.show_category(text)
        self.control_window.set_state('normal')
        self.information_window.set_state('normal')
        self.information_window.bind('add', '<Button-1>', self._update_category(last_pos))
        self.update_idletasks()
        self.update()
