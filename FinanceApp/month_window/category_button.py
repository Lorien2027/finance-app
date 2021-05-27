"""Month category data."""
import tkinter as tk

from tkinter import font, Canvas
from PIL import ImageTk
from FinanceApp.utils import config_widget


class CategoryButton:
    """
    A category button container with a background image and a category name.

    :param master: master window
    :type master: tkinter.Frame
    :param image: background image
    :type image: PIL.Image.Image
    :param position: coordinates of the button in the category grid
    :type position: Tuple[int, int]
    :param state: button visibility mode
    :type state: str
    """

    def __init__(self, master, image, position, state='normal'):
        """Create category button of month window."""
        self.text = None
        self.font = font.Font(font=('Lucida Sans', 22, 'normal'))
        self.position = tuple(position)
        self.tk_image = ImageTk.PhotoImage(image, master=master)
        self.widget = Canvas(master, width=60, height=60, bd=0, highlightthickness=0, bg='#e2ddec')
        self.widget_image = self.widget.create_image(0, 0, image=self.tk_image, anchor='nw', state=state)
        self.widget_text = self.widget.create_text(30, 30, font=self.font, text=self.text, state=state,
                                                   justify=tk.CENTER)
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=25, pady=25)
        config_widget(self.widget)

    def change_position(self, position):
        """
        Сhange the button position in the category grid.

        :param position: new button position
        :type position: Tuple[int, int]
        """
        self.position = tuple(position)
        self.widget.grid(row=position[0], column=position[1], sticky=tk.NSEW, padx=20, pady=20)
        config_widget(self.widget)

    def set_text(self, text):
        """
        Set the button text.

        :param text: button text
        :type text: str
        """
        self.text = text
        self.widget.itemconfig(self.widget_text, text=text)

    def set_state(self, state):
        """
        Set the button visibility.

        :param state: button visibility mode
        :type state: str
        """
        self.widget.itemconfig(self.widget_image, state=state)
        self.widget.itemconfig(self.widget_text, state=state)


class Category:
    """
    Category data.

    :param position: coordinates of the button in the category grid
    :type position: Tuple[int, int]
    :param name: category name
    :type name: str
    """

    def __init__(self, position, name):
        """Create a category data container."""
        self.position = position
        self.name = name
        self.fields = []

    def add_field(self, amount, date, description, subcategory):
        """
        Add a category data field.

        :param amount: amount of expenses
        :type amount: float
        :param date: date of expenses
        :type date: str
        :param description: description of expenses
        :type description: str
        :param subcategory: subcategory of expenses
        :type subcategory: str
        """
        self.fields.append({'amount': amount, 'date': date, 'description': description, 'subcategory': subcategory})

    def delete_field(self, index):
        """
        Delete the category data field.

        :param index: index of the data field to delete
        :type index: int
        """
        del self.fields[index]

    def change_field(self, index, amount=None, date=None, description=None, subcategory=None):
        """
        Change the category data field.

        :param index: index of the data field to change
        :type index: int
        :param amount: amount of expenses
        :type amount: float
        :param date: date of expenses
        :type date: str
        :param description: description of expenses
        :type description: str
        :param subcategory: subcategory of expenses
        :type subcategory: str
        """
        if index >= len(self.fields):
            return
        for key, value in zip(('amount',  'date', 'description', 'subcategory'),
                              (amount, date, description, subcategory)):
            if value is not None:
                self.fields[index][key] = value
