import numpy as np
from matplotlib import use
use("Agg")

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QStandardPaths
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))

        return np.min(zs)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, pxsize=3.45):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.fig.tight_layout(pad=2)
        super().__init__(self.fig)

        self.update_poincare(np.array([[1,1],[0,0],[0,0]]))

        self.data_directory = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)

    def update_poincare(self, stokes):
        self.axes.clear()
        self.axes.set_axis_off()
        # Generate data for a sphere
        u = np.linspace(0, 2 * np.pi, 18)   # azimuthal angle
        v = np.linspace(0, np.pi, 18)       # polar angle

        # Parametric equations for the sphere
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        self.axes.plot_wireframe(x, y, z, color='gray', alpha=0.7, zorder=0)
        

        params = dict(mutation_scale=20, arrowstyle='-|>', color='k', lw=2, alpha=0.9, zorder=1)
        self.axes.add_artist(Arrow3D([-1.5,1.5],[0,0],[0,0],**params))
        self.axes.text(1.5,0,0,'S1')
        self.axes.add_artist(Arrow3D([0,0],[-1.5,1.5],[0,0],**params))
        self.axes.text(0,1.5,0,'S2')
        self.axes.add_artist(Arrow3D([0,0],[0,0],[-1.5,1.5],**params))
        self.axes.text(0,0,1.5,'S3')
        self.axes.set_box_aspect([1,1,1])
        
        #self.axes.set_xlabel('S1')
        #self.axes.set_ylabel('S2')
        #self.axes.set_zlabel('S3')
        self.line = self.axes.plot(*stokes, marker='.', color='k', zorder=5)
        self.end = self.axes.plot(*stokes[:,-1], marker='o', color='r', zorder=10)
        self.start = self.axes.plot(*stokes[:,0], marker='o',color='b', zorder=10)
        
        
        self.figure.canvas.draw()

    def save(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("Image Files(*.png *.jpg)")
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setDirectory(self.data_directory)
        if dialog.exec():
            filepath = dialog.selectedFiles()[0]
            self.figure.savefig(filepath)
        self.data_directory = dialog.directory()