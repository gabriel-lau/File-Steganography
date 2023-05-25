import typing
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QPlainTextEdit, QComboBox, QMessageBox, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys

# Widget for image/document/audio drag and drop
class DNDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.filePath = ""
        self.mainLayout = QHBoxLayout()
        self.dndInfoWidget = QWidget()
        self.imageWidget = QLabel()
        
        self.imageWidget.setHidden(True)
        
        selectFilePushButton = QPushButton("Click here to select files")
        selectFilePushButton.clicked.connect(self.return_clicked)
        
        dndInfoVerticalLayout = QVBoxLayout()
        dndInfoVerticalLayout.addStretch()
        dndInfoVerticalLayout.addWidget(QLabel("Drag and drop files here"), alignment=Qt.AlignmentFlag.AlignCenter)
        dndInfoVerticalLayout.addWidget(QLabel("or"), alignment=Qt.AlignmentFlag.AlignCenter)
        dndInfoVerticalLayout.addWidget(selectFilePushButton)
        dndInfoVerticalLayout.addStretch()
        self.dndInfoWidget.setLayout(dndInfoVerticalLayout)
        
        self.mainLayout.addWidget(self.dndInfoWidget)
        self.mainLayout.addWidget(self.imageWidget)
        
        
        self.setLayout(self.mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.setFilePath(f)
    
    def return_clicked(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dlg.setNameFilter("Images (*.png  *.jpg);;Text (*.txt);;Audio (*.mp3)")
        if dlg.exec():
            self.setFilePath(dlg.selectedFiles()[0])
    
    def setFilePath(self, filePath):
        print(filePath)
        if filePath.endswith(".png") or filePath.endswith(".jpg"):
            pixmap = QPixmap(filePath)
            self.imageWidget.setPixmap(pixmap.scaled(720, 480, Qt.AspectRatioMode.KeepAspectRatio))
            self.imageWidget.setHidden(False)
            self.dndInfoWidget.setHidden(True)
        self.filePath = filePath
    
    def getFilePath(self):
        return self.filePath

# Widget for encrypting text
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

# Widget for decrypting text
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

# Main window
# Contains all widgets above, buttons to encrypt/decrypt and save
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # BASIC WINDOW SETTINGS
        self.setWindowTitle("My App")
        self.resize(720, 720)
        self.setFixedWidth(720)
        mainWidget = QWidget()
        
        # LAYOUT
        gridLayout = QGridLayout()
        self.dndWidget = DNDWidget()
        gridLayout.addWidget(self.dndWidget, 0, 0, 1, 2)
        
        # ENCRYPT WIDGET
        self.encryptWidget = EncryptWidget()
        gridLayout.addWidget(self.encryptWidget, 1, 0)
        
        # ENCRYPT BUTTON
        encryptPushButton = QPushButton("Encrypt")
        gridLayout.addWidget(encryptPushButton, 2, 0)
        encryptPushButton.clicked.connect(self.encyptClicked)
        
        # DECRYPT WIDGET
        self.decryptWidget = DecryptWidget()
        gridLayout.addWidget(self.decryptWidget, 1, 1)
        
        # DECRYPT BUTTONS
        decryptPushButton = QPushButton("Decrypt")
        gridLayout.addWidget(decryptPushButton, 2, 1)
        decryptPushButton.clicked.connect(self.decrypt_clicked)
        
        # SAVE BUTTON
        savePushButton = QPushButton("Save")
        gridLayout.addWidget(savePushButton, 3, 0, 1, 2)
        savePushButton.clicked.connect(self.save_clicked)
        
        # FINAL WINDOW SETTINGS
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
            
    def save_clicked(self):
        filePath = self.dndWidget.getFilePath()
        if filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that all fields are filled")
            dlg.exec()
        else:
            dlg = QFileDialog()
            dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dlg.saveFileContent(filePath)
            if dlg.exec():
                filenames = dlg.selectedFiles()
                print(filenames)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec())