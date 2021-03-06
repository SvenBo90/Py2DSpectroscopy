# import PyQt5 elements
from PyQt5.QtWidgets import QProgressDialog, QApplication
from PyQt5.QtCore import Qt
# general imports
import numpy
from os import path
import pandas


class QCoDeS2D:

    def __init__(self, file_name):

        self._file_name = file_name

    def load_data(self):

        # get the directory from path
        dir_name = path.dirname(self._file_name)

        #  load the data file
        df = pandas.read_pickle(self._file_name)

        # read the number of pixels
        v_x = numpy.sort(numpy.array(list(set(numpy.array(df.index.tolist())[:,0]))))
        v_y = numpy.sort(numpy.array(list(set(numpy.array(df.index.tolist())[:,1]))))
        nx = len(v_x)
        ny = len(v_y)

        # read the resolution of the CCD from the first spectrum file
        resolution = 1024

        # create variables for the data
        spectra = numpy.zeros((nx, ny, resolution, 2))
        data = numpy.zeros((2, nx, ny))

        # read column names and map name
        data_names = {0: 'x voltage', 1: 'y voltage'}
        map_name = 'blub'

        # read spectra
        data_energies = numpy.array(df.index.tolist())[:,2]
        data_energies.shape = (nx, ny, resolution)
        data_spectra = numpy.array(df.values.tolist())
        data_spectra.shape = (nx, ny, resolution)
        spectra[:, :, :, 0] = 1239.841842144513 / data_energies
        spectra[:, :, :, 1] = data_spectra

        # read data
        grid = numpy.meshgrid(v_x, v_y)
        data[0, :, :] = grid[0].transpose()
        data[1, :, :] = grid[1].transpose()

        return map_name, spectra, data_names, data
