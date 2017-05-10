# import PyQt5 elements
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QDialogButtonBox, QPushButton, QWidget


class UiAddMicrographDialog(object):

    """
    UiAddMicrographDialog
    User interface for the add micrograph dialog which is used to import a micrograph into the program.
    """

    def __init__(self, add_micrograph_dialog):

        # set window title, object name and window size
        add_micrograph_dialog.setWindowTitle("Add Micrograph")
        add_micrograph_dialog.setObjectName("AddMicrographDialog")
        add_micrograph_dialog.resize(960, 480)

        # button box
        self.button_box = QDialogButtonBox(add_micrograph_dialog)
        self.button_box.setEnabled(True)
        self.button_box.setGeometry(QRect(415, 440, 535, 32))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        # widget for the two plots
        self.plot_widget = QWidget(add_micrograph_dialog)
        self.plot_widget.setGeometry(QRect(10, 10, 940, 350))
        self.plot_widget.setObjectName("plot_widget")

        # widget for the toolbar
        self.toolbar_widget = QWidget(add_micrograph_dialog)
        self.toolbar_widget.setGeometry(QRect(10, 420, 400, 50))
        self.toolbar_widget.setObjectName("toolbar_widget")

        # widget for buttons controlling the points on the plots
        self.button_widget = QWidget(add_micrograph_dialog)
        self.button_widget.setGeometry(QRect(10, 365, 940, 32))
        self.button_widget.setObjectName("button_widget")

        # button to remove all moving points
        self.clear_all_moving_button = QPushButton(self.button_widget)
        self.clear_all_moving_button.setEnabled(False)
        self.clear_all_moving_button.setGeometry(QRect(580, 2, 100, 28))
        self.clear_all_moving_button.setObjectName("clear_all_moving_button")
        self.clear_all_moving_button.setText("Clear All")

        # button to remove last moving point
        self.clear_last_moving_button = QPushButton(self.button_widget)
        self.clear_last_moving_button.setEnabled(False)
        self.clear_last_moving_button.setGeometry(QRect(475, 2, 100, 28))
        self.clear_last_moving_button.setObjectName("clear_last_moving_button")
        self.clear_last_moving_button.setText("Clear Last")

        # button to remove all fixed points
        self.clear_all_fixed_button = QPushButton(self.button_widget)
        self.clear_all_fixed_button.setEnabled(False)
        self.clear_all_fixed_button.setGeometry(QRect(110, 2, 100, 28))
        self.clear_all_fixed_button.setObjectName("clear_all_fixed_button")
        self.clear_all_fixed_button.setText("Clear All")

        # button to remove last fixed point
        self.clear_last_fixed_button = QPushButton(self.button_widget)
        self.clear_last_fixed_button.setEnabled(False)
        self.clear_last_fixed_button.setGeometry(QRect(5, 2, 100, 28))
        self.clear_last_fixed_button.setObjectName("clear_last_fixed_button")
        self.clear_last_fixed_button.setText("Clear Last")

        # connect accept and reject
        self.button_box.accepted.connect(add_micrograph_dialog.accept)
        self.button_box.rejected.connect(add_micrograph_dialog.reject)
