import tkinter as tk

from tkinter import font
from utils import config_widget


class InformationWindow:
    def __init__(self, master):
        self.label_font = font.Font(font=('Lucida Sans', 13, 'normal'))
        self.widget_font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.control_frame = tk.Frame(master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.information_frame = tk.Frame(master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.control_frame.grid(sticky=tk.NSEW, row=0, column=0)
        self.information_frame.grid(sticky=tk.NSEW, row=0, column=1)
        state = 'disabled'

        self.control_var = tk.StringVar()
        self.control_label = tk.Label(self.control_frame, textvariable=self.control_var, font=self.label_font,
                                      bg='#e2ddec', relief='flat', state=state)
        self.control_label.grid(row=0, column=0)
        self.control_widgets = {}
        for i, (name, text) in enumerate(zip(('add', 'remove', 'change', 'delete'),
                                             ('Add field', 'Remove field', 'Change field', 'Delete category'))):
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
                                font=self.widget_font, width=25, height=5, state=state, selectmode=tk.BROWSE,
                                exportselection=False)
            widget.grid(row=1, column=i, padx=5, pady=5)
            widget.bind("<<ListboxSelect>>", self._select_row)
            self.list_widgets[name] = {'widget': widget, 'label': label, 'length': 0}

        config_widget(master)
        config_widget(self.control_frame)
        config_widget(self.information_frame)

    def _select_row(self, event):
        selection = event.widget.curselection()
        if selection:
            for name in self.list_widgets:
                widget = self.list_widgets[name]['widget']
                index = widget.curselection()
                if not index or index != selection[0]:
                    self.list_widgets[name]['widget'].select_clear(0, 'end')
                    self.list_widgets[name]['widget'].select_set(selection[0])

    def get_selected_index(self):
        for name in self.list_widgets:
            widget = self.list_widgets[name]['widget']
            selection = widget.curselection()
            if not selection:
                return None
            else:
                return selection[0]

    def change_index_field(self, index, field):
        for name in self.list_widgets:
            widget = self.list_widgets[name]['widget']
            widget.delete(index)
            widget.insert(index, f'{index}: {field[name]}')

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

    def unbind(self, button_name, bind_name):
        self.control_widgets[button_name]['widget'].unbind(bind_name)

    def set_state(self, state):
        for widgets in (self.list_widgets, self.control_widgets):
            for name in widgets:
                for widget_name, widget in widgets[name].items():
                    if widget_name != 'length':
                        widget.config(state=state)
