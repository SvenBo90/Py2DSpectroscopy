# import PyQt5 elements
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QCheckBox, QGridLayout, QSizePolicy, QWidget


class UiSpectrumWidget(object):

    """
    UiSpectrumWidget
    User interface for the spectrum window, which shows experimental spectra and fits.
    """

    def __init__(self, spectrum_window):

        # set object name, window title and size
        spectrum_window.setWindowTitle("Spectrum")
        spectrum_window.setObjectName("spectrum_window")

        # create grid layout
        self.gridLayout = QGridLayout(spectrum_window)
        self.gridLayout.setObjectName("gridLayout")

        # plot widget
        self.plot_widget = QWidget()
        self.plot_widget.setParent(spectrum_window)
        self.plot_widget.setObjectName("plot_widget")
        self.plot_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.gridLayout.addWidget(self.plot_widget, 1, 0, 1, 1)

        # toolbar widget
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setParent(spectrum_window)
        self.toolbar_widget.setObjectName("toolbar_widget")
        self.toolbar_widget.setFixedHeight(50)
        self.gridLayout.addWidget(self.toolbar_widget, 2, 0, 1, 1)

        # widget for the plot selection checkboxes
        self.checkbox_widget = QWidget()
        self.checkbox_widget.setParent(spectrum_window)
        self.checkbox_widget.setObjectName("checkbox_widget")
        self.checkbox_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.grid_layout_2 = QGridLayout(self.checkbox_widget)
        self.grid_layout_2.setObjectName("gridLayout_2")


        # checkbox for the measured spectrum
        self.spectrum_check_box = QCheckBox(self.checkbox_widget)
        self.spectrum_check_box.setText("Spectrum")
        self.spectrum_check_box.setChecked(True)
        self.spectrum_check_box.setObjectName("spectrum_check_box")
        self.grid_layout_2.addWidget(self.spectrum_check_box, 0, 0)
        
        # checkbox for the initial fit
        self.initial_fit_check_box = QCheckBox(self.checkbox_widget)
        self.initial_fit_check_box.setText("Initial Fit")
        self.initial_fit_check_box.setObjectName("initial_fit_check_box")
        self.grid_layout_2.addWidget(self.initial_fit_check_box, 0, 1)
        
        # checkbox for the optimized fit
        self.optimized_fit_check_box = QCheckBox(self.checkbox_widget)
        self.optimized_fit_check_box.setText("Optimized Fit")
        self.optimized_fit_check_box.setObjectName("optimized_fit_check_box")
        self.grid_layout_2.addWidget(self.optimized_fit_check_box, 1, 1)

        # checkbox for initial peaks
        self.initial_peaks_check_box = QCheckBox(self.checkbox_widget)
        self.initial_peaks_check_box.setText("Initial Peaks")
        self.initial_peaks_check_box.setObjectName("initial_peaks_check_box")
        self.grid_layout_2.addWidget(self.initial_peaks_check_box, 0, 2)

        # checkbox for optimized peaks
        self.optimized_peaks_check_box = QCheckBox(self.checkbox_widget)
        self.optimized_peaks_check_box.setText("Optimized Peaks")
        self.optimized_peaks_check_box.setObjectName("optimized_peaks_check_box")
        self.grid_layout_2.addWidget(self.optimized_peaks_check_box, 1, 2)

        self.gridLayout.addWidget(self.checkbox_widget, 0, 0, 1, 1)
