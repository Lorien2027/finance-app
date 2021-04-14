"""Base window of application"""
import tkinter as tk
from tkinter import font


class Application(tk.Frame):
    """Main window of application"""

    def __init__(self, master=None, title='Application'):
        """
        Initialize main window

        :param master: master window
        :param title: title of the application
        """
        super().__init__(master=master, relief='ridge', bg='white', takefocus=1)
        self.master.title(title)
        self.master.minsize(width=1000, height=600)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))

        self.create_widgets()

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.grid(sticky=tk.NSEW)

    def create_widgets(self):
        """
        Create all basic widgets of the main window

        :return: None
        """
        self.months_frame = tk.Frame(self, borderwidth=5, bg='#3e3362')
        self.months_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.months_buttons_list = []
        self.months_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                             'October', 'November', 'December']

        self.months_frame.columnconfigure(0, weight=1)
        for i in range(12):
            month_button = tk.Button(self.months_frame, text=self.months_names[i], font=self.font, bg='#f0f4f9',
                                  relief='flat', height=2, width=12, border=5)
            month_button.grid(row=i, column=0, sticky=tk.NSEW, padx=3, pady=3)
            month_button.configure(command=lambda obj=month_button: None)
            self.months_buttons_list.append(month_button)
            self.months_frame.rowconfigure(i, weight=1)

        self.groups_frame = tk.Frame(self, borderwidth=5, bg='#e2ddec')
        self.groups_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.groups_frame.rowconfigure(0, weight=1)
        self.groups_frame.columnconfigure(0, weight=1)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root, 'Finance management app')
    app.mainloop()
