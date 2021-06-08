import unittest

from FinanceApp.month_window import Category
from FinanceApp.statistic_window import StatisticsWindow
from test import TkinterTestCase


class TestStatisticWindow(TkinterTestCase):
    test_category = Category(0, 'food')
    test_data = {
        'amount': 152.,
        'date': 0,
        'description': 'description',
        'subcategory': 'cat food'
    }

    def test_0_window_size(self):
        self.test_category.add_field(**self.test_data)
        app = StatisticsWindow(self.test_category, draw=False, master=self.root)
        self.pump_events()
        app_shape = (app.winfo_width(), app.winfo_height())
        app.iconify()
        self.assertEqual(app_shape, (1200, 600))

    def test_1_data(self):
        self.test_category.add_field(**self.test_data)
        app = StatisticsWindow(self.test_category, draw=False, master=self.root)
        app.iconify()
        self.pump_events()
        self.assertEqual(app.data[app.columns['amount']][0], self.test_data['amount'])


if __name__ == '__main__':
    unittest.main()
