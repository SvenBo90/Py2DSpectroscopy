# import PyQt5 elements
from PyQt5.QtWidgets import QApplication, QDialog
# general imports
import numpy
# import canvas class
from mplCanvas import MicrographCanvas
# import UI
from UIs.addMicrographDialogUi import UiAddMicrographDialog


class AddMicrographDialog(QDialog):

    """
    AddMicrographDialog
    This dialog enables the user to import a micrograph into the program. The dialog
    asks for at least three fixed and moving points in order to align the micrograph
    with the map.
    """

    def __init__(self, parent, file_name):

        # call widget init
        QDialog.__init__(self, parent)

        # link app
        # noinspection PyArgumentList
        self._app = QApplication.instance()

        # link map
        self._map = self._app.maps.get_selected_map()

        # fixed and moving points
        self._points_fixed = numpy.array([])
        self._points_moving = numpy.array([])

        # load and set up UI
        self.ui = UiAddMicrographDialog(self)

        # link actions for dialog buttons
        self.ui.clear_last_fixed_button.clicked.connect(self.cb_clear_last_fixed)
        self.ui.clear_all_fixed_button.clicked.connect(self.cb_clear_all_fixed)
        self.ui.clear_last_moving_button.clicked.connect(self.cb_clear_last_moving)
        self.ui.clear_all_moving_button.clicked.connect(self.cb_clear_all_moving)

        # link and disable submit button
        self._ok_button = self.ui.button_box.button(self.ui.button_box.Ok)
        self._ok_button.setEnabled(False)

        # create map canvas
        self._micro_canvas = MicrographCanvas(self._map.get_data(), self._map.get_data_name(), file_name,
                                              self.ui.plot_widget)
        self._micro_canvas.add_callback('button_press_event', self.cb_map_clicked)

        # get axes
        self._map_axes, self._micro_axes = self._micro_canvas.get_axes()

        # add toolbar to the toolbar widget
        self._micro_canvas.add_toolbar(self.ui.toolbar_widget)

    def cb_clear_all_fixed(self):

        # clear all fixed points
        self._points_fixed = numpy.array([])

        # disable buttons for fixed point removing
        self.ui.clear_all_fixed_button.setEnabled(False)
        self.ui.clear_last_fixed_button.setEnabled(False)

        # update the canvas
        self._micro_canvas.update_points(self._points_fixed, self._points_moving)

        # disable the submit button
        self._ok_button.setEnabled(False)

    def cb_clear_all_moving(self):

        # remove all moving points
        self._points_moving = numpy.array([])

        # disable buttons for moving points removing
        self.ui.clear_all_moving_button.setEnabled(False)
        self.ui.clear_last_moving_button.setEnabled(False)

        # update the canvas
        self._micro_canvas.update_points(self._points_fixed, self._points_moving)

        # disable the submit button
        self._ok_button.setEnabled(False)

    def cb_clear_last_fixed(self):

        # remove last added fixed point
        self._points_fixed = self._points_fixed[:-2]

        # check if this was the only point and disable buttons for fixed points removing
        if len(self._points_fixed) == 0:
            self.ui.clear_all_fixed_button.setEnabled(False)
            self.ui.clear_last_fixed_button.setEnabled(False)

        # update micro canvas
        self._micro_canvas.update_points(self._points_fixed, self._points_moving)

        # check if the submit button should be enabled or disabled
        if len(self._points_fixed) == len(self._points_moving) and len(self._points_fixed) > 2:
            self._ok_button.setEnabled(True)
        else:
            self._ok_button.setEnabled(False)

    def cb_clear_last_moving(self):

        # remove last added moving point
        self._points_moving = self._points_moving[:-2]

        # check if this was the only one and disable buttons for moving points removing
        if len(self._points_moving) == 0:
            self.ui.clear_all_moving_button.setEnabled(False)
            self.ui.clear_last_moving_button.setEnabled(False)

        # update canvas
        self._micro_canvas.update_points(self._points_fixed, self._points_moving)

        # check whether submit button should be enabled or disabled
        if len(self._points_fixed) == len(self._points_moving) and len(self._points_fixed) > 2:
            self._ok_button.setEnabled(True)
        else:
            self._ok_button.setEnabled(False)

    def cb_map_clicked(self, event):

        # check if toolbar is active
        if self._micro_canvas.get_toolbar_active() is None:

            # check which axes were clicked
            if event.inaxes is None:

                return

            elif event.inaxes == self._map_axes:

                # add fixed point
                self._points_fixed = numpy.concatenate((self._points_fixed, [event.xdata, event.ydata]), axis=0)

            elif event.inaxes == self._micro_axes:

                # add moving point
                self._points_moving = numpy.concatenate((self._points_moving, [event.xdata, event.ydata]), axis=0)

            # update canvas
            self._micro_canvas.update_points(self._points_fixed, self._points_moving)

            # enable or disable buttons for fixed points removing
            if len(self._points_fixed) > 0:
                self.ui.clear_all_fixed_button.setEnabled(True)
                self.ui.clear_last_fixed_button.setEnabled(True)
            else:
                self.ui.clear_all_fixed_button.setEnabled(False)
                self.ui.clear_last_fixed_button.setEnabled(False)

            # enable or disable buttons for moving points removing
            if len(self._points_moving) > 0:
                self.ui.clear_all_moving_button.setEnabled(True)
                self.ui.clear_last_moving_button.setEnabled(True)
            else:
                self.ui.clear_all_moving_button.setEnabled(False)
                self.ui.clear_last_moving_button.setEnabled(False)

            # enable or disable submit button
            if len(self._points_fixed) == len(self._points_moving) and len(self._points_fixed) > 2:
                self._ok_button.setEnabled(True)
            else:
                self._ok_button.setEnabled(False)

    def get_points_fixed(self):

        # return the fixed points
        return self._points_fixed

    def get_points_moving(self):

        # return the moving points
        return self._points_moving
