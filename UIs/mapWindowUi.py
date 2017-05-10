# import PyQt5 elements
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QAction, QTabWidget, QWidget


class UiMapWindow(object):

    """
    UiMapWindow
    User interface for the main window which shows the maps and menus.
    """

    def __init__(self, map_window):

        # set object name and size
        map_window.setObjectName("map_window")
        map_window.resize(640, 480)

        # central widget
        self.central_widget = QWidget(map_window)
        self.central_widget.setObjectName("central_widget")
        map_window.setCentralWidget(self.central_widget)

        # tab widget
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setGeometry(QRect(10, 10, 620, 440))
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setObjectName("tab_widget")
        self.tab_widget.setCurrentIndex(-1)

        # menu
        self.menu_bar = map_window.menuBar()

        # file menu
        self.file_menu = self.menu_bar.addMenu('File')

        # open menu
        self.open_menu = self.file_menu.addMenu('Open')

        # 1d action
        self.action_1d_map = QAction(map_window)
        self.action_1d_map.setObjectName("action_1d_map")
        self.action_1d_map.setText("1D Map")
        self.action_1d_map.setEnabled(False)
        self.open_menu.addAction(self.action_1d_map)

        # 2d action
        self.action_2d_map = QAction(map_window)
        self.action_2d_map.setObjectName("action_2d_map")
        self.action_2d_map.setText("2D Map")
        self.action_2d_map.setEnabled(True)
        self.open_menu.addAction(self.action_2d_map)

        # save action
        self.action_save = QAction(map_window)
        self.action_save.setObjectName("action_save")
        self.action_save.setText("Save")
        self.action_save.setEnabled(False)
        self.file_menu.addAction(self.action_save)

        # add separator
        self.file_menu.addSeparator()

        # exit action
        self.action_exit = QAction(map_window)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setText("Exit")
        self.action_exit.setEnabled(False)
        self.file_menu.addAction(self.action_exit)

        # view menu
        self.view_menu = self.menu_bar.addMenu('View')

        # spectrum action
        self.action_spectrum = QAction(map_window)
        self.action_spectrum.setObjectName("action_spectrum")
        self.action_spectrum.setText("Spectrum")
        self.action_spectrum.setEnabled(False)
        self.view_menu.addAction(self.action_spectrum)

        # pixel information action
        self.action_pixel_information = QAction(map_window)
        self.action_pixel_information.setObjectName("action_pixel_information")
        self.action_pixel_information.setText("Pixel Information")
        self.action_pixel_information.setEnabled(False)
        self.view_menu.addAction(self.action_pixel_information)

        # tools menu
        self.tools_menu = self.menu_bar.addMenu('Tools')

        # add micrograph action
        self.action_add_micrograph = QAction(map_window)
        self.action_add_micrograph.setObjectName("action_add_micrograph")
        self.action_add_micrograph.setText("Add Micrograph")
        self.action_add_micrograph.setEnabled(False)
        self.tools_menu.addAction(self.action_add_micrograph)

        # fitting action
        self.action_fitting = QAction(map_window)
        self.action_fitting.setObjectName("action_fitting")
        self.action_fitting.setText("Fitting")
        self.action_fitting.setEnabled(False)
        self.tools_menu.addAction(self.action_fitting)

        # remove background action
        self.action_remove_background = QAction(map_window)
        self.action_remove_background.setObjectName("action_remove_background")
        self.action_remove_background.setText("Remove Background")
        self.action_remove_background.setEnabled(False)
        self.tools_menu.addAction(self.action_remove_background)

        # remove cosmic rays action
        self.action_remove_cosmic_rays = QAction(map_window)
        self.action_remove_cosmic_rays.setObjectName("action_remove_cosmic_rays")
        self.action_remove_cosmic_rays.setText("Remove Cosmic Rays")
        self.action_remove_cosmic_rays.setEnabled(False)
        self.tools_menu.addAction(self.action_remove_cosmic_rays)

        # about menu
        self.about_menu = self.menu_bar.addMenu('About')

        # about action
        self.action_about = QAction(map_window)
        self.action_about.setObjectName("action_about")
        self.action_about.setText("About")
        self.action_about.setEnabled(True)
        self.about_menu.addAction(self.action_about)
