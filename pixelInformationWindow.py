# general imports
import numpy
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
# import UI
from UIs.pixelInformationWindowUi import UiPixelInformationWindow


class PixelInformationWindow(QMainWindow):

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # load and set up UI
        self.ui = UiPixelInformationWindow(self)

        # set fixed size
        self.setFixedWidth(320)
        self.setFixedHeight(240)

    def clear(self):

        # clear the table
        self.ui.pixel_information_table.clear()

    def update(self):

        # get map dimension
        dimension = self._app.maps.get_selected_map().get_dimension()

        # get data names
        data_names = self._app.maps.get_selected_map().get_data_names()

        # get fit data
        fit_functions, fit_initial_parameters, fit_optimized_parameters = self._app.maps.get_selected_map().get_fit()
        n_parameters = 4*numpy.sum(numpy.int_(fit_functions == 1)) + \
            4*numpy.sum(numpy.int_(fit_functions == 2)) + \
            5*numpy.sum(numpy.int_(fit_functions == 3))

        # update table
        self.ui.pixel_information_table.setRowCount(len(data_names)+n_parameters+dimension)
        self.ui.pixel_information_table.setColumnCount(2)
        self.ui.pixel_information_table.horizontalHeader().setStretchLastSection(True)
        self.ui.pixel_information_table.horizontalHeader().hide()
        self.ui.pixel_information_table.verticalHeader().hide()

        # add pixel number
        focused_pixel = self._app.maps.get_selected_map().get_focus()
        if dimension == 1:
            name_widget = QTableWidgetItem('x pixel')
            name_widget.setFlags(Qt.ItemIsEnabled)
            data_widget = QTableWidgetItem(str(focused_pixel))
            data_widget.setFlags(Qt.ItemIsEnabled)
            self.ui.pixel_information_table.setItem(0, 0, name_widget)
            self.ui.pixel_information_table.setItem(0, 1, data_widget)
        else:
            name_widget = QTableWidgetItem('x pixel')
            name_widget.setFlags(Qt.ItemIsEnabled)
            data_widget = QTableWidgetItem(str(focused_pixel[0]))
            data_widget.setFlags(Qt.ItemIsEnabled)
            self.ui.pixel_information_table.setItem(0, 0, name_widget)
            self.ui.pixel_information_table.setItem(0, 1, data_widget)
            name_widget = QTableWidgetItem('y pixel')
            name_widget.setFlags(Qt.ItemIsEnabled)
            data_widget = QTableWidgetItem(str(focused_pixel[1]))
            data_widget.setFlags(Qt.ItemIsEnabled)
            self.ui.pixel_information_table.setItem(1, 0, name_widget)
            self.ui.pixel_information_table.setItem(1, 1, data_widget)

        for data_id, data_name in data_names.items():

            # name column
            name_widget = QTableWidgetItem(data_name)
            name_widget.setFlags(Qt.ItemIsEnabled)

            # data column
            data_value = self._app.maps.get_selected_map().get_data(data_index=data_id, pixel=-2)
            data_widget = QTableWidgetItem(str(data_value))
            data_widget.setFlags(Qt.ItemIsEnabled)

            # add widgets to table
            self.ui.pixel_information_table.setItem(data_id+dimension, 0, name_widget)
            self.ui.pixel_information_table.setItem(data_id+dimension, 1, data_widget)

        j_parameter = 0
        for i_peak in range(len(fit_functions)):

            if fit_functions[i_peak] > 0:

                # intensity
                name_widget = QTableWidgetItem('I'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(fit_optimized_parameters[i_peak, 0]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # wavelength
                name_widget = QTableWidgetItem('λ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(fit_optimized_parameters[i_peak, 1]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

            if fit_functions[i_peak] == 1:

                # gamma
                name_widget = QTableWidgetItem('γ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # FWHM
                name_widget = QTableWidgetItem('FWHM'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(2*1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

            if fit_functions[i_peak] == 2:

                # sigma
                name_widget = QTableWidgetItem('σ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # FWHM
                name_widget = QTableWidgetItem('FWHM'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(2.35482*1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

            if fit_functions[i_peak] == 3:

                # sigma
                name_widget = QTableWidgetItem('σ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 2]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # gamma
                name_widget = QTableWidgetItem('γ'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                data_widget = QTableWidgetItem(str(1000*fit_optimized_parameters[i_peak, 3]))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1

                # FWHM
                name_widget = QTableWidgetItem('FWHM'+str(i_peak+1))
                name_widget.setFlags(Qt.ItemIsEnabled)
                sigma = 1000*fit_optimized_parameters[i_peak, 2]
                gamma = 1000*fit_optimized_parameters[i_peak, 3]
                data_widget = QTableWidgetItem(str(0.5346*2.*gamma+numpy.sqrt(0.2166*4.*gamma**2.+2.35482**2.*sigma**2.)))
                data_widget.setFlags(Qt.ItemIsEnabled)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 0, name_widget)
                self.ui.pixel_information_table.setItem(len(data_names)+j_parameter+dimension, 1, data_widget)
                j_parameter += 1
