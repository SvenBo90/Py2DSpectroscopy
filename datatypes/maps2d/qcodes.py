# import PyQt5 elements
from PyQt5.QtWidgets import QProgressDialog, QApplication
from PyQt5.QtCore import Qt
# general imports
import numpy
from os import path


class QCoDeS2D:

    def __init__(self, file_name):

        self._file_name = file_name

    def load_data(self):

        # get the directory from path
        dir_name = path.dirname(self._file_name)

        #  load the data file
        file_data = numpy.loadtxt(self._file_name)

        # read the number of pixels
        file_text = open(self._file_name, 'r')
        file_text.readline()
        data_name_line = file_text.readline()
        pixel_line = file_text.readline().split()
        nx = int(pixel_line[1])
        ny = int(pixel_line[2])

        # read the resolution of the CCD from the first spectrum file
        resolution = 1024

        # create variables for the data
        spectra = numpy.zeros((nx, ny, resolution, 2))
        data = numpy.zeros((file_data.shape[1] - 3, nx, ny))

        # read column names and map name
        data_names = {0: 'x voltage', 1: 'y voltage'}
        map_name = 'blub'

        # read spectra
        data_energies = file_data[:,3]
        data_energies.shape = (nx, ny, resolution)
        data_spectra = file_data[:,4]
        data_spectra.shape = (nx, ny, resolution)
        spectra[:, :, :, 0] = data_energies
        spectra[:, :, :, 1] = data_spectra

        # read data
        for ix in range(nx):
            for iy in range(ny):
                for idata in range(data.shape[0]):
                    data[idata, ix, iy] = file_data[resolution*(ny*ix+iy), idata]

        return map_name, spectra, data_names, data
