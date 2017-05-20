# import PyQt5 elements
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class UiAbout(object):

    """
    UiAbout
    User interface for the about window showing the credits of this code.
    """

    def __init__(self, about_window):

        # set window title, object name and bjoect size
        about_window.setWindowTitle("About")
        about_window.setObjectName("about")
        about_window.setFixedWidth(385)
        about_window.setFixedHeight(184)

        # Juelich logo
        self.label = QLabel(about_window)
        self.label.setGeometry(QRect(100, 40, 311, 171))
        self.label.setText("")
        self.label.setPixmap(QPixmap("Jülich_fz_logo.svg.png"))
        self.label.setObjectName("label")

        # mail contact
        self.label_2 = QLabel(about_window)
        self.label_2.setGeometry(QRect(10, 0, 311, 81))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("<html><head/><body><p><span style=\" font-weight:600;\">Py2DLuminescence 0.1.4</span>"
                             "</p><p>Sven Borghardt, <a href=\"mailto:s.borghardt@fz-juelich.de\">"
                             "<span style=\" text-decoration: underline; color:#0000ff;\">s.borghardt@fz-juelich.de"
                             "</span></a></p></body></html>")
