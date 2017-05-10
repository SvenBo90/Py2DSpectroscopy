# general imports
import sys
# import PyQt5 elements
from PyQt5.QtWidgets import QApplication
# import map classes
from maps import MapList
# import window classes
from aboutWindow import AboutWindow
from backgroundWindow import BackgroundWindow
from fittingWindow import FittingWindow
from mapWindow import MapWindow
from pixelInformationWindow import PixelInformationWindow
from spectrumWindow import SpectrumWindow


class Py2DSpectroscopy(QApplication):

    """
    Py2DSpectroscopy
    This is the main class of the application. It controls the different windows
    of the window and saves the maps in a map list.
    """

    def __init__(self):

        # call super init
        super().__init__(sys.argv)

        # list for all loaded maps
        self.maps = MapList()

        # dictionary for all windows
        self.windows = {
            "aboutWindow": AboutWindow(),
            "backgroundWindow": BackgroundWindow(),
            "fittingWindow": FittingWindow(),
            "mapWindow": MapWindow(),
            "pixelInformationWindow": PixelInformationWindow(),
            "spectrumWindow": SpectrumWindow()
        }

        # show the map window
        self.windows['mapWindow'].show()

        # connect exit method
        self.aboutToQuit.connect(self.exit_app)

    @staticmethod
    def exit_app():

        print('Thanks for using me!')

if __name__ == "__main__":

    # create app
    app = Py2DSpectroscopy()

    # execute app and close system afterwards
    sys.exit(app.exec_())
