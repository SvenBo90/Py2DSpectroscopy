# import PyQt5 elements
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QComboBox, QWidget


class UiMapTabWidget(object):

    """
    UiMapTabWidget
    Widget for the map tab widget that shows the data map, colorbar and data selection combo box.
    """

    def __init__(self, map_tab_widget):

        # set object name
        map_tab_widget.setObjectName("mapTab")

        # create plot widget
        self.plot_widget = QWidget(map_tab_widget)
        self.plot_widget.setGeometry(QRect(10, 10, 600, 350))
        self.plot_widget.setObjectName("plotWidget")

        # create toolbar widget
        self.toolbar_widget = QWidget(map_tab_widget)
        self.toolbar_widget.setGeometry(QRect(10, 365, 400, 50))
        self.toolbar_widget.setObjectName("toolbarWidget")

        # data selection box
        self.data_selection_box = QComboBox(map_tab_widget)
        self.data_selection_box.setGeometry(QRect(415, 370, 195, 30))
