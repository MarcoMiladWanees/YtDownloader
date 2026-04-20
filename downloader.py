import yt_dlp
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QProgressBar

ydl_opts = {'format': 'bestvideo+bestaudio/best',
            'ffmpeg_location': 'C:/ffmpeg/bin',
            #'quiet': True,
            #'no_warnings': True,
            'noplaylist': False,
            'outtmpl': 'C:/Users/LENOVO/Desktop/%(title)s.%(ext)s',
            'merge_output_format': 'mp4'}



class downloader(QObject):
    def __init__(self):
        super().__init__()
        self.progressSignal = pyqtSignal(int)
        self.finishedSignal = pyqtSignal()
        self.errorSignal = pyqtSignal()

    def set_url(self, url):
        self.url = url


    def yt_progress(self, progress_dictionary):
        if progress_dictionary['status'] == 'downloading':



    def download(self, url):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
