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
        map_window.setWindowTitle("Py2DSpectroscopy")
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
        self.action_1d_map.setEnabled(True)
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

        # save action
        self.action_export = QAction(map_window)
        self.action_export.setObjectName("action_export")
        self.action_export.setText("Export")
        self.action_export.setEnabled(False)
        self.file_menu.addAction(self.action_export)

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
        self.action_fitting.setText("Fit Map")
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

        # flip map menu
        self.flip_menu = self.tools_menu.addMenu('Flip map')

        # flip horizontally action
        self.action_horizontally = QAction(map_window)
        self.action_horizontally.setObjectName("action_horizontally")
        self.action_horizontally.setText("Horizontally")
        self.action_horizontally.setEnabled(False)
        self.flip_menu.addAction(self.action_horizontally)

        # flip vertically action
        self.action_vertically = QAction(map_window)
        self.action_vertically.setObjectName("action_vertically")
        self.action_vertically.setText("Vertically")
        self.action_vertically.setEnabled(False)
        self.flip_menu.addAction(self.action_vertically)

        # flip map menu
        self.rotate_menu = self.tools_menu.addMenu('Rotate map')

        # flip horizontally action
        self.action_clockwise = QAction(map_window)
        self.action_clockwise.setObjectName("action_clockwise")
        self.action_clockwise.setText("Clockwise")
        self.action_clockwise.setEnabled(False)
        self.rotate_menu.addAction(self.action_clockwise)

        # flip vertically action
        self.action_anticlockwise = QAction(map_window)
        self.action_anticlockwise.setObjectName("action_anticlockwise")
        self.action_anticlockwise.setText("Anticlockwise")
        self.action_anticlockwise.setEnabled(False)
        self.rotate_menu.addAction(self.action_anticlockwise)

        # about menu
        self.help_menu = self.menu_bar.addMenu('Help')

        # about action
        self.action_about = QAction(map_window)
        self.action_about.setObjectName("action_about")
        self.action_about.setText("About")
        self.action_about.setEnabled(True)
        self.help_menu.addAction(self.action_about)

        # wiki action
        self.action_wiki = QAction(map_window)
        self.action_wiki.setObjectName("action_wiki")
        self.action_wiki.setText("Wiki")
        self.action_wiki.setEnabled(True)
        self.help_menu.addAction(self.action_wiki)
