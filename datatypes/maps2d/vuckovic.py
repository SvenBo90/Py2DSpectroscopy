# general imports
import numpy
from os import path


class Vuckovic2D:

    def __init__(self, file_name):

        self._file_name = file_name

    def load_data(self):

        # get the directory from path
        dir_name = path.dirname(self._file_name)

        # set map name to the file name
        map_name = self._file_name[len(dir_name)+1:-5]

        # read text file
        file_data = numpy.loadtxt(self._file_name)

        # get map shape
        nx = file_data.shape[0]
        ny = file_data.shape[1]

        # create data structures for spectra and position data
        spectra = numpy.zeros((nx, ny, 1, 2))
        data_names = {0: 'intensity'}
        data = numpy.zeros((1, nx, ny))

        # read intensities
        for ix in range(nx):
            for iy in range(ny):
                    spectra[ix, iy, :, 0] = 0
                    spectra[ix, iy, :, 1] = file_data[ix, iy]
                    data[0, ix, iy] = file_data[ix, iy]

        return map_name, spectra, data_names, data
