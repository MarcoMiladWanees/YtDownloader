import yt_dlp
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QProgressBar



class downloader(QObject):
    progressSignal = pyqtSignal(int)
    statusSignal = pyqtSignal(str)
    finishedSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.url = None

    def yt_progress(self, progress_dictionary):
        if progress_dictionary['status'] == 'downloading':
            percentage = progress_dictionary.get('_percent_str', '0%').replace('%', '')
            percentage = int(float(percentage))
            self.progressSignal.emit(percentage)
            speed = progress_dictionary['_speed_str']
            remaining_time = progress_dictionary['_eta_str']
            total_size = progress_dictionary['_total_bytes_str']
            total_downloaded = (progress_dictionary.get('downloaded_bytes', 0)/ 1000000 )
            status = f"{remaining_time: >10} remaining | {speed: >10} | {total_downloaded: >8.2f}/{total_size}"
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
            self.finishedSignal.emit()
