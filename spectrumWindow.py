# general imports
import numpy
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# import fit functions
import fitting
# import spectrum canvas
from mplCanvas import SpectrumCanvas
# import UI
from UIs.spectrumWindowUi import UiSpectrumWindow


class SpectrumWindow(QMainWindow):

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # load and set up UI
        self.ui = UiSpectrumWindow(self)

        # set fixed size
        self.setFixedWidth(480)
        self.setFixedHeight(415)

        # visible flag used for the curser
        self._visible_flag = False

        # create plot canvas
        self._spectrum_canvas = SpectrumCanvas(self.ui.plot_widget)

        # widget including the toolbar
        self._spectrum_canvas.add_toolbar(self.ui.toolbar_widget)

        # add callbacks
        self.ui.spectrum_check_box.stateChanged.connect(self.update)
        self.ui.initial_fit_check_box.stateChanged.connect(self.update)
        self.ui.initial_peaks_check_box.stateChanged.connect(self.update)
        self.ui.optimized_fit_check_box.stateChanged.connect(self.update)
        self.ui.optimized_peaks_check_box.stateChanged.connect(self.update)

    def clear(self):

        # clear spectrum
        self._spectrum_canvas.clear()

    def create_cursors(self, x1, x2):

        # check whether the spectrum window was visible
        self._visible_flag = self.isVisible()

        # create cursor
        self._spectrum_canvas.create_cursors(x1, x2)

        # bring window to front
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def update_cursors(self, x1, x2):

        self._spectrum_canvas.update_cursors(x1, x2)

    def destroy_cursors(self):

        # hide the window if it was hided before
        if not self._visible_flag:
            self.hide()

        # destroy the cursor
        self._spectrum_canvas.destroy_cursors()

    def update(self):
 
        # empty dictionary for spectra
        data = dict()
        
        # original spectrum
        data['spectrum'] = self._app.maps.get_selected_map().get_spectrum()
        
        # request fit data
        fit_functions, fit_initial_parameters, fit_optimized_parameters = self._app.maps.get_selected_map().get_fit()
        # add fit spectra to the data dictionary
        if numpy.sum(fit_functions) > 0:
            data['fit (init.)'] = numpy.zeros((self._app.maps.get_selected_map().get_resolution(), 2))
            data['fit (init.)'][:, 0] = data['spectrum'][:, 0]
            data['fit (opt.)'] = numpy.zeros((self._app.maps.get_selected_map().get_resolution(), 2))
            data['fit (opt.)'][:, 0] = data['spectrum'][:, 0]
            
        for i_peak in range(len(fit_functions)):
            if fit_functions[i_peak] > 0:
                data[str(i_peak)+' (init.)'] = numpy.zeros((self._app.maps.get_selected_map().get_resolution(), 2))
                data[str(i_peak)+' (init.)'][:, 0] = data['spectrum'][:, 0]
                data[str(i_peak)+' (opt.)'] = numpy.zeros((self._app.maps.get_selected_map().get_resolution(), 2))
                data[str(i_peak)+' (opt.)'][:, 0] = data['spectrum'][:, 0]
            if fit_functions[i_peak] == 1:
                data[str(i_peak)+' (init.)'][:, 1] = fitting.gaussian(data['spectrum'][:, 0],
                                                                      *fit_initial_parameters[i_peak, :3])
                data[str(i_peak)+' (opt.)'][:, 1] = fitting.gaussian(data['spectrum'][:, 0],
                                                                     *fit_optimized_parameters[i_peak, :3])
            elif fit_functions[i_peak] == 2:
                data[str(i_peak)+' (init.)'][:, 1] = fitting.lorentzian(data['spectrum'][:, 0],
                                                                        *fit_initial_parameters[i_peak, :3])
                data[str(i_peak)+' (opt.)'][:, 1] = fitting.lorentzian(data['spectrum'][:, 0],
                                                                       *fit_optimized_parameters[i_peak, :3])
            elif fit_functions[i_peak] == 3:
                data[str(i_peak)+' (init.)'][:, 1] = fitting.voigt(data['spectrum'][:, 0],
                                                                   *fit_initial_parameters[i_peak, :])
                data[str(i_peak)+' (opt.)'][:, 1] = fitting.voigt(data['spectrum'][:, 0],
                                                                  *fit_optimized_parameters[i_peak, :])
            if fit_functions[i_peak] > 0:
                data['fit (init.)'][:, 1] = data['fit (init.)'][:, 1]+data[str(i_peak)+' (init.)'][:, 1]
                data['fit (opt.)'][:, 1] = data['fit (opt.)'][:, 1]+data[str(i_peak)+' (opt.)'][:, 1]

        # checkboxes
        checkboxes = [self.ui.spectrum_check_box.isChecked(),
                      self.ui.initial_fit_check_box.isChecked(),
                      self.ui.initial_peaks_check_box.isChecked(),
                      self.ui.optimized_fit_check_box.isChecked(),
                      self.ui.optimized_peaks_check_box.isChecked()
                      ]

        # update spectrum canvas
        self._spectrum_canvas.update_data(data, checkboxes)
