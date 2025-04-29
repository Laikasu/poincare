import numpy as np
import matplotlib
matplotlib.use("Agg")

from typing import List

from scipy.signal import savgol_filter

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QMenuBar
from PySide6.QtCore import QStandardPaths, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt


class PlotWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Plot")
        self.resize(640, 480)
        self.plot = MplPlot(self)

        self.save_act = QAction("Save")
        self.save_act.triggered.connect(self.plot.save)
        self.save_act.setShortcut(QKeySequence.Save)

        self.close_act = QAction("Close")
        self.close_act.triggered.connect(self.close)
        self.close_act.setShortcuts([QKeySequence.Quit, QKeySequence.Cancel])

        self.menu_bar = QMenuBar()
        file_menu = self.menu_bar.addMenu("File")
        file_menu.addAction(self.save_act)
        file_menu.addSeparator()
        file_menu.addAction(self.close_act)

        plot_layout = QVBoxLayout()
        plot_layout.setContentsMargins(0,0,0,0)
        plot_layout.setAlignment(Qt.AlignTop)
        plot_layout.addWidget(self.menu_bar,0)
        plot_layout.addWidget(self.plot)
        self.setLayout(plot_layout)


class MplPlot(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.tight_layout(pad=6)
        super().__init__(fig)
        self.plot(np.array([1,0]))


    def plot(self, jones):
        self.axes.clear()
        phase = np.linspace(0, 2*np.pi, 100)
        x = jones[0]
        y = jones[1]
        
        xs = x*np.exp(1j*phase)
        ys = y*np.exp(1j*phase)
        # Linear
        if np.abs(np.imag(x*np.conj(y)))<0.001:
            imin = np.argmax(np.real(xs)**2+np.real(ys)**2)
            xmax = np.real(xs[imin])
            ymax = np.real(ys[imin])
            self.axes.add_artist(FancyArrowPatch((-xmax, -ymax), (xmax, ymax), mutation_scale=20, arrowstyle='<|-|>', color='b', lw=2))
        else:
            line, = self.axes.plot(np.real(xs), np.real(ys), lw=2, color='blue')

            imin = np.argmin(np.real(xs)**2+np.real(ys)**2)
            xmin = np.real(xs[imin])
            ymin = np.real(ys[imin])
            xmin1 = np.real(xs[imin+1])
            ymin1 = np.real(ys[imin+1])

            line.axes.annotate('',
                xytext=(xmin, ymin),
                xy=(xmin1, ymin1),
                arrowprops=dict(arrowstyle="-|>", color='blue'),
                size=20)
            line.axes.annotate('',
                xytext=(-xmin, -ymin),
                xy=(-xmin1, -ymin1),
                arrowprops=dict(arrowstyle="-|>", color='blue'),
                size=20)
        
        self.axes.set_xlim(-1.1, 1.1)
        self.axes.set_ylim(-1.1, 1.1)
        self.axes.set_aspect('equal')
        self.axes.set_xlabel('$E_x$')
        self.axes.set_ylabel('$E_y$')
        self.figure.canvas.draw()


    def save(self):
        loc = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Figure", loc,"Image Files(*.png *.jpg)")
        if filepath:
            self.figure.savefig(filepath)