import unittest
import _tkinter
import tkinter as tk


class TkinterTestCase(unittest.TestCase):
    """GUI test."""

    def setUp(self):
        self.root = tk.Tk()
        self.root.iconify()
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        while self.root.dooneevent(_tkinter.ALL_EVENTS | _tkinter.DONT_WAIT):
            pass
