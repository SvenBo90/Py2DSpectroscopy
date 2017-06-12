# general imports
import numpy
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QProgressDialog, QPushButton, QMainWindow, QWidget
# import UI
from UIs.backgroundWidgetUi import UiBackgroundWidget


class BackgroundWidget(QWidget):

    """
    BackgroundWidget
    This widget is used to remove background from a single pixel or the whole map.
    """

    # TODO: implement 1D maps

    def __init__(self, parent, map_handle):

        # call widget init
        super().__init__()

        # link app
        self._app = QApplication.instance()

        # link map handle
        self._map = map_handle

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
        self.ui.minimum_counts_radio_button.toggled.connect(self.cb_background_settings_buttons)
        self.ui.interval_average_radio_button.toggled.connect(self.cb_background_settings_buttons)
        self.ui.background_from_pixel_radio_button.toggled.connect(self.cb_background_settings_buttons)
        self.ui.background_from_file_radio_button.toggled.connect(self.cb_background_settings_buttons)

        # link callbacks for sliders
        self.ui.lower_boundary_slider.sliderPressed.connect(self.cb_boundary_slider_pressed)
        self.ui.lower_boundary_slider.sliderMoved.connect(self.cb_boundary_slider_moved)
        self.ui.lower_boundary_slider.sliderReleased.connect(self.cb_boundary_slider_released)
        self.ui.upper_boundary_slider.sliderPressed.connect(self.cb_boundary_slider_pressed)
        self.ui.upper_boundary_slider.sliderMoved.connect(self.cb_boundary_slider_moved)
        self.ui.upper_boundary_slider.sliderReleased.connect(self.cb_boundary_slider_released)

        # link callback for button
        self.ui.file_browse_push_button.clicked.connect(self.cb_file_browse_push_button)
        self.ui.remove_background_push_button.clicked.connect(self.cb_remove_background_push_button)
                
    def cb_background_settings_buttons(self):

        # check which radio button is clicked and enable or disable the respective UI elements
        if self.ui.minimum_counts_radio_button.isChecked():

            self.ui.lower_boundary_slider.setEnabled(False)
            self.ui.upper_boundary_slider.setEnabled(False)
            self.ui.x_spin_box.setEnabled(False)
            self.ui.y_spin_box.setEnabled(False)
            self.ui.file_browse_push_button.setEnabled(False)
            self.ui.file_path_line_edit.setEnabled(False)

        elif self.ui.interval_average_radio_button.isChecked():

            self.ui.lower_boundary_slider.setEnabled(True)
            self.ui.upper_boundary_slider.setEnabled(True)
            self.ui.x_spin_box.setEnabled(False)
            self.ui.y_spin_box.setEnabled(False)
            self.ui.file_browse_push_button.setEnabled(False)
            self.ui.file_path_line_edit.setEnabled(False)

        elif self.ui.background_from_pixel_radio_button.isChecked():

            self.ui.lower_boundary_slider.setEnabled(False)
            self.ui.upper_boundary_slider.setEnabled(False)
            self.ui.x_spin_box.setEnabled(True)
            if self._map.get_dimension() == 2:
                self.ui.y_spin_box.setEnabled(True)
            self.ui.file_browse_push_button.setEnabled(False)
            self.ui.file_path_line_edit.setEnabled(False)

        elif self.ui.background_from_file_radio_button.isChecked():

            self.ui.lower_boundary_slider.setEnabled(False)
            self.ui.upper_boundary_slider.setEnabled(False)
            self.ui.x_spin_box.setEnabled(False)
            self.ui.y_spin_box.setEnabled(False)
            self.ui.file_browse_push_button.setEnabled(True)
            self.ui.file_path_line_edit.setEnabled(True)

    def cb_file_browse_push_button(self):

        # get file name
        file_name = QFileDialog.getOpenFileName(self._app.windows['backgroundWindow'], 'Select File', '')
        file_name = file_name[0]

        # check if a file has been selected
        if file_name == '':
            return

        # set file name to line edit
        self.ui.file_path_line_edit.setText(file_name)

    def cb_remove_background_push_button(self):
        
        # remove background on focused pixel
        if self.ui.focused_pixel_radio_button.isChecked():
            
            # load spectrum
            spectrum = self._map.get_spectrum()
            
            if self.ui.minimum_counts_radio_button.isChecked():

                # remove minimum as a background
                spectrum[:, 1] = spectrum[:, 1]-numpy.min(spectrum[:, 1])
                
            elif self.ui.interval_average_radio_button.isChecked():

                # remove interval average as a background
                spectrum[:, 1] = spectrum[:, 1]-numpy.mean(
                    spectrum[self.ui.lower_boundary_slider.value():self.ui.upper_boundary_slider.value(), 1])

            elif self.ui.background_from_pixel_radio_button.isChecked():

                # remove spectrum at specific pixel as a background
                spectrum[:, 1] = spectrum[:, 1]-self._map.get_spectrum(
                    pixel=[self.ui.x_spin_box.value(), self.ui.y_spin_box.value()])[:, 1]

            elif self.ui.background_from_file_radio_button.isChecked():

                # remove spectrum from file as a background
                background = numpy.loadtxt(self.ui.file_path_line_edit.text())
                spectrum[:, 1] = spectrum[:, 1]-background[:, 1]

            # update spectrum
            self._map.set_spectrum(spectrum, emit=True)
                
        # remove background on whole map
        else:

            # check the dimension of the map
            if self._map.get_dimension() == 1:

                return

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

                # start live plotting
                self._app.start_live_plotting()

                # remove background on each pixel
                if self.ui.minimum_counts_radio_button.isChecked():

                    for ix in range(nx):

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove minimum as a background
                            spectrum[:, 1] = spectrum[:, 1]-numpy.min(spectrum[:, 1])

                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=True)

                            else:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=False)

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                elif self.ui.interval_average_radio_button.isChecked():

                    for ix in range(nx):

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove interval average as a background
                            spectrum[:, 1] = spectrum[:, 1]-numpy.mean(
                                spectrum[self.ui.lower_boundary_slider.value():self.ui.upper_boundary_slider.value(), 1])

                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=True)

                            else:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=False)

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                elif self.ui.background_from_pixel_radio_button.isChecked():

                    background = numpy.copy(self._map.get_spectrum(pixel=[self.ui.x_spin_box.value(),
                                                                          self.ui.y_spin_box.value()])[:, 1])

                    for ix in range(nx):

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove spectrum at specific pixel as a background
                            spectrum[:, 1] = spectrum[:, 1] - background

                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=True)

                            else:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=False)

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                elif self.ui.background_from_file_radio_button.isChecked():

                    background = numpy.loadtxt(self.ui.file_path_line_edit.text())

                    for ix in range(nx):

                        for iy in range(ny):

                            # check if process was cancelled
                            if progress_dialog.wasCanceled():
                                break

                            # load spectrum
                            spectrum = self._map.get_spectrum(pixel=[ix, iy])

                            # remove spectrum from file as a background
                            spectrum[:, 1] = spectrum[:, 1]-background[:, 1]

                            if ix == self._map.get_focus()[0] and iy == self._map.get_focus()[1]:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=True)

                            else:

                                # update spectrum
                                self._map.set_spectrum(spectrum, pixel=[ix, iy], emit=False)

                            # process events
                            self._app.processEvents()

                            # update progress bar
                            progress_dialog.setValue(ix * ny + iy + 1)

                        # check if process was cancelled
                        if progress_dialog.wasCanceled():
                            break

                # stop live plotting
                self._app.stop_live_plotting()

    def cb_boundary_slider_moved(self):

        # update cursors on spectru mwindow
        self._app.windows['spectrumWindow'].get_current_widget().update_cursors(self.ui.lower_boundary_slider.value(),
                                                                                self.ui.upper_boundary_slider.value())

    def cb_boundary_slider_pressed(self):

        # create cursors on spectru mwindow
        self._app.windows['spectrumWindow'].get_current_widget().create_cursors(self.ui.lower_boundary_slider.value(),
                                                                                self.ui.upper_boundary_slider.value())

    def cb_boundary_slider_released(self):

        # destroy cursors on spectru mwindow
        self._app.windows['spectrumWindow'].get_current_widget().destroy_cursors()

        # bring window to front
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()


class BackgroundWindow(QMainWindow):

    """
    BackgroundWindow
    Hosts a background widget for each loaded map.
    """

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

    def add_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # add a widget to the widgets list
        self._background_widgets[map_handle.get_id()] = BackgroundWidget(self, map_handle)

    def change_widget(self, map_id):

        # get map handle
        map_handle = self._app.maps.get_map(map_id)

        # hide all widgets
        for key in self._background_widgets.keys():
            self._background_widgets[key].setVisible(False)

        # make the widget for the select map visible
        self._background_widgets[map_handle.get_id()].setVisible(True)

    def remove_widget(self, map_id):

        # remove the widget of the deleted map
        self._background_widgets[map_id].setParent(None)
        self._background_widgets[map_id].deleteLater()
        del self._background_widgets[map_id]

        # close the window if there are no more maps
        if len(self._background_widgets) == 0:
            self.close()
