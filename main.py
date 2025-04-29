from PySide6.QtWidgets import QApplication


from windows.mainwindow import MainWindow

def main():
    app = QApplication()
    app.setApplicationName("polarization-visualization")
    app.setApplicationDisplayName("Polarization Visualization")
    app.setStyle("fusion")

    w = MainWindow()
    w.show()
    

    app.exec()
    

if __name__ == "__main__":
    main()