# import PyQt5 elements
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QCheckBox, QWidget


class UiSpectrumWidget(object):

    """
    UiSpectrumWidget
    User interface for the spectrum window, which shows experimental spectra and fits.
    """

    def __init__(self, spectrum_window):

        # set object name, window title and size
        spectrum_window.setWindowTitle("Spectrum")
        spectrum_window.setObjectName("spectrum_window")
        spectrum_window.setFixedWidth(480)
        spectrum_window.setFixedHeight(415)

        # plot widget
        self.plot_widget = QWidget()
        self.plot_widget.setParent(spectrum_window)
        self.plot_widget.setGeometry(QRect(10, 65, 460, 285))
        self.plot_widget.setObjectName("plot_widget")

        # toolbar widget
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setParent(spectrum_window)
        self.toolbar_widget.setGeometry(QRect(10, 355, 460, 50))
        self.toolbar_widget.setObjectName("toolbar_widget")

        # widget for the plot selection checkboxes
        self.checkbox_widget = QWidget()
        self.checkbox_widget.setParent(spectrum_window)
        self.checkbox_widget.setGeometry(QRect(10, 10, 460, 50))
        self.checkbox_widget.setObjectName("checkbox_widget")

        # checkbox for the measured spectrum
        self.spectrum_check_box = QCheckBox(self.checkbox_widget)
        self.spectrum_check_box.setText("Spectrum")
        self.spectrum_check_box.setGeometry(QRect(0, 0, 100, 27))
        self.spectrum_check_box.setChecked(True)
        self.spectrum_check_box.setObjectName("spectrum_check_box")
        
        # checkbox for the initial fit
        self.initial_fit_check_box = QCheckBox(self.checkbox_widget)
        self.initial_fit_check_box.setText("Initial Fit")
        self.initial_fit_check_box.setGeometry(QRect(100, 0, 100, 27))
        self.initial_fit_check_box.setObjectName("initial_fit_check_box")
        
        # checkbox for the optimized fit
        self.optimized_fit_check_box = QCheckBox(self.checkbox_widget)
        self.optimized_fit_check_box.setText("Optimized Fit")
        self.optimized_fit_check_box.setGeometry(QRect(210, 0, 131, 27))
        self.optimized_fit_check_box.setObjectName("optimized_fit_check_box")

        # checkbox for initial peaks
        self.initial_peaks_check_box = QCheckBox(self.checkbox_widget)
        self.initial_peaks_check_box.setText("Initial Peaks")
        self.initial_peaks_check_box.setGeometry(QRect(100, 25, 111, 27))
        self.initial_peaks_check_box.setObjectName("initial_peaks_check_box")

        # checkbox for optimized peaks
        self.optimized_peaks_check_box = QCheckBox(self.checkbox_widget)
        self.optimized_peaks_check_box.setText("Optimized Peaks")
        self.optimized_peaks_check_box.setGeometry(QRect(210, 25, 141, 27))
        self.optimized_peaks_check_box.setObjectName("optimized_peaks_check_box")
