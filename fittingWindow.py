# general imports
import numpy
from scipy.optimize import curve_fit
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QMessageBox, QProgressDialog, QPushButton,\
    QTableWidgetItem, QToolTip, QWidget
# import fit functions
import fitting
# import UI
from UIs.fittingWidgetUi import UiFittingWidget


class FittingWidget(QWidget):

    """
    FittingWidget
    The fitting widget is used for the fitting of the map.
    """

    # TODO: 1D Map Fitting
    # TODO: Fit parameter for pixel selection

    def __init__(self, parent, map_handle):

        # call widget init
        super().__init__()

        # link app
        self._app = QApplication.instance()

        # link map handle
        self._map = map_handle

        # load and set up UI
        self.ui = UiFittingWidget(self)

        # fill threshold combo box
        for key, value in self._map.get_data_names().items():
            if self._map.get_dimension() == 2 or key > 0:
                self.ui.threshold_type_combo.addItems([value])

        # set area slider limits
        map_size = self._map.get_size()
        if self._map.get_dimension() == 2:
            self.ui.area_slider_x1.setMinimum(0)
            self.ui.area_slider_x1.setMaximum(map_size[0]-1)
            self.ui.area_slider_x2.setMinimum(0)
            self.ui.area_slider_x2.setMaximum(map_size[0]-1)
            self.ui.area_slider_x2.setValue(map_size[0]-1)
            self.ui.area_slider_y1.setMinimum(0)
            self.ui.area_slider_y1.setMaximum(map_size[1]-1)
            self.ui.area_slider_y2.setMinimum(0)
            self.ui.area_slider_y2.setMaximum(map_size[1]-1)
            self.ui.area_slider_y2.setValue(map_size[1]-1)
        else:
            self.ui.area_slider_x1.setMinimum(0)
            self.ui.area_slider_x1.setMaximum(map_size-1)
            self.ui.area_slider_x2.setMinimum(0)
            self.ui.area_slider_x2.setMaximum(map_size-1)
            self.ui.area_slider_x2.setValue(map_size-1)

        # set maximum value for the limit selections
        map_resolution = self._map.get_resolution()
        self.ui.lower_limit_slider.setMaximum(map_resolution-1)
        self.ui.upper_limit_slider.setMaximum(map_resolution-1)
        self.ui.upper_limit_slider.setValue(map_resolution-1)

        # fill parameter table with combo boxes for function selection and disable cells
        self._function_combo_boxes = {}
        for i_row in range(6):
            for i_col in range(5):
                self.ui.table_widget.setItem(i_row, i_col, QTableWidgetItem())
                if i_col == 0:
                    self._function_combo_boxes['function_' + str(i_row)] = QComboBox()
                    self._function_combo_boxes['function_' + str(i_row)].setObjectName('function_'+str(i_row))
                    self._function_combo_boxes['function_' + str(i_row)].addItem("Off")
                    self._function_combo_boxes['function_' + str(i_row)].addItem("Gau.")
                    self._function_combo_boxes['function_' + str(i_row)].addItem("Lor.")
                    self._function_combo_boxes['function_' + str(i_row)].addItem("Voi.")
                    self._function_combo_boxes['function_' + str(i_row)].currentIndexChanged.connect(self.cb_function_selected)
                    self.ui.table_widget.setCellWidget(i_row, i_col, self._function_combo_boxes['function_' + str(i_row)])
                else:
                    self.ui.table_widget.item(i_row, i_col).setFlags(Qt.NoItemFlags)

        # fill boundary tables
        for i_row in range(6):
            for i_col in range(4):
                self.ui.table_widget_2.setItem(i_row, i_col, QTableWidgetItem())
                self.ui.table_widget_3.setItem(i_row, i_col, QTableWidgetItem())
                self.ui.table_widget_2.item(i_row, i_col).setText('0')
                self.ui.table_widget_3.item(i_row, i_col).setText('Inf')

        # set parent
        self.setParent(parent)

        # link callbacks for radio buttons
        self.ui.focused_pixel_radio_button.toggled.connect(self.cb_radio_button_buttons)

        # link callbacks for sliders
        self.ui.lower_limit_slider.sliderPressed.connect(self.cb_limit_slider_pressed)
        self.ui.lower_limit_slider.sliderMoved.connect(self.cb_limit_slider_moved)
        self.ui.lower_limit_slider.sliderReleased.connect(self.cb_limit_slider_released)
        self.ui.upper_limit_slider.sliderPressed.connect(self.cb_limit_slider_pressed)
        self.ui.upper_limit_slider.sliderMoved.connect(self.cb_limit_slider_moved)
        self.ui.upper_limit_slider.sliderReleased.connect(self.cb_limit_slider_released)
        self.ui.lower_threshold_slider.sliderPressed.connect(self.cb_threshold_slider_pressed)
        self.ui.lower_threshold_slider.sliderMoved.connect(self.cb_threshold_slider_moved)
        self.ui.lower_threshold_slider.sliderReleased.connect(self.cb_threshold_slider_released)
        self.ui.upper_threshold_slider.sliderPressed.connect(self.cb_threshold_slider_pressed)
        self.ui.upper_threshold_slider.sliderMoved.connect(self.cb_threshold_slider_moved)
        self.ui.upper_threshold_slider.sliderReleased.connect(self.cb_threshold_slider_released)
        self.ui.area_slider_x1.sliderPressed.connect(self.cb_area_slider_pressed)
        self.ui.area_slider_x1.sliderMoved.connect(self.cb_area_slider_moved)
        self.ui.area_slider_x1.sliderReleased.connect(self.cb_area_slider_released)
        self.ui.area_slider_x2.sliderPressed.connect(self.cb_area_slider_pressed)
        self.ui.area_slider_x2.sliderMoved.connect(self.cb_area_slider_moved)
        self.ui.area_slider_x2.sliderReleased.connect(self.cb_area_slider_released)
        self.ui.area_slider_y1.sliderPressed.connect(self.cb_area_slider_pressed)
        self.ui.area_slider_y1.sliderMoved.connect(self.cb_area_slider_moved)
        self.ui.area_slider_y1.sliderReleased.connect(self.cb_area_slider_released)
        self.ui.area_slider_y2.sliderPressed.connect(self.cb_area_slider_pressed)
        self.ui.area_slider_y2.sliderMoved.connect(self.cb_area_slider_moved)
        self.ui.area_slider_y2.sliderReleased.connect(self.cb_area_slider_released)

        # link callbacks for buttons
        self.ui.clear_push_button.clicked.connect(self.cb_clear_push_button)
        self.ui.fit_push_button.clicked.connect(self.cb_fit_push_button)

    def cb_area_slider_moved(self):

        # update area map on the map canvas
        if self._map.get_dimension() == 2:
            self._app.windows['mapWindow'].ui.tab_widget.currentWidget().update_area_map(
                self.ui.area_slider_x1.value(), self.ui.area_slider_x2.value(),
                self.ui.area_slider_y1.value(), self.ui.area_slider_y2.value())
        else:
            return

    def cb_area_slider_pressed(self):

        # create area map on the map canvas
        if self._map.get_dimension() == 2:
            self._app.windows['mapWindow'].ui.tab_widget.currentWidget().create_area_map(
                self.ui.area_slider_x1.value(), self.ui.area_slider_x2.value(),
                self.ui.area_slider_y1.value(), self.ui.area_slider_y2.value())
        else:
            return

    def cb_area_slider_released(self):

        # remove area map from the map canvas
        self._app.windows['mapWindow'].ui.tab_widget.currentWidget().destroy_area_map()

        # bring this window to front again
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def cb_clear_push_button(self):

        if self.ui.focused_pixel_radio_button.isChecked():

            # clear fit of the focused pixel
            self._map.clear_fit(emit=True)

        else:

            # check dimension of the map
            if self._map.get_dimension() == 2:

                # get the area to be cleared
                if self.ui.area_slider_x2.value() < self.ui.area_slider_x1.value():
                    x2 = self.ui.area_slider_x1.value()
                    x1 = self.ui.area_slider_x2.value()
                else:
                    x1 = self.ui.area_slider_x1.value()
                    x2 = self.ui.area_slider_x2.value()
                if self.ui.area_slider_y2.value() < self.ui.area_slider_y1.value():
                    y2 = self.ui.area_slider_y1.value()
                    y1 = self.ui.area_slider_y2.value()
                else:
                    y1 = self.ui.area_slider_y1.value()
                    y2 = self.ui.area_slider_y2.value()
                fit_area = [x1, x2, y1, y2]

                # get the threshold and the threshold data
                threshold_data = self._map.get_data(data_index=self.ui.threshold_type_combo.currentIndex())
                min_data = numpy.min(threshold_data)
                max_data = numpy.max(threshold_data)
                lower_threshold = min_data+1./10000.*self.ui.lower_threshold_slider.value()*(max_data-min_data)
                upper_threshold = min_data+1./10000.*self.ui.upper_threshold_slider.value()*(max_data-min_data)

                # clear fits from the area which fulfills the threshold condition
                for ix in range(int(numpy.ceil(fit_area[0])), int(numpy.ceil(fit_area[1]))):

                    for iy in range(int(numpy.ceil(fit_area[2])), int(numpy.ceil(fit_area[3]))):

                        if lower_threshold <= threshold_data[ix, iy] <= upper_threshold:

                            # check if this is the last cleared fit in this column
                            if numpy.sum(numpy.logical_and(
                                            lower_threshold <= threshold_data[ix, iy:int(numpy.ceil(fit_area[3]))],
                                            threshold_data[ix, iy] <= upper_threshold)) == 1:
                                self._map.clear_fit(pixel=[ix, iy], emit=True)
                            else:
                                self._map.clear_fit(pixel=[ix, iy], emit=False)

                        # process events
                        self._app.processEvents()

            else:

                return

    def cb_fit_push_button(self):

        # get fit functions
        fit_functions = numpy.zeros(6)
        n_parameters = 0
        for i_peak in range(6):
            fit_functions[i_peak] = self._function_combo_boxes['function_'+str(i_peak)] .currentIndex()
            if fit_functions[i_peak] == 1 or fit_functions[i_peak] == 2:
                n_parameters += 3
            elif fit_functions[i_peak] == 3:
                n_parameters += 4

        # arrays for the submitted parameters
        fit_initial_parameters = numpy.zeros(n_parameters)
        fit_lower_boundaries = numpy.zeros(n_parameters)
        fit_upper_boundaries = numpy.zeros(n_parameters)

        # read array from table
        j_parameter = 0
        for i_peak in range(6):

            # check which columns need to be read
            parameters = []
            if fit_functions[i_peak] == 1:
                parameters = [1, 2, 3]
            elif fit_functions[i_peak] == 2:
                parameters = [1, 2, 4]
            elif fit_functions[i_peak] == 3:
                parameters = [1, 2, 3, 4]

            # read the parameters and boundaries
            for i_parameter in parameters:

                # read parameter
                try:
                    if 3 <= i_parameter <= 4:
                        fit_initial_parameters[j_parameter] = float(self.ui.table_widget.item(i_peak, i_parameter).text())/1000
                    else:
                        fit_initial_parameters[j_parameter] = float(self.ui.table_widget.item(i_peak, i_parameter).text())
                except ValueError:
                    parameter_names = ['I', 'ε', 'σ', 'γ']
                    subscripts = [u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086']
                    message_box = QMessageBox(self._app.windows['fittingWindow'])
                    message_box.setIcon(QMessageBox.Information)
                    message_box.setWindowTitle('Wrong parameter!')
                    message_box.setText('Could not read parameter '+parameter_names[i_parameter-1]+subscripts[i_peak])
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                    return

                # read lower boundary
                try:
                    if 3 <= i_parameter <= 4:
                        fit_lower_boundaries[j_parameter] = float(self.ui.table_widget_2.item(i_peak, i_parameter-1).text())/1000
                    else:
                        fit_lower_boundaries[j_parameter] = float(self.ui.table_widget_2.item(i_peak, i_parameter-1).text())
                except ValueError:
                    parameter_names = ['I', 'ε', 'σ', 'γ']
                    subscripts = [u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086']
                    message_box = QMessageBox(self._app.windows['fittingWindow'])
                    message_box.setIcon(QMessageBox.Information)
                    message_box.setWindowTitle('Wrong boundary!')
                    message_box.setText('Could not read lower boundary for '+parameter_names[i_parameter-1]+subscripts[i_peak])
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                    return

                # read upper boundary
                try:
                    if 3 <= i_parameter <= 4:
                        fit_upper_boundaries[j_parameter] = float(self.ui.table_widget_3.item(i_peak, i_parameter-1).text())/1000
                    else:
                        fit_upper_boundaries[j_parameter] = float(self.ui.table_widget_3.item(i_peak, i_parameter-1).text())
                except ValueError:
                    parameter_names = ['I', 'ε', 'σ', 'γ']
                    subscripts = [u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086']
                    message_box = QMessageBox(self._app.windows['fittingWindow'])
                    message_box.setIcon(QMessageBox.Information)
                    message_box.setWindowTitle('Wrong boundary!')
                    message_box.setText('Could not read upper boundary for '+parameter_names[i_parameter-1]+subscripts[i_peak])
                    message_box.setStandardButtons(QMessageBox.Ok)
                    message_box.exec_()
                    return
                j_parameter += 1

        # define fit function
        def fit_function(x, *p):
            result = numpy.zeros(len(x))
            k_parameter = 0
            for k_peak in range(len(fit_functions)):
                if fit_functions[k_peak] == 1:
                    result = result + fitting.gaussian(x, *p[k_parameter:k_parameter+3])
                    k_parameter += 3
                elif fit_functions[k_peak] == 2:
                    result = result + fitting.lorentzian(x, *p[k_parameter:k_parameter+3])
                    k_parameter += 3
                elif fit_functions[k_peak] == 3:
                    result = result + fitting.voigt(x, *p[k_parameter:k_parameter+4])
                    k_parameter += 4
            return result

        # check if only one or multiple pixels are to be fitted
        if self.ui.focused_pixel_radio_button.isChecked():

            # load spectrum
            spectrum = self._map.get_spectrum()

            # perform fit
            try:
                fit_optimized_parameters, covariance = curve_fit(fit_function,
                                                                 spectrum[
                                                                    self.ui.lower_limit_slider.value():
                                                                    self.ui.upper_limit_slider.value(), 0],
                                                                 spectrum[
                                                                    self.ui.lower_limit_slider.value():
                                                                    self.ui.upper_limit_slider.value(), 1],
                                                                 p0=fit_initial_parameters,
                                                                 bounds=(fit_lower_boundaries, fit_upper_boundaries))
                # save fit
                self._map.set_fit(fit_functions, fit_initial_parameters, fit_optimized_parameters, emit=True)
            except RuntimeError:
                message_box = QMessageBox(self._app.windows['fittingWindow'])
                message_box.setIcon(QMessageBox.Information)
                message_box.setWindowTitle('Fitting failed!')
                message_box.setText('Fitting failed for focused pixel!')
                message_box.setStandardButtons(QMessageBox.Ok)
                message_box.exec_()
            
        else:

            if self._map.get_dimension() == 2:

                # get the area to fit
                if self.ui.area_slider_x2.value() < self.ui.area_slider_x1.value():
                    x2 = self.ui.area_slider_x1.value()
                    x1 = self.ui.area_slider_x2.value()
                else:
                    x1 = self.ui.area_slider_x1.value()
                    x2 = self.ui.area_slider_x2.value()
                if self.ui.area_slider_y2.value() < self.ui.area_slider_y1.value():
                    y2 = self.ui.area_slider_y1.value()
                    y1 = self.ui.area_slider_y2.value()
                else:
                    y1 = self.ui.area_slider_y1.value()
                    y2 = self.ui.area_slider_y2.value()
                fit_area = [x1, x2, y1, y2]

                # threshold settings
                threshold_data = self._map.get_data(data_index=self.ui.threshold_type_combo.currentIndex())
                min_data = numpy.min(threshold_data)
                max_data = numpy.max(threshold_data)
                lower_threshold = min_data+1./10000.*self.ui.lower_threshold_slider.value()*(max_data-min_data)
                upper_threshold = min_data+1./10000.*self.ui.upper_threshold_slider.value()*(max_data-min_data)

                # get existing fit functions in order to check for already fitted pixels
                existing_fit_functions = self._map.get_fit_functions()

                # number of pixels to fit
                n_pixels = numpy.count_nonzero(numpy.logical_and(
                        lower_threshold <= threshold_data[int(numpy.ceil(fit_area[0])):1+int(numpy.floor(fit_area[1])), int(numpy.ceil(fit_area[2])):1+int(numpy.floor(fit_area[3]))],
                        upper_threshold >= threshold_data[int(numpy.ceil(fit_area[0])):1+int(numpy.floor(fit_area[1])), int(numpy.ceil(fit_area[2])):1+int(numpy.floor(fit_area[3]))]))

                # create progressbar dialog
                progress_dialog = QProgressDialog('', '', 0, n_pixels, self._app.windows['fittingWindow'])
                progress_dialog.setWindowTitle('Fitting')
                progress_dialog.setWindowModality(Qt.WindowModal)
                progress_dialog_cancel_button = QPushButton('Stop')
                progress_dialog.setCancelButton(progress_dialog_cancel_button)
                progress_dialog.show()

                # start fitting
                i_px = 0

                for ix in range(int(numpy.ceil(fit_area[0])), 1+int(numpy.floor(fit_area[1]))):

                    # check if process was canceled
                    if progress_dialog.wasCanceled():
                        break

                    for iy in range(int(numpy.ceil(fit_area[2])), 1+int(numpy.floor(fit_area[3]))):

                        # check if process was canceled
                        if progress_dialog.wasCanceled():
                            break

                        # check if pixel is within threshold area
                        if lower_threshold <= threshold_data[ix, iy] <= upper_threshold:

                            # check if pixel is already fitted
                            if self.ui.overwrite_check_box.isChecked() or \
                                            numpy.sum(existing_fit_functions[ix, iy, :]) == 0:

                                # load spectrum
                                spectrum = self._map.get_spectrum(pixel=[ix, iy])

                                # get parameters from neighbours
                                if self.ui.neighbour_check_box.isChecked():

                                    # define order in which to look for neighbours
                                    neighbours = [[[ix-1, iy], [ix+1, iy], [ix, iy-1], [ix, iy+1]],
                                                  [[ix-1, iy-1], [ix-1, iy+1], [ix+1, iy-1], [ix+1, iy+1]],
                                                  [[ix-2, iy], [ix+2, iy], [ix, iy-2], [ix, iy+2]],
                                                  [[ix-1, iy-2], [ix-1, iy+2], [ix+1, iy-2], [ix+1, iy+2], [ix-2, iy-1], [ix-2, iy+1], [ix+2, iy-1], [ix+2, iy+1]]]

                                    # counter for suitable neighbours
                                    n_neighbours = 0

                                    # averaged neighbour parameters
                                    parameters_neighbours = numpy.zeros(n_parameters)

                                    # iterate neighbour orders: check first closest neighbours, then second closest neighbours ...
                                    for i_neighbour_order in range(len(neighbours)):

                                        for i_neighbour in range(len(neighbours[i_neighbour_order])):

                                            # check if potential neighbour is on map
                                            if neighbours[i_neighbour_order][i_neighbour][0] < 0 or neighbours[i_neighbour_order][i_neighbour][0] >= self._map.get_size()[0]:
                                                break
                                            if neighbours[i_neighbour_order][i_neighbour][1] < 0 or neighbours[i_neighbour_order][i_neighbour][1] >= self._map.get_size()[1]:
                                                break

                                            # get fit functions from neighbour
                                            fit_functions_neighbour = self._map.get_fit_functions(pixel=neighbours[i_neighbour_order][i_neighbour])

                                            # check if fit functions are the same as the current ones
                                            if (fit_functions == fit_functions_neighbour).all():

                                                # get parameters at neighbour pixel
                                                parameters_neighbour = self._map.get_fit_parameters(pixel=neighbours[i_neighbour_order][i_neighbour])
                                                j_parameter = 0
                                                for neighbour_peak in range(6):
                                                    if 1 <= fit_functions_neighbour[neighbour_peak] <= 2:
                                                        parameters_neighbours[j_parameter:j_parameter+3] += parameters_neighbour[neighbour_peak, 0:3]
                                                        j_parameter += 3
                                                    elif fit_functions_neighbour[neighbour_peak] == 3:
                                                        parameters_neighbours[j_parameter:j_parameter+4] += parameters_neighbour[neighbour_peak, 0:4]
                                                        j_parameter += 4
                                                n_neighbours += 1

                                        # if at least one neighbour was found do not look at higher neighbor orders
                                        if n_neighbours > 0:
                                            break

                                    # if a neighbour was found, take the neighbour parameters, otherwise initial parameters
                                    if n_neighbours > 0:
                                        parameters_neighbours /= n_neighbours
                                        start_parameters = parameters_neighbours
                                    else:
                                        start_parameters = fit_initial_parameters

                                # if neighbour function is not checked
                                else:
                                    start_parameters = fit_initial_parameters

                                # perform fit
                                try:
                                    fit_optimized_parameters, covariance = curve_fit(
                                        fit_function,
                                        spectrum[self.ui.lower_limit_slider.value():self.ui.upper_limit_slider.value(), 0],
                                        spectrum[self.ui.lower_limit_slider.value():self.ui.upper_limit_slider.value(), 1],
                                        p0=start_parameters, bounds=(fit_lower_boundaries, fit_upper_boundaries))

                                    # check if this is the last cleared fit in this column
                                    if numpy.sum(numpy.logical_and(
                                                    lower_threshold <= threshold_data[ix, iy:1+int(numpy.floor(fit_area[3]))],
                                                    threshold_data[ix, iy] <= upper_threshold)) == 1:
                                        # save fit
                                        self._map.set_fit(fit_functions, start_parameters, fit_optimized_parameters,
                                                          pixel=[ix, iy], emit=True)
                                    else:
                                        # save fit
                                        self._map.set_fit(fit_functions, start_parameters, fit_optimized_parameters,
                                                          pixel=[ix, iy], emit=False)

                                except RuntimeError:
                                    message_box = QMessageBox(self._app.windows['fittingWindow'])
                                    message_box.setIcon(QMessageBox.Information)
                                    message_box.setWindowTitle('Fitting failed!')
                                    message_box.setText('Fitting failed for pixel ('+str(ix)+','+str(iy)+')')
                                    message_box.addButton('Continue Fitting', QMessageBox.AcceptRole)
                                    message_box.addButton('Stop Fitting', QMessageBox.AcceptRole)
                                    message_box.exec_()
                                    if message_box.result() == 1:
                                        progress_dialog.close()
                                        return

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            i_px += 1
                            progress_dialog.setValue(i_px)

            else:

                return
        
    def cb_function_selected(self, index):

        # get the peak number of the changed function
        i_peak = int(self.sender().objectName()[-1])

        # check which function has been selected and update the table flags accordingly
        if index == 0:

            # peak has been turned off
            for i_row in range(1, 5):
                self.ui.table_widget.item(i_peak, i_row).setFlags(Qt.NoItemFlags)

        elif index == 1:

            # gaussian  has been selected
            for i_row in range(1, 4):
                self.ui.table_widget.item(i_peak, i_row).setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.ui.table_widget.item(i_peak, 4).setFlags(Qt.NoItemFlags)

        elif index == 2:

            # lorentzian has been selected
            for i_row in range(1, 3):
                self.ui.table_widget.item(i_peak, i_row).setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
            self.ui.table_widget.item(i_peak, 3).setFlags(Qt.NoItemFlags)
            self.ui.table_widget.item(i_peak, 4).setFlags(
                Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)

        elif index == 3:

            # voigt has been selected
            for i_row in range(1, 5):
                self.ui.table_widget.item(i_peak, i_row).setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)

    def cb_limit_slider_moved(self):

        # update cursor on the spectrum canvas
        self._app.windows['spectrumWindow'].get_current_widget().update_cursors(self.ui.lower_limit_slider.value(),
                                                                                self.ui.upper_limit_slider.value())

    def cb_limit_slider_pressed(self):

        # create cursor on the spectrum canvas
        self._app.windows['spectrumWindow'].get_current_widget().create_cursors(self.ui.lower_limit_slider.value(),
                                                                                self.ui.upper_limit_slider.value())

    def cb_limit_slider_released(self):

        # remove cursor from the spectrum canvas
        self._app.windows['spectrumWindow'].get_current_widget().destroy_cursors()

        # bring window to front
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def cb_radio_button_buttons(self):

        # check which radio button is clicked
        if self.ui.focused_pixel_radio_button.isChecked():

            self.ui.threshold_type_combo.setEnabled(False)
            self.ui.lower_threshold_slider.setEnabled(False)
            self.ui.upper_threshold_slider.setEnabled(False)
            self.ui.area_slider_x1.setEnabled(False)
            self.ui.area_slider_x2.setEnabled(False)
            self.ui.area_slider_y1.setEnabled(False)
            self.ui.area_slider_y2.setEnabled(False)
            self.ui.overwrite_check_box.setEnabled(False)
            self.ui.neighbour_check_box.setEnabled(False)

        elif self.ui.multiple_pixels_radio_button.isChecked():

            self.ui.threshold_type_combo.setEnabled(True)
            self.ui.lower_threshold_slider.setEnabled(True)
            self.ui.upper_threshold_slider.setEnabled(True)
            self.ui.area_slider_x1.setEnabled(True)
            self.ui.area_slider_x2.setEnabled(True)
            if self._map.get_dimension() == 2:
                self.ui.area_slider_y1.setEnabled(True)
                self.ui.area_slider_y2.setEnabled(True)
            self.ui.overwrite_check_box.setEnabled(True)
            self.ui.neighbour_check_box.setEnabled(True)

    def cb_threshold_slider_moved(self):

        # get threshold data and calculate threshold value
        if self._map.get_dimension() == 2:
            data = self._map.get_data(data_index=self.ui.threshold_type_combo.currentIndex())
        else:
            data = self._map.get_data(data_index=1+self.ui.threshold_type_combo.currentIndex())
        min_data = numpy.min(data)
        max_data = numpy.max(data)
        lower_threshold = min_data+1./10000.*self.ui.lower_threshold_slider.value()*(max_data-min_data)
        upper_threshold = min_data+1./10000.*self.ui.upper_threshold_slider.value()*(max_data-min_data)
        # update threshold map on map canvas
        self._app.windows['mapWindow'].ui.tab_widget.currentWidget().update_threshold_map(
            data, [lower_threshold, upper_threshold])

        # update tool tip for the threshold value
        if self.sender() == self.ui.lower_threshold_slider:
            QToolTip.showText(QCursor.pos(), str(lower_threshold), self.ui.lower_threshold_slider)
        else:
            QToolTip.showText(QCursor.pos(), str(upper_threshold), self.ui.upper_threshold_slider)

    def cb_threshold_slider_pressed(self):

        # get threshold data and calculate threshold value
        if self._map.get_dimension() == 2:
            data = self._map.get_data(data_index=self.ui.threshold_type_combo.currentIndex())
        else:
            data = self._map.get_data(data_index=1+self.ui.threshold_type_combo.currentIndex())
        min_data = numpy.min(data)
        max_data = numpy.max(data)
        lower_threshold = min_data+1./10000.*self.ui.lower_threshold_slider.value()*(max_data-min_data)
        upper_threshold = min_data+1./10000.*self.ui.upper_threshold_slider.value()*(max_data-min_data)

        # create threshold map on map canvas
        self._app.windows['mapWindow'].ui.tab_widget.currentWidget().create_threshold_map(
            data, [lower_threshold, upper_threshold])

        # create tool tip for the threshold value
        if self.sender() == self.ui.lower_threshold_slider:
            QToolTip.showText(QCursor.pos(), str(lower_threshold), self.ui.lower_threshold_slider)
        else:
            QToolTip.showText(QCursor.pos(), str(upper_threshold), self.ui.upper_threshold_slider)

    def cb_threshold_slider_released(self):

        # destroy threshold map from the map canvas
        self._app.windows['mapWindow'].ui.tab_widget.currentWidget().destroy_threshold_map()

        # bring window to front
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()


class FittingWindow(QMainWindow):

    """
    FittingWindow
    The fitting window hosts a fitting widget for each loaded map.
    """

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # dictionary for fitting widgets
        self._fitting_widgets = {}

        # set fixed size
        self.setFixedWidth(350)
        self.setFixedHeight(600)

        # set window title
        self.setWindowTitle("Fitting")

    def add_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # add a widget to the widgets list
        self._fitting_widgets[map_handle.get_id()] = FittingWidget(self, map_handle)

    def change_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # hide all widgets
        for key in self._fitting_widgets.keys():
            self._fitting_widgets[key].setVisible(False)

        # make the widget for the select map visible
        self._fitting_widgets[map_handle.get_id()].setVisible(True)

    def remove_widget(self, map_id):

        # remove the widget of the deleted map
        self._fitting_widgets[map_id].setParent(None)
        self._fitting_widgets[map_id].deleteLater()
        del self._fitting_widgets[map_id]

        # close the window if there are no more maps
        if len(self._fitting_widgets) == 0:
            self.close()
