"""Month information window."""
import tkinter as tk

from tkinter import font
from utils import config_widget


class InformationWindow:
    """
    A window for displaying and controlling a list of information about categories.

    :param master: master window
    :type master: tkinter.Frame
    """

    def __init__(self, master):
        """Create month information window."""
        self.label_font = font.Font(font=('Lucida Sans', 13, 'normal'))
        self.widget_font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.control_frame = tk.Frame(master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.information_frame = tk.Frame(master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.control_frame.grid(sticky=tk.NSEW, row=0, column=0)
        self.information_frame.grid(sticky=tk.NSEW, row=0, column=1)
        state = 'disabled'

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
        """
        Select a list row by mouse click.

        :param event: mouse click event
        :type event: tkinter.Event
        """
        selection = event.widget.curselection()
        if selection:
            for name in self.list_widgets:
                widget = self.list_widgets[name]['widget']
                index = widget.curselection()
                if not index or index != selection[0]:
                    self.list_widgets[name]['widget'].select_clear(0, 'end')
                    self.list_widgets[name]['widget'].select_set(selection[0])

    def get_selected_index(self):
        """
        Get the index of the selected row.

        :return: selected row index
        :rtype: int
        """
        for name in self.list_widgets:
            widget = self.list_widgets[name]['widget']
            selection = widget.curselection()
            if not selection:
                return None
            else:
                return selection[0]

    def change_index_field(self, index, field):
        """
        Change the list field by index.

        :param index: field index to change
        :type index: int
        :param field: field value
        :type field: Dict[str, float]
        """
        for name in self.list_widgets:
            widget = self.list_widgets[name]['widget']
            widget.delete(index)
            widget.insert(index, f'{index}: {field[name]}')

    def update_list(self, fields, delete_list=False):
        """
        Update the list with new fields.

        :param fields: fields to add
        :type fields: List
        :param delete_list: delete the list or not
        :type delete_list: bool
        """
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
        """
        Bind the callback function to the widget by name.

        :param button_name: category button name to bind
        :type button_name: str
        :param bind_name: event name
        :type bind_name: str
        :param callback: callback function
        :type callback: method
        """
        self.control_widgets[button_name]['widget'].bind(bind_name, callback)

    def unbind(self, button_name, bind_name):
        """
        Unbind the widget by name.

        :param button_name: category button name to unbind
        :type button_name: str
        :param bind_name: event name
        :type bind_name: str
        """
        self.control_widgets[button_name]['widget'].unbind(bind_name)

    def set_state(self, state):
        """
        Set the window visibility mode.

        :param state: window visibility mode
        :type state: str
        """
        for widgets in (self.list_widgets, self.control_widgets):
            for name in widgets:
                for widget_name, widget in widgets[name].items():
                    if widget_name != 'length':
                        widget.config(state=state)
