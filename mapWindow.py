# general imports
from os import path
import numpy
from matplotlib import image
from skimage import transform
import webbrowser
# import PyQt5 elements
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog, QMainWindow, QMessageBox, \
    QProgressDialog, QWidget
# import UI
from UIs.mapWindowUi import UiMapWindow
from UIs.mapTabWidgetUi import UiMapTabWidget
from addMicrographDialog import AddMicrographDialog
from exportDialog import ExportDialog
# import map canvas
from mplCanvas import MapCanvas1D, MapCanvas2D


class MapTab(QWidget):

    def __init__(self, map_handle):

        # call QWidget init
        super().__init__()

        # link app
        self._app = QApplication.instance()

        # link map handle
        self._map = map_handle

        # load and set up UI
        self.ui = UiMapTabWidget(self)

        if self._map.get_dimension() == 2:

            # create map canvas
            self._map_canvas = MapCanvas2D(self.ui.plot_widget, self._map)

        elif self._map.get_dimension() == 1:

            # create map canvas
            self._map_canvas = MapCanvas1D(self.ui.plot_widget, self._map)

        # add callbacks to map canvas
        self._map_canvas.add_callback('key_press_event', self.cb_map_key_press_event)
        self._map_canvas.add_callback('button_press_event', self.cb_map_button_press_event)

        # create widget including the toolbar
        self._map_canvas.add_toolbar(self.ui.toolbar_widget)

        # fill data selection widget
        for key, value in self._map.get_data_names().items():
            self.ui.data_selection_combo_box.addItems([value])
        self.ui.data_selection_combo_box.currentIndexChanged.connect(self.cb_data_selection_changed)

    def cb_data_selection_changed(self, index):

        # I don't know why this is needed actually
        if index == -1:
            index = 0

        # change the selected data and update the map canvas
        self._map.set_selected_data(index)

    def cb_map_button_press_event(self, event):

        # set focus on the canvas in order to make keys usable
        self._map_canvas.setFocusPolicy(Qt.ClickFocus)
        self._map_canvas.setFocus()

        # check if toolbar or area selector is active and if the left mouse button was used
        if self._map_canvas.get_toolbar_active() is None and event.button == 1:

            # check if outer area has been clicked
            if event.inaxes is None:

                return

            # set focus of the map
            if self._map.get_dimension() == 1:
                self._map.set_focus(int(numpy.round(event.ydata)))
            elif self._map.get_dimension() == 2:
                self._map.set_focus([int(numpy.round(event.xdata)), int(numpy.round(event.ydata))])

    def cb_map_key_press_event(self, event):

        # get current focus
        focus = self._map.get_focus()

        # check the dimension of the map
        if self._map.get_dimension() == 2:
            if event.key == 'down':
                focus[1] -= 1
            elif event.key == 'up':
                focus[1] += 1
            elif event.key == 'left':
                focus[0] -= 1
            elif event.key == 'right':
                focus[0] += 1
        elif self._map.get_dimension() == 1:
            if event.key == 'down':
                focus -= 1
            elif event.key == 'up':
                focus += 1

        # set new focus
        self._map.set_focus(focus)

    def create_area_map(self, *coordinates):

        # create area map on the map canvas
        self._map_canvas.create_area_map(*coordinates)

        # bring window to front
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def create_threshold_map(self, threshold_data, threshold):

        # create threshold map on the map canvas
        self._map_canvas.create_threshold_map(threshold_data, threshold)

        # bring window to front
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def destroy_area_map(self):

        # destroy area map
        self._map_canvas.destroy_area_map()

    def destroy_threshold_map(self):

        # destroy threshold map
        self._map_canvas.destroy_threshold_map()

    def get_map(self):

        # return the map of this tab
        return self._map

    def update(self):

        # update data
        self.update_data()

        # update cross hair
        self.update_crosshair()

        # update data selection box
        self.update_data_selection_combo_box()

    def update_area_map(self, *coordinates):

        # update area map on the map canvas
        self._map_canvas.update_area_map(*coordinates)

    def update_crosshair(self):

        # update cross hair
        self._map_canvas.update_crosshair()

    def update_data(self):

        # update data
        self._map_canvas.update_data()

    def update_data_selection_combo_box(self):

        # save the currently selected index
        current_index = self.ui.data_selection_combo_box.currentIndex()

        # clear the data selection box
        self.ui.data_selection_combo_box.clear()

        # add data to the selection box
        for key, value in self._map.get_data_names().items():
            self.ui.data_selection_combo_box.addItems([value])

        # add micrographs to the selection box
        if self._map.get_dimension() == 2:
            for key, value in self._map.get_micrograph_names().items():
                self.ui.data_selection_combo_box.addItems([value])

        # add fit data to the selection box
        fit_functions = self._map.get_fit_functions()
        subscripts = [u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086']
        if self._map.get_dimension() == 2:
            for i_peak in range(6):
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] > 0)) > 0:
                    self.ui.data_selection_combo_box.addItems(['I'+subscripts[i_peak], 'ε'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 1)) > 0 or numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 3)) > 0:
                    self.ui.data_selection_combo_box.addItems(['σ'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 2)) > 0 or numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 3)) > 0:
                    self.ui.data_selection_combo_box.addItems(['γ'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] > 0)) > 0:
                    self.ui.data_selection_combo_box.addItems(['FWHM'+subscripts[i_peak]])
        else:
            for i_peak in range(6):
                if numpy.sum(numpy.int_(fit_functions[:, i_peak] == 3)) > 0:
                    self.ui.data_selection_combo_box.addItems(['I'+str(i_peak), 'λ'+str(i_peak),
                                                               'σ'+str(i_peak), 'γ'+str(i_peak)])
                elif numpy.sum(numpy.int_(fit_functions[:, i_peak] == 1)) > 0 or \
                        numpy.sum(numpy.int_(fit_functions[:, i_peak] == 2)) > 0:
                    self.ui.data_selection_combo_box.addItems(['I'+str(i_peak), 'λ'+str(i_peak), 'σ'+str(i_peak)])

        # if the selected index is still available select it
        if current_index <= self.ui.data_selection_combo_box.count():

            self.ui.data_selection_combo_box.setCurrentIndex(current_index)

        else:

            self.ui.data_selection_combo_box.setCurrentIndex(0)

    def update_threshold_map(self, threshold_data, threshold):

        # update threshold map on the map canvas
        self._map_canvas.update_threshold_map(threshold_data, threshold)


class MapWindow(QMainWindow):

    def __init__(self, parent=None):

        # call widget init
        QWidget.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # dictionary for map tabs
        self._map_tab_widgets = {}

        # load and set up UI
        self.ui = UiMapWindow(self)

        # set fixed size
        self.setFixedWidth(640)
        self.setFixedHeight(480)

        # link actions for the file menu
        self.ui.action_1d_map.triggered.connect(self.cb_action1d_map)
        self.ui.action_2d_map.triggered.connect(self.cb_action2d_map)
        self.ui.action_save.triggered.connect(self.cb_action_save)
        self.ui.action_export.triggered.connect(self.cb_action_export)
        self.ui.action_exit.triggered.connect(self.cb_action_exit)

        # link actions for the view menu
        self.ui.action_spectrum.triggered.connect(self.cb_action_spectrum)
        self.ui.action_pixel_information.triggered.connect(self.cb_action_pixel_information)

        # link actions for the tools menu
        self.ui.action_add_micrograph.triggered.connect(self.cb_action_add_micrograph)
        self.ui.action_fitting.triggered.connect(self.cb_action_fitting)
        self.ui.action_remove_background.triggered.connect(self.cb_action_remove_background)
        self.ui.action_remove_cosmic_rays.triggered.connect(self.cb_action_remove_cosmic_rays)
        self.ui.action_horizontally.triggered.connect(self.cb_action_horizontally)
        self.ui.action_vertically.triggered.connect(self.cb_action_vertically)
        self.ui.action_clockwise.triggered.connect(self.cb_action_clockwise)
        self.ui.action_anticlockwise.triggered.connect(self.cb_action_anticlockwise)

        # link actions for the help menu
        self.ui.action_about.triggered.connect(self.cb_action_about)
        self.ui.action_wiki.triggered.connect(self.cb_action_wiki)

        # link actions for the tab widget
        self.ui.tab_widget.currentChanged.connect(self.cb_change_map)
        self.ui.tab_widget.tabCloseRequested.connect(self.cb_close_map)

    def cb_action_about(self):

        # open spectrum window
        self._app.windows['aboutWindow'].show()

    def cb_action_add_micrograph(self):

        # get micrograph file
        file_name = QFileDialog.getOpenFileName(self._app.windows['mapWindow'], 'Open File', '')
        file_name = file_name[0]

        # check if file has been selected
        if file_name == '':
            return

        # open micrograph dialog
        add_micrograph_dialog = AddMicrographDialog(self, file_name)
        add_micrograph_dialog.exec_()

        # check if the micrograph dialog has been submitted
        if add_micrograph_dialog.result() == 1:

            # map handle for the selected map
            map_handle = self._app.maps.get_selected_map()

            # load micrograph
            micrograph = image.imread(file_name)
            micrograph = micrograph[-1:0:-1, :, :]

            # get micrograph name
            dir_name = path.dirname(file_name)
            micrograph_name = file_name[len(dir_name)+1:]

            # get fixed and moving points from micrograph dialog
            points_fixed = add_micrograph_dialog.get_points_fixed()
            points_moving = add_micrograph_dialog.get_points_moving()
            points_fixed.shape = (int(len(points_fixed)/2), 2)
            points_moving.shape = (int(len(points_moving)/2), 2)

            # get the transformation for the micrograph
            transform_1 = transform.estimate_transform('affine', points_fixed, points_moving)

            # calculate scaling factor
            transform_matrix = transform_1.params
            transform_factor = int(numpy.ceil(numpy.sqrt(
                (transform_matrix[0, 0] + transform_matrix[0, 1]) ** 2. +
                (transform_matrix[1, 0] + transform_matrix[1, 1]) ** 2.)) / numpy.sqrt(2))

            # create scaling transformation
            transform_2 = transform.SimilarityTransform(
                                        scale=1./transform_factor,
                                        rotation=0,
                                        translation=(0, 0))

            # combine transformations
            transform_sum = transform_2 + transform_1

            # size of the output image
            output_shape = (transform_factor*map_handle.get_size()[1], transform_factor*map_handle.get_size()[0])

            # transform micrograph
            micrograph_transformed = transform.warp(micrograph, transform_sum, output_shape=output_shape)

            # save the micrograph and get the data id of this micrograph
            data_id = map_handle.add_micrograph(micrograph_name, micrograph_transformed)

            # update data selection box
            self.ui.tab_widget.currentWidget().update_data_selection_combo_box()

            # set current data to the new micrograph
            self.ui.tab_widget.currentWidget().ui.data_selection_combo_box.setCurrentIndex(data_id)

    def cb_action_anticlockwise(self):

        # rotate the currently selected map clockwise
        self._app.maps.get_selected_map().rotate('anticlockwise')

    def cb_action_clockwise(self):

        # rotate the currently selected map clockwise
        self._app.maps.get_selected_map().rotate('clockwise')

    def cb_action_exit(self):

        # ask the user if he wants to close the program
        reply = QMessageBox.question(self._app.windows['mapWindow'], 'Close Program',
                                     "Are you sure you want to exit the program?", QMessageBox.Yes, QMessageBox.No)

        # check the answer
        if reply == QMessageBox.Yes:
            self._app.closeAllWindows()

    def cb_action_export(self):

        # open export dialog
        export_dialog = ExportDialog(self)
        export_dialog.exec_()

        # check if the micrograph dialog has been submitted
        if export_dialog.result() == 1:

            # get micrograph file
            file_name = QFileDialog.getSaveFileName(self._app.windows['mapWindow'], 'Export Data', '')
            file_name = file_name[0]

            if file_name == '':

                return

            numpy.savetxt(file_name,
                          self._app.maps.get_selected_map().get_data(data_index=export_dialog.get_data_selection()))

    def cb_action_fitting(self):

        # open spectrum window
        self._app.windows['fittingWindow'].show()

    def cb_action_horizontally(self):

        # flip the currently selected map horizontally
        self._app.maps.get_selected_map().flip('horizontally')

    def cb_action1d_map(self):

        # get file to load
        file_name = QFileDialog.getOpenFileName(self._app.windows['mapWindow'], 'Open File', '', '')
        file_name = file_name[0]

        # add map
        map_handle = self._app.maps.append_1d(file_name)

        # create new tab for map
        map_tab = MapTab(map_handle)
        map_tab.update()
        self.ui.tab_widget.addTab(map_tab, map_handle.get_map_name())
        self.ui.tab_widget.setCurrentWidget(map_tab)

        # update menus
        self.update_menus()

    def cb_action2d_map(self):

        # get file to load
        file_name = QFileDialog.getOpenFileName(self._app.windows['mapWindow'], 'Open File', '', '')
        file_name = file_name[0]

        # check if file has been selected
        if file_name == '':
            return

        # add map
        map_handle = self._app.maps.append_2d(file_name)

        # create new tab for map
        self._map_tab_widgets[map_handle.get_id()] = MapTab(map_handle)
        self._map_tab_widgets[map_handle.get_id()].update()
        self.ui.tab_widget.addTab(self._map_tab_widgets[map_handle.get_id()], map_handle.get_map_name())
        self.ui.tab_widget.setCurrentWidget(self._map_tab_widgets[map_handle.get_id()])

        # update menus
        self.update_menus()

    def cb_action_pixel_information(self):

        # open spectrum window
        self._app.windows['pixelInformationWindow'].show()

    def cb_action_remove_background(self):

        # open remove background window
        self._app.windows['backgroundWindow'].show()

    def cb_action_remove_cosmic_rays(self):

        # get threshold for cosmic ray detection
        threshold, ok = QInputDialog.getInt(self._app.windows['mapWindow'], "Remove Cosmic Rays",
                                            "Threshold parameter:", 20, 0, 1e8, 1)
        if not ok:
            return

        # get map handle
        map_handle = self._app.maps.get_selected_map()

        if map_handle.get_dimension() == 1:

            # get map size
            nx = map_handle.get_size()[0]

            # create progressbar dialog
            progress_dialog = QProgressDialog('', '', 0, nx, self)
            progress_dialog.setWindowTitle('Removing Cosmic Rays')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setCancelButton(None)
            progress_dialog.show()

            for ix in range(nx):

                # spectrum = map_handle.get_spectrum(pixel=ix)

                # TODO: think of a good algorithm for cosmic removal for maps with varying parameters, e.g. power

                progress_dialog.setValue(ix + 1)

        else:

            # get map size
            nx, ny = map_handle.get_size()

            # create progressbar dialog
            progress_dialog = QProgressDialog('', '', 0, nx * ny, self)
            progress_dialog.setWindowTitle('Removing Cosmic Rays')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setCancelButton(None)
            progress_dialog.show()

            for ix in range(nx):
                for iy in range(ny):
                    spectrum = map_handle.get_spectrum(pixel=[ix, iy])

                    # calculate average neighbour spectrum
                    spectrum_neighbours = numpy.zeros(spectrum.shape[0])
                    n_neighbours = 0
                    if ix > 0:
                        spectrum_neighbours += map_handle.get_spectrum(pixel=[ix - 1, iy])[:, 1]
                        n_neighbours += 1
                    if ix < nx-1:
                        spectrum_neighbours += map_handle.get_spectrum(pixel=[ix + 1, iy])[:, 1]
                        n_neighbours += 1
                    if iy > 0:
                        spectrum_neighbours += map_handle.get_spectrum(pixel=[ix, iy - 1])[:, 1]
                        n_neighbours += 1
                    if iy < ny-1:
                        spectrum_neighbours += map_handle.get_spectrum(pixel=[ix, iy + 1])[:, 1]
                        n_neighbours += 1
                    spectrum_neighbours *= 1./n_neighbours

                    # calculate difference between spectrum and averaged neighbour spectrum
                    diff = spectrum[:, 1]-spectrum_neighbours
                    spectrum[diff > threshold, 1] = spectrum_neighbours[diff > threshold]

                    if numpy.sum(diff > threshold) > 0:
                        if iy == ny-1 or (ix == map_handle.get_focus()[0] and iy == map_handle.get_focus()[1]):
                            map_handle.set_spectrum(spectrum, pixel=[ix, iy], emit=True)
                        else:
                            map_handle.set_spectrum(spectrum, pixel=[ix, iy], emit=False)

                    progress_dialog.setValue(ix * ny + iy + 1)

    def cb_action_save(self):

        # get destination file name
        file_name = QFileDialog.getSaveFileName(self._app.windows['mapWindow'], 'Save Map', '', '')
        file_name = file_name[0]

        # save the map
        if file_name == '':
            return
        self._app.maps.save_map(file_name)

    def cb_action_vertically(self):

        # flip the currently selected map horizontally
        self._app.maps.get_selected_map().flip('vertically')

    @staticmethod
    def cb_action_wiki(self):

        # open wiki page
        webbrowser.open('https://github.com/SvenBo90/Py2DSpectroscopy/wiki')

    def cb_action_spectrum(self):

        # open spectrum window
        self._app.windows['spectrumWindow'].show()

    def cb_change_map(self, index):

        # check if last map has been removed
        if index >= 0:

            # change selected map in the map list
            map_handle = self.ui.tab_widget.widget(index).get_map()
            self._app.maps.set_selected_map(map_handle)

        else:

            # reset list
            self._app.maps.reset()

        # update menus
        self.update_menus()

    def cb_close_map(self, index):

        # safety check
        reply = QMessageBox.question(self._app.windows['mapWindow'], 'Close Map', "Do you want to close this map?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            # remove the map from the map list
            map_handle = self.ui.tab_widget.widget(index).get_map()
            self._app.maps.remove_map(map_handle)

            # remove the tab from the tab widget
            self.ui.tab_widget.removeTab(index)

    def closeEvent(self, event):

        if self.sender() is None:

            # ask the user if he wants to close the program
            reply = QMessageBox.question(self._app.windows['mapWindow'], 'Close Program',
                                         "Are you sure you want to exit the program?", QMessageBox.Yes,
                                         QMessageBox.No)

            # check the answer
            if reply == QMessageBox.Yes:
                self._app.closeAllWindows()
            else:
                event.ignore()

    def update_crosshair(self, map_id):

        # update data in the currently selected tab
        self._map_tab_widgets[map_id].update_crosshair()

    def update_data(self, map_id):

        # update data in the currently selected tab
        self._map_tab_widgets[map_id].update_data()

    def update_data_selection_combo_box(self):

        # update the data selection box in the currently selected tab
        self.ui.tab_widget.currentWidget().update_data_selection_combo_box()

    def update_menus(self):

        # check if there are maps
        if self._app.maps.get_count() > 0:

            self.ui.action_save.setEnabled(True)
            if self._app.maps.get_selected_map().get_dimension() == 2:
                self.ui.action_export.setEnabled(True)
            else:
                self.ui.action_export.setEnabled(False)
            if self._app.maps.get_selected_map().get_dimension() == 2:
                self.ui.action_add_micrograph.setEnabled(True)
            else:
                self.ui.action_add_micrograph.setEnabled(False)
            self.ui.action_fitting.setEnabled(True)
            self.ui.action_spectrum.setEnabled(True)
            self.ui.action_pixel_information.setEnabled(True)
            self.ui.action_remove_background.setEnabled(True)
            self.ui.action_remove_cosmic_rays.setEnabled(True)
            if self._app.maps.get_selected_map().get_dimension() == 2:
                self.ui.action_horizontally.setEnabled(True)
                self.ui.action_vertically.setEnabled(True)
                self.ui.action_clockwise.setEnabled(True)
                self.ui.action_anticlockwise.setEnabled(True)
            else:
                self.ui.action_clockwise.setEnabled(False)
                self.ui.action_anticlockwise.setEnabled(False)

        else:

            self.ui.action_save.setEnabled(False)
            self.ui.action_export.setEnabled(False)
            self.ui.action_add_micrograph.setEnabled(False)
            self.ui.action_fitting.setEnabled(False)
            self.ui.action_spectrum.setEnabled(False)
            self.ui.action_pixel_information.setEnabled(False)
            self.ui.action_remove_background.setEnabled(False)
            self.ui.action_remove_cosmic_rays.setEnabled(False)
            self.ui.action_horizontally.setEnabled(False)
            self.ui.action_vertically.setEnabled(False)
            self.ui.action_clockwise.setEnabled(False)
            self.ui.action_anticlockwise.setEnabled(False)
