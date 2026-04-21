import yt_dlp
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QProgressBar



class downloader(QObject):
    progressSignal = pyqtSignal(int)
    statusSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.url = None

    def yt_progress(self, progress_dictionary):
        if progress_dictionary['status'] == 'downloading':
            percentage = progress_dictionary.get('_percent_str', '0%').replace('%', '')
            percentage = int(float(percentage))
            self.progressSignal.emit(percentage)
            status = f"{progress_dictionary['_speed_str']} - {progress_dictionary['_eta_str']} remaining"
            self.statusSignal.emit(status)




    def download(self):
        ydl_opts = {'format': 'bestvideo+bestaudio/best',
                    'ffmpeg_location': 'C:/ffmpeg/bin',
                    # 'quiet': True,
                    # 'no_warnings': True,
                    'noplaylist': False,
                    'outtmpl': 'C:/Users/LENOVO/Desktop/%(title)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    "progress_hooks": [self.yt_progress], }
        if self.url:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
