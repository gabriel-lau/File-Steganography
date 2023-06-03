import steganography as steg
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QPlainTextEdit, QComboBox, QMessageBox, QFileDialog, QStackedLayout, QSlider, QStyle)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QUrl, QThreadPool, QRunnable, pyqtSlot, pyqtSignal, QObject
import sys, traceback
import signal

# DRAG AND DROP MAIN WIDGET
# Widget for image/document/audio drag and drop
class DNDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.filePath = ""
        self.setFixedSize(700, 480)
        self.setObjectName("dndWidget")
        
        # LABEL AND FILE SELECT BUTTON WIDGET
        self.dndInfoWidget = QWidget()
        
        # IMAGE WIDGET
        self.imageWidget = None
        
        # GIF WIDGET
        self.gifWidget = None
        
        # TEXT WIDGET
        self.textWidget = None
        
        # DOCX WIDGET
        self.docxWidget = None
        
        # VIDEO WIDGET
        self.videoWidget = None
        
        # AUDIO WIDGET
        self.audioWidget = None
        
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
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".gif") or f.endswith(".txt") or f.endswith(".docx") or f.endswith(".mp3") or f.endswith(".mp4") or f.endswith(".wav"):
                self.setFilePath(f)
        
    # FILE SELECT BUTTON ACTION
    def fileSelectClicked(self):
        # DISPLAY FILE SELECT WINDOW
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dlg.setNameFilter("Images (*.png *.jpg *.gif);;Text (*.txt *.docx);;Audio/Video (*.mp3 *.mp4 *.wav)")
        if dlg.exec():
            self.setFilePath(dlg.selectedFiles()[0])
    
    # UPDATE DND FIELD WITH FILE
    def setFilePath(self, filePath):
        print(filePath)
        if filePath.endswith(".png") or filePath.endswith(".jpg"):
            self.deleteWidgets()
            self.imageWidget = QLabel()
            pixmap = QPixmap(filePath)
            self.imageWidget.setPixmap(pixmap.scaled(700, 480, Qt.AspectRatioMode.KeepAspectRatio))
            self.mainLayout.addWidget(self.imageWidget)
            
        elif filePath.endswith(".gif"):
            self.deleteWidgets()
            self.gifWidget = GifWidget(filePath)
            self.mainLayout.addWidget(self.gifWidget)
    
        elif filePath.endswith(".txt"):
            self.deleteWidgets()
            self.textWidget = QPlainTextEdit()
            self.textWidget.setPlainText(open(filePath, "r").read())
            self.textWidget.setReadOnly(True)
            self.mainLayout.addWidget(self.textWidget)
        
        elif filePath.endswith(".docx"):
            self.deleteWidgets()
            self.docxWidget = FileNameWidget(filePath)
            self.mainLayout.addWidget(self.docxWidget)
        
        elif filePath.endswith(".mp3") or filePath.endswith(".wav"):
            self.deleteWidgets()
            self.audioWidget = AudioWidget(filePath)
            self.mainLayout.addWidget(self.audioWidget)

            
        elif filePath.endswith(".mp4"):
            self.deleteWidgets()
            self.videoWidget = VideoWidget(filePath)
            self.mainLayout.addWidget(self.videoWidget)
            
        self.filePath = filePath
    
    def deleteWidgets(self):
        # self.mainLayout.removeWidget(widget) only removes the view of it, but the instance still exists
        # del widget deletes the instance
        # Took me too long to figure this out, I hate this        
        self.mainLayout.removeWidget(self.dndInfoWidget)
        self.mainLayout.removeWidget(self.imageWidget)
        self.mainLayout.removeWidget(self.gifWidget)
        self.mainLayout.removeWidget(self.textWidget)
        self.mainLayout.removeWidget(self.docxWidget)
        self.mainLayout.removeWidget(self.audioWidget)
        self.mainLayout.removeWidget(self.videoWidget)
        
        del self.dndInfoWidget
        del self.imageWidget
        del self.gifWidget
        del self.textWidget
        del self.docxWidget
        del self.audioWidget
        del self.videoWidget
        
        self.dndInfoWidget = None
        self.imageWidget = None
        self.gifWidget = None
        self.textWidget = None
        self.docxWidget = None
        self.audioWidget = None
        self.videoWidget = None
    
    # GET FILE PATH (Called from MainWindow.decodeClicked and MainWindow.encodeClicked)
    def getFilePath(self):
        return self.filePath
        
# VIDEO PLAYER WIDGET FOR DRAG AND DROP
class VideoWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
        
        # VIDEO PLAYER WIDGET
        self.videoWidget = QVideoWidget()
        
        # AUDIO OUTPUT
        self.audioOutput = QAudioOutput()
        
        # MEDIA PLAYER
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setSource(QUrl.fromLocalFile(*args))
        self.mediaPlayer.setLoops(-1)
        self.mediaPlayer.play()
        
        # TRANSPARENT WIDGET (To enable drag and drop on video widget as video widget got problem)
        transprentWidget = QWidget()
        transprentWidget.setStyleSheet('background-color: transparent;')
        transprentWidget.setAutoFillBackground(True)
        
        # LAYOUT SETUP
        layout = QStackedLayout()
        layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        layout.addWidget(self.videoWidget)
        layout.addWidget(transprentWidget)

        self.setLayout(layout)
        
# AUDIO PLAYER WIDGET FOR DRAG AND DROP
class AudioWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
        
        # AUDIO OUTPUT
        self.audioOutput = QAudioOutput()
        
        # MEDIA PLAYER
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setLoops(-1)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        
        # PLAY/PAUSE BUTTON
        self.playPauseButton = QPushButton()
        self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self.playPauseButton.clicked.connect(self.playPauseClicked)
        
        # PROGRESS SLIDER
        self.progressSlider = QSlider(Qt.Orientation.Horizontal)
        self.progressSlider.setRange(0, 100)
        self.progressSlider.sliderMoved.connect(self.progressSliderMoved)
        
        # LAYOUT SETUP
        layout = QHBoxLayout()
        layout.addWidget(self.playPauseButton)
        layout.addWidget(self.progressSlider)
        self.setLayout(layout)
        
        # PLAY AUDIO
        self.mediaPlayer.setSource(QUrl.fromLocalFile(*args))
        self.playPauseClicked()
        self.mediaPlayer.play()

class FileNameWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
        
        self.label = QLabel(*args)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class NotSupportedWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.label = QLabel("File type cannot be displayed")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
    
class GifWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
        
        self.movie = QMovie(*args)
        
        self.label = QLabel()
        self.label.setMovie(self.movie)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie.start()
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    # PLAY/PAUSE BUTTON ACTION
    def playPauseClicked(self):
        if self.mediaPlayer.isPlaying() == True:
            self.mediaPlayer.pause()
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.mediaPlayer.play()
            self.playPauseButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
    
    # PROGRESS SLIDER MOVEMENT ACTION
    def positionChanged(self, position):
        self.progressSlider.setValue(position)

    # PROGRESS SLIDER MOVEMENT ACTION
    def durationChanged(self, duration):
        self.progressSlider.setRange(0, duration)
    
    # PROGRESS SLIDER MOVEMENT ACTION
    def progressSliderMoved(self, position):
        self.mediaPlayer.setPosition(position)
        
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
        self.plainTextEdit.setReadOnly(True)
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
        self.threadPool = QThreadPool()
        self.threadPool.setMaxThreadCount(1)
        
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
        
        # Check if all fields are filled
        if text == "" or bits == 0 or filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that all fields are filled")
            dlg.exec()
            
        # Encode text
        else:
            # SET DISPLAYED FILE
            encodeWorker = EncodeWorker(text, bits, filePath)
            encodeWorker.signals.result.connect(self.encodeResult)
            encodeWorker.signals.finished.connect(self.encodeFinished)
            self.threadPool.start(encodeWorker)
    
    def encodeResult(self, result):
        self.dndWidget.setFilePath(result)
        
    def encodeFinished(self):
        self.threadPool.clear()
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Encoded")
        dlg.setText("Displaying encoded file")
        dlg.exec()

    # DECODE BUTTON ACTION
    def decodeClicked(self):
        bits = self.decodeWidget.getBits()
        filePath = self.dndWidget.getFilePath()
        
        # Check if all fields are filled
        if bits == 0 or filePath == "":
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Please ensure that all fields are filled")
            dlg.exec()
        
        # Decode text
        else:
            # SET DECODE TEXT BOX
            decodeWorker = DecodeWorker(bits, filePath)
            decodeWorker.signals.result.connect(self.decodeResult)
            decodeWorker.signals.finished.connect(self.decodeFinished)
            self.threadPool.start(decodeWorker)
    
    def decodeResult(self, result):
        self.decodeWidget.setText(result)
        
    def decodeFinished(self):
        self.threadPool.clear()
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Decoded")
        dlg.setText("Displaying decoded text")
        dlg.exec()
    
    # SAVE BUTTON ACTION
    def saveClicked(self):
        filePath = self.dndWidget.getFilePath()
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
            
# SIGNALS FOR THREADS 
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

# ENCODE THREADS
class EncodeWorker(QRunnable):
    def __init__(self, *args, **kwargs):
        super(EncodeWorker, self).__init__()
        self.fn = steg.encode
        self.args = args
        self.kwargs = kwargs        
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

# DECODE THREADS
class DecodeWorker(QRunnable):
    def __init__(self, *args):
        super(DecodeWorker, self).__init__()
        self.fn = steg.decode
        self.args = args
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL) # ctl + c to quit
    sys.exit(app.exec())