# import PyQt5 elements
from PyQt5.QtWidgets import QGroupBox, QLabel, QLineEdit, QPushButton, QRadioButton, QSpinBox, QSlider
from PyQt5.QtCore import QRect, Qt


class UiBackgroundWidget(object):

    """
    UiBackgroundWidget
    User interface for the background remove window.
    """

    def __init__(self, background_widget):

        # set window title, object name and widget size
        background_widget.setWindowTitle("Remove Background")
        background_widget.setObjectName("background_widget")
        background_widget.resize(320, 321)

        # group box for pixel selection
        self.group_box = QGroupBox(background_widget)
        self.group_box.setTitle("Pixel Selection")
        self.group_box.setGeometry(QRect(10, 10, 300, 68))
        self.group_box.setObjectName("group_box")

        # radio button for focused pixel selection
        self.focused_pixel_radio_button = QRadioButton(self.group_box)
        self.focused_pixel_radio_button.setText("Focused Pixel")
        self.focused_pixel_radio_button.setGeometry(QRect(0, 20, 220, 22))
        self.focused_pixel_radio_button.setChecked(True)
        self.focused_pixel_radio_button.setObjectName("focused_pixel_radio_button")

        # radio button for whole selection
        self.whole_map_radio_button = QRadioButton(self.group_box)
        self.whole_map_radio_button.setText("Whole Map")
        self.whole_map_radio_button.setGeometry(QRect(0, 42, 220, 22))
        self.whole_map_radio_button.setObjectName("whole_map_radio_button")

        # group box for background settings
        self.group_box_2 = QGroupBox(background_widget)
        self.group_box_2.setTitle("Background Settings")
        self.group_box_2.setGeometry(QRect(10, 78, 300, 204))
        self.group_box_2.setObjectName("group_box_2")

        # radio button for minimum counts
        self.minimum_counts_radio_button = QRadioButton(self.group_box_2)
        self.minimum_counts_radio_button.setText("Minimum Counts")
        self.minimum_counts_radio_button.setGeometry(QRect(0, 20, 220, 22))
        self.minimum_counts_radio_button.setChecked(True)
        self.minimum_counts_radio_button.setObjectName("minimum_counts_radio_button")

        # radio button for interval average
        self.interval_average_radio_button = QRadioButton(self.group_box_2)
        self.interval_average_radio_button.setText("Interval Average")
        self.interval_average_radio_button.setGeometry(QRect(0, 42, 220, 22))
        self.interval_average_radio_button.setObjectName("interval_average_radio_button")

        # label for interval selection
        self.label_5 = QLabel(self.group_box_2)
        self.label_5.setText("Int. Boundaries")
        self.label_5.setGeometry(QRect(40, 64, 121, 27))
        self.label_5.setObjectName("label_5")

        # slider for lower interval boundary
        self.lower_boundary_slider = QSlider(self.group_box_2)
        self.lower_boundary_slider.setEnabled(False)
        self.lower_boundary_slider.setGeometry(QRect(160, 64, 70, 29))
        self.lower_boundary_slider.setOrientation(Qt.Horizontal)
        self.lower_boundary_slider.setObjectName("lower_boundary_slider")

        # slider for the upper inverval boundary
        self.upper_boundary_slider = QSlider(self.group_box_2)
        self.upper_boundary_slider.setEnabled(False)
        self.upper_boundary_slider.setGeometry(QRect(230, 64, 70, 29))
        self.upper_boundary_slider.setOrientation(Qt.Horizontal)
        self.upper_boundary_slider.setObjectName("upper_boundary_slider")

        # background from pixel radio
        self.background_from_pixel_radio_button = QRadioButton(self.group_box_2)
        self.background_from_pixel_radio_button.setText("Background from Map Pixel")
        self.background_from_pixel_radio_button.setGeometry(QRect(0, 91, 220, 22))
        self.background_from_pixel_radio_button.setObjectName("background_from_pixel_radio_button")

        # label for x pixel selection
        self.label_7 = QLabel(self.group_box_2)
        self.label_7.setText("X")
        self.label_7.setGeometry(QRect(40, 113, 16, 27))
        self.label_7.setObjectName("label_7")

        # spin box for x pixel selection
        self.x_spin_box = QSpinBox(self.group_box_2)
        self.x_spin_box.setEnabled(False)
        self.x_spin_box.setGeometry(QRect(60, 113, 61, 27))
        self.x_spin_box.setObjectName("x_spin_box")

        # label for y pixel selection
        self.label_8 = QLabel(self.group_box_2)
        self.label_8.setText("Y")
        self.label_8.setGeometry(QRect(140, 113, 16, 27))
        self.label_8.setObjectName("label_8")

        # spin box for y pixel selection
        self.y_spin_box = QSpinBox(self.group_box_2)
        self.y_spin_box.setEnabled(False)
        self.y_spin_box.setGeometry(QRect(160, 113, 61, 27))
        self.y_spin_box.setObjectName("y_spin_box")

        # radio button for file background
        self.background_from_file_radio_button = QRadioButton(self.group_box_2)
        self.background_from_file_radio_button.setText("Background from File")
        self.background_from_file_radio_button.setEnabled(True)
        self.background_from_file_radio_button.setGeometry(QRect(0, 140, 220, 22))
        self.background_from_file_radio_button.setObjectName("background_from_file_radio_button")

        # label for file selection
        self.label_9 = QLabel(self.group_box_2)
        self.label_9.setText("File")
        self.label_9.setGeometry(QRect(40, 167, 31, 27))
        self.label_9.setObjectName("label_9")

        # line edit for file path
        self.file_path_line_edit = QLineEdit(self.group_box_2)
        self.file_path_line_edit.setEnabled(False)
        self.file_path_line_edit.setGeometry(QRect(70, 167, 171, 27))
        self.file_path_line_edit.setObjectName("file_path_line_edit")

        # file browse button
        self.file_browse_push_button = QPushButton(self.group_box_2)
        self.file_browse_push_button.setText("...")
        self.file_browse_push_button.setEnabled(False)
        self.file_browse_push_button.setGeometry(QRect(250, 167, 31, 27))
        self.file_browse_push_button.setObjectName("file_browse_push_button")

        # remove background button
        self.remove_background_push_button = QPushButton(background_widget)
        self.remove_background_push_button.setText("Remove Background")
        self.remove_background_push_button.setGeometry(QRect(150, 283, 161, 27))
        self.remove_background_push_button.setObjectName("remove_background_push_button")
