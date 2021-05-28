"""Module for plotting expenses statistics."""
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import PIL

from FinanceApp.utils import config_widget
from tkinter import font

sns.set(font='Times New Roman', font_scale=2)
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})


class StatisticsWindow(tk.Toplevel):
    """Main window for statistics. Different from main app window."""

    def __init__(self, raw_data, data_type='category', master=None):
        """
        Configures statistics window and draws basic plots.

        :param raw_data: data to plot
        :param data_type: type of data. Supports 'month' or 'category'.
        :param master: master
        """
        super().__init__(master=master)
        self.title('Stats')
        self.geometry('1000x550')
        self.configure(bg='#e2ddec')
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.raw_data = raw_data
        self.data_type = data_type
        self.widgets = {}
        self._create_widgets()
        config_widget(self)
        self._draw()

    def _create_widgets(self):
        """Create all widgets of statistic window."""

        for idx in range(2):
            self.widgets[idx] = {}
            self.widgets[idx]['canvas'] = (tk.Canvas(self, bd=0, highlightthickness=0, bg='#e2ddec'))
            self.widgets[idx]['canvas'].bind("<Configure>", self.resize_plot(idx))
            self.widgets[idx]['canvas'].grid(sticky=tk.NSEW, row=0, column=idx, padx=5, pady=5)
            config_widget(self.widgets[idx]['canvas'])

        # self.buttons_frame = tk.Frame(master=self, bg='#e2ddec')
        # self.buttons_frame.grid(row=1, column=0, columnspan=2)
        # config_widget(self.buttons_frame)
        self.draw_year_button = tk.Button(master=self, text=_('Show year statistics'))
        self.draw_year_button.grid(sticky=tk.NS, row=1, column=0, columnspan=2, padx=5, pady=5)

    def _draw(self):
        """Draw default statistics from data."""
        self._collect_data()
        self._draw_by_category()
        self._draw_by_date()

    def _collect_data(self):
        """Process gathered data for plot."""
        columns = {
            'category': _('category'),
            'date': _('date'),
            'amount': _('amount')
        }
        self.columns = columns
        if self.data_type == 'month':
            self.data = []
            for category in self.raw_data.categories:
                category_name = self.raw_data.categories[category].name
                category_data = pd.DataFrame(self.raw_data.categories[category].fields)
                category_data['category'] = category_name
                self.data.append(category_data)
            self.data = pd.concat(self.data, ignore_index=True)
            self.data.rename(columns=columns, inplace=True)
            self.data.replace({columns['date']: {'': 'unknown'}}, inplace=True)
            self.data_by_category = self.data.groupby([columns['category']])[columns['amount']].sum().reset_index()
            self.data_by_date = self.data.groupby([columns['date']])[columns['amount']].sum().reset_index()
        elif self.data_type == 'category':
            self.data = pd.DataFrame(self.raw_data.fields).rename(columns={'subcategory': 'category'}, inplace=True)
            self.data.rename(columns=columns, inplace=True)
            self.data.replace({'date': {'': 'unknown'}}, inplace=True)
            self.data_by_category = self.data.groupby([columns['category']])[columns['amount']].sum().reset_index()
            self.data_by_date = self.data.groupby([columns['date']])[columns['amount']].sum().reset_index()
        else:
            raise AttributeError('unknown data type')

    def _draw_by_category(self):
        """Draw barplot of expenses per category."""
        self.plot(0, self.data_by_category, x='category', y='amount')

    def _draw_by_date(self):
        """Draw barplot of expenses per date."""
        self.plot(1, self.data_by_date, x='date', y='amount')

    def plot(self, idx, data, x='date', y='amount'):
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(ax=ax, data=data, x=self.columns[x], y=self.columns[y])
        self.show_values_on_bars(ax)
        plt.grid(alpha=0.35)
        fig.canvas.draw()

        widget = self.widgets[idx]
        widget['img'] = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        widget['tk_img'] = PIL.ImageTk.PhotoImage(widget['img'], master=self)
        widget['widget_img'] = widget['canvas'].create_image(0, 0, image=widget['tk_img'], anchor='nw')
        plt.close()

    def resize_plot(self, canvas_id):
        """Resize callback for canvas widgets"""
        def _resize_image(event):
            widget = self.widgets[canvas_id]
            widget['canvas'].config(width=event.width, height=event.height)
            image = widget['img'].resize((event.width, event.height))
            widget['tk_img'] = PIL.ImageTk.PhotoImage(image)
            widget['canvas'].itemconfig(widget['widget_img'], image=widget['tk_img'])

        return _resize_image

    @staticmethod
    def show_values_on_bars(ax):
        """
        Add bar values as text on bars.

        :param ax: Axes object.
        """
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + p.get_height()
            value = '{:.2f}'.format(p.get_height())
            ax.text(_x, _y, value, ha="center")

    def validate(self, data):
        pass
