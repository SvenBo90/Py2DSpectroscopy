# general imports
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QSizePolicy
from PyQt5.QtGui import QIcon
import numpy
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import gridspec, image
import matplotlib.patches as patches
# import UI
from UIs.colormapDialogUi import UiColormapDialog


class ColormapDialog(QDialog):

    def __init__(self, parent, current_colormap):

        # call widget init
        QDialog.__init__(self, parent)

        # define available colormaps
        colormaps = ['bwr', 'gnuplot', 'gnuplot2', 'inferno', 'nipy_spectral', 'seismic', 'viridis']

        # load and set up UI
        self.ui = UiColormapDialog(self)

        # fill combobox with colormaps
        current_id = 0
        for i_colormap in range(len(colormaps)):
            if colormaps[i_colormap] == current_colormap:
                current_id = i_colormap
            self.ui.colormap_combobox.addItem(QIcon('./img/cm_'+colormaps[i_colormap]+'.png'), colormaps[i_colormap])
        self.ui.colormap_combobox.setCurrentIndex(current_id)

    def get_colormap(self):

        # return the colormap selection
        return self.ui.colormap_combobox.currentIndex()


class PlotCanvas(FigureCanvas):

    def add_callback(self, event, callback):

        # add callback
        self._fig.canvas.mpl_connect(event, callback)

    def add_toolbar(self, parent):

        # add toolbar
        self._toolbar = NavigationToolbar(self._fig.canvas, parent)

    def get_toolbar_active(self):

        # return the status of the toolbar
        return self._toolbar._active


class MapCanvas1D(PlotCanvas):

    def __init__(self, parent, map_handle):

        # link app
        self._app = QApplication.instance()

        # link map
        self._map = map_handle

        # set extent
        self._extent = [self._map.get_resolution(), self._map.get_size()[0]]

        # create figure
        app_dpi_x = float(QApplication.desktop().physicalDpiX())
        app_dpi_y = float(QApplication.desktop().physicalDpiY())
        self._fig = Figure(figsize=(600./app_dpi_x, 350./app_dpi_y), dpi=app_dpi_x)
        self._fig.set_facecolor('#f7f6f6')

        # create a grid for plot and colorbar
        gs = gridspec.GridSpec(1, 2, width_ratios=[10, 1])

        # create axes for plot
        self._axes = self._fig.add_subplot(gs[0])
        self._axes.set_xlabel('x pixel')
        self._axes.set_ylabel('y pixel')
        self._axes.set_title(self._map.get_data_name())

        # create plots
        self._map_plot_1d, = self._axes.plot([0], [0], color='black')
        self._map_plot_2d = self._axes.imshow(self._map.get_data(), animated=True, aspect='auto',
                                              interpolation='none', origin='lower', cmap='nipy_spectral')

        # create crosshair
        self._crosshair_x, = self._axes.plot([0], [0], color='black')

        # create axes for colorbar
        self._caxes = self._fig.add_subplot(gs[1])
        self._colorbar = self._fig.colorbar(self._map_plot_2d, cax=self._caxes)

        # set tight layout
        self._fig.tight_layout()

        # call super canvas init
        FigureCanvas.__init__(self, self._fig)

        # set parent widget
        self.setParent(parent)

        # set size policy
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # update geometry
        FigureCanvas.updateGeometry(self)

        self._fig.canvas.draw()

    def create_area_map(self, x1, x2):

        # check boundaries for consistency
        if x2 < x1:
            tmp = x2
            x2 = x1
            x1 = tmp

        # create rectangle patch
        self._area_rectangle = patches.Rectangle((-1000000000, x1 - 0.5), 2000000000, x2-x1+1, alpha=0.5)
        self._axes.add_patch(self._area_rectangle)

        # redraw
        self._fig.canvas.draw()

    def update_area_map(self, x1, x2):

        # check boundaries for consistency
        if x2 < x1:
            tmp = x2
            x2 = x1
            x1 = tmp

        # update rectangle patch
        self._area_rectangle.set_y(x1-0.5)
        self._area_rectangle.set_height(x2-x1+1)

        # redraw
        self._fig.canvas.draw()

    def destroy_area_map(self):

        # destroy rectangle patch
        self._area_rectangle.remove()

        # redraw
        self._fig.canvas.draw()

    def create_threshold_map(self, threshold_data, threshold):

        # create threshold map
        self._threshold_map = self._axes.contourf(numpy.transpose([threshold_data, threshold_data]),
                                                  [threshold[0], threshold[1]], origin='lower',
                                                  alpha=0.5,
                                                  extent=[-100000000, 100000000, -0.5, self._extent[1] - 0.5])

        # redraw
        self._fig.canvas.draw()

    def update_threshold_map(self, threshold_data, threshold):

        # remove old threshold map
        for collection in self._threshold_map.collections:
            collection.remove()

        # create new threshold map
        self._threshold_map = self._axes.contourf(numpy.transpose([threshold_data, threshold_data]),
                                                  [threshold[0], threshold[1]], origin='lower',
                                                  alpha=0.5,
                                                  extent=[-100000000, 100000000, -0.5, self._extent[1] - 0.5])

        # redraw
        self._fig.canvas.draw()

    def destroy_threshold_map(self):

        # destroy threshold map
        for collection in self._threshold_map.collections:
            collection.remove()

        # redraw
        self._fig.canvas.draw()

    def update_crosshair(self):

        # get focus
        focus = self._map.get_focus()

        # remove old crosshair
        self._axes.lines.remove(self._crosshair_x)

        # plot new crosshair
        self._crosshair_x, = self._axes.plot([-9999999999, 9999999999], [focus, focus], color='black')

        # redraw canvas
        self._fig.canvas.draw()

    def update_data(self, fix_limits=True):

        # get data
        data = self._map.get_data()

        # get current limits
        old_lim = numpy.array(self._axes.get_ylim())

        # check if the data is a 1D data or 2D (spectra) data
        if len(data.shape) == 2:

            # plot new 2d data
            self._map_plot_2d.set_data(data)

            # set extent and axes limits
            self._map_plot_2d.set_extent([-0.5, self._extent[0] - 0.5, -0.5, self._extent[1] - 0.5])
            if not fix_limits:
                self._axes.set_ylim([-0.5, self._extent[1] - 0.5])
            else:
                self._axes.set_ylim(old_lim)
            self._axes.set_xlim([-0.5, self._extent[0] - 0.5])

            # set visibilities
            self._map_plot_1d.set_visible(False)
            self._map_plot_2d.set_visible(True)

        else:

            self._axes.lines.remove(self._map_plot_1d)
            self._map_plot_1d, = self._axes.plot(data, range(self._extent[1]), color='black')

            # set axes limits
            self._axes.set_xlim([numpy.min(data), numpy.max(data)])
            if not fix_limits:
                self._axes.set_ylim([-0.5, self._extent[1] - 0.5])
            else:
                self._axes.set_ylim(old_lim)
            self._axes.set_xlim([numpy.min(data[~numpy.isnan(data)]), numpy.max(data[~numpy.isnan(data)])])

            # plot new 1d data
            self._map_plot_1d.set_visible(True)
            self._map_plot_2d.set_visible(False)

        # update title
        self._axes.set_title(self._map.get_data_name())

        # set tight layout
        self._fig.tight_layout()

        # redraw canvas
        self._fig.canvas.draw()


class MapCanvas2D(PlotCanvas):

    def __init__(self, parent, map_handle):

        # link app
        self._app = QApplication.instance()

        # link map
        self._map = map_handle

        # set extent
        self._extent = self._map.get_size()

        # create figure
        app_dpi_x = float(QApplication.desktop().physicalDpiX())
        app_dpi_y = float(QApplication.desktop().physicalDpiY())
        self._fig = Figure(figsize=(600./app_dpi_x, 350./app_dpi_y), dpi=app_dpi_x)
        self._fig.set_facecolor('#f7f6f6')

        # create a grid for plot and colorbar
        gs = gridspec.GridSpec(1, 2, width_ratios=[10, 1])

        # create axes for plot
        self._axes = self._fig.add_subplot(gs[0])
        self._axes.set_xlabel('x pixel')
        self._axes.set_ylabel('y pixel')
        self._axes.set_title(self._map.get_data_name())

        # create plot
        self._map_plot = self._axes.imshow(numpy.transpose(self._map.get_data()), animated=True, aspect='auto',
                                           interpolation='none', origin='lower', cmap='nipy_spectral')

        # create crosshair
        self._crosshair_x, = self._axes.plot([0], [0], color='black')
        self._crosshair_y, = self._axes.plot([0], [0], color='black')

        # create axes for colorbar
        self._caxes = self._fig.add_subplot(gs[1])
        self._colorbar = self._fig.colorbar(self._map_plot, cax=self._caxes)

        # set tight layout
        self._fig.tight_layout()

        # call super canvas init
        FigureCanvas.__init__(self, self._fig)

        # set parent widget
        self.setParent(parent)

        # set size policy
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # update geometry
        FigureCanvas.updateGeometry(self)

        # draw canvas
        self._fig.canvas.draw()

    def add_toolbar(self, parent):

        # add toolbar
        self._toolbar = MapCanvas2DToolbar(self._fig.canvas, parent)

    def create_area_map(self, x1, x2, y1, y2):

        # check boundaries for consistency
        if x2 < x1:
            tmp = x2
            x2 = x1
            x1 = tmp
        if y2 < y1:
            tmp = y2
            y2 = y1
            y1 = tmp

        # create rectangle patch
        self._area_rectangle = patches.Rectangle((x1-0.5, y1-0.5), x2-x1+1, y2-y1+1, linewidth=1.5,
                                                 facecolor=(1, 1, 1, 0.5), edgecolor=(0, 0, 0, 1))
        self._axes.add_patch(self._area_rectangle)

        # redraw
        self._fig.canvas.draw()

    def update_area_map(self, x1, x2, y1, y2):

        # check boundaries for consistency
        if x2 < x1:
            tmp = x2
            x2 = x1
            x1 = tmp
        if y2 < y1:
            tmp = y2
            y2 = y1
            y1 = tmp

        # update rectangle patch
        self._area_rectangle.set_x(x1-0.5)
        self._area_rectangle.set_y(y1-0.5)
        self._area_rectangle.set_width(x2-x1+1)
        self._area_rectangle.set_height(y2-y1+1)

        # redraw
        self._fig.canvas.draw()

    def destroy_area_map(self):

        # remove rectangle patch
        self._area_rectangle.remove()

        # redraw
        self._fig.canvas.draw()

    def create_threshold_map(self, threshold_data, threshold):

        # create threshold map
        self._threshold_map_lines = self._axes.contour(numpy.transpose(threshold_data), threshold, colors=('k', 'k'),
                                                       origin='lower',
                                                       extent=[-0.5, self._extent[0] - 0.5, -0.5, self._extent[1] - 0.5])
        self._threshold_map_filling = self._axes.contourf(numpy.transpose(threshold_data), threshold, colors='w',
                                                          origin='lower',
                                                          extent=[-0.5, self._extent[0] - 0.5, -0.5, self._extent[1] - 0.5],
                                                          alpha=0.5)

        # redraw
        self._fig.canvas.draw()

    def update_threshold_map(self, threshold_data, threshold):

        # remove old threshold map
        for collection in self._threshold_map_lines.collections:
            collection.remove()
        for collection in self._threshold_map_filling.collections:
            collection.remove()

        # create new threshold map
        self._threshold_map_lines = self._axes.contour(numpy.transpose(threshold_data),
                                                       threshold, colors=('k', 'k'), origin='lower',
                                                       extent=[-0.5, self._extent[0] - 0.5, -0.5, self._extent[1] - 0.5])
        self._threshold_map_filling = self._axes.contourf(numpy.transpose(threshold_data),
                                                          threshold, colors='w', origin='lower',
                                                          extent=[-0.5, self._extent[0] - 0.5, -0.5, self._extent[1] - 0.5],
                                                          alpha=0.5)

        # redraw
        self._fig.canvas.draw()

    def destroy_threshold_map(self):

        # remove threshold map
        for collection in self._threshold_map_lines.collections:
            collection.remove()
        for collection in self._threshold_map_filling.collections:
            collection.remove()

        # redraw
        self._fig.canvas.draw()

    def update_crosshair(self):

        # get focus
        focus = self._map.get_focus()

        # remove old crosshair
        self._axes.lines.remove(self._crosshair_x)
        self._axes.lines.remove(self._crosshair_y)

        # plot new crosshair
        self._crosshair_x, = self._axes.plot([focus[0], focus[0]], [-9999999999, 9999999999], color='black')
        self._crosshair_y, = self._axes.plot([-9999999999, 9999999999], [focus[1], focus[1]], color='black')

        # redraw canvas
        self._fig.canvas.draw()

    def update_data(self, fix_limits=True):

        # get data
        data = self._map.get_data()

        # get current limits
        old_x_lim = numpy.array(self._axes.get_xlim())
        old_y_lim = numpy.array(self._axes.get_ylim())

        # check if the data is a 2D data or 3D micrograph data
        if len(data.shape) == 2:
            data = numpy.transpose(data)

        # set new data
        self._map_plot.set_data(data)

        # check if map size was changed (this means if the map has been rotated)
        if self._extent != self._map.get_size():
            self._extent = self._map.get_size()
            fix_limits = False

        # set extent and axes limits
        self._map_plot.set_extent([-0.5, self._extent[0] - 0.5, -0.5, self._extent[1] - 0.5])
        if not fix_limits:
            self._axes.set_xlim([-0.5, self._extent[0] - 0.5])
            self._axes.set_ylim([-0.5, self._extent[1] - 0.5])
        else:
            self._axes.set_xlim(old_x_lim)
            self._axes.set_ylim(old_y_lim)

        # update colorbar limits
        self._map_plot.set_clim([numpy.min(data[~numpy.isnan(data)]), numpy.max(data[~numpy.isnan(data)])])

        # update title
        self._axes.set_title(self._map.get_data_name())

        # set tight layout
        self._fig.tight_layout()

        # redraw canvas
        self._fig.canvas.draw()


class MapCanvas2DToolbar(NavigationToolbar):

    """
    MapCanvas2DToolbar
    Toolbar for the MapCanvas2D
    """

    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Axes Scaling', 'Toggles the axes scaling', os.path.dirname(os.path.abspath(__file__))+'/img/axis_equal', 'toggle_axes_aspect'),
            ('Colormap', 'Choose the colormap', os.path.dirname(os.path.abspath(__file__))+'/img/colormap', 'choose_colormap'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure')
        )
        NavigationToolbar.__init__(self, canvas_, parent_)

    def choose_colormap(self):

        # open micrograph dialog
        colormap_dialog = ColormapDialog(self, self.canvas._map_plot.get_cmap().name)
        colormap_dialog.exec_()

        # change the colormap
        if colormap_dialog.result() == 1:
            colormaps = ['bwr', 'gnuplot', 'gnuplot2', 'inferno', 'nipy_spectral', 'seismic', 'viridis']
            self.canvas._map_plot.set_cmap(colormaps[colormap_dialog.get_colormap()])

            # redraw
            self.canvas.draw()

    def toggle_axes_aspect(self):

        # toggle the aspect
        if self.canvas._axes.get_aspect() == 'auto':
            self.canvas._axes.set_aspect('equal')
        elif self.canvas._axes.get_aspect() == 'equal':
            self.canvas._axes.set_aspect('auto')

        # redraw
        self.canvas.draw()


class MicrographCanvas(PlotCanvas):

    def __init__(self, map_data, map_data_title, micrograph_file, parent):

        # load micrograph and flip up and down
        micrograph = image.imread(micrograph_file)
        micrograph = micrograph[-1:0:-1, :, :]

        # create figure
        app_dpi_x = float(QApplication.desktop().physicalDpiX())
        app_dpi_y = float(QApplication.desktop().physicalDpiX())
        self._fig = Figure(figsize=(940. / app_dpi_x, 350. / app_dpi_y), dpi=app_dpi_x)
        self._fig.set_facecolor('#F2F1F0')

        # create a grid for plot and colorbar
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

        # create axes for map plot
        self._map_axes = self._fig.add_subplot(gs[0])
        self._map_axes.set_title(map_data_title)
        self._map_axes.set_xticks([], [])
        self._map_axes.set_yticks([], [])

        # create axes for micrograph plot
        self._micro_axes = self._fig.add_subplot(gs[1])
        self._micro_axes.set_title('Micrograph')
        self._micro_axes.set_xticks([], [])
        self._micro_axes.set_yticks([], [])

        # create plot
        self._map_plot = self._map_axes.imshow(numpy.transpose(map_data), animated=True, aspect='auto',
                                               interpolation='none', origin='lower', cmap='nipy_spectral')
        self._plots_fixed_points = {}

        # create plot
        self._micro_plot = self._micro_axes.imshow(micrograph, animated=True, aspect='auto', interpolation='none',
                                                   origin='lower')
        self._plots_moving_points = {}

        # set tight layout
        self._fig.tight_layout()

        # call super canvas init
        FigureCanvas.__init__(self, self._fig)

        # set parent widget
        self.setParent(parent)

        # set size policy
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # update geometry
        FigureCanvas.updateGeometry(self)

    def add_toolbar(self, parent):

        # add toolbar
        self._toolbar = MicrographCanvasToolbar(self._fig.canvas, parent)

    def get_axes(self):

        return self._map_axes, self._micro_axes

    def update_points(self, fixed_points, moving_points):

        # remove old points
        for i_plot in range(len(self._plots_fixed_points)):
            self._map_axes.lines.remove(self._plots_fixed_points[i_plot])
            del self._plots_fixed_points[i_plot]
        for i_plot in range(len(self._plots_moving_points)):
            self._micro_axes.lines.remove(self._plots_moving_points[i_plot])
            del self._plots_moving_points[i_plot]

        # draw new points
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
        for i_point in range(int(len(fixed_points)/2)):
            self._plots_fixed_points[i_point], = self._map_axes.plot(fixed_points[2*i_point], fixed_points[2*i_point+1],
                                                                     color=colors[i_point], marker='o')
        for i_point in range(int(len(moving_points)/2)):
            self._plots_moving_points[i_point], = self._micro_axes.plot(moving_points[2*i_point],
                                                                        moving_points[2*i_point+1], color=colors[i_point], marker='o')

        # redraw canvas
        self._fig.canvas.draw()


class MicrographCanvasToolbar(NavigationToolbar):

    """
    MicrograpCanvashToolbar
    Toolbar for the micrograp canvas
    """

    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Axes Scaling', 'Toggles the axes scaling', os.path.dirname(os.path.abspath(__file__))+'/img/axis_equal', 'toggle_axes_aspect'),
        )
        NavigationToolbar.__init__(self, canvas_, parent_)

    def toggle_axes_aspect(self):

        # toggle the aspect
        if self.canvas._map_axes.get_aspect() == 'auto':
            self.canvas._map_axes.set_aspect('equal')
            self.canvas._micro_axes.set_aspect('equal')
        elif self.canvas._map_axes.get_aspect() == 'equal':
            self.canvas._micro_axes.set_aspect('auto')

        # redraw
        self.canvas.draw()


class SpectrumCanvas(PlotCanvas):

    def __init__(self, parent, map_handle):

        # link map
        self._map = map_handle

        # create figure
        app_dpi_x = float(QApplication.desktop().physicalDpiX())
        app_dpi_y = float(QApplication.desktop().physicalDpiX())
        self._fig = Figure(figsize=(460. / app_dpi_x, 285. / app_dpi_y), dpi=app_dpi_x)
        self._fig.set_facecolor('#F2F1F0')

        # create axes for spectrum plot
        self._axes = self._fig.add_subplot(111)
        self._axes.set_xlabel('energy [eV]')
        self._axes.set_ylabel('counts')

        # plot initial spectrum
        spectrum = self._map.get_spectrum()
        self._axes.plot(spectrum[:, 0], spectrum[:, 1], color='black', label='Spectrum')
        self._axes.plot([spectrum[0, 0], spectrum[0, 0]], [-100000000, 100000000], 'r--')
        self._axes.plot([spectrum[-1, 0], spectrum[-1, 0]], [-100000000, 100000000], 'r--')
        self._axes.set_xlim([numpy.min(spectrum[:, 0]), numpy.max(spectrum[:, 0])])
        self._axes.set_ylim([numpy.min(spectrum[:, 1]), numpy.max(spectrum[:, 1]) + 0.1 *
                             (numpy.max(spectrum[:, 1]) - numpy.min(spectrum[:, 1]))])
        self._axes.legend()

        # get energies for cursor positioning
        self._energies = spectrum[:, 0]

        # create cursor rectangle
        self._cursor_rectangle = patches.Rectangle(
                                    (750, 50),   # (x,y)
                                    5,          # width
                                    5,          # height
        )

        # set tight layout
        self._fig.tight_layout()

        # call super canvas init
        FigureCanvas.__init__(self, self._fig)

        # set parent widget
        self.setParent(parent)

        # set size policy
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # update geometry
        FigureCanvas.updateGeometry(self)

    def add_toolbar(self, parent):

        # add toolbar
        self._toolbar = SpectrumCanvasToolbar(self._fig.canvas, parent)

    def clear(self):

        # remove plots
        self._axes.clear()

        # update axes limites
        self._axes.set_xlim([-0.05, 0.05])
        self._axes.set_ylim([-0.05, 0.05])

        # redraw canvas
        self._fig.canvas.draw()

    def create_cursors(self, x1, x2):

        # create cursor rectangle
        self._cursor_rectangle = patches.Rectangle((self._energies[x1], -1000000),
                                                   self._energies[x2] - self._energies[x1], 2000000,
                                                   linewidth=1.5, facecolor=(0, 0, 1, 0.5), edgecolor=(0, 0, 0, 1))
        self._axes.add_patch(self._cursor_rectangle)

        # redraw
        self._fig.canvas.draw()

    def update_cursors(self, x1, x2):

        # update cursor rectangle
        self._cursor_rectangle.set_x(self._energies[x1])
        self._cursor_rectangle.set_width(self._energies[x2]-self._energies[x1])

        # redraw
        self._fig.canvas.draw()

    def destroy_cursors(self):

        # remove cursor rectangle
        self._cursor_rectangle.remove()

        # redraw
        self._fig.canvas.draw()

    def update_data(self, data, checkboxes):

        # remove old plots
        self._axes.clear()

        # update energies for cursor positioning
        self._energies = data['spectrum'][:, 0]

        # plot spectra
        for key in sorted(data.keys()):
            if key == 'spectrum' and checkboxes[0]:
                self._axes.plot(data[key][:, 0], data[key][:, 1], color='black', label=key)
            elif key == 'fit (init.)' and checkboxes[1]:
                self._axes.plot(data[key][:, 0], data[key][:, 1], color='red', label=key)
            elif key == 'fit (opt.)' and checkboxes[3]:
                self._axes.plot(data[key][:, 0], data[key][:, 1], color='blue', label=key)
            elif len(key) == 9:
                if key[-7:] == '(init.)' and checkboxes[2]:
                    self._axes.plot(data[key][:, 0], data[key][:, 1], linestyle='dashed', color='red', label=key)
            elif len(key) == 8:
                if key[-6:] == '(opt.)' and checkboxes[4]:
                    self._axes.plot(data[key][:, 0], data[key][:, 1], linestyle='dashed',  color='blue', label=key)

        # interval boundaries
        interval = self._map.get_interval()
        self._axes.plot([self._energies[interval[0]], self._energies[interval[0]]], [-100000000, 100000000], 'r--')
        self._axes.plot([self._energies[interval[1]], self._energies[interval[1]]], [-100000000, 100000000], 'r--')

        # update axes limits
        self._axes.set_xlim([numpy.min(data['spectrum'][:, 0]), numpy.max(data['spectrum'][:, 0])])
        self._axes.set_ylim([numpy.min(data['spectrum'][:, 1]), numpy.max(data['spectrum'][:, 1]) + 0.1 *
                             (numpy.max(data['spectrum'][:, 1]) - numpy.min(data['spectrum'][:, 1]))])

        # set labels and titles
        self._axes.set_xlabel('energy [eV]')
        self._axes.set_ylabel('counts')

        # legend
        self._axes.legend()

        # set tight layout
        self._fig.tight_layout()

        # redraw canvas
        self._fig.canvas.draw()


class SpectrumCanvasToolbar(NavigationToolbar):

    """
    SpectrumCanvasToolbar
    Toolbar for the SpectrumCanvas
    """

    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure')
        )
        NavigationToolbar.__init__(self, canvas_, parent_)
