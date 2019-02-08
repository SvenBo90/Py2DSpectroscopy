# general imports
import numpy
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget
# import fit functions
import fitting
# import spectrum canvas
from mplCanvas import SpectrumCanvas
# import UI
from UIs.spectrumWidgetUi import UiSpectrumWidget


class SpectrumWidget(QWidget):

    def __init__(self, parent, map_handle):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # link map handle
        self._map = map_handle

        # load and set up UI
        self.ui = UiSpectrumWidget(self)

        # visible flag used for the curser
        self._visible_flag = False

        # create plot canvas
        self._spectrum_canvas = SpectrumCanvas(self.ui.plot_widget, self._map)

        # add callbacks to map canvas
        self._spectrum_canvas.add_callback('button_press_event', self.cb_spectrum_button_press_event)

        # widget including the toolbar
        self._spectrum_canvas.add_toolbar(self.ui.toolbar_widget)

        # add callbacks
        self.ui.spectrum_check_box.stateChanged.connect(self.update_data)
        self.ui.initial_fit_check_box.stateChanged.connect(self.update_data)
        self.ui.initial_peaks_check_box.stateChanged.connect(self.update_data)
        self.ui.optimized_fit_check_box.stateChanged.connect(self.update_data)
        self.ui.optimized_peaks_check_box.stateChanged.connect(self.update_data)

    def cb_spectrum_button_press_event(self, event):

        # check if toolbar is active and if the left mouse button was used
        if self._spectrum_canvas.get_toolbar_active() is None and event.button == 1:

            # check if outer area has been clicked
            if event.inaxes is None:
                return

            # find pixel of clicked energy
            energies = self._map.get_spectrum()[:,0]
            for i_energy in range(len(energies)):
                if energies[i_energy] > event.xdata:
                    self._map.set_interval('left', i_energy)
                    break

        elif self._spectrum_canvas.get_toolbar_active() is None and event.button == 3:

            # check if outer area has been clicked
            if event.inaxes is None:
                return

            # find pixel of clicked energy
            energies = self._map.get_spectrum()[:,0]
            for i_energy in range(len(energies)):
                if energies[i_energy] > event.xdata:
                    self._map.set_interval('right', i_energy)
                    break

    def clear(self):

        # clear spectrum
        self._spectrum_canvas.clear()

    def create_cursors(self, x1, x2):

        # check whether the spectrum window was visible
        self._visible_flag = self.parent().isVisible()

        # create cursor
        self._spectrum_canvas.create_cursors(x1, x2)

        # bring window to front
        self.parent().show()
        self.parent().setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.parent().activateWindow()

    def destroy_cursors(self):

        # hide the window if it was hided before
        if not self._visible_flag:
            self.parent().hide()

        # destroy the cursor
        self._spectrum_canvas.destroy_cursors()

    def update_cursors(self, x1, x2):

        # update cursors
        self._spectrum_canvas.update_cursors(x1, x2)

    def update_data(self):

        # empty dictionary for spectra
        data = dict()
        
        # original spectrum
        data['spectrum'] = self._map.get_spectrum()
        
        # request fit data
        fit_functions, fit_initial_parameters, fit_optimized_parameters = self._map.get_fit()
        # add fit spectra to the data dictionary
        if numpy.sum(fit_functions) > 0:
            data['fit (init.)'] = numpy.zeros((self._map.get_resolution(), 2))
            data['fit (init.)'][:, 0] = data['spectrum'][:, 0]
            data['fit (opt.)'] = numpy.zeros((self._map.get_resolution(), 2))
            data['fit (opt.)'][:, 0] = data['spectrum'][:, 0]
            
        for i_peak in range(len(fit_functions)):
            if fit_functions[i_peak] > 0:
                data[str(i_peak)+' (init.)'] = numpy.zeros((self._map.get_resolution(), 2))
                data[str(i_peak)+' (init.)'][:, 0] = data['spectrum'][:, 0]
                data[str(i_peak)+' (opt.)'] = numpy.zeros((self._map.get_resolution(), 2))
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


class SpectrumWindow(QMainWindow):

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # dictionary for spectrum widgets
        self._spectrum_widgets = {}
        self._current_widget = None

        # central widget
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        # grid layout
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("grid_layout")

        # set window title
        self.setWindowTitle("Spectrum")

    def add_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # add a widget to the widgets list
        self._spectrum_widgets[map_handle.get_id()] = SpectrumWidget(self, map_handle)
        self.grid_layout.addWidget(self._spectrum_widgets[map_handle.get_id()])

    def change_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # hide all widgets
        for key in self._spectrum_widgets.keys():
            self._spectrum_widgets[key].setVisible(False)

        # make the widget for the select map visible
        self._spectrum_widgets[map_handle.get_id()].setVisible(True)
        self._current_widget = self._spectrum_widgets[map_handle.get_id()]

    def get_current_widget(self):

        # return the current widget
        return self._current_widget

    def remove_widget(self, map_id):

        # remove the widget of the deleted map
        self._spectrum_widgets[map_id].setParent(None)
        self._spectrum_widgets[map_id].deleteLater()
        del self._spectrum_widgets[map_id]

        # close the window if there are no more maps
        if len(self._spectrum_widgets) == 0:
            self._current_widget = None
            self.close()

    def update_data(self, map_id):

        # update spectrum widget data
        self._spectrum_widgets[map_id].update_data()
