import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QPlainTextEdit, QComboBox, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
import sys


class DNDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.filePath = ""
        
        selectFilePushButton = QPushButton("Click here to select files")
        selectFilePushButton.clicked.connect(self.return_clicked)
        
        dndInfoVerticalLayout = QVBoxLayout()
        dndInfoVerticalLayout.addStretch()
        dndInfoVerticalLayout.addWidget(QLabel("Drag and drop files here"), alignment=Qt.AlignmentFlag.AlignCenter)
        dndInfoVerticalLayout.addWidget(QLabel("or"), alignment=Qt.AlignmentFlag.AlignCenter)
        dndInfoVerticalLayout.addWidget(selectFilePushButton)
        dndInfoVerticalLayout.addStretch()
        
        self.setLayout(dndInfoVerticalLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.filePath = f
    
    def return_clicked(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dlg.setNameFilter("Images (*.png  *.jpg);;Text (*.txt);;Audio (*.mp3)")
        if dlg.exec():
            filenames = dlg.selectedFiles()
            print(filenames)
    
    def getFilePath(self):
        return self.filePath

class EncryptWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plainTextEdit = QPlainTextEdit()

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Select the number of bits", "1 bits", "2 bits", "3 bits", "4 bits", "5 bits"])
        
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Encrypt"))
        layout.addWidget(self.plainTextEdit)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)
        
    def getText(self):
        return self.plainTextEdit.toPlainText()
    
    def getBits(self):
        return self.comboBox.currentIndex()

class DecryptWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setEnabled(False)
        
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Select the number of bits", "1 bits", "2 bits", "3 bits", "4 bits", "5 bits"])
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Decrypt"))
        layout.addWidget(self.plainTextEdit)
        layout.addWidget(self.comboBox)
        self.setLayout(layout)
        
    def setText(self, text):
        self.plainTextEdit.setPlainText(text)
    
    def getBits(self):
        return self.comboBox.currentIndex()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.resize(720, 480)
        mainWidget = QWidget()
        
        gridLayout = QGridLayout()
        self.dndWidget = DNDWidget()
        gridLayout.addWidget(self.dndWidget, 0, 0, 1, 2)
        
        self.encryptWidget = EncryptWidget()
        gridLayout.addWidget(self.encryptWidget, 1, 0)
        
        self.decryptWidget = DecryptWidget()
        gridLayout.addWidget(self.decryptWidget, 1, 1)
        
        encryptPushButton = QPushButton("Encrypt")
        gridLayout.addWidget(encryptPushButton, 2, 0)
        encryptPushButton.clicked.connect(self.encyptClicked)
        
        decryptPushButton = QPushButton("Decrypt")
        gridLayout.addWidget(decryptPushButton, 2, 1)
        decryptPushButton.clicked.connect(self.decrypt_clicked)
        
        # Set the central widget of the Window.
        mainWidget.setLayout(gridLayout)
        self.setCentralWidget(mainWidget)
        
    def encyptClicked(self):
        text = self.encryptWidget.getText()
        bits = self.encryptWidget.getBits()
        filePath = self.dndWidget.getFilePath()
        if text == "" or bits == 0 or filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that all fields are filled")
            dlg.exec()

        else:
            print(text)
            print(bits)
            print(filePath)
            # encrypt(text, bits, filePath)

    def decrypt_clicked(self):
        filePath = self.dndWidget.getFilePath()
        bits = self.decryptWidget.getBits()
        if bits == 0 or filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that all fields are filled")
            dlg.exec()
        else:
            print(filePath)
            print(bits)
            #self.decryptWidget.setText(decrypt(filePath, bits))
            self.decryptWidget.setText(filePath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())