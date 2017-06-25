# import PyQt5 elements
from PyQt5.QtWidgets import QApplication, QDialog
# general imports
import numpy
# import canvas class
from mplCanvas import MicrographCanvas
# import UI
from UIs.exportDialogUi import UiExportDialog


class ExportDialog(QDialog):

    """
    ExportDialog
    This dialog exports data.
    """

    def __init__(self, parent):

        # call widget init
        QDialog.__init__(self, parent)

        # link app
        self._app = QApplication.instance()

        # link map
        self._map = self._app.maps.get_selected_map()

        # load and set up UI
        self.ui = UiExportDialog(self)

        # add data to the selection box
        self.ui.data_combo_box.addItems(['spectra', '-- integral', '-- mean', '-- maximum'])
        self.ui.data_combo_box.model().item(0).setEnabled(False)
        self.ui.data_combo_box.setCurrentIndex(1)
        for key, value in self._map.get_data_names().items():
            if self._map.get_dimension() == 2 or key > 0:
                self.ui.data_combo_box.addItems([value])

        # add micrographs to the selection box
        if self._map.get_dimension() == 2:
            for key, value in self._map.get_micrograph_names().items():
                self.ui.data_combo_box.addItems([value])

        # add fit data to the selection box
        fit_functions = self._map.get_fit_functions()
        subscripts = [u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086']
        if self._map.get_dimension() == 2:
            for i_peak in range(6):
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] > 0)) > 0:
                    self.ui.data_combo_box.addItems(['I'+subscripts[i_peak], 'ε'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 1)) > 0 or numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 3)) > 0:
                    self.ui.data_combo_box.addItems(['σ'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 2)) > 0 or numpy.sum(numpy.int_(fit_functions[:, :, i_peak] == 3)) > 0:
                    self.ui.data_combo_box.addItems(['γ'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, :, i_peak] > 0)) > 0:
                    self.ui.data_combo_box.addItems(['FWHM'+subscripts[i_peak]])
        else:
            for i_peak in range(6):
                if numpy.sum(numpy.int_(fit_functions[:, i_peak] > 0)) > 0:
                    self.ui.data_combo_box.addItems(['I'+subscripts[i_peak], 'ε'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, i_peak] == 1)) > 0 or numpy.sum(numpy.int_(fit_functions[:, i_peak] == 3)) > 0:
                    self.ui.data_combo_box.addItems(['σ'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, i_peak] == 2)) > 0 or numpy.sum(numpy.int_(fit_functions[:, i_peak] == 3)) > 0:
                    self.ui.data_combo_box.addItems(['γ'+subscripts[i_peak]])
                if numpy.sum(numpy.int_(fit_functions[:, i_peak] > 0)) > 0:
                    self.ui.data_combo_box.addItems(['FWHM'+subscripts[i_peak]])

    def get_data_selection(self):

        return self.ui.data_combo_box.currentIndex()

    def get_type_selection(self):

        return self.ui.type_combo_box.currentIndex()
