# import PyQt5 elements
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QTableWidget


class UiPixelInformationWidget(object):

    """
    UiPixelInformationWidget
    User interface for the pixel information widget including a simple table.
    """
    
    def __init__(self, pixel_information_window):

        # set window title, object name and window size
        pixel_information_window.setWindowTitle("Pixel Information")
        pixel_information_window.setObjectName("PixelInformationWindow")
        pixel_information_window.resize(320, 240)

        # pixel information table
        self.pixel_information_table_widget = QTableWidget()
        self.pixel_information_table_widget.setParent(pixel_information_window)
        self.pixel_information_table_widget.setGeometry(QRect(10, 10, 300, 220))
        self.pixel_information_table_widget.setObjectName("pixel_information_table")
        self.pixel_information_table_widget.setColumnCount(0)
        self.pixel_information_table_widget.setRowCount(0)
