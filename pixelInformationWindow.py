# general imports
import numpy
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
# import UI
from UIs.pixelInformationWidgetUi import UiPixelInformationWidget


class PixelInformationWidget(QWidget):

    def __init__(self, parent, map_handle):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # link map handle
        self._map = map_handle

        # load and set up UI
        self.ui = UiPixelInformationWidget(self)

        # set fixed size
        self.setFixedWidth(320)
        self.setFixedHeight(240)

    def clear(self):

        # clear the table
        self.ui.pixel_information_table_widget.clear()

    def update_data(self):

        # get map dimension
        dimension = self._map.get_dimension()

        # get data names
        data_names = self._map.get_data_names()

        # get fit data
        fit_functions, fit_initial_parameters, fit_optimized_parameters = self._map.get_fit()
        n_parameters = 4*numpy.sum(numpy.int_(fit_functions == 1)) + \
            4*numpy.sum(numpy.int_(fit_functions == 2)) + \
            5*numpy.sum(numpy.int_(fit_functions == 3))

        # update table
        self.ui.pixel_information_table_widget.setRowCount(3+len(data_names)+n_parameters+dimension)
        self.ui.pixel_information_table_widget.setColumnCount(2)
        self.ui.pixel_information_table_widget.horizontalHeader().setStretchLastSection(True)
        self.ui.pixel_information_table_widget.horizontalHeader().hide()
        self.ui.pixel_information_table_widget.verticalHeader().hide()

        # add pixel number
        focused_pixel = self._map.get_focus()
        if dimension == 1:
            name_widget = QTableWidgetItem('x pixel')
            name_widget.setFlags(Qt.ItemIsEnabled)
            data_widget = QTableWidgetItem(str(focused_pixel[0]))
            data_widget.setFlags(Qt.ItemIsEnabled)
            self.ui.pixel_information_table_widget.setItem(0, 0, name_widget)
            self.ui.pixel_information_table_widget.setItem(0, 1, data_widget)
        else:
            name_widget = QTableWidgetItem('x pixel')
            name_widget.setFlags(Qt.ItemIsEnabled)
            data_widget = QTableWidgetItem(str(focused_pixel[0]))
            data_widget.setFlags(Qt.ItemIsEnabled)
            self.ui.pixel_information_table_widget.setItem(0, 0, name_widget)
            self.ui.pixel_information_table_widget.setItem(0, 1, data_widget)
            name_widget = QTableWidgetItem('y pixel')
            name_widget.setFlags(Qt.ItemIsEnabled)
            data_widget = QTableWidgetItem(str(focused_pixel[1]))
            data_widget.setFlags(Qt.ItemIsEnabled)
            self.ui.pixel_information_table_widget.setItem(1, 0, name_widget)
            self.ui.pixel_information_table_widget.setItem(1, 1, data_widget)

        # add data derived from spectra
        names = {0: '-- integral', 1: '-- mean', 2: '-- maximum'}
        for i in range(len(names)):
            name_widget = QTableWidgetItem(names[i])
            name_widget.setFlags(Qt.ItemIsEnabled)
            data_value = self._map.get_data(data_index=i+1, pixel=-2)
            data_widget = QTableWidgetItem(str(data_value))
            data_widget.setFlags(Qt.ItemIsEnabled)
            self.ui.pixel_information_table_widget.setItem(dimension+i, 0, name_widget)
            self.ui.pixel_information_table_widget.setItem(dimension+i, 1, data_widget)

        for data_id, data_name in data_names.items():

            # name column
            name_widget = QTableWidgetItem(data_name)
            name_widget.setFlags(Qt.ItemIsEnabled)

            # data column
            data_value = self._map.get_data(data_index=4+data_id, pixel=-2)
            data_widget = QTableWidgetItem(str(data_value))
            data_widget.setFlags(Qt.ItemIsEnabled)

            # add widgets to table
            self.ui.pixel_information_table_widget.setItem(3+data_id+dimension, 0, name_widget)
            self.ui.pixel_information_table_widget.setItem(3+data_id+dimension, 1, data_widget)

        j_parameter = 0
        for i_peak in range(len(fit_functions)):

            if fit_functions[i_peak] > 0:

                # intensity
                name_widget = QTableWidgetItem('I'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(fit_optimized_parameters[i_peak, 0]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # wavelength
                name_widget = QTableWidgetItem('ε'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(fit_optimized_parameters[i_peak, 1]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

            if fit_functions[i_peak] == 1:

                # gamma
                name_widget = QTableWidgetItem('γ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # FWHM
                name_widget = QTableWidgetItem('FWHM'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(2*1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

            if fit_functions[i_peak] == 2:

                # sigma
                name_widget = QTableWidgetItem('σ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # FWHM
                name_widget = QTableWidgetItem('FWHM'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(2.35482*1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

            if fit_functions[i_peak] == 3:

                # sigma
                name_widget = QTableWidgetItem('σ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # gamma
                name_widget = QTableWidgetItem('γ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 3]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # FWHM
                name_widget = QTableWidgetItem('FWHM'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                sigma = 1000*fit_optimized_parameters[i_peak, 2]
                gamma = 1000*fit_optimized_parameters[i_peak, 3]
                data_widget = QTableWidgetItem(str(0.5346*2.*gamma+numpy.sqrt(0.2166*4.*gamma**2.+2.35482**2.*sigma**2.)))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table_widget.setItem(3+len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1


class PixelInformationWindow(QMainWindow):

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # dictionary for pixel information widgets
        self._pixel_information_widgets = {}
        self._current_widget = None

        # set fixed size
        self.setFixedWidth(320)
        self.setFixedHeight(240)

        # set window title
        self.setWindowTitle("Pixel Information")

    def add_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # add a widget to the widgets list
        self._pixel_information_widgets[map_handle.get_id()] = PixelInformationWidget(self, map_handle)

    def change_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # hide all widgets
        for key in self._pixel_information_widgets.keys():
            self._pixel_information_widgets[key].setVisible(False)

        # make the widget for the select map visible
        self._pixel_information_widgets[map_handle.get_id()].setVisible(True)
        self._current_widget = self._pixel_information_widgets[map_handle.get_id()]

    def get_current_widget(self):

        # return the current widget
        return self._current_widget

    def remove_widget(self, map_id):

        # remove the widget of the deleted map
        self._pixel_information_widgets[map_id].setParent(None)
        self._pixel_information_widgets[map_id].deleteLater()
        del self._pixel_information_widgets[map_id]

        # close the window if there are no more maps
        if len(self._pixel_information_widgets) == 0:
            self._current_widget = None
            self.close()

    def update_data(self, map_id):

        # update pixel information widget data
        self._pixel_information_widgets[map_id].update_data()
