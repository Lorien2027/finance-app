"""Module for plotting expenses statistics."""
import tkinter as tk
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import PIL

from FinanceApp.utils import config_widget
from tkinter import font
matplotlib.use('agg')
sns.set(font='Times New Roman', font_scale=2)
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})


class StatisticsWindow(tk.Toplevel):
    """Main window for statistics. Different from main app window."""

    def __init__(self, raw_data, data_type='category', master=None):
        """
        Configure statistics window and draw basic plots.

        :param raw_data: data to plot
        :param data_type: type of data. Supports 'month' or 'category'.
        :param master: master
        """
        super().__init__(master=master)
        self.title('Stats')
        self.geometry('1200x600')
        self.configure(bg='#e2ddec')
        self.font = font.Font(font=('Lucida Sans', 12, 'normal'))
        self.raw_data = raw_data
        self.data_type = data_type
        self.is_valid = self.validate_data()
        self.plot_changed = False
        self.widgets = {}
        self.titles = {
            'date': _('Expenses by date'),
            'category': _('Expenses by category'),
            'month': _('Expenses by month')
        }
        self._create_widgets()
        self._collect_data()
        self._draw()
        if not self.is_valid:
            self.destroy()

    def _create_widgets(self):
        """Create all widgets of statistic window."""
        self.buttons_frame = tk.Frame(master=self, bg='#e2ddec')
        self.buttons_frame.grid(row=1, column=0, columnspan=2)

        for idx in range(2):
            self.widgets[idx] = {}
            widget = self.widgets[idx]
            widget['canvas'] = tk.Canvas(self, bd=0, highlightthickness=0, bg='#e2ddec')
            widget['canvas'].bind('<Configure>', self.resize_plot(idx))
            widget['canvas'].grid(sticky=tk.NSEW, row=0, column=idx, padx=5, pady=5)
            widget['widget_img'] = widget['canvas'].create_image(0, 0, anchor='nw')
            config_widget(self.widgets[idx]['canvas'])

        if self.data_type == 'month':
            self.draw_year_button = tk.Button(master=self.buttons_frame, text=_('Show year statistics'), bg='#f0f4f9')
        else:
            self.draw_year_button = tk.Button(master=self.buttons_frame, text=_('Show month statistics'), bg='#f0f4f9')
        self.draw_year_button.grid(sticky=tk.NS, row=0, column=0, columnspan=2, padx=5, pady=5)
        self.draw_year_button.configure(command=self.show_yearly_stats)

        config_widget(self.buttons_frame)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def _draw(self):
        """Draw default statistics from data."""
        if not self.is_valid:
            return
        self.plot(0, self.data_by_category, x='category', y='amount', title=self.titles['category'])
        self.plot(1, self.data_by_date, x='date', y='amount', title=self.titles['date'])

    def _collect_data(self):
        """Process gathered data for plot."""
        columns = {
            'category': _('category'),
            'date': _('date'),
            'amount': _('amount'),
            'month': _('month')
        }
        self.columns = columns
        if not self.is_valid:
            return
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
            self.data = pd.DataFrame(self.raw_data.fields)
            self.data.rename(columns={'subcategory': 'category'}, inplace=True)
            self.data.rename(columns=columns, inplace=True)
            self.data.replace({'date': {'': 'unknown'}}, inplace=True)
            self.data_by_category = self.data.groupby([columns['category']])[columns['amount']].sum().reset_index()
            self.data_by_date = self.data.groupby([columns['date']])[columns['amount']].sum().reset_index()
        else:
            raise AttributeError('unknown data type')

    def _collect_year_data(self):
        """Collect yearly statistics."""
        if self.data_type == 'category' or self.plot_changed:
            return
        app = self.master
        self.year_data = []
        for month_id, month in app.months_groups.items():
            month_name = month_id + 1
            for category in month.categories:
                category_name = month.categories[category].name
                category_data = pd.DataFrame(month.categories[category].fields)
                category_data['category'] = category_name
                category_data['month'] = month_name
                self.year_data.append(category_data)
        self.year_data = pd.concat(self.year_data, ignore_index=True)
        self.year_data.rename(columns=self.columns, inplace=True)
        self.year_data.replace({self.columns['date']: {'': 'unknown'}}, inplace=True)
        self.data_by_category = self.year_data.groupby([self.columns['category']])[
            self.columns['amount']].sum().reset_index()
        self.data_by_month = self.year_data.groupby([self.columns['month']])[self.columns['amount']].sum().reset_index()

    def _draw_by_category(self):
        """Draw barplot of expenses per category."""
        self.plot(0, self.data_by_category, x='category', y='amount')

    def _draw_by_date(self):
        """Draw barplot of expenses per date."""
        self.plot(1, self.data_by_date, x='date', y='amount')

    def plot(self, idx, data, x='date', y='amount', title=None):
        """
        Plot bars according to given data.

        :param idx: canvas id for plot
        :param data: data to use for plot
        :type data: pandas.DataFrame
        :param x: x axis column name in data
        :param y: y axis column name in data
        :param title: plot title
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(ax=ax, data=data, x=self.columns[x], y=self.columns[y])
        self.show_values_on_bars(ax)
        plt.grid(alpha=0.35)
        if title:
            plt.title(title, y=1.03)
        fig.canvas.draw()

        widget = self.widgets[idx]
        image = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
        widget['img'] = image
        if self.plot_changed:
            image = widget['img'].resize((widget['tk_img'].width(), widget['tk_img'].height()))
        widget['tk_img'] = PIL.ImageTk.PhotoImage(image, master=self)
        widget['canvas'].itemconfig(widget['widget_img'], image=widget['tk_img'])
        plt.close()

    def _plot_year(self):
        """Plot yearly statistics."""
        self.plot(0, self.data_by_category, x='category', y='amount', title=self.titles['category'])
        self.plot(1, self.data_by_month, x='month', y='amount', title=self.titles['month'])

    def resize_plot(self, canvas_id):
        """Resize callback for canvas widgets."""

        def _resize_image(event):
            widget = self.widgets[canvas_id]
            widget['canvas'].config(width=event.width, height=event.height)
            image = widget['img'].resize((event.width, event.height))
            widget['tk_img'] = PIL.ImageTk.PhotoImage(image)
            widget['canvas'].itemconfig(widget['widget_img'], image=widget['tk_img'])

        return _resize_image

    def show_yearly_stats(self):
        """Show yearly or monthly statistics depending on the initial type."""
        if self.plot_changed:
            return
        if self.data_type == 'month':
            self._collect_year_data()
            self.plot_changed = True
            self._plot_year()
        else:
            self.data_type = 'month'
            self.raw_data = self.master
            self._collect_data()
            self.plot_changed = True
            self._draw()

    def validate_data(self):
        """Validate input data."""
        if self.data_type == 'month':
            for category in self.raw_data.categories:
                if len(self.raw_data.categories[category].fields) > 0:
                    return True
        else:
            if len(self.raw_data.fields) > 0:
                return True
        tk.messagebox.showwarning('Error', 'No data to plot')
        return False

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
