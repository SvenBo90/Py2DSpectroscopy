# import PyQt5 elements
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import QComboBox, QDialogButtonBox


class UiColormapDialog(object):

    """
    UiAddMicrographDialog
    User interface for the add micrograph dialog which is used to import a micrograph into the program.
    """

    def __init__(self, colormap_dialog):

        # set window title, object name and window size
        colormap_dialog.setWindowTitle("Choose Colormap")
        colormap_dialog.setObjectName("ColormapDialog")
        colormap_dialog.setFixedWidth(455)
        colormap_dialog.setFixedHeight(100)

        # button box
        self.button_box = QDialogButtonBox(colormap_dialog)
        self.button_box.setEnabled(True)
        self.button_box.setGeometry(QRect(10, 60, 435, 30))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        # colormap selector
        self.colormap_combobox = QComboBox(colormap_dialog)
        self.colormap_combobox.setGeometry(QRect(10, 10, 435, 30))
        self.colormap_combobox.setIconSize(QSize(435, 20))

        # connect accept and reject
        self.button_box.accepted.connect(colormap_dialog.accept)
        self.button_box.rejected.connect(colormap_dialog.reject)
