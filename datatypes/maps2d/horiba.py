# general imports
import numpy
from os import path


class Horiba2D:

    def __init__(self, file_name):

        self._file_name = file_name

    def load_data(self):

        # get the directory from path
        dir_name = path.dirname(self._file_name)

        # set map name to the file name
        map_name = self._file_name[len(dir_name)+1:-4]

        # read text file
        file_data = open(self._file_name)
        data_lines = file_data.readlines()

        # convert the data into numpy arrays
        data_list = []
        for i_line in range(len(data_lines)):
            # check if the line is a comment
            if data_lines[i_line][0] == '#':
                continue
            else:
                data_list.append(data_lines[i_line].split('\t'))

        # the first line of the text file includes the energies of the spectra
        energies = numpy.array(data_list[0][2:], dtype='float64')
        del data_list[0]

        # check if data is given in eV or nm TODO: read this from the .txt file
        if numpy.mean(energies) > 100:
            energies = 1239.841842144513 / energies

        # set the resolution to the number of pixels of the CCD
        resolution = len(energies)

        # convert the list into a numpy array
        data_array = numpy.array(data_list, dtype='float64')

        # get map shape
        x_positions = []
        y_positions = []
        for i_px in range(len(data_array)):
            if data_array[i_px, 0] not in x_positions:
                x_positions.append(data_array[i_px, 0])
            if data_array[i_px, 1] not in y_positions:
                y_positions.append(data_array[i_px, 1])
        nx = len(x_positions)
        ny = len(y_positions)

        # create data structures for spectra and position data
        spectra = numpy.zeros((nx, ny, resolution, 2))
        data_names = {0: 'intensity', 1: 'x position', 2: 'y position'}
        data = numpy.zeros((3, nx, ny))

        # read spectra and position data
        i_px = 0
        for ix in range(nx):
            for iy in range(ny):
                spectra[ix, iy, :, 0] = numpy.flipud(energies)
                spectra[ix, iy, :, 1] = numpy.flipud(data_array[i_px, 2:])
                data[0, ix, iy] = numpy.sum(spectra[ix, iy, :, 1])
                data[1, ix, iy] = data_array[i_px, 0]
                data[2, ix, iy] = data_array[i_px, 1]
                i_px += 1

        return map_name, spectra, data_names, data
