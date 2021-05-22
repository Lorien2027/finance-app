def config_widget(widget):
    """
    Configure the columns and rows of the widget grid.

    :param widget: tk.Frame
    """
    for column in range(widget.grid_size()[0]):
        widget.columnconfigure(column, weight=1)
    for row in range(widget.grid_size()[1]):
        widget.rowconfigure(row, weight=1)
