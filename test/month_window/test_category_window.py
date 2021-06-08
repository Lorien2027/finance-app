import unittest

from FinanceApp import Application
from test import TkinterTestCase


class TestFinanceApplication(TkinterTestCase):
    def test_0_window_size(self):
        app = Application(self.root)
        self.pump_events()
        self.assertEqual((app.winfo_width(), app.winfo_height()), (1265, 755))

    def test_1_change_month(self):
        default_month = 0
        test_month = 7

        app = Application(self.root)
        self.pump_events()
        self.assertEqual(app.current_month, default_month)
        app.months_buttons[test_month].invoke()
        self.pump_events()
        self.assertEqual(app.current_month, test_month)

    def test_2_add_category(self):
        test_string = 'dog'
        app = Application(self.root)
        self.pump_events()
        group = app.months_groups[0]
        entry = group.control_window.widgets['category']['widget']
        self.root.deiconify()
        entry.focus_set()
        entry.insert(0, test_string)
        self.pump_events()
        group.category_window.create_button.widget.event_generate('<Button-1>')
        self.pump_events()
        self.root.iconify()
        self.assertEqual(group.category_window.buttons[group.active_category].text, test_string)

    def test_3_add_field(self):
        category_name = 'dog'
        test_amount = 255.0

        app = Application(self.root)
        self.pump_events()
        group = app.months_groups[0]
        category_entry = group.control_window.widgets['category']['widget']
        self.root.deiconify()
        category_entry.focus_set()
        category_entry.insert(0, category_name)
        self.pump_events()
        group.category_window.create_button.widget.event_generate('<Button-1>')
        self.pump_events()
        amount_entry = group.control_window.widgets['amount']['widget']
        amount_entry.focus_set()
        amount_entry.insert(0, str(test_amount))
        self.pump_events()
        info_window = group.information_window
        info_window.control_widgets['add']['widget'].event_generate('<Button-1>')
        self.pump_events()
        self.root.iconify()
        self.assertEqual(group.categories[group.active_category].fields[0]['amount'], test_amount)


if __name__ == '__main__':
    unittest.main()
