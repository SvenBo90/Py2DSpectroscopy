# general imports
from PyQt5.QtWidgets import QProgressDialog, QApplication
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from os import path
import numpy
import pickle


class Map:

    """
    Map
    This class defines the basic functions of all maps.
    The Map1D and Map2D classes inherit from this class.
    """

    def __init__(self):

        # create all general variables
        self._app = None
        self._data_names = {}       # dictionary for all data names
        self._dimension = 0         # the dimension of the map (1D, 2D)
        self._focus = []            # the currently focused pixel
        self._id = 0                # the map id
        self._interval = [0, 0]     # integration interval for energy
        self._map_name = ''         # the map name
        self._resolution = 0        # the pixels on the CCD
        self._selected_data = 0     # a flag for the currently selected data

        # call super init
        super(Map, self).__init__()

    def set_app(self, app):

        # set map list
        self._app = app

    def get_data_names(self):

        # return data names
        return self._data_names

    def get_selected_data(self):

        # return the currently selected data
        return self._selected_data

    def get_dimension(self):

        # return map dimension
        return self._dimension

    def get_focus(self):

        # return focus
        return self._focus

    def get_id(self):

        # return the map ID
        return self._id

    def get_interval(self):

        # return interval
        return self._interval

    def get_map_name(self):

        # return map name
        return self._map_name

    def get_resolution(self):

        # return pixels on CCD
        return self._resolution

    def set_selected_data(self, selected_data):

        # update data selection if the new data is different from the old one
        if selected_data != self._selected_data:
            self._selected_data = selected_data

            # emit signal
            self._app.selected_data_changed.emit(self._id)

    def set_id(self, map_id):

        # set map id
        self._id = map_id


class Map1D(Map):

    """
    Map1D
    Class for one-dimensional maps such as gate dependences or power dependences.
    """

    def __init__(self, map_id, file_name):

        # call super init
        super(Map1D, self).__init__()

        # set dimension of the map
        self._dimension = 1

        # set the map id
        self._id = map_id

        # get the directory from path and load the data file
        dir_name = path.dirname(file_name)
        file_data = numpy.loadtxt(file_name)

        # read the number of pixels and check for consistency
        self._nx = int(file_data[-1, 0]) + 1

        # read the number of pixels on the CCD from the first spectrum
        spectrum = numpy.loadtxt(dir_name + '/spectrum_0.asc')
        self._resolution = len(spectrum)

        # create variables for the data
        self._spectra = numpy.zeros((self._nx, self._resolution, 2))
        self._data = numpy.zeros((file_data.shape[1], self._nx))

        # read column names and map name
        self._data_names = {0: 'spectra', 1: 'intensity'}
        file_lines = open(file_name).readlines()
        for i_line in range(len(file_lines)):
            line_split = file_lines[i_line].split()
            if len(line_split) > 1:
                if line_split[1] == 'Filename:':
                    self._map_name = line_split[2][:-4]
                if line_split[1] == 'Column' and int(line_split[2][:-1]) > 1:
                    next_split = file_lines[i_line + 1].split()
                    self._data_names[int(line_split[2][:-1])] = ' '.join(next_split[2:])

        # check if there are .npy files available in order to accelerate the loading
        if path.isfile(dir_name + '/spectra.npy') and path.isfile(dir_name + '/wavelengths.npy'):

            # load data from npy files
            self._spectra[:, :, 0] = numpy.load(dir_name + '/wavelengths.npy')
            self._spectra[:, :, 1] = numpy.load(dir_name + '/spectra.npy')

            # integrate counts
            self._data[0, :] = numpy.sum(self._spectra[:, :, 1], axis=1)

            # read other quantities
            for ix in range(self._nx):
                self._data[1:, ix] = file_data[ix, 1:]

        else:

            # create progressbar dialog
            progress_dialog = QProgressDialog('', '', 0, self._nx,
                                              QApplication.instance().windows['mapWindow'])
            progress_dialog.setWindowTitle('Loading Map')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setCancelButton(None)
            progress_dialog.show()

            # read data
            for ix in range(self._nx):
                spectrum = numpy.loadtxt(dir_name + '/spectrum_' + str(ix) + '.asc')
                spectrum[:, 0] = 1e9 * spectrum[:, 0]
                self._spectra[ix, :, :] = spectrum
                self._data[0, ix] = numpy.sum(spectrum[:, 1])
                self._data[1:, ix] = file_data[ix, 1:]
                progress_dialog.setValue(ix + 1)

            # save .npy files for the next time
            numpy.save(dir_name + '/wavelengths.npy', self._spectra[:, :, 0])
            numpy.save(dir_name + '/spectra.npy', self._spectra[:, :, 1])

        # check which columns are trivial (==0)
        col_trivial = []
        for i_data in range(len(self._data)):
            if i_data < len(self._data) and sum(self._data[i_data, :]) == 0:
                col_trivial.append(i_data)

        # delete columns and data names
        for i_col in range(len(col_trivial)-1, -1, -1):
            del self._data_names[col_trivial[i_col]+1]
            self._data = numpy.delete(self._data, col_trivial[i_col], 0)

        # sort data names dictionary
        i_data = 0
        for key in self._data_names.keys():
            self._data_names[i_data] = self._data_names.pop(key)
            i_data += 1

        # create variables for the fit data
        self._fit_functions = numpy.zeros((self._nx, 6))
        self._fit_initial_parameters = numpy.zeros((self._nx, 6, 4))
        self._fit_initial_parameters[:] = numpy.NAN
        self._fit_optimized_parameters = numpy.zeros((self._nx, 6, 4))
        self._fit_optimized_parameters[:] = numpy.NAN

        # set focus to the center of the map
        self._focus = int(self._nx / 2)

        # set fit area
        self._fit_area = (-0.5, self._nx)

    def get_data(self, **kwargs):

        # if no data index is given, return the currently selected data
        if 'data_index' in kwargs.keys():
            data_index = kwargs['data_index']
        else:
            data_index = self._selected_data

        # check if the id belongs to a data or a micrograph or a fit parameter
        if data_index == 0:

            return numpy.transpose(self._spectra[:, :, 1])

        elif 0 < data_index <= len(self._data):

            if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
                return self._data[data_index-1]
            elif kwargs['pixel'] == -2:
                return self._data[data_index-1][self._focus]
            else:
                return self._data[data_index-1][kwargs['pixel']]

        else:

            # return fit data
            data_index -= len(self._data)+1
            parameters = []
            for i_peak in range(6):
                if numpy.sum(numpy.int_(self._fit_functions[:, i_peak] == 3)) > 0:
                    parameters.append([i_peak, 0])
                    parameters.append([i_peak, 1])
                    parameters.append([i_peak, 2])
                    parameters.append([i_peak, 3])
                elif numpy.sum(numpy.int_(self._fit_functions[:, i_peak] == 1)) > 0 or \
                        numpy.sum(numpy.int_(self._fit_functions[:, i_peak] == 2)) > 0:
                    parameters.append([i_peak, 0])
                    parameters.append([i_peak, 1])
                    parameters.append([i_peak, 2])
            return self._fit_optimized_parameters[:, parameters[data_index][0], parameters[data_index][1]]

    def get_data_name(self, **kwargs):

        # if no data index is given, return the currently selected data
        if 'data_index' in kwargs.keys():
            data_index = kwargs['data_index']
        else:
            data_index = self._selected_data

        # check whether a data or a micrograph is selected
        if data_index < len(self._data)+1:

            # return data name
            return self._data_names[data_index]

        else:

            # return parameter name
            data_index = data_index - len(self._data) - 1
            parameters = []
            for i_peak in range(6):
                if numpy.sum(numpy.int_(self._fit_functions[:, i_peak] == 3)) > 0:
                    parameters.append([i_peak, 'A'])
                    parameters.append([i_peak, 'B'])
                    parameters.append([i_peak, 'C'])
                    parameters.append([i_peak, 'D'])
                elif numpy.sum(numpy.int_(self._fit_functions[:, i_peak] == 1)) > 0 or \
                        numpy.sum(numpy.int_(self._fit_functions[:, i_peak] == 2)) > 0:
                    parameters.append([i_peak, 'A'])
                    parameters.append([i_peak, 'B'])
                    parameters.append([i_peak, 'C'])
            return parameters[data_index][1]+str(parameters[data_index][0])

    def get_fit(self, **kwargs):

        # if no pixel was provided the current pixel is returned
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            px = self._focus
        else:
            px = kwargs['pixel']

        return self._fit_functions[px, :], self._fit_initial_parameters[px, :, :], self._fit_optimized_parameters[px, :, :]

    def get_fit_functions(self):

        return self._fit_functions[:, :]

    def get_size(self):

        # return the size of the map
        return [self._nx]

    def get_spectrum(self, **kwargs):

        # if no pixel is given, return the focussed pixel's spectrum
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            return self._spectra[self._focus, :, :]
        else:
            return self._spectra[kwargs['pixel'], :, :]

    def set_fit(self, fit_functions, fit_initial_parameters, fit_optimized_parameters, **kwargs):

        # if no pixel was provided the current pixel is updated
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            px = self._focus
        else:
            px = kwargs['pixel']

        # clear the old fit data
        self._fit_functions[px, :] = numpy.zeros(6)
        self._fit_initial_parameters[px, :, :] = numpy.NAN
        self._fit_optimized_parameters[px, :, :] = numpy.NAN

        # set new fit data
        i_parameter = 0
        for i_peak in range(len(fit_functions)):
            if fit_functions[i_peak] == 1:
                self._fit_functions[px, i_peak] = 1
                self._fit_initial_parameters[px, i_peak, :3] = fit_initial_parameters[i_parameter:i_parameter+3]
                self._fit_initial_parameters[px, i_peak, 3] = 0
                self._fit_optimized_parameters[px, i_peak, :3] = fit_optimized_parameters[i_parameter:i_parameter+3]
                self._fit_optimized_parameters[px, i_peak, 3] = 0
                i_parameter += 3
            elif fit_functions[i_peak] == 2:
                self._fit_functions[px, i_peak] = 2
                self._fit_initial_parameters[px, i_peak, :3] = fit_initial_parameters[i_parameter:i_parameter+3]
                self._fit_initial_parameters[px, i_peak, 3] = 0
                self._fit_optimized_parameters[px, i_peak, :3] = fit_optimized_parameters[i_parameter:i_parameter+3]
                self._fit_optimized_parameters[px, i_peak, 3] = 0
                i_parameter += 3
            elif fit_functions[i_peak] == 3:
                self._fit_functions[px, i_peak] = 3
                self._fit_initial_parameters[px, i_peak, :] = fit_initial_parameters[i_parameter:i_parameter+4]
                self._fit_optimized_parameters[px, i_peak, :] = fit_optimized_parameters[i_parameter:i_parameter+4]
                i_parameter += 4

    def set_focus(self, focus):

        # set focus if it is within the map
        if 0 <= numpy.round(focus) < self._nx:
            self._focus = int(numpy.round(focus))

    def set_spectrum(self, spectrum, **kwargs):

        # if no pixel was provided update the focused pixel
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            px = self._focus
        else:
            px = kwargs['pixel']

        # update spectrum
        self._spectra[px, :, :] = spectrum

        # update integrated counts
        self._data[0, px] = numpy.sum(spectrum[:, 1])


class Map2D(Map):

    """
    Map2D
    Class for two-dimensional maps which are mainly spatial maps.
    """

    def __init__(self, map_id, file_name):

        # call super init
        super(Map2D, self).__init__()

        # set dimension of the map
        self._dimension = 2

        # set the map id
        self._id = map_id

        # get the directory from path
        dir_name = path.dirname(file_name)

        # check for the file type of the map
        # .dat files are acquired in the PGI9 (FZJ) lab using QTLab
        if file_name[-4:] == '.dat':

            #  load the data file
            file_data = numpy.loadtxt(file_name)

            # read the number of pixels and check for consistency
            self._nx = int(file_data[-1, 1]) + 1
            self._ny = int(file_data[-1, 2]) + 1
            if self._nx * self._ny < file_data.shape[0]:
                self._nx -= 1
                self._ny = file_data[-1 - self._ny, 2]

            # read the resolution of the CCD from the first spectrum file
            spectrum = numpy.loadtxt(dir_name + '/spectrum_0_0.asc')
            self._resolution = len(spectrum)

            # create variables for the data
            self._spectra = numpy.zeros((self._nx, self._ny, self._resolution, 2))
            self._data = numpy.zeros((file_data.shape[1] - 2, self._nx, self._ny))

            # read column names and map name
            self._data_names = {0: 'intensity'}
            file_lines = open(file_name).readlines()
            for i_line in range(len(file_lines)):
                line_split = file_lines[i_line].split()
                if len(line_split) > 1:
                    if line_split[1] == 'Filename:':
                        self._map_name = line_split[2][:-4]
                    if line_split[1] == 'Column' and int(line_split[2][:-1]) > 3:
                        next_split = file_lines[i_line + 1].split()
                        self._data_names[int(line_split[2][:-1]) - 3] = ' '.join(next_split[2:])

            # check if there are .npy files available to accelerate the loading procedure
            if path.isfile(dir_name + '/spectra.npy') and path.isfile(dir_name + '/energies.npy'):

                # load data from npy files
                self._spectra[:, :, :, 0] = numpy.load(dir_name + '/energies.npy')
                self._spectra[:, :, :, 1] = numpy.load(dir_name + '/spectra.npy')

                # integrate counts
                self._data[0, :, :] = numpy.sum(self._spectra[:, :, :, 1], axis=2)

                # read other quantities
                for ix in range(self._nx):
                    for iy in range(self._ny):
                        self._data[1:, ix, iy] = file_data[ix * self._ny + iy, 3:]

            # if no .npy files are available the spectra need to be loaded from .asc files
            else:

                # create progressbar dialog
                progress_dialog = QProgressDialog('', '', 0, self._nx * self._ny,
                                                  QApplication.instance().windows['mapWindow'])
                progress_dialog.setWindowTitle('Loading Map')
                progress_dialog.setWindowModality(Qt.WindowModal)
                progress_dialog.setCancelButton(None)
                progress_dialog.show()

                # read data
                for ix in range(self._nx):
                    for iy in range(self._ny):
                        spectrum = numpy.loadtxt(dir_name + '/spectrum_' + str(ix) + '_' + str(iy) + '.asc')
                        spectrum[:, 0] = 1e-9 * 1239.841842144513 / spectrum[:, 0]
                        spectrum = numpy.flipud(spectrum)
                        self._spectra[ix, iy, :, :] = spectrum
                        self._data[0, ix, iy] = numpy.sum(spectrum[:, 1])
                        self._data[1:, ix, iy] = file_data[ix * self._ny + iy, 3:]
                        progress_dialog.setValue(ix * self._ny + iy + 1)

                # save .npy files for the next time the map is loaded
                numpy.save(dir_name + '/energies.npy', self._spectra[:, :, :, 0])
                numpy.save(dir_name + '/spectra.npy', self._spectra[:, :, :, 1])

        # .txt files are acquired in the Heinz Group at Stanford
        elif file_name[-4:] == '.txt':

            # set map name to the file name
            self._map_name = file_name[len(dir_name)+1:-4]

            # read text file
            file_data = open(file_name)
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

            # set the resolution to the number of pixels of the CCD
            self._resolution = len(energies)

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
            self._nx = len(x_positions)
            self._ny = len(y_positions)

            # create data structures for spectra and position data
            self._spectra = numpy.zeros((self._nx, self._ny, self._resolution, 2))
            self._data_names = {0: 'intensity', 1: 'x position', 2: 'y position'}
            self._data = numpy.zeros((3, self._nx, self._ny))

            # read spectra and position data
            i_px = 0
            for ix in range(self._nx):
                for iy in range(self._ny):
                    self._spectra[ix, iy, :, 0] = numpy.flipud(energies)
                    self._spectra[ix, iy, :, 1] = numpy.flipud(data_array[i_px, 2:])
                    self._data[0, ix, iy] = numpy.sum(self._spectra[ix, iy, :, 1])
                    self._data[1, ix, iy] = data_array[i_px, 0]
                    self._data[2, ix, iy] = data_array[i_px, 1]
                    i_px += 1

        # check which columns are trivial (==0)
        col_trivial = []
        for i_data in range(len(self._data)):
            if numpy.sum(self._data[i_data, :]) == 0:
                col_trivial.append(i_data)

        # delete trivial columns and data names
        for i_col in range(len(col_trivial)-1, -1, -1):
            del self._data_names[col_trivial[i_col]]
            self._data = numpy.delete(self._data, col_trivial[i_col], 0)

        # sort data names dictionary again
        i_data = 0
        data_names_new = {}
        for key in self._data_names.keys():
            data_names_new[i_data] = self._data_names[key]
            i_data += 1
        self._data_names = data_names_new

        # create variables for the fit data
        self._fit_functions = numpy.zeros((self._nx, self._ny, 6))
        self._fit_initial_parameters = numpy.zeros((self._nx, self._ny, 6, 4))
        self._fit_initial_parameters[:, :, :, :] = numpy.NAN
        self._fit_optimized_parameters = numpy.zeros((self._nx, self._ny, 6, 4))
        self._fit_optimized_parameters[:, :, :, :] = numpy.NAN

        # set focus to the center of the map
        self._focus = [int(self._nx / 2), int(self._ny / 2)]

        # dictionary for micrographs
        self._micrographs = {}
        self._micrograph_names = {}

    def add_micrograph(self, file_name, micrograph):

        # obtain maximum key so far
        if len(self._micrographs) == 0:
            max_key = -1
        else:
            max_key = max(self._micrographs.keys())

        # add micrograph and micrograph name
        self._micrographs[int(max_key) + 1] = micrograph
        self._micrograph_names[int(max_key) + 1] = file_name

        return len(self._data_names) + int(max_key) + 1

    def clear_fit(self, **kwargs):

        # if no pixel was provided the current pixel is updated
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            px = self._focus[0]
            py = self._focus[1]
        else:
            px = kwargs['pixel'][0]
            py = kwargs['pixel'][1]

        # clear fit
        self._fit_functions[px, py, :] = numpy.zeros(6)
        self._fit_initial_parameters[px, py, :, :] = numpy.NAN
        self._fit_optimized_parameters[px, py, :, :] = numpy.NAN

        # emit signal
        if 'emit' not in kwargs or kwargs['emit']:
            self._app.fit_changed.emit(self._id, [px, py])

    def get_data(self, **kwargs):

        # if no data index is given, return the currently selected data
        if 'data_index' in kwargs.keys():
            data_index = kwargs['data_index']
        else:
            data_index = self._selected_data

        # check if the id belongs to a data or a micrograph or a fit parameter
        if data_index < len(self._data):

            # check if the whole map data (pixel = -1) or the focussed pixel (pixel = -2)
            # or a specific pixel (pixel = [x,y]) are requested
            if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
                return self._data[data_index]
            elif kwargs['pixel'] == -2:
                return self._data[data_index][self._focus[0], self._focus[1]]
            else:
                return self._data[data_index][kwargs['pixel'][0], kwargs['pixel'][1]]

        elif data_index < len(self._data) + len(self._micrographs):

            # return micrograph
            data_index -= len(self._data)
            return self._micrographs[data_index]
            
        else:
            
            # check which fit parameters are there
            data_index -= len(self._data) + len(self._micrographs)
            parameters = []
            for i_peak in range(6):
                if numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] > 0)) > 0:
                    parameters.append([i_peak, 0])
                    parameters.append([i_peak, 1])
                if numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 2)) > 0 or \
                        numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 3)) > 0:
                    parameters.append([i_peak, 2])
                if numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 1)) > 0 or \
                        numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 3)) > 0:
                    parameters.append([i_peak, 3])
                if numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] > 0)) > 0:
                    parameters.append([i_peak, 4])

            # return intensities
            if parameters[data_index][1] == 0:
                return self._fit_optimized_parameters[:, :, parameters[data_index][0], 0]

            # return central energies
            elif parameters[data_index][1] == 1:
                return self._fit_optimized_parameters[:, :, parameters[data_index][0], 1]

            # return sigma
            elif parameters[data_index][1] == 2:
                sigma = numpy.zeros((self._nx, self._ny))
                sigma[:] = numpy.NAN
                sigma_from_gaussian = self._fit_optimized_parameters[:, :, parameters[data_index][0], 2][self._fit_functions[:, :, parameters[data_index][0]] == 2]
                sigma_from_voigt = self._fit_optimized_parameters[:, :, parameters[data_index][0], 2][self._fit_functions[:, :, parameters[data_index][0]] == 3]
                sigma[self._fit_functions[:, :, parameters[data_index][0]] == 2] = sigma_from_gaussian
                sigma[self._fit_functions[:, :, parameters[data_index][0]] == 3] = sigma_from_voigt
                return 1000*sigma

            # return gamma
            elif parameters[data_index][1] == 3:
                gamma = numpy.zeros((self._nx, self._ny))
                gamma[:] = numpy.NAN
                gamma_from_lorentzian = self._fit_optimized_parameters[:, :, parameters[data_index][0], 2][self._fit_functions[:, :, parameters[data_index][0]] == 1]
                gamma_from_voigt = self._fit_optimized_parameters[:, :, parameters[data_index][0], 3][self._fit_functions[:, :, parameters[data_index][0]] == 3]
                gamma[self._fit_functions[:, :, parameters[data_index][0]] == 1] = gamma_from_lorentzian
                gamma[self._fit_functions[:, :, parameters[data_index][0]] == 3] = gamma_from_voigt
                return 1000*gamma

            # return FWHM
            elif parameters[data_index][1] == 4:
                fwhm = numpy.zeros((self._nx, self._ny))
                fwhm[:] = numpy.NAN
                sigma_from_gaussian = self._fit_optimized_parameters[:, :, parameters[data_index][0], 2][self._fit_functions[:, :, parameters[data_index][0]] == 2]
                gamma_from_lorentzian = self._fit_optimized_parameters[:, :, parameters[data_index][0], 2][self._fit_functions[:, :, parameters[data_index][0]] == 1]
                gamma_from_voigt = self._fit_optimized_parameters[:, :, parameters[data_index][0], 3][self._fit_functions[:, :, parameters[data_index][0]] == 3]
                sigma_from_voigt = self._fit_optimized_parameters[:, :, parameters[data_index][0], 2][self._fit_functions[:, :, parameters[data_index][0]] == 3]
                fwhm[self._fit_functions[:, :, parameters[data_index][0]] == 1] = 2*gamma_from_lorentzian
                fwhm[self._fit_functions[:, :, parameters[data_index][0]] == 2] = 2.35482*sigma_from_gaussian
                fwhm[self._fit_functions[:, :, parameters[data_index][0]] == 3] = 0.5346*2.*gamma_from_voigt+numpy.sqrt(0.2166*4.*gamma_from_voigt**2.+2.35482**2.*sigma_from_voigt**2.)
                return 1000*fwhm

    def get_data_name(self, **kwargs):

        # if no data index is given, return the currently selected data name
        if 'data_index' in kwargs.keys():
            data_index = kwargs['data_index']
        else:
            data_index = self._selected_data

        # check whether a data or a micrograph or a fit parameter is selected
        if data_index < len(self._data):
            # return data name
            return self._data_names[data_index]

        elif data_index < len(self._data) + len(self._micrographs):

            # return micrograph name
            return self._micrograph_names[data_index - len(self._data)]

        else:

            # return parameter name
            data_index = data_index - len(self._data)-len(self._micrographs)
            parameters = []
            subscripts = [u'\u2081', u'\u2082', u'\u2083', u'\u2084', u'\u2085', u'\u2086']
            for i_peak in range(6):
                if numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] > 0)) > 0:
                    parameters.append('I'+subscripts[i_peak])
                    parameters.append('ε'+subscripts[i_peak])
                if numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 1)) > 0 or \
                        numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 3)) > 0:
                    parameters.append('σ'+subscripts[i_peak])
                if numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 2)) > 0 or \
                        numpy.sum(numpy.int_(self._fit_functions[:, :, i_peak] == 3)) > 0:
                    parameters.append('γ'+subscripts[i_peak])
                parameters.append('FWHM'+subscripts[i_peak])
            return parameters[data_index]

    def get_fit(self, **kwargs):

        # if no pixel was provided the current pixel is returned
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            px = self._focus[0]
            py = self._focus[1]
        else:
            px = kwargs['pixel'][0]
            py = kwargs['pixel'][1]
            
        return self._fit_functions[px, py, :], self._fit_initial_parameters[px, py, :, :], self._fit_optimized_parameters[px, py, :, :]
        
    def get_fit_functions(self, **kwargs):

        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            return self._fit_functions[:, :, :]
        elif kwargs['pixel'] == -2:
            return self._fit_functions[self._focus[0], self._focus[1], :]
        else:
            return self._fit_functions[kwargs['pixel'][0], kwargs['pixel'][1], :]

    def get_fit_parameters(self, **kwargs):

        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            return self._fit_optimized_parameters[:, :, :, :]
        elif kwargs['pixel'] == -2:
            return self._fit_optimized_parameters[self._focus[0], self._focus[1], :, :]
        else:
            return self._fit_optimized_parameters[kwargs['pixel'][0], kwargs['pixel'][1], :, :]

    def get_micrographs(self):

        # return micrographs
        return self._micrographs

    def get_micrograph_names(self):

        # return micrograph names
        return self._micrograph_names

    def get_size(self):

        return [self._nx, self._ny]

    def get_spectrum(self, **kwargs):

        # if no pixel is given, return the focussed pixel's spectrum
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            return self._spectra[self._focus[0], self._focus[1]]
        else:
            return self._spectra[kwargs['pixel'][0], kwargs['pixel'][1], :, :]
    
    def set_fit(self, fit_functions, fit_initial_parameters, fit_optimized_parameters, **kwargs):

        # if no pixel was provided the current pixel is updated
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            px = self._focus[0]
            py = self._focus[1]
        else:
            px = kwargs['pixel'][0]
            py = kwargs['pixel'][1]

        # clear the old fit data
        self._fit_functions[px, py, :] = numpy.zeros(6)
        self._fit_initial_parameters[px, py, :, :] = numpy.NAN
        self._fit_optimized_parameters[px, py, :, :] = numpy.NAN

        # set new fit data
        i_parameter = 0
        for i_peak in range(len(fit_functions)):
            if fit_functions[i_peak] == 1:
                self._fit_functions[px, py, i_peak] = 1
                self._fit_initial_parameters[px, py, i_peak, :3] = fit_initial_parameters[i_parameter:i_parameter+3]
                self._fit_initial_parameters[px, py, i_peak, 3] = 0
                self._fit_optimized_parameters[px, py, i_peak, :3] = fit_optimized_parameters[i_parameter:i_parameter+3]
                self._fit_optimized_parameters[px, py, i_peak, 3] = 0
                i_parameter += 3
            elif fit_functions[i_peak] == 2:
                self._fit_functions[px, py, i_peak] = 2
                self._fit_initial_parameters[px, py, i_peak, :3] = fit_initial_parameters[i_parameter:i_parameter+3]
                self._fit_initial_parameters[px, py, i_peak, 3] = 0
                self._fit_optimized_parameters[px, py, i_peak, :3] = fit_optimized_parameters[i_parameter:i_parameter+3]
                self._fit_optimized_parameters[px, py, i_peak, 3] = 0
                i_parameter += 3
            elif fit_functions[i_peak] == 3:
                self._fit_functions[px, py, i_peak] = 3
                self._fit_initial_parameters[px, py, i_peak, :] = fit_initial_parameters[i_parameter:i_parameter+4]
                self._fit_optimized_parameters[px, py, i_peak, :] = fit_optimized_parameters[i_parameter:i_parameter+4]
                i_parameter += 4

        # emit signal
        if 'emit' not in kwargs or kwargs['emit']:
            self._app.fit_changed.emit(self._id, [px, py])

    def set_focus(self, focus):

        # set focus if it is within the map
        if 0 <= numpy.round(focus[0]) < self._nx:
            if 0 <= numpy.round(focus[1]) < self._ny:
                self._focus = [int(numpy.round(focus[0])), int(numpy.round(focus[1]))]

                # emit signal
                self._app.focus_changed.emit(self._id)

    def set_interval(self, side, value):

        # check if a good interval has been given
        if side == 'left' and value < 0:
            return
        if side == 'right' and value >= self._resolution:
            return
        if side == 'left' and self._interval[1] <= value:
            return
        if side == 'right' and self._interval[0] >= value:
            return

        # set interval
        if side == 'left':
            self._interval[0] = value
        if side == 'right':
            self._interval[1] = value

        # recalculate intensities
        for ix in range(self._nx):
            for iy in range(self._ny):
                spectrum = self._spectra[ix, iy, :, :]
                self._data[0, ix, iy] = numpy.sum(spectrum[self._interval[0]:self._interval[1], 1])

        # emit signal
        self._app.interval_changed.emit(self._id)

    def set_spectrum(self, spectrum, **kwargs):

        # if no pixel was provided update the focused pixel
        if 'pixel' not in kwargs.keys() or kwargs['pixel'] == -1:
            px = self._focus[0]
            py = self._focus[1]
        else:
            px = kwargs['pixel'][0]
            py = kwargs['pixel'][1]

        # update spectrum
        self._spectra[px, py, :, :] = spectrum

        # update integrated counts
        self._data[0, px, py] = numpy.sum(spectrum[:, 1])

        # emit signal
        if 'emit' not in kwargs or kwargs['emit']:
            self._app.spectrum_changed.emit(self._id, [px, py])


class MapList(QObject):

    """
    MapList
    A map list stores all maps loaded into the program.
    """

    def __init__(self):

        # link app
        self._app = QApplication.instance()

        # create dictionary for maps
        self._maps = {}

        # set flags for selected map and map counter
        self._selected = -1
        self._counter = 0
        self._id_counter = 0

        # call super init
        super(MapList, self).__init__()

    def append_1d(self, file_name):

        # check if the loaded file is a .py2ds file
        if file_name[-6:] == '.py2ds':

            # pickle map object from .py2ds file
            map_file = open(file_name, 'rb')
            self._maps[self._id_counter] = pickle.load(map_file)
            self._maps[self._id_counter].set_id(self._id_counter)
            self._maps[self._id_counter].set_map_list(self)

        else:

            # create a new map object and select this map
            self._maps[self._id_counter] = Map1D(self._id_counter, file_name)
            self._maps[self._id_counter].set_map_list(self)

        # increase the map  and id counter
        self._counter += 1
        self._id_counter += 1

        # emit signal
        self._app.map_added.emit(self._id_counter - 1)

        # return map object
        return self._maps[self._id_counter - 1]

    def append_2d(self, file_name):

        # check if the loaded file is a .py2dl file
        if file_name[-6:] == '.py2dl':

            # pickle map object from .py2dl file
            map_file = open(file_name, 'rb')
            self._maps[self._id_counter] = pickle.load(map_file)
            self._maps[self._id_counter].set_id(self._id_counter)
            self._maps[self._id_counter].set_app(self._app)

        else:

            # create a new map object and select this map
            self._maps[self._id_counter] = Map2D(self._id_counter, file_name)
            self._maps[self._id_counter].set_app(self._app)

        # increase the map  and id counter
        self._counter += 1
        self._id_counter += 1

        # emit signal
        self._app.map_added.emit(self._id_counter - 1)

        # return map object
        return self._maps[self._id_counter - 1]

    def get_count(self):

        # return the map counter
        return self._counter

    def get_map(self, map_id):

        return self._maps[map_id]

    def get_maps(self):

        # return maps
        return self._maps

    def get_selected_map(self):

        # return currently selected map object
        return self._selected

    def remove_map(self, map_handle):

        # get id of the map that is to be removed
        map_id = map_handle.get_id()

        # remove map from dictionary
        del self._maps[map_id]

        # decrease map counter
        self._counter -= 1

        # emit signal
        self._app.map_removed.emit(map_id)

    def reset(self):

        # create dictionary for maps
        self._maps = {}

        # set flags for selected map and map counter
        self._selected = -1
        self._counter = 0
        self._id_counter = 0

    def save_map(self, file_name):

        # dump map object to the pickle file
        self._selected.set_app(None)
        dump_file = open(file_name, 'wb')
        pickle.dump(self._selected, dump_file, protocol=pickle.HIGHEST_PROTOCOL)
        self._selected.set_app(self._app)

    def set_selected_map(self, map_handle):

        # set the selected map flag
        self._selected = map_handle

        # emit signal
        self._app.selected_map_changed.emit(map_handle.get_id())
