from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from downloader import downloader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        #adding the backend thread
        self.background_thread = QThread()
        self.download_manager = downloader()
        self.download_manager.moveToThread(self.background_thread )

        self.initUI()


        self.download_manager.progressSignal.connect(self.progressBar.setValue)
        self.download_manager.statusSignal.connect(self.statusLabel.setText)


        #tell the thread what to do when it starts
        self.background_thread.started.connect(self.download_manager.download)

        #working with the backend
        self.download_button.clicked.connect(self.start_download)

    def start_download(self):
        url = self.textbox1.text()
        self.download_manager.url = url
        if not url:
            QMessageBox.critical(self, "Error", "Please enter a valid URL")
        else:
            self.download_button.setEnabled(False)
            self.background_thread.start()

    def initUI(self):
        #defining the UI's characteristics
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setGeometry(600, 200, 600, 600)
        self.setStyleSheet("background-color:white")

        #Introducing main_widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        #Defining everything
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        self.main_layout.addLayout(self.layout1)
        self.main_layout.addLayout(self.layout2)
        self.download_button = QPushButton("Download")
        self.label1 = QLabel("Enter Video Link:")
        self.textbox1 = QLineEdit()
        self.progressBar = QProgressBar()
        self.statusLabel = QLabel()

        #Adding stuff to layout 1
        self.layout1.addWidget(self.label1)
        self.layout1.addWidget(self.textbox1)
        self.layout1.addWidget(self.download_button)
        self.layout1.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Adding stuff to layout 2
        self.layout2.addWidget(self.progressBar)
        self.layout2.addWidget(self.statusLabel)

        #SETTING THE CENTRAL WIDGET
        self.setCentralWidget(self.main_widget)
