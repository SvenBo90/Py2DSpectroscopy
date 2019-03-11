# import PyQt5 elements
from PyQt5.QtWidgets import QProgressDialog, QApplication
from PyQt5.QtCore import Qt
# general imports
import numpy
from os import path
import pandas


class QCoDeS1D:

    def __init__(self, file_name):

        self._file_name = file_name

    def load_data(self):

        # get the directory from path
        dir_name = path.dirname(self._file_name)

        #  load the data file
        df = pandas.read_pickle(self._file_name)

        # read the number of pixels
        v_x =  numpy.sort(numpy.array(list(set(numpy.array(df.index.tolist())[:,0]))))
        nx = len(v_x)

        # read the resolution of the CCD from the first spectrum file
        resolution = 1024

        # create variables for the data
        spectra = numpy.zeros((nx, resolution, 2))
        data = numpy.zeros((1, nx))

        # read column names and map name
        data_names = {0: 'x voltage'}
        map_name = 'blub'

        # read spectra
        data_energies = numpy.array(df.index.tolist())[:,1]
        data_energies.shape = (nx, resolution)
        data_spectra = numpy.array(df.values.tolist())
        data_spectra.shape = (nx, resolution)
        spectra[:, :, 0] = 1239.841842144513 / data_energies
        spectra[:, :, 1] = data_spectra

        # read data
        data[0, :] = v_x

        return map_name, spectra, data_names, data
