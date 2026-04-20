from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
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

        #working with the url
        url = self.textbox1.text()

        #working with the backend
        self.background_thread.started.connect(self.download_manager.download)


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
        self.main_layout.addLayout(self.layout1)
        self.download_button = QPushButton("Download")
        self.label1 = QLabel("Enter Video Link:")
        self.textbox1 = QLineEdit()

        #Adding stuff to layout 1
        self.layout1.addWidget(self.label1)
        self.layout1.addWidget(self.textbox1)
        self.layout1.addWidget(self.download_button)
        self.layout1.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        #working with the backend
        self.download_button.clicked.connect(self.background_thread.start)


        #SETTING THE CENTRAL WIDGET
        self.setCentralWidget(self.main_widget)
