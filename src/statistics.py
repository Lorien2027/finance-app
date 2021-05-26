import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import config_widget


class StatisticsWindow(tk.Toplevel):
    def __init__(self, categories, data_type='category', master=None):
        super().__init__(master=master)
        self.title('Stats')
        self.geometry('800x600')
        self.row_data = categories
        self.data_type = data_type
        self._draw()
        # self.label = tk.Label(self, text="This is a new Window")
        # self.label.grid()
        config_widget(self)

    def _collect_data(self):
        self.data = {}
        if self.data_type == 'month':
            # self.categories = self.row_data.categories.keys()
            for category in self.row_data.categories:
                category_name = self.row_data.categories[category].name
                # self.data[category_name] = 0
                category_data = pd.DataFrame(self.row_data.categories[category].fields)
                # for row in self.row_data.categories[category].fields:
                #     self.data[category_name] += row['amount']
                self.data[category_name] = category_data['amount'].sum()
            self.data = pd.DataFrame(data=self.data.values(), index=self.data.keys(), columns=['total'])
        elif self.data_type == 'category':
            return
            # for row in self.row_data.fields:
            #     if row['subcategory'] not in self.data:
            #         self.data[row['subcategory']] = 0
            #     else:
            #         self.data[row['subcategory']] += row['amount']
        else:
            raise AttributeError('unknown data type')

    def _draw(self):
        self._collect_data()
        print(self.data)
        sns.barplot(data=self.data, x=self.data.index, y='total')
        plt.show()
        plt.close()
