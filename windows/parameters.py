from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QDoubleSpinBox, QSpinBox, QGroupBox, QTabWidget, QVBoxLayout, QGridLayout, QDockWidget
from PySide6.QtCore import Signal

import numpy as np

# TO DO: Parameter overhaul

class ParameterWindow(QDockWidget):
    """Window where you set the parameters."""

    stokes_changed = Signal(np.ndarray)
    jones_changed = Signal(np.ndarray)

    def stokes_from_jones(self, jones):
        if jones[0] == 0:
            s = np.inf
        else:
            s = jones[1]/jones[0]
        
        S1 = np.cos(2*np.arctan(np.abs(s)))
        S2 = np.sin(2*np.arctan(np.abs(s)))*np.cos(np.angle(s))
        S3 = np.sin(2*np.arctan(np.abs(s)))*np.sin(np.angle(s))
        return np.array([S1, S2, S3])
    
    def jones_from_stokes(self, stokes):
        stokes = stokes/np.sqrt(stokes[0]**2+stokes[1]**2+stokes[2]**2)
        p=np.sqrt(stokes[0]**2+stokes[1]**2+stokes[2]**2)
        Q, U, V = stokes/p
        A=np.sqrt((1+Q)/2)
        if A == 0:
            B=1
        else:
            B = U/(2*A)+1j*V/(2*A)
        return np.sqrt(p)*np.array([A, B])

    
    def jones_matrix(self, jones):
        matrix = np.array([[self.xx.value()+self.xxi.value()*1j, self.xy.value()+self.xyi.value()*1j],
                           [self.yx.value()+self.yxi.value()*1j, self.yy.value()+self.yyi.value()*1j]])
        return np.dot(matrix, jones)
    
    def update_stokes(self):
        self.stokes = [self.stokes_from_jones(self.jones)]
        # Apply Jones matrices
        s = self.jones
        for i in range(self.times.value()):
            s = self.jones_matrix(s)
            self.stokes.append(self.stokes_from_jones(s))
        self.stokes = np.array(self.stokes).T
        self.stokes_changed.emit(self.stokes)
        

    def update_jones_from_jones(self):
        self.jones = np.array(
            [self.Ex.value()*np.exp(1j*np.radians(self.phase_x.value())),
              self.Ey.value()*np.exp(1j*np.radians(self.phase_y.value()))])
        self.jones_changed.emit(self.jones)
        # Update UI
        stokes = self.stokes_from_jones(self.jones)
        params = [self.S1, self.S2, self.S3]
        for param in params:
            param.blockSignals(True)
        self.S1.setValue(stokes[0])
        self.S2.setValue(stokes[1])
        self.S3.setValue(stokes[2])
        for param in params:
            param.blockSignals(False)

        self.update_stokes()

    def update_jones_from_stokes(self):
        stokes = np.array([self.S1.value(), self.S2.value(), self.S3.value()])
        self.jones = self.jones_from_stokes(stokes)
        self.jones_changed.emit(self.jones)

        # Update UI without triggering recursive loop
        params = [self.Ex, self.Ey, self.phase_x, self.phase_y]
        for param in params:
            param.blockSignals(True)
        self.Ex.setValue(np.abs(self.jones[0]))
        self.Ey.setValue(np.abs(self.jones[1]))
        self.phase_x.setValue(np.angle(self.jones[0], deg=True))
        self.phase_y.setValue(np.angle(self.jones[1], deg=True))
        for param in params:
            param.blockSignals(False)

        self.update_stokes()
        
    def clip_phase_x(self, value):
        if np.abs(value>=180):
            self.phase_x.blockSignals(True)
            self.phase_x.setValue(((value + 180) % 360) - 180)
            self.phase_x.blockSignals(False)
    
    def clip_phase_y(self, value):
        if np.abs(value>=180):
            self.phase_y.blockSignals(True)
            self.phase_y.setValue(((value + 180) % 360) - 180)
            self.phase_y.blockSignals(False)

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        # should probably have associated units
        
        self.jones = np.array([1,0])
        self.stokes = self.stokes_from_jones(self.jones)

        self.tabwidget = QTabWidget(self)
        self.setWidget(self.tabwidget)

        
        # All parameters
        self.Ex = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1)
        self.Ex.setValue(self.jones[0])
        self.Ey = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1)
        self.Ey.setValue(self.jones[1])
        self.phase_x = QSpinBox(minimum=-360, maximum=360, value=0, singleStep=10, suffix="°")
        self.phase_x.valueChanged.connect(self.clip_phase_x)
        self.phase_y = QSpinBox(minimum=-360, maximum=360, value=0, singleStep=10, suffix="°")
        self.phase_y.valueChanged.connect(self.clip_phase_y)
        for param in [self.Ex, self.Ey, self.phase_x, self.phase_y]:
            param.valueChanged.connect(self.update_jones_from_jones)


        self.S1 = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=1)
        self.S2 = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        self.S3 = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        for param in [self.S1, self.S2, self.S3]:
            param.valueChanged.connect(self.update_jones_from_stokes)


        self.xx = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=1)
        self.xy = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        self.yx = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        self.yy = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=1)
        self.xxi = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        self.xyi = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        self.yxi = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        self.yyi = QDoubleSpinBox(minimum=-1, maximum=1, singleStep=0.1, value=0)
        self.times = QSpinBox(minimum=0, maximum=200, value=1, singleStep=1)

        for param in [self.xx, self.xy, self.yx, self.yy,self.xxi, self.xyi, self.yxi, self.yyi, self.times]:
            param.valueChanged.connect(self.update_stokes)

        # Animation
        
        # self.misc = QComboBox()
        # sweepable_params = [k.lstrip("_") for k, v in self.params.to_dict().items() if type(v) in (int, float)]
        # self.misc.addItems(sweepable_params)
        # self.misc.setCurrentText("wavelen")

        # self.start = QDoubleSpinBox(minimum=-10, maximum=1000)
        # self.start.setValue(500)
        # self.stop = QDoubleSpinBox(minimum=-10, maximum=1000)
        # self.stop.setValue(600)
        # #self.start.valueChanged.connect(lambda value: self.stop.setValue(max(value, self.stop.value())))
        # #self.stop.valueChanged.connect(lambda value: self.start.setValue(min(value, self.start.value())))
        # self.num = QSpinBox(minimum=1, maximum=200, value=10)
        # self.fps = QSpinBox(minimum=1, maximum=200, value=10)
        # self.fps.valueChanged.connect(self.fps_changed.emit)
        # self.start_sweep = QPushButton("Start sweep")
        # self.start_sweep.clicked.connect(self.sweep)
        

        # Group into groups and tabs

        self.vector_group = QGroupBox("Vector")
        setup_layout = QGridLayout()
        setup_layout.addWidget(QLabel("Magnitude"),0,1)
        setup_layout.addWidget(QLabel("Phase"),0,2)
        setup_layout.addWidget(QLabel("x"),1,0)
        setup_layout.addWidget(QLabel("y"),2,0)
        setup_layout.addWidget(self.Ex,1,1)
        setup_layout.addWidget(self.Ey,2,1)
        setup_layout.addWidget(self.phase_x,1,2)
        setup_layout.addWidget(self.phase_y,2,2)
        
        self.vector_group.setLayout(setup_layout)

        self.matrix_group = QGroupBox("Matrix")
        matrixbox_layout = QVBoxLayout()
        matrix_layout = QGridLayout()
        matrix_layout.addWidget(self.xx,0,0)
        matrix_layout.addWidget(QLabel('+'),0,1)
        matrix_layout.addWidget(self.xxi,0,2)
        matrix_layout.addWidget(QLabel('i  '),0,3)
        matrix_layout.addWidget(self.xy,0,4)
        matrix_layout.addWidget(QLabel('+'),0,5)
        matrix_layout.addWidget(self.xyi,0,6)
        matrix_layout.addWidget(QLabel('i'),0,7)
        matrix_layout.addWidget(self.yx,1,0)
        matrix_layout.addWidget(QLabel('+'),1,1)
        matrix_layout.addWidget(self.yxi,1,2)
        matrix_layout.addWidget(QLabel('i  '),1,3)
        matrix_layout.addWidget(self.yy,1,4)
        matrix_layout.addWidget(QLabel('+'),1,5)
        matrix_layout.addWidget(self.yyi,1,6)
        matrix_layout.addWidget(QLabel('i'),1,7)

        matrixbox_layout.addLayout(matrix_layout)
        repeat_layout = QFormLayout()
        repeat_layout.addRow("repetitions", self.times)
        matrixbox_layout.addLayout(repeat_layout)
        
        self.matrix_group.setLayout(matrixbox_layout)


        # Stokes tab
        self.stokes_tab = QWidget(self)
        self.tabwidget.addTab(self.stokes_tab, "Stokes")
        stokestab_layout = QFormLayout()
        stokestab_layout.addRow('S1', self.S1)
        stokestab_layout.addRow('S2', self.S2)
        stokestab_layout.addRow('S3', self.S3)
        self.stokes_tab.setLayout(stokestab_layout)

        # Jones tab
        self.jones_tab = QWidget(self)
        self.tabwidget.addTab(self.jones_tab, "Jones")
        jonestab_layout = QVBoxLayout()
        jonestab_layout.addWidget(self.vector_group)
        jonestab_layout.addWidget(self.matrix_group)
        jonestab_layout.addStretch(1)

        self.jones_tab.setLayout(jonestab_layout)