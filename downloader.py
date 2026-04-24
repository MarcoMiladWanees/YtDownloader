import yt_dlp
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from pathlib import Path



class downloader(QObject):
    progressSignal  = pyqtSignal(int)
    statusSignal    = pyqtSignal(str)
    finishedSignal  = pyqtSignal()
    errorSignal     = pyqtSignal(str)
    metadata        = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.downloads_folder = Path.home() / "Downloads" / "Youtube Downloader"
        self.url = None
        self.format_id = None
        self.label = None


    def yt_progress(self, progress_dictionary):
         if progress_dictionary['status'] == 'downloading':
            percentage = progress_dictionary.get('_percent_str', '0%').replace('%', '')
            percentage = int(float(percentage))
            self.progressSignal.emit(percentage)
            speed = progress_dictionary['_speed_str']
            remaining_time = progress_dictionary['_eta_str']
            total_size = progress_dictionary.get('_total_bytes_str', "Unknown")
            total_downloaded = (progress_dictionary.get('downloaded_bytes', 0)/ 1000000 )
            status = f"{remaining_time: >10} remaining | {speed: >10} | {total_downloaded: >8.2f}/{total_size}"
            self.statusSignal.emit(status)

    def fetch_info(self):
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            formats = info.get('formats', [])
        options = []
        for f in formats:
            if f.get('vcodec') == 'none':
                continue
            res     = f.get('resolution')
            height  = f.get('height')
            note    = f.get('format_note')
            if height:
                label = f"{height}p"
            elif res and 'x' in str(res):
                # Extract 1080 from "1920x1080"
                label = f"{str(res).split('x')[1]}p"
            elif note:
                label = note
            else:
                label = "Standard Quality"

            extention = f.get('ext')
            id = f.get('format_id')
            options.append((f"{label} ({extention})", id))
        self.metadata.emit(options)

    def download(self):
        try:
            #ydl_opts variables
            format               = f"{self.format_id}+bestaudio"
            label                = self.label.split(" ")
            quality, extension   = label
            extension = extension.strip().strip("()")
            self.downloads_folder.mkdir(parents=True, exist_ok=True)
            download_path = str(self.downloads_folder/ f"%(title)s_{quality}.%(ext)s")

            ydl_opts = {'format': format,
                        'ffmpeg_location': 'C:/ffmpeg/bin',
                        # 'quiet': True,
                        # 'no_warnings': True,
                        'noplaylist': False,
                        'outtmpl': download_path,
                        'merge_output_format': extension,
                        "progress_hooks": [self.yt_progress] }


            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.finishedSignal.emit()
        except Exception as e:
            self.errorSignal.emit(str(e))