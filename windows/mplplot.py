import numpy as np
from matplotlib import use
use("Agg")

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QFileDialog, QDockWidget, QVBoxLayout, QMenuBar
from PySide6.QtCore import QStandardPaths, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch


class PlotWindow(QDockWidget):
    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        self.plot = MplPlot(self, width=4, height=5)

        self.save_act = QAction("Save")
        self.save_act.triggered.connect(self.plot.save)
        self.save_act.setShortcut(QKeySequence.Save)
        self.setWidget(self.plot)


class MplPlot(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.tight_layout(pad=6)
        super().__init__(fig)
        self.plot(np.array([1,0]), np.array([1,0]))


    def plot(self, jones1, jonesmatrix):
        self.axes.clear()
        phase = np.linspace(0, 2*np.pi, 100)
        for jones, color in zip([jonesmatrix, jones1], ['red', 'blue']):
            x = jones[0]
            y = jones[1]
            
            xs = x*np.exp(1j*phase)
            ys = y*np.exp(1j*phase)
            # Linear
            if np.abs(np.imag(x*np.conj(y)))<0.001:
                imin = np.argmax(np.real(xs)**2+np.real(ys)**2)
                xmax = np.real(xs[imin])
                ymax = np.real(ys[imin])
                self.axes.add_artist(FancyArrowPatch((-xmax, -ymax), (xmax, ymax), mutation_scale=20, arrowstyle='<|-|>', color=color, lw=2))
            else:
                line, = self.axes.plot(np.real(xs), np.real(ys), lw=2, color=color)

                imin = np.argmin(np.real(xs)**2+np.real(ys)**2)
                xmin = np.real(xs[imin])
                ymin = np.real(ys[imin])
                xmin1 = np.real(xs[imin+1])
                ymin1 = np.real(ys[imin+1])

                line.axes.annotate('',
                    xytext=(xmin, ymin),
                    xy=(xmin1, ymin1),
                    arrowprops=dict(arrowstyle="-|>", color=color),
                    size=20)
                line.axes.annotate('',
                    xytext=(-xmin, -ymin),
                    xy=(-xmin1, -ymin1),
                    arrowprops=dict(arrowstyle="-|>", color=color),
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