# import PyQt5 elements
from PyQt5.QtWidgets import QComboBox, QGridLayout, QPushButton, QSizePolicy, QWidget


class UiMapTabWidget(object):

    """
    UiMapTabWidget
    Widget for the map tab widget that shows the data map, colorbar and data selection combo box.
    """

    def __init__(self, map_tab_widget):

        # set object name
        map_tab_widget.setObjectName("mapTab")

        # create grid layout
        self.gridLayout = QGridLayout(map_tab_widget)
        self.gridLayout.setObjectName("gridLayout")

        # create plot widget
        self.plot_widget = QWidget(map_tab_widget)
        self.plot_widget.setObjectName("plotWidget")
        self.plot_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addWidget(self.plot_widget, 0, 0, 1, 2)

        # create toolbar widget
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setObjectName("toolbarWidget")
        self.toolbar_widget.setFixedHeight(50)
        self.gridLayout.addWidget(self.toolbar_widget, 1, 0, 1, 1)

        # data selection box
        self.data_selection_combo_box = QComboBox()
        self.data_selection_combo_box.setObjectName("dataSelectionComboBox")
        self.data_selection_combo_box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.gridLayout.addWidget(self.data_selection_combo_box, 1, 1, 1, 1)



"""
        # create plot widget
        self.plot_widget = QWidget()
        self.plot_widget.setObjectName("plotWidget")

        # create toolbar widget
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setObjectName("toolbarWidget")

        # data selection box
        self.data_selection_combo_box = QComboBox()

        # grid layout
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        self.grid_layout.addWidget(self.plot_widget, 0, 0, 1, 1)

        map_tab_widget.setCentralWidget(self.grid_layout)
"""
