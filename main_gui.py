import sys
import yt_dlp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


ydl_opts = {'format': 'bestvideo+bestaudio/best',
            'ffmpeg_location': 'C:/ffmpeg/bin',
            #'quiet': True,
            #'no_warnings': True,
            'noplaylist': False,
            'outtmpl': 'C:/Users/LENOVO/Desktop/%(title)s.%(ext)s',
            'merge_output_format': 'mp4'}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #setting up default app values
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(600, 200, 600, 600)
        self.setStyleSheet("background-color:white")

        #introducing main_widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)


        self.layout1 = QVBoxLayout()
        self.main_layout.addLayout(self.layout1)
        self.download_button = QPushButton("Download")
        self.label1 = QLabel("Enter Video Link:")
        self.textbox1 = QLineEdit()


        self.initUI()

        self.setCentralWidget(self.main_widget)

    def initUI(self):
        #adding stuff to layout 1
        self.layout1.addWidget(self.label1)
        self.layout1.addWidget(self.textbox1)
        self.layout1.addWidget(self.download_button)
        self.layout1.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.download_button.clicked.connect(self.download)

    def download(self):
        url = self.textbox1.text()
        self.textbox1.clear()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()