# general imports
import numpy
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QProgressDialog, QPushButton, QMainWindow, QWidget
# import UI
from UIs.backgroundWidgetUi import UiBackgroundWidget


class BackgroundWidget(QWidget):

    def __init__(self, parent, map_handle):

        # call widget init
        super().__init__()

        # link app
        self._app = QApplication.instance()

        # link map handle
        self._map = map_handle

        # set object name
        self.setObjectName("backgroundWidget" + str(self._map.get_id()))

        # load and set up UI
        self.ui = UiBackgroundWidget(self)

        # set limits to for the interval selection
        self.ui.lower_boundary_slider.setMaximum(self._map.get_resolution()-1)
        self.ui.upper_boundary_slider.setMaximum(self._map.get_resolution()-1)
        self.ui.upper_boundary_slider.setValue(self._map.get_resolution()-1)

        # fill combo boxes for pixel selection
        self.ui.x_spin_box.setMaximum(self._map.get_size()[0]-1)
        if self._map.get_dimension() == 2:
            self.ui.y_spin_box.setMaximum(self._map.get_size()[1]-1)

        # set parent
        self.setParent(parent)

        # link callbacks for radio buttons
        self.ui.minimum_counts_radio.toggled.connect(self.cb_background_settings_buttons)
        self.ui.interval_average_radio.toggled.connect(self.cb_background_settings_buttons)
        self.ui.background_from_pixel_radio.toggled.connect(self.cb_background_settings_buttons)
        self.ui.background_from_file_radio.toggled.connect(self.cb_background_settings_buttons)

        # link callbacks for sliders
        self.ui.lower_boundary_slider.sliderPressed.connect(self.cb_slider_pressed)
        self.ui.lower_boundary_slider.sliderMoved.connect(self.cb_slider_moved)
        self.ui.lower_boundary_slider.sliderReleased.connect(self.cb_slider_released)
        self.ui.upper_boundary_slider.sliderPressed.connect(self.cb_slider_pressed)
        self.ui.upper_boundary_slider.sliderMoved.connect(self.cb_slider_moved)
        self.ui.upper_boundary_slider.sliderReleased.connect(self.cb_slider_released)

        # link callback for button
        self.ui.file_browse_button.clicked.connect(self.cb_file_browse_button)
        self.ui.remove_background_button.clicked.connect(self.cb_remove_background_button)
                
    def cb_background_settings_buttons(self):

        # check which radio button is clicked and enable or disable the respective UI elements
        if self.ui.minimum_counts_radio.isChecked():

            self.ui.lower_boundary_slider.setEnabled(False)
            self.ui.upper_boundary_slider.setEnabled(False)
            self.ui.x_spin_box.setEnabled(False)
            self.ui.y_spin_box.setEnabled(False)
            self.ui.file_browse_button.setEnabled(False)
            self.ui.file_path_line_edit.setEnabled(False)

        elif self.ui.interval_average_radio.isChecked():

            self.ui.lower_boundary_slider.setEnabled(True)
            self.ui.upper_boundary_slider.setEnabled(True)
            self.ui.x_spin_box.setEnabled(False)
            self.ui.y_spin_box.setEnabled(False)
            self.ui.file_browse_button.setEnabled(False)
            self.ui.file_path_line_edit.setEnabled(False)

        elif self.ui.background_from_pixel_radio.isChecked():

            self.ui.lower_boundary_slider.setEnabled(False)
            self.ui.upper_boundary_slider.setEnabled(False)
            self.ui.x_spin_box.setEnabled(True)
            if self._map.get_dimension() == 2:
                self.ui.y_spin_box.setEnabled(True)
            self.ui.file_browse_button.setEnabled(False)
            self.ui.file_path_line_edit.setEnabled(False)

        elif self.ui.background_from_file_radio.isChecked():

            self.ui.lower_boundary_slider.setEnabled(False)
            self.ui.upper_boundary_slider.setEnabled(False)
            self.ui.x_spin_box.setEnabled(False)
            self.ui.y_spin_box.setEnabled(False)
            self.ui.file_browse_button.setEnabled(True)
            self.ui.file_path_line_edit.setEnabled(True)

    def cb_file_browse_button(self):

        # get file name
        file_name = QFileDialog.getOpenFileName(self._app.windows['backgroundWindow'], 'Select File', '')
        file_name = file_name[0]
        self.ui.file_path_line_edit.setText(file_name)

    def cb_remove_background_button(self):
        
        # remove background on focused pixel
        if self.ui.focused_pixel_radio.isChecked():
            
            # load spectrum
            spectrum = self._map.get_spectrum()
            
            if self.ui.minimum_counts_radio.isChecked():

                # remove minimum as a background
                spectrum[:, 1] = spectrum[:, 1]-numpy.min(spectrum[:, 1])
                
            elif self.ui.interval_average_radio.isChecked():

                # remove interval average as a background
                spectrum[:, 1] = spectrum[:, 1]-numpy.mean(
                    spectrum[self.ui.lower_boundary_slider.value():self.ui.upper_boundary_slider.value(), 1])

            elif self.ui.background_from_pixel_radio.isChecked():

                # remove spectrum at specific pixel as a background
                spectrum[:, 1] = spectrum[:, 1]-self._map.get_spectrum(
                    pixel=[self.ui.x_spin_box.value(), self.ui.y_spin_box.value()])[:, 1]

            elif self.ui.background_from_file_radio.isChecked():

                # remove spectrum from file as a background
                background = numpy.loadtxt(self.ui.file_path_line_edit.text())
                spectrum[:, 1] = spectrum[:, 1]-background[:, 1]

            # update spectrum
            self._map.set_spectrum(spectrum)
                
        # remove background on whole map
        else:

            # check the dimension of the map TODO: check the 1D section (e.g. add live plot updates)
            if self._map.get_dimension() == 1:

                # get map size
                nx = self._map.get_size()[0]

                # create progressbar dialog
                progress_dialog = QProgressDialog('', '', 0, nx, self._app.windows['backgroundWindow'])
                progress_dialog.setWindowTitle('Removing Background')
                progress_dialog.setWindowModality(Qt.WindowModal)
                progress_dialog_cancel_button = QPushButton('Stop')
                progress_dialog.setCancelButton(progress_dialog_cancel_button)
                progress_dialog.show()

                # remove background on each pixel
                if self.ui.minimum_counts_radio.isChecked():

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        # load spectrum
                        spectrum = self._map.get_spectrum(pixel=ix)

                        # remove minimum as a background
                        spectrum[:, 1] = spectrum[:, 1]-numpy.min(spectrum[:, 1])

                        # update spectrum
                        self._map.set_spectrum(spectrum, pixel=ix)

                        # update progress bar
                        progress_dialog.setValue(ix + 1)

                elif self.ui.interval_average_radio.isChecked():

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        # load spectrum
                        spectrum = self._map.get_spectrum(pixel=ix)

                        # remove interval average as a background
                        spectrum[:, 1] = spectrum[:, 1]-numpy.mean(
                            spectrum[self.ui.lower_boundary_slider.value():self.ui.upper_boundary_slider.value(), 1])

                        # update spectrum
                        self._map.set_spectrum(spectrum, pixel=ix)

                        # update progress bar
                        progress_dialog.setValue(ix + 1)

                elif self.ui.background_from_pixel_radio.isChecked():

                    background = numpy.copy(self._map.get_spectrum(pixel=self.ui.x_spin_box.value())[:, 1])

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        # load spectrum
                        spectrum = self._map.get_spectrum(pixel=ix)

                        # remove spectrum at specific pixel as a background
                        spectrum[:, 1] = spectrum[:, 1] - background
                        # update spectrum
                        self._map.set_spectrum(spectrum, pixel=ix)

                        # update progress bar
                        progress_dialog.setValue(ix + 1)

                elif self.ui.background_from_file_radio.isChecked():

                    background = numpy.loadtxt(self.ui.file_path_line_edit.text())

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        # load spectrum
                        spectrum = self._map.get_spectrum(pixel=ix)

                        # remove spectrum from file as a background
                        spectrum[:, 1] = spectrum[:, 1]-background[:, 1]

                        # update spectrum
                        self._map.set_spectrum(spectrum, pixel=ix)

                        # update progress bar
                        progress_dialog.setValue(ix + 1)

            elif self._map.get_dimension() == 2:

                # get map size
                nx, ny = self._map.get_size()

                # create progressbar dialog
                progress_dialog = QProgressDialog('', '', 0, nx * ny, self._app.windows['backgroundWindow'])
                progress_dialog.setWindowTitle('Removing Background')
                progress_dialog.setWindowModality(Qt.WindowModal)
                progress_dialog_cancel_button = QPushButton('Stop')
                progress_dialog.setCancelButton(progress_dialog_cancel_button)
                progress_dialog.show()

                # remove background on each pixel
                if self.ui.minimum_counts_radio.isChecked():

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove minimum as a background
                            spectrum[:, 1] = spectrum[:, 1]-numpy.min(spectrum[:, 1])

                            # update spectrum
                            self._map.set_spectrum(spectrum, pixel=[ix, iy])

                            # update background information window and spectrum window
                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:
                                self._app.windows['spectrumWindow'].update()
                                self._app.windows['pixelInformationWindow'].update()

                            # update map window
                            if self._map.get_data_selected() == 0:
                                self._app.windows['mapWindow'].update_data()

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

                elif self.ui.interval_average_radio.isChecked():

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove interval average as a background
                            spectrum[:, 1] = spectrum[:, 1]-numpy.mean(
                                spectrum[self.ui.lower_boundary_slider.value():self.ui.upper_boundary_slider.value(), 1])

                            # update spectrum
                            self._map.set_spectrum(spectrum, pixel=[ix, iy])

                            # update background information window and spectrum window
                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:
                                self._app.windows['spectrumWindow'].update()
                                self._app.windows['pixelInformationWindow'].update()

                            # update map window
                            if self._map.get_data_selected() == 0:
                                self._app.windows['mapWindow'].update_data()

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

                elif self.ui.background_from_pixel_radio.isChecked():

                    background = numpy.copy(self._map.get_spectrum(pixel=[self.ui.x_spin_box.value(),
                                                                          self.ui.y_spin_box.value()])[:, 1])

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove spectrum at specific pixel as a background
                            spectrum[:, 1] = spectrum[:, 1] - background

                            # update spectrum
                            self._map.set_spectrum(spectrum, pixel=[ix, iy])

                            # update background information window and spectrum window
                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:
                                self._app.windows['spectrumWindow'].update()
                                self._app.windows['pixelInformationWindow'].update()

                            # update map window
                            if self._map.get_data_selected() == 0:
                                self._app.windows['mapWindow'].update_data()

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

                elif self.ui.background_from_file_radio.isChecked():

                    background = numpy.loadtxt(self.ui.file_path_line_edit.text())

                    for ix in range(nx):

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove spectrum from file as a background
                            spectrum[:, 1] = spectrum[:, 1]-background[:, 1]

                            # update spectrum
                            self._map.set_spectrum(spectrum, pixel=[ix, iy])

                            # update background information window and spectrum window
                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:
                                self._app.windows['spectrumWindow'].update()
                                self._app.windows['pixelInformationWindow'].update()

                            # update map window
                            if self._map.get_data_selected() == 0:
                                self._app.windows['mapWindow'].update_data()

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

        # update windows
        self._app.windows['spectrumWindow'].update()
        self._app.windows['pixelInformationWindow'].update()
        self._app.windows['mapWindow'].update_data()

    def cb_slider_moved(self):

        self._app.windows['spectrumWindow'].update_cursors(self.ui.lower_boundary_slider.value(),
                                                           self.ui.upper_boundary_slider.value())

    def cb_slider_pressed(self):

        self._app.windows['spectrumWindow'].create_cursors(self.ui.lower_boundary_slider.value(),
                                                           self.ui.upper_boundary_slider.value())

    def cb_slider_released(self):

        self._app.windows['spectrumWindow'].destroy_cursors()

        # bring window to front
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()


class BackgroundWindow(QMainWindow):

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # dictionary for remove background widgets
        self._background_widgets = {}

        # set fixed size
        self.setFixedWidth(320)
        self.setFixedHeight(321)

        # set window title
        self.setWindowTitle("Remove Background")

    def update(self):

        # check if the selected map already has a widget
        map_handle = self._app.maps.get_selected_map()
        if map_handle.get_id() not in self._background_widgets.keys():
            self._background_widgets[map_handle.get_id()] = BackgroundWidget(self, map_handle)
        if not self._background_widgets[map_handle.get_id()].isVisible():
            for key in self._background_widgets.keys():
                self._background_widgets[key].setVisible(False)
            self._background_widgets[map_handle.get_id()].setVisible(True)
