# import PyQt5 elements
from PyQt5.QtWidgets import QMainWindow, QWidget
# import UI
from UIs.aboutWindowUi import UiAbout


class AboutWindow(QMainWindow):

    """
    AboutWindow
    A window showing the credits of this code.
    """

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # load and set up UI
        self.ui = UiAbout(self)

        # set fixed size
        self.setFixedWidth(385)
        self.setFixedHeight(184)
