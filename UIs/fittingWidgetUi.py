# import PyQt5 elements
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import QCheckBox, QComboBox, QGroupBox, QLabel, QPushButton, QRadioButton, QSlider, QTableWidget, \
    QTableWidgetItem, QTabWidget, QWidget


class UiFittingWidget(object):

    """
    Uifitting_window
    User interface for the fitting window used to fit the maps.
    """

    def __init__(self, fitting_window):

        # set object name and
        fitting_window.setObjectName("fitting_window")
        fitting_window.resize(347, 600)

        # group box for the pixel selection
        self.group_box = QGroupBox(fitting_window)
        self.group_box.setTitle("Pixel Selection")
        self.group_box.setGeometry(QRect(10, 10, 320, 225))
        self.group_box.setObjectName("group_box")

        # radio button for the focused pixel selection
        self.focused_pixel_radio = QRadioButton(self.group_box)
        self.focused_pixel_radio.setText("Focused Pixel")
        self.focused_pixel_radio.setGeometry(QRect(0, 25, 220, 27))
        self.focused_pixel_radio.setChecked(True)
        self.focused_pixel_radio.setObjectName("focused_pixel_radio")

        # radio button for multiple pixel selection
        self.multiple_pixels_radio = QRadioButton(self.group_box)
        self.multiple_pixels_radio.setText("Multiple Pixels")
        self.multiple_pixels_radio.setGeometry(QRect(0, 50, 220, 27))
        self.multiple_pixels_radio.setObjectName("multiple_pixels_radio")

        # label for the threshold data selection
        self.label = QLabel(self.group_box)
        self.label.setText("Threshold data")
        self.label.setGeometry(QRect(40, 75, 121, 27))
        self.label.setObjectName("label")

        # combo box for the threshold data selection
        self.threshold_type_combo = QComboBox(self.group_box)
        self.threshold_type_combo.setEnabled(False)
        self.threshold_type_combo.setGeometry(QRect(160, 75, 160, 27))
        self.threshold_type_combo.setObjectName("threshold_type_combo")

        # label for the threshold value
        self.label_2 = QLabel(self.group_box)
        self.label_2.setText("Threshold value")
        self.label_2.setGeometry(QRect(40, 100, 121, 27))
        self.label_2.setObjectName("label_2")

        # slider for the lower threshold
        self.lower_threshold_slider = QSlider(self.group_box)
        self.lower_threshold_slider.setEnabled(False)
        self.lower_threshold_slider.setGeometry(QRect(160, 100, 80, 27))
        self.lower_threshold_slider.setMinimum(0)
        self.lower_threshold_slider.setMaximum(10000)
        self.lower_threshold_slider.setProperty("value", 0)
        self.lower_threshold_slider.setOrientation(Qt.Horizontal)
        self.lower_threshold_slider.setTickPosition(QSlider.NoTicks)
        self.lower_threshold_slider.setObjectName("lower_threshold_slider")

        # slider for the area selection y2
        self.upper_threshold_slider = QSlider(self.group_box)
        self.upper_threshold_slider.setEnabled(False)
        self.upper_threshold_slider.setGeometry(QRect(240, 100, 80, 27))
        self.upper_threshold_slider.setMaximum(10000)
        self.upper_threshold_slider.setProperty("value", 10000)
        self.upper_threshold_slider.setOrientation(Qt.Horizontal)
        self.upper_threshold_slider.setTickPosition(QSlider.NoTicks)
        self.upper_threshold_slider.setObjectName("upper_threshold_slider")

        # label for
        self.label_3 = QLabel(self.group_box)
        self.label_3.setText("Area Selection")
        self.label_3.setGeometry(QRect(40, 125, 121, 27))
        self.label_3.setObjectName("label_3")

        # slider for the area selection x1
        self.area_slider_x1 = QSlider(self.group_box)
        self.area_slider_x1.setEnabled(False)
        self.area_slider_x1.setGeometry(QRect(160, 125, 80, 27))
        self.area_slider_x1.setOrientation(Qt.Horizontal)
        self.area_slider_x1.setTickPosition(QSlider.NoTicks)
        self.area_slider_x1.setObjectName("area_slider_x1")

        # slider for the area selection x2
        self.area_slider_x2 = QSlider(self.group_box)
        self.area_slider_x2.setEnabled(False)
        self.area_slider_x2.setGeometry(QRect(240, 125, 80, 27))
        self.area_slider_x2.setOrientation(Qt.Horizontal)
        self.area_slider_x2.setTickPosition(QSlider.NoTicks)
        self.area_slider_x2.setObjectName("area_slider_x2")

        # slider for the area selection x3
        self.area_slider_y1 = QSlider(self.group_box)
        self.area_slider_y1.setEnabled(False)
        self.area_slider_y1.setGeometry(QRect(160, 150, 80, 27))
        self.area_slider_y1.setOrientation(Qt.Horizontal)
        self.area_slider_y1.setTickPosition(QSlider.NoTicks)
        self.area_slider_y1.setObjectName("area_slider_y1")

        # slider for the area selection y1
        self.area_slider_y2 = QSlider(self.group_box)
        self.area_slider_y2.setEnabled(False)
        self.area_slider_y2.setGeometry(QRect(240, 150, 80, 27))
        self.area_slider_y2.setOrientation(Qt.Horizontal)
        self.area_slider_y2.setTickPosition(QSlider.NoTicks)
        self.area_slider_y2.setObjectName("area_slider_y2")

        # checkbox for the overwrite decision
        self.overwrite_check_box = QCheckBox(self.group_box)
        self.overwrite_check_box.setText("Overwrite Fits")
        self.overwrite_check_box.setEnabled(False)
        self.overwrite_check_box.setGeometry(QRect(160, 175, 171, 22))
        self.overwrite_check_box.setChecked(True)
        self.overwrite_check_box.setObjectName("overwrite_check_box")

        # checkbox for the neighbour option
        self.neighbour_check_box = QCheckBox(self.group_box)
        self.neighbour_check_box.setText("Param. f. Neighbour")
        self.neighbour_check_box.setEnabled(False)
        self.neighbour_check_box.setGeometry(QRect(160, 200, 171, 22))
        self.neighbour_check_box.setChecked(True)
        self.neighbour_check_box.setObjectName("neighbour_check_box")

        # group box for the fit settings
        self.group_box_2 = QGroupBox(fitting_window)
        self.group_box_2.setTitle("Fit Settings")
        self.group_box_2.setGeometry(QRect(10, 235, 320, 48))
        self.group_box_2.setObjectName("group_box_2")

        # label for the interval selection
        self.label_4 = QLabel(self.group_box_2)
        self.label_4.setText("Int. Boundaries")
        self.label_4.setGeometry(QRect(5, 25, 121, 27))
        self.label_4.setObjectName("label_4")

        # slider for the lower interval limit
        self.lower_limit_slider = QSlider(self.group_box_2)
        self.lower_limit_slider.setGeometry(QRect(160, 25, 80, 27))
        self.lower_limit_slider.setMaximum(1023)
        self.lower_limit_slider.setOrientation(Qt.Horizontal)
        self.lower_limit_slider.setObjectName("lower_limit_slider")

        # slider for the upper interval limit
        self.upper_limit_slider = QSlider(self.group_box_2)
        self.upper_limit_slider.setGeometry(QRect(240, 25, 80, 27))
        self.upper_limit_slider.setMaximum(1023)
        self.upper_limit_slider.setProperty("value", 1023)
        self.upper_limit_slider.setOrientation(Qt.Horizontal)
        self.upper_limit_slider.setObjectName("upper_limit_slider")

        # group box for parameter settings
        self.group_box_3 = QGroupBox(fitting_window)
        self.group_box_3.setTitle("Fit Parameters")
        self.group_box_3.setGeometry(QRect(10, 290, 327, 271))
        self.group_box_3.setObjectName("group_box_3")

        # tab widget for parameter settings
        self.tab_widget = QTabWidget(self.group_box_3)
        self.tab_widget.setGeometry(QRect(0, 25, 327, 241))
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        self.tab_widget.setIconSize(QSize(16, 16))
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setObjectName("tab_widget")

        # tab for initial parameters
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.table_widget = QTableWidget(self.tab)
        self.table_widget.setGeometry(QRect(0, 0, 323, 207))
        self.table_widget.setRowCount(6)
        self.table_widget.setColumnCount(5)
        self.table_widget.setObjectName("table_widget")
        item = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.table_widget.setHorizontalHeaderItem(4, item)
        item = self.table_widget.horizontalHeaderItem(0)
        item.setText("f")
        item = self.table_widget.horizontalHeaderItem(1)
        item.setText("I")
        item = self.table_widget.horizontalHeaderItem(2)
        item.setText("ε [eV]")
        item = self.table_widget.horizontalHeaderItem(3)
        item.setText("σ [meV]")
        item = self.table_widget.horizontalHeaderItem(4)
        item.setText("γ [meV]")
        self.table_widget.horizontalHeader().setVisible(True)
        self.table_widget.horizontalHeader().setDefaultSectionSize(60)
        self.table_widget.horizontalHeader().setHighlightSections(True)
        self.table_widget.verticalHeader().setVisible(True)
        self.table_widget.verticalHeader().setDefaultSectionSize(30)
        self.tab_widget.addTab(self.tab, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab), "Initial")

        # tab for the lower boundary selection
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.table_widget_2 = QTableWidget(self.tab_2)
        self.table_widget_2.setGeometry(QRect(0, 0, 323, 207))
        self.table_widget_2.setRowCount(6)
        self.table_widget_2.setColumnCount(4)
        self.table_widget_2.setObjectName("table_widget_2")
        item = QTableWidgetItem()
        self.table_widget_2.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.table_widget_2.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.table_widget_2.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.table_widget_2.setHorizontalHeaderItem(3, item)
        item = self.table_widget_2.horizontalHeaderItem(0)
        item.setText("I")
        item = self.table_widget_2.horizontalHeaderItem(1)
        item.setText("ε [eV]")
        item = self.table_widget_2.horizontalHeaderItem(2)
        item.setText("σ [meV]")
        item = self.table_widget_2.horizontalHeaderItem(3)
        item.setText("γ [meV]")
        self.table_widget_2.horizontalHeader().setDefaultSectionSize(75)
        self.table_widget_2.verticalHeader().setDefaultSectionSize(30)
        self.tab_widget.addTab(self.tab_2, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_2), "Lower Bound.")

        # tab for the upper boundary selection
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.table_widget_3 = QTableWidget(self.tab_3)
        self.table_widget_3.setGeometry(QRect(0, 0, 323, 207))
        self.table_widget_3.setRowCount(6)
        self.table_widget_3.setColumnCount(4)
        self.table_widget_3.setObjectName("table_widget_3")
        item = QTableWidgetItem()
        self.table_widget_3.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.table_widget_3.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.table_widget_3.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.table_widget_3.setHorizontalHeaderItem(3, item)
        item = self.table_widget_3.horizontalHeaderItem(0)
        item.setText("I")
        item = self.table_widget_3.horizontalHeaderItem(1)
        item.setText("ε [eV]")
        item = self.table_widget_3.horizontalHeaderItem(2)
        item.setText("σ [meV]")
        item = self.table_widget_3.horizontalHeaderItem(3)
        item.setText("γ [meV]")
        self.table_widget_3.horizontalHeader().setDefaultSectionSize(75)
        self.table_widget_3.verticalHeader().setDefaultSectionSize(30)
        self.tab_widget.addTab(self.tab_3, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_3), "Upper Bound.")

        # clear button
        self.clear_button = QPushButton(fitting_window)
        self.clear_button.setText("Clear")
        self.clear_button.setGeometry(QRect(10, 565, 100, 27))
        self.clear_button.setObjectName("clear_button")

        # fit button
        self.fit_button = QPushButton(fitting_window)
        self.fit_button.setText("Fit")
        self.fit_button.setGeometry(QRect(230, 565, 100, 27))
        self.fit_button.setObjectName("fit_button")

        # set current tab
        self.tab_widget.setCurrentIndex(0)
