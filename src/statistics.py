import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import PIL

from utils import config_widget
from tkinter import font


class StatisticsWindow(tk.Toplevel):
    def __init__(self, categories, data_type='category', master=None):
        super().__init__(master=master)
        self.title('Stats')
        self.geometry('800x600')
        self.configure(bg='#e2ddec')
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.row_data = categories
        self.data_type = data_type
        self._create_widgets()
        config_widget(self)
        self._draw()

    def _create_widgets(self):
        self.canvas_1 = tk.Canvas(self, bd=0, highlightthickness=0, bg='#e2ddec')
        self.canvas_1.bind("<Configure>", self._resize_image)
        self.canvas_1.grid(sticky=tk.NSEW, row=0, column=0, padx=5, pady=5)
        config_widget(self.canvas_1)
        # self.canvas_2 = tk.Canvas(self, bd=0, highlightthickness=0, bg='#e2ddec')
        # self.canvas_2.bind("<Configure>", self._resize_image)
        # self.canvas_2.grid(sticky=tk.NSEW, row=0, column=1, padx=5, pady=5)
        # config_widget(self.canvas_2)
        self.draw_year_button = tk.Button(master=self, text='Show year statistics')
        self.draw_year_button.grid(sticky=tk.NS, row=1, column=0, padx=5, pady=5)

    def _draw(self):
        self._collect_data()
        self._draw_by_category()
        self._draw_by_date()

    def _collect_data(self):
        if self.data_type == 'month':
            self.data = []
            for category in self.row_data.categories:
                category_name = self.row_data.categories[category].name
                category_data = pd.DataFrame(self.row_data.categories[category].fields)
                category_data['category'] = category_name
                self.data.append(category_data)
            self.data = pd.concat(self.data, ignore_index=True)
            self.data_by_category = self.data.groupby(['category'])['amount'].sum().reset_index()
            self.data_by_date = self.data.groupby(['date'])['amount'].sum().reset_index()
        elif self.data_type == 'category':
            self.data = pd.DataFrame(self.row_data.fields)
            self.data_by_category = self.data.groupby(['subcategory'])['amount'].sum().reset_index()
            self.data_by_category.rename(columns={'subcategory': 'category'}, inplace=True)
            self.data_by_date = self.data.groupby(['date'])['amount'].sum().reset_index()
        else:
            raise AttributeError('unknown data type')

    def _draw_by_category(self):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111)
        sns.barplot(ax=ax, data=self.data_by_category, x='category', y='amount')
        fig.canvas.draw()

        self.category_img = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        self.tk_image = PIL.ImageTk.PhotoImage(self.category_img, master=self)
        self.widget_image = self.canvas_1.create_image(0, 0, image=self.tk_image, anchor='nw')
        plt.close()

    def _draw_by_date(self):
        if self.data_type == 'month':
            return
        elif self.data_type == 'category':
            return
        else:
            raise AttributeError('unknown data type')

    def _resize_image(self, event):
        self.canvas_1.config(width=event.width, height=event.height)
        # self.canvas_2.config(width=event.width, height=event.height)
        image = self.category_img.resize((event.width, event.height))
        self.tk_image = PIL.ImageTk.PhotoImage(image)
        self.canvas_1.itemconfig(self.widget_image, image=self.tk_image)
        # self.canvas_2.itemconfig(self.widget_image, image=self.tk_image)
