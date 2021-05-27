import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import PIL

from utils import config_widget
from tkinter import font

sns.set(font='Times New Roman', font_scale=2)
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})


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
        self.canvas_2 = tk.Canvas(self, bd=0, highlightthickness=0, bg='#e2ddec')
        self.canvas_2.bind("<Configure>", self._resize_image)
        self.canvas_2.grid(sticky=tk.NSEW, row=0, column=1, padx=5, pady=5)
        config_widget(self.canvas_2)
        self.draw_year_button = tk.Button(master=self, text=_('Show year statistics'))
        self.draw_year_button.grid(sticky=tk.NS, row=1, column=0, padx=5, pady=5)

    def _draw(self):
        self._collect_data()
        self._draw_by_category()
        self._draw_by_date()

    def _collect_data(self):
        columns = {
            'category': _('category'),
            'date': _('date'),
            'amount': _('amount')
        }
        self.columns = columns
        if self.data_type == 'month':
            self.data = []
            for category in self.row_data.categories:
                category_name = self.row_data.categories[category].name
                category_data = pd.DataFrame(self.row_data.categories[category].fields)
                category_data['category'] = category_name
                self.data.append(category_data)
            self.data = pd.concat(self.data, ignore_index=True)
            self.data.rename(columns=columns, inplace=True)
            self.data.replace({columns['date']: {'': 'unknown'}}, inplace=True)
            self.data_by_category = self.data.groupby([columns['category']])[columns['amount']].sum().reset_index()
            self.data_by_date = self.data.groupby([columns['date']])[columns['amount']].sum().reset_index()
        elif self.data_type == 'category':
            self.data = pd.DataFrame(self.row_data.fields).rename(columns={'subcategory': 'category'}, inplace=True)
            self.data.rename(columns=columns, inplace=True)
            self.data.replace({'date': {'': 'unknown'}}, inplace=True)
            self.data_by_category = self.data.groupby([columns['category']])[columns['amount']].sum().reset_index()
            self.data_by_date = self.data.groupby([columns['date']])[columns['amount']].sum().reset_index()
        else:
            raise AttributeError('unknown data type')

    def _draw_by_category(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        print(ax)
        sns.barplot(ax=ax, data=self.data_by_category, x=self.columns['category'], y=self.columns['amount'])
        self.show_values_on_bars(ax)
        plt.grid(alpha=0.35)
        fig.canvas.draw()

        self.category_img = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        self.category_tk_image = PIL.ImageTk.PhotoImage(self.category_img, master=self)
        self.widget_image_1 = self.canvas_1.create_image(0, 0, image=self.category_tk_image, anchor='nw')
        plt.close()

    def _draw_by_date(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        # ax = fig.add_subplot(111)
        sns.barplot(ax=ax, data=self.data_by_date, x=self.columns['date'], y=self.columns['amount'])
        self.show_values_on_bars(ax)
        plt.grid(alpha=0.35)
        fig.canvas.draw()

        self.date_img = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        self.date_tk_image = PIL.ImageTk.PhotoImage(self.date_img, master=self)
        self.widget_image_2 = self.canvas_2.create_image(0, 0, image=self.date_tk_image, anchor='nw')
        plt.close()

    def _resize_image(self, event):
        self.canvas_1.config(width=event.width, height=event.height)
        self.canvas_2.config(width=event.width, height=event.height)
        category_image = self.category_img.resize((event.width, event.height))
        date_image = self.date_img.resize((event.width, event.height))
        self.category_tk_image = PIL.ImageTk.PhotoImage(category_image)
        self.date_tk_image = PIL.ImageTk.PhotoImage(date_image)
        self.canvas_1.itemconfig(self.widget_image_1, image=self.category_tk_image)
        self.canvas_2.itemconfig(self.widget_image_2, image=self.date_tk_image)

    @staticmethod
    def show_values_on_bars(ax):
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + p.get_height()
            value = '{:.2f}'.format(p.get_height())
            ax.text(_x, _y, value, ha="center")
