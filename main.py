from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from os.path import join, abspath
import sys


from windows.mainwindow import MainWindow

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller. """
    if hasattr(sys, '_MEIPASS'):
        # Running in a bundled app
        return join(sys._MEIPASS, relative_path)
    else:
        # Running in a normal environment
        return join(abspath("."), relative_path)

def main():
    app = QApplication()
    app.setApplicationName("poincare")
    app.setApplicationDisplayName("Poincaré")
    app.setStyle("fusion")
    app.setWindowIcon(QIcon(resource_path("images/poincare.ico")))

    w = MainWindow()
    w.show()
    

    app.exec()
    

if __name__ == "__main__":
    main()