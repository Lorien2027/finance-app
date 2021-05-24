"""Base window of application."""
import tkinter as tk
import gettext
import locale
import platform

from tkinter import font
from group_storage import GroupStorage
from utils import config_widget

if platform.system() != 'Windows':
    locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
localedir = gettext.find('Months')
localedir = localedir if localedir is not None else '.'
gettext.install('Months', localedir, names=('ngettext', ))


class Application(tk.Frame):
    """
    Main window class.

    :param master: master window
    :param title: title of the application
    """

    def __init__(self, master=None, title='Application'):
        """Create main window of application with widgets."""
        super().__init__(master=master, relief='ridge', bg='white', takefocus=1)
        self.master.title(title)
        self.master.minsize(width=1000, height=600)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self._create_widgets()
        self.grid(sticky=tk.NSEW, row=0, column=0)
        config_widget(self.master)
        config_widget(self)

    def _create_widgets(self):
        """Create all basic widgets of the main window."""
        self.months_frame = tk.Frame(self, borderwidth=5, bg='#3e3362')
        self.months_frame.grid(sticky=tk.NSEW, row=0, column=0, columnspan=1)

        self.months_names = [_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'),
                             _('August'), _('September'), _('October'), _('November'), _('December')]

        self.months_buttons_list = []
        for i in range(12):
            month_button = tk.Button(self.months_frame, text=self.months_names[i], font=self.font, bg='#f0f4f9',
                                     relief='flat', height=2, width=12, border=5)
            month_button.grid(row=i, column=0, sticky=tk.NSEW, padx=3, pady=3)
            month_button.configure(command=lambda obj=month_button: None)
            self.months_buttons_list.append(month_button)

        self.groups_frame = tk.Frame(self, borderwidth=5, bg='#e2ddec')
        self.groups_frame.grid(sticky=tk.NSEW, row=0, column=1, columnspan=4)
        config_widget(self.months_frame)
        self.storage = GroupStorage(self.groups_frame)
        config_widget(self.groups_frame)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root, _('Finance management app'))
    app.mainloop()
