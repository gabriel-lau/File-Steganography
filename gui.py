from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QPushButton
import sys


class DNDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(720, 200)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.resize(720, 480)
        mainWidget = QWidget()
        
        gridLayout = QGridLayout()
        dndWidget = DNDWidget()
        gridLayout.addWidget(dndWidget, 0, 0)
        
        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(QPushButton("Button 1"))
        verticalLayout.addWidget(QPushButton("Button 2"))
        gridLayout.addLayout(verticalLayout, 1, 0)
        
        # Set the central widget of the Window.
        mainWidget.setLayout(gridLayout)
        self.setCentralWidget(mainWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())