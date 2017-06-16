# import PyQt5 elements
from PyQt5.QtWidgets import QProgressDialog, QApplication
from PyQt5.QtCore import Qt
# general imports
import numpy
from os import path

class QtLab1D:

    def __init__(self, file_name):

        self._file_name = file_name

    def load_data(self):

        # get the directory from path
        dir_name = path.dirname(self._file_name)

        #  load the data file
        file_data = numpy.loadtxt(self._file_name)

        # read the number of pixels
        nx = int(file_data[-1, 0]) + 1

        # read the resolution of the CCD from the first spectrum file
        spectrum = numpy.loadtxt(dir_name + '/spectrum_0.asc')
        resolution = len(spectrum)

        # create variables for the data
        spectra = numpy.zeros((nx, resolution, 2))
        data = numpy.zeros((file_data.shape[1], nx))

        # read column names and map name
        data_names = {0: 'intensity', 1: 'int. intensity'}
        file_lines = open(self._file_name).readlines()
        for i_line in range(len(file_lines)):
            line_split = file_lines[i_line].split()
            if len(line_split) > 1:
                if line_split[1] == 'Filename:':
                    map_name = line_split[2][:-4]
                if line_split[1] == 'Column' and int(line_split[2][:-1]) > 1:
                    next_split = file_lines[i_line + 1].split()
                    data_names[int(line_split[2][:-1])] = ' '.join(next_split[2:])

        # check if there are .npy files available to accelerate the loading procedure
        if path.isfile(dir_name + '/spectra.npy') and path.isfile(dir_name + '/energies.npy'):

            # load data from npy files
            spectra[:, :, 0] = numpy.load(dir_name + '/energies.npy')
            spectra[:, :, 1] = numpy.load(dir_name + '/spectra.npy')

            # integrate counts
            data[0, :] = numpy.sum(spectra[:, :, 1], axis=1)

            # read other quantities
            for ix in range(nx):
                data[1:, ix] = file_data[ix, 1:]

        # if no .npy files are available the spectra need to be loaded from .asc files
        else:

            # create progressbar dialog
            progress_dialog = QProgressDialog('', '', 0, nx,
                                              QApplication.instance().windows['mapWindow'])
            progress_dialog.setWindowTitle('Loading Map')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setCancelButton(None)
            progress_dialog.show()

            # read data
            for ix in range(nx):
                spectrum = numpy.loadtxt(dir_name + '/spectrum_' + str(ix) + '.asc')
                spectrum[:, 0] = 1e-9 * 1239.841842144513 / spectrum[:, 0]
                spectrum = numpy.flipud(spectrum)
                spectra[ix, :, :] = spectrum
                data[0, ix] = numpy.sum(spectrum[:, 1])
                data[1:, ix] = file_data[ix, 1:]
                progress_dialog.setValue(ix + 1)

            # save .npy files for the next time the map is loaded
            numpy.save(dir_name + '/energies.npy', spectra[:, :, 0])
            numpy.save(dir_name + '/spectra.npy', spectra[:, :, 1])

        return map_name, spectra, data_names, data
