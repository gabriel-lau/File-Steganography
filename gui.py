import steganography as steg
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QPlainTextEdit, QComboBox, QMessageBox, QFileDialog
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QUrl
import sys
import signal

# DRAG AND DROP MAIN WIDGET
# Widget for image/document/audio drag and drop
class DNDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.filePath = "" # TODO: fileByteArray or filepath?
        self.setFixedSize(700, 480)
        # self.fileByteArray = None
        
        # LABEL AND FILE SELECT BUTTON WIDGET
        self.dndInfoWidget = QWidget()
        
        # IMAGE WIDGET
        self.imageWidget = QLabel()
        self.imageWidget.setHidden(True)
        
        # VIDEO WIDGET
        self.mediaPlayer = QMediaPlayer()
        self.videoWidget = QVideoWidget()
        self.videoWidget.setHidden(True)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        # AUDIO WIDGET
        
        
        # DOCUMENT WIDGET
        self.documentWidget = QPlainTextEdit()
        
        # LABEL AND FILE SELECT BUTTON WIDGET CREATION
        dndInfoVerticalLayout = QVBoxLayout()
        dndInfoVerticalLayout.addStretch()
        dndInfoVerticalLayout.addWidget(QLabel("Drag and drop files here"), alignment=Qt.AlignmentFlag.AlignCenter)
        dndInfoVerticalLayout.addWidget(QLabel("or"), alignment=Qt.AlignmentFlag.AlignCenter)
        selectFilePushButton = QPushButton("Click here to select files")
        selectFilePushButton.clicked.connect(self.fileSelectClicked)
        dndInfoVerticalLayout.addWidget(selectFilePushButton)
        dndInfoVerticalLayout.addStretch()
        self.dndInfoWidget.setLayout(dndInfoVerticalLayout)
        
        # MAIN LAYOUT SETUP
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.dndInfoWidget)
        self.mainLayout.addWidget(self.imageWidget)
        self.mainLayout.addWidget(self.videoWidget)
        self.setLayout(self.mainLayout)

    # DRAG AND DROP ENTRYPOINT
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # DRAG AND DROP ACTION
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".txt") or f.endswith(".mp3") or f.endswith(".mp4"):
                self.setFilePath(f)
    
    # FILE SELECT BUTTON ACTION
    def fileSelectClicked(self):
        # DISPLAY FILE SELECT WINDOW
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dlg.setNameFilter("Images (*.png  *.jpg);;Text (*.txt);;Audio/Video (*.mp3 *.mp4 *.wav)")
        if dlg.exec():
            self.setFilePath(dlg.selectedFiles()[0])
    
    # UPDATE DND FIELD WITH FILE
    def setFilePath(self, filePath):
        print(filePath)
        if filePath.endswith(".png") or filePath.endswith(".jpg"):
            pixmap = QPixmap(filePath)
            # pixmap.loadFromData(byteArray)
            self.imageWidget.setPixmap(pixmap.scaled(700, 480, Qt.AspectRatioMode.KeepAspectRatio))
            self.dndInfoWidget.setHidden(True)
            self.imageWidget.setHidden(False)
            self.videoWidget.setHidden(True)
        elif filePath.endswith(".txt"):
            #TODO: display text
            self.dndInfoWidget.setHidden(True)
            self.imageWidget.setHidden(True)
            self.videoWidget.setHidden(True)
            
        elif filePath.endswith(".mp3"):
            # TODO: play audio
            print()
            
        elif filePath.endswith(".mp4"):
            self.mediaPlayer.setSource(QUrl.fromLocalFile(filePath))
            self.mediaPlayer.play()
            self.dndInfoWidget.setHidden(True)
            self.imageWidget.setHidden(True)
            self.videoWidget.setHidden(False)
            
        self.filePath = filePath
    
    # GET FILE PATH (Called from MainWindow.decodeClicked and MainWindow.encodeClicked)
    def getFilePath(self):
        return self.filePath
    
# ENCODE PARAMETERS WIDGET
# Contains textfield to enter endcode text and bits selection
class EncodeWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # WIDGET LAYOUT
        layout = QVBoxLayout()
        
        # ENCODE LABEL
        layout.addWidget(QLabel("Encode"))
        
        # ENCODE TEXTFIELD
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setFixedHeight(60)
        layout.addWidget(self.plainTextEdit)
        
        # ENCODE DROPDOWN BOX
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Select the number of bits", "1 bits", "2 bits", "3 bits", "4 bits", "5 bits"])
        layout.addWidget(self.comboBox)
        
        # ASSIGNING LAYOUT TO  WIDGET
        self.setLayout(layout)
        
    # GET TEXT TO ENCODE (Called from MainWindow.encodeClicked)
    def getText(self):
        return self.plainTextEdit.toPlainText()
    
    # GET BIT SELECTION (Called from MainWindow.encodeClicked)
    def getBits(self):
        return self.comboBox.currentIndex()

# DECODE PARAMETERS WIDGET
# Contains textfield to show decode text and bits selection
class DecodeWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # WIDGET LAYOUT
        layout = QVBoxLayout()
        
        # ADD DECODE LABEL TO LAYOUT
        layout.addWidget(QLabel("Decode"))
        
        # ADD DECODE TEXTFIELD TO LAYOUT
        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setFixedHeight(60)
        layout.addWidget(self.plainTextEdit)
        
        # ADD DECODE DROPDOWN BOX TO LAYOUT
        self.comboBox = QComboBox()
        self.comboBox.addItems(["Select the number of bits", "1 bits", "2 bits", "3 bits", "4 bits", "5 bits"])
        layout.addWidget(self.comboBox)
        
        # ASSIGNING LAYOUT TO  WIDGET
        self.setLayout(layout)
    
    # SET DECODED TEXT (Called from MainWindow.decodeClicked)
    def setText(self, text):
        self.plainTextEdit.setPlainText(text)
    
    # GET BIT SELECTION (Called from MainWindow.decodeClicked)
    def getBits(self):
        return self.comboBox.currentIndex()

# Main window
# Contains all widgets above, buttons to encode/decode and save
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # BASIC WINDOW SETTINGS
        self.setWindowTitle("Steganography Encoder/Decoder")
        self.setFixedWidth(720)
        
        #  LAYOUT
        gridLayout = QGridLayout()
        
        # DRAG AND DRIO WIDGET
        self.dndWidget = DNDWidget()
        gridLayout.addWidget(self.dndWidget, 0, 0, 1, 2)
        
        # ENCODE WIDGET
        self.encodeWidget = EncodeWidget()
        gridLayout.addWidget(self.encodeWidget, 1, 0)
        
        # ENCODE BUTTON
        encodePushButton = QPushButton("Encode")
        gridLayout.addWidget(encodePushButton, 2, 0)
        encodePushButton.clicked.connect(self.encodeClicked)
        
        # DECODE WIDGET
        self.decodeWidget = DecodeWidget()
        gridLayout.addWidget(self.decodeWidget, 1, 1)
        
        # DECODE BUTTONS
        decodePushButton = QPushButton("Decode")
        gridLayout.addWidget(decodePushButton, 2, 1)
        decodePushButton.clicked.connect(self.decodeClicked)
        
        # SAVE BUTTON
        savePushButton = QPushButton("Save file as")
        gridLayout.addWidget(savePushButton, 3, 0, 1, 2)
        savePushButton.clicked.connect(self.saveClicked)
        
        # FINAL WINDOW SETTINGS
        mainWidget = QWidget()
        mainWidget.setLayout(gridLayout)
        self.setCentralWidget(mainWidget)
        
    # ENCODE BUTTON ACTION
    def encodeClicked(self):
        text = self.encodeWidget.getText()
        bits = self.encodeWidget.getBits()
        filePath = self.dndWidget.getFilePath()
        if text == "" or bits == 0 or filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that all fields are filled")
            dlg.exec()

        else:
            # TODO: ENTRYPOINT TO DIFFERENT ENCODE ALGO
            print(text)
            print(bits)
            print(filePath)
            # SET DISPLAYED FILE
            # steg.encode(text, bits, filePath)
            self.dndWidget.setFilePath(filePath)

    # DECODE BUTTON ACTION
    def decodeClicked(self):
        bits = self.decodeWidget.getBits()
        filePath = self.dndWidget.getFilePath()
        if bits == 0 or filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that all fields are filled")
            dlg.exec()
        else:
            # TODO: ENTRYPOINT TO DIFFERENT DECODE ALGO
            print(bits)
            print(filePath)
            # SET DECODE TEXT BOX
            #self.decodeWidget.setText(steg.decode(filePath, bits))
            self.decodeWidget.setText(filePath)
            
    # SAVE BUTTON ACTION
    def saveClicked(self):
        filePath = self.dndWidget.getFilePath() # TODO: Use fileByteArray or filePath?
        if filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that a file is open")
            dlg.exec()
        else:
            # TODO: Fix file saving
            file = open(filePath, 'rb')
            data = bytearray(file.read())
            file.close()
    
            dlg = QFileDialog()
            dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
            dlg.saveFileContent(data)
            if dlg.exec():
                filenames = dlg.selectedFiles()
                print(filenames)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL) # ctl + c to quit
    sys.exit(app.exec())