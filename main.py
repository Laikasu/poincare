from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from os.path import join


from windows.mainwindow import MainWindow

def main():
    app = QApplication()
    app.setApplicationName("polarization-visualization")
    app.setApplicationDisplayName("Polarization Visualization")
    app.setStyle("fusion")
    app.setWindowIcon(QIcon(join("images", "poincare.ico")))

    w = MainWindow()
    w.show()
    

    app.exec()
    

if __name__ == "__main__":
    main()