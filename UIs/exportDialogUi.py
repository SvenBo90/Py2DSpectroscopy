# import PyQt5 elements
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QComboBox, QDialogButtonBox, QGroupBox, QLabel

class UiExportDialog(object):

    """
    UiExportDialog
    User interface for the export dialog that is used in order to export data from the program.
    """

    def __init__(self, export_dialog):

        # set window title, object name and window size
        export_dialog.setWindowTitle("Export Data")
        export_dialog.setObjectName("export_dialog")
        export_dialog.setFixedWidth(242)
        export_dialog.setFixedHeight(174)

        # button box
        self.button_box = QDialogButtonBox(export_dialog)
        self.button_box.setGeometry(QRect(10, 130, 221, 41))
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        # group box for data selection
        self.group_box = QGroupBox(export_dialog)
        self.group_box.setGeometry(QRect(10, 10, 231, 61))
        self.group_box.setObjectName("group_box")
        self.group_box.setTitle("Dialog")

        # combo box for data selection
        self.data_combo_box = QComboBox(self.group_box)
        self.data_combo_box.setGeometry(QRect(60, 25, 160, 27))
        self.data_combo_box.setObjectName("data_combo_box")

        # group box for type selection
        self.group_box_2 = QGroupBox(export_dialog)
        self.group_box_2.setGeometry(QRect(10, 70, 231, 61))
        self.group_box_2.setObjectName("group_box_2")
        self.group_box_2.setTitle("Dialog")

        # combo box for type selection
        self.type_combo_box = QComboBox(self.group_box_2)
        self.type_combo_box.setGeometry(QRect(60, 25, 160, 27))
        self.type_combo_box.setObjectName("type_combo_box")
        self.type_combo_box.addItems(['ASCII'])

        # labels
        self.label = QLabel(self.group_box)
        self.label.setGeometry(QRect(0, 25, 61, 27))
        self.label.setObjectName("label")
        self.label.setText("Dialog")
        self.label_2 = QLabel(self.group_box_2)
        self.label_2.setGeometry(QRect(0, 25, 61, 27))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Dialog")

        # connect accept and reject
        self.button_box.accepted.connect(export_dialog.accept)
        self.button_box.rejected.connect(export_dialog.reject)
