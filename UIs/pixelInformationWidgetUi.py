# import PyQt5 elements
from PyQt5.QtWidgets import QGridLayout, QSizePolicy, QTableWidget, QTableView, QWidget


class UiPixelInformationWidget(object):

    """
    UiPixelInformationWidget
    User interface for the pixel information widget including a simple table.
    """
    
    def __init__(self, pixel_information_window):

        # set window title, object name and window size
        pixel_information_window.setObjectName("Pixel Information")
        pixel_information_window.setObjectName("PixelInformationWindow")

        # create grid layout
        self.grid_layout = QGridLayout(pixel_information_window)

        # pixel information table
        self.pixel_information_table_widget = QTableWidget(pixel_information_window)
        self.pixel_information_table_widget.setObjectName("pixel_information_table")
        self.pixel_information_table_widget.setColumnCount(0)
        self.pixel_information_table_widget.setRowCount(0)
        self.grid_layout.addWidget(self.pixel_information_table_widget)
