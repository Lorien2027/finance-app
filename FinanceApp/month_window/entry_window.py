"""Month entry window."""
import tkinter as tk
import tkinter.messagebox

from functools import partial
from math import isnan
from tkinter import font, StringVar


class EntryWindow:
    """
    A window for entering information about categories.

    :param master: master window
    :type master: tkinter.Frame
    """

    def __init__(self, master):
        """Create month entry window."""
        self.widgets = {}
        self.label_font = font.Font(font=('Lucida Sans', 13, 'normal'))
        self.widget_font = font.Font(font=('Lucida Sans', 12, 'normal'))
        for name, text in zip(('category', 'amount', 'date', 'description', 'subcategory'),
                              (_('category'), _('amount'), _('date'), _('description'), _('subcategory'))):
            state = 'disabled' if name != 'category' else 'normal'
            label = tk.Label(master, text=text.capitalize() + ':', font=self.label_font, bg='#e2ddec', relief='flat',
                             state=state)
            label.pack(side=tk.LEFT, fill='both', expand=True)
            var = StringVar()
            widget = tk.Entry(master, textvariable=var, relief='groove', highlightthickness=3, highlightcolor='#e2ddec',
                              width=14, font=self.widget_font, state=state)
            widget.pack(side=tk.LEFT, fill='both', expand=True)
            widget.bind('<FocusOut>', partial(self._remove_focus, name))
            widget.bind('<Button-1>', partial(self._set_focus, name))
            self.widgets[name] = {'widget': widget, 'label': label, 'var': var}

    def validate(self, name):
        """
        Validate input by field name.

        :param name: field name
        :type name: str
        :return: validation successful or not
        :rtype: bool
        """
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

    def validate_success(self, name):
        """
        Get the value of the field when the input is successfully validated.

        :param name: field name
        :type name: str
        :return: field value
        :rtype: str
        """
        self._remove_focus(name)
        var = self.widgets[name]['var']
        value = var.get()
        var.set('')
        return value if name != 'amount' else float(value)

    def validate_error(self, name, message=None):
        """
        Display an error message when the input validation fails.

        :param name: field name
        :type name: str
        :param message: error message
        :type message: str
        """
        widget = self.widgets[name]['widget']
        self._set_focus(name)
        if message:
            tk.messagebox.showwarning('Error', message, parent=widget)
        self._set_focus(name)
        widget.config(highlightthickness=3)
        widget.config(highlightcolor='#3e3362')

    def _set_focus(self, name, *args):
        """
        Set the focus on the field.

        :param name: field name
        :type name: str
        """
        widget = self.widgets[name]['widget']
        widget.focus_set()
        widget.update()

    def remove_window_focus(self):
        """Remove focus from the window."""
        for name in self.widgets:
            self._remove_focus(name)

    def _remove_focus(self, name, *args):
        """
        Set the focus from the field.

        :param name: field name
        :type name: str
        """
        widget = self.widgets[name]['widget']
        widget.config(highlightthickness=3)
        widget.config(highlightcolor='#e2ddec')
        widget.master.focus_set()
        widget.update()

    def set_state(self, state):
        """
        Set the window visibility mode.

        :param state: window visibility mode
        :type state: str
        """
        for name in self.widgets:
            if name == 'category':
                continue
            for widget_name, widget in self.widgets[name].items():
                if widget_name != 'var':
                    widget.config(state=state)
