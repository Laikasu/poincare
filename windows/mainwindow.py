from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication
import os


from windows.mplcanvas import MplCanvas
from windows.parameters import ParameterWindow
from windows.mplplot import PlotWindow

class MainWindow(QMainWindow):
    def __init__(self):
        application_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(os.path.join(application_path, "images", "poincare.png")))

        self.display = MplCanvas(self)

        self.plot_window = PlotWindow("xy polarization",self)
        self.parameter_window = ParameterWindow("Parameters", self)
        self.parameter_window.stokes_changed.connect(self.display.update_poincare)
        self.parameter_window.jones_changed.connect(self.plot_window.plot.plot)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.plot_window)
        self.addDockWidget(Qt.RightDockWidgetArea, self.parameter_window)
        
        

        self.createUI()
            
    
    def closeEvent(self, event):
        # with open(self.parameters_file, 'w') as file:
        #     json.dump(asdict(self.parameter_window.params), file)
        QApplication.quit()

    def createUI(self):
        self.resize(1024, 600)

        #=========#
        # Actions #
        #=========#
        application_path = os.path.abspath(os.path.dirname(__file__)) + os.sep
        
        self.show_parameters_act = QAction("&Parameters", self)
        self.show_parameters_act.setStatusTip("Show parameter panel")
        self.show_parameters_act.triggered.connect(lambda: self.parameter_window.setVisible(not self.parameter_window.isVisible()))

        self.show_polarization_act = QAction("&Polarization", self)
        self.show_polarization_act.setStatusTip("Show polarization plot")
        self.show_polarization_act.triggered.connect(lambda: self.plot_window.setVisible(not self.plot_window.isVisible()))

        self.save_figure_act = QAction("Save", self)
        self.save_figure_act.setStatusTip("Save figure")
        self.save_figure_act.triggered.connect(self.display.save)
        self.save_figure_act.setShortcut(QKeySequence.Save)
        
        self.exit_act = QAction("E&xit", self)
        self.exit_act.setShortcut(QKeySequence.Quit)
        self.exit_act.setStatusTip("Exit program")
        self.exit_act.triggered.connect(self.close)

        #=========#
        # Menubar #
        #=========#

        # edit_menu = self.menuBar().addMenu("&Edit")
        # edit_menu.addAction(self.edit_parameters_act)

        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.save_figure_act)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_act)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self.show_parameters_act)
        view_menu.addAction(self.show_polarization_act)

        
        



        #=========#
        # Toolbar #
        #=========#

        # toolbar = QToolBar(self)
        # self.addToolBar(Qt.TopToolBarArea, toolbar)
        # toolbar.addAction(self.device_select_act)
        # toolbar.addAction(self.device_properties_act)
        # toolbar.addSeparator()
        # toolbar.addAction(self.trigger_mode_act)
        # toolbar.addSeparator()
        # toolbar.addAction(self.start_live_act)
        # toolbar.addSeparator()
        # toolbar.addAction(self.subtract_background_act)
        # toolbar.addAction(self.set_roi_act)
        # toolbar.addAction(self.move_act)
        # toolbar.addSeparator()
        # toolbar.addAction(self.snap_background_act)
        # toolbar.addAction(self.snap_raw_photo_act)
        # toolbar.addAction(self.snap_processed_photo_act)
        # toolbar.addAction(self.z_sweep_act)



        self.setCentralWidget(self.display)