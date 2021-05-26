import os

from month_window import CategoryButton
from PIL import Image, ImageTk


class CategoryWindow:
    def __init__(self, master, grid_shape):
        self.grid_shape = grid_shape
        self.last_pos = (0, 0)
        self.button_names = []
        self.create_image = Image.open(os.path.join('images', 'create_button.png'))
        self.button_image = Image.open(os.path.join('images', 'category_window.png'))
        self.buttons = {}
        for ypos in range(self.grid_shape[0]):
            for xpos in range(self.grid_shape[1]):
                button = CategoryButton(master, self.button_image, (ypos, xpos), state='hidden')
                if not xpos and not ypos:
                    button.widget.bind("<Configure>", self._resize_button_callback)
                self.buttons[(ypos, xpos)] = button
        self.create_button = CategoryButton(master, self.create_image, (0, 0))
        self.create_button.widget.bind("<Configure>", self._resize_create_callback)

    def show_category(self, text):
        button = self.buttons[self.last_pos]
        self._change_last_pos()
        if self.last_pos[0] != self.grid_shape[0]:
            self.create_button.change_position(self.last_pos)
        else:
            self.create_button.widget.grid_forget()
            self.create_button.set_state('hidden')
            self.create_button.widget.tag_unbind(self.create_button.widget_image, '<Button-1>')
        button.change_text(text)
        self.button_names.append(text)
        button.set_state('normal')

    def delete_category(self, button_id):
        self._change_last_pos(increase=False)
        self.buttons[self.last_pos].set_state('hidden')
        self.buttons[self.last_pos].widget.unbind('<Button-1>')
        last_index = self.grid_shape[0] * button_id[0] + button_id[1]
        self.create_button.change_position(self.last_pos)
        for index, text in enumerate(self.button_names[last_index+1:], start=last_index):
            button = self.buttons[(index // self.grid_shape[0], index % self.grid_shape[1])]
            button.change_text(text)
        del self.button_names[last_index]
        if self.last_pos[0] == self.grid_shape[0] - 1 and self.last_pos[1] == self.grid_shape[1] - 1:
            self.create_button.set_state('normal')
            return True
        else:
            return False

    def bind(self, button_id, bind_name, callback):
        button = self.buttons[button_id]
        button.widget.bind(bind_name, callback(button))

    def tag_bind(self, button_id, bind_name, callback):
        button = self.buttons[button_id]
        button.widget.tag_bind(button.widget_image, bind_name, callback(button))

    def _change_last_pos(self, increase=True):
        last_pos = list(self.last_pos)
        if increase:
            last_pos[0] += (last_pos[1] == self.grid_shape[1] - 1)
            last_pos[1] = (last_pos[1] + 1) % self.grid_shape[1]
        elif last_pos[0] or last_pos[1]:
            last_pos[0] -= last_pos[0] and not last_pos[1]
            last_pos[1] = (last_pos[1] - 1) % self.grid_shape[1]
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