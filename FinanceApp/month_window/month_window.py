"""Month window of application."""
import tkinter as tk
import tkinter.messagebox

from tkinter import font

from FinanceApp.month_window import Category, EntryWindow, CategoryWindow, InformationWindow


class MonthWindow(tk.Frame):
    """
    A month window containing entry, information and category widgets.

    :param master: master window
    :type master: tkinter.Frame
    :param grid_shape: category grid size
    :type grid_shape: Tuple[int, int]
    """

    def __init__(self, master, grid_shape=(6, 4)):
        """Create a month window of application."""
        super().__init__(master=master, relief='ridge', bg='#e2ddec', takefocus=1)
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.grid_shape = grid_shape
        self.categories = {}
        self.active_category = None
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
        self.control_window = EntryWindow(self.control_frame)
        self.category_window = CategoryWindow(self.category_frame,  self.grid_shape)
        self.information_window = InformationWindow(self.information_frame)

        create_button = self.category_window.create_button
        create_button.widget.tag_bind(create_button.widget_image, '<Button-1>', self._create_category)

    def _set_active(self, button):
        """
        Set the active category on mouse click.

        :param button: button that was clicked
        :type button: month_window.category_button.CategoryButton
        :return: mouse click callback
        :rtype: function
        """
        def config(event):
            if self.active_category:
                self.category_window.buttons[self.active_category].set_active(active=False)
            self.active_category = button.position
            button.set_active()
            self._information_window_bind(button.position)
            self.information_window.update_list(self.categories[button.position].fields, delete_list=True)
        return config

    def _information_window_bind(self, button_id):
        """
        Bind the information window buttons to a category.

        :param button_id: category button id
        :type button_id: Tuple[int, int]
        """
        self.information_window.bind('add', '<Button-1>', self._update_category(button_id))
        self.information_window.bind('remove', '<Button-1>', self._remove_category_field(button_id))
        self.information_window.bind('change', '<Button-1>', self._change_category_field(button_id))
        self.information_window.bind('delete', '<Button-1>', self._delete_category)

    def _information_window_unbind(self):
        """Unbind the information window buttons."""
        for name in ('add', 'remove', 'change', 'delete'):
            self.information_window.unbind(name, '<Button-1>')

    def _change_category_field(self, button_id):
        """
        Change the category field using the button.

        :param button_id: category button id to change
        :type button_id: Tuple[int, int]
        :return: mouse click callback
        :rtype: function
        """
        def change(event):
            text = {}
            for name in ('amount', 'date', 'description', 'subcategory'):
                if not self.control_window.validate(name):
                    self.control_window.validate_error(name, message=f'Invalid {name} field')
                    return
                text[name] = self.control_window.validate_success(name)
            index = self.information_window.get_selected_index()
            if index is None:
                tk.messagebox.showwarning('Error', 'Field not selected', parent=self)
            else:
                category = self.categories[button_id]
                category.change_field(index, **text)
                self.information_window.change_index_field(index, category.fields[index])
        return change

    def _remove_category_field(self, button_id):
        """
        Remove the category field using the button.

        :param button_id: category button id to remove the field
        :type button_id: Tuple[int, int]
        :return: mouse click callback
        :rtype: function
        """
        def remove(event):
            self.control_window.remove_window_focus()
            index = self.information_window.get_selected_index()
            if index is None:
                tk.messagebox.showwarning('Error', 'Field not selected', parent=self)
            else:
                category = self.categories[button_id]
                category.delete_field(index)
                self.information_window.update_list(category.fields, delete_list=True)
        return remove

    def _update_category(self, button_id):
        """
        Update the category field using the button.

        :param button_id: category button id to update
        :type button_id: Tuple[int, int]
        :return: mouse click callback
        :rtype: function
        """
        def update(event):
            text = {}
            for name in ('amount', 'date', 'description', 'subcategory'):
                if not self.control_window.validate(name):
                    self.control_window.validate_error(name, message=f'Invalid {name} field')
                    return
                text[name] = self.control_window.validate_success(name)
            self.categories[button_id].add_field(**text)
            self.information_window.update_list(text)
        return update

    def _create_category(self, event):
        """
        Create the category field using the button.

        :param event: mouse click event
        :type event: tkinter.Event
        """
        if not self.control_window.validate('category'):
            self.control_window.validate_error('category', message='Invalid category name')
            return
        text = self.control_window.validate_success('category')
        last_pos = self.category_window.last_pos
        category = Category(last_pos, text)
        self.categories[last_pos] = category
        self.category_window.show_category(text)
        self.category_window.bind(last_pos, '<Button-1>', self._set_active)
        self.control_window.set_state('normal')
        self.information_window.set_state('normal')
        self._information_window_bind(last_pos)
        self.information_window.update_list([], delete_list=True)
        self.category_window.buttons[last_pos].widget.event_generate('<Button-1>')
        self.active_category = last_pos
        self.update_idletasks()
        self.update()

    def _delete_category(self, event):
        """
        Delete the category field using the button.

        :param event: mouse click event
        :type event: tkinter.Event
        """
        if not self.active_category:
            return
        del self.categories[self.active_category]
        self.information_window.update_list([], delete_list=True)
        if len(self.categories):
            self._information_window_bind((0, 0))
            new_categories = {}
            for button_id, category in self.categories.items():
                if (button_id[0] >= self.active_category[0] and button_id[1] >= self.active_category[1]
                        and (button_id[0] or button_id[1])):
                    button_id = list(button_id)
                    button_id[0] -= button_id[0] and not button_id[1]
                    button_id[1] = (button_id[1] - 1) % self.grid_shape[1]
                new_categories[tuple(button_id)] = category
            self.categories = new_categories
        else:
            self._information_window_unbind()
            self.control_window.set_state('disable')
            self.information_window.set_state('disable')
        create_button_bind = self.category_window.delete_category(self.active_category)
        if create_button_bind:
            create_button = self.category_window.create_button
            create_button.widget.tag_bind(create_button.widget_image, '<Button-1>', self._create_category)
        self.active_category = (0, 0)
        if self.category_window.buttons[self.active_category].get_state() == 'normal':
            self.category_window.buttons[self.active_category].widget.event_generate('<Button-1>')
