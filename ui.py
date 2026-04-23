from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QProgressBar, QMessageBox, QGridLayout, QGroupBox, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject

from constants import UI_MESSAGES
from downloader import downloader
from pathlib import Path

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
        self.download_manager.finishedSignal.connect(self.finished_download)
        self.download_dir_label.setText(str(self.download_manager.downloads_folder))
        self.download_dir_button.clicked.connect(self.browse_folders)
        self.download_manager.errorSignal.connect(self.handle_errors)
        #tell the thread what to do when it starts
        self.background_thread.started.connect(self.download_manager.download)

        #working with the backend
        self.download_button.clicked.connect(self.start_download)
        self.textbox1.textChanged.connect(lambda: self.textbox1.setStyleSheet("color: #333333;"))
    def resetUI(self):
        self.textbox1.clear()
        self.download_button.setEnabled(True)
        self.progressBar.hide()
        self.statusLabel.clear()
        self.background_thread.quit()

    def start_download(self):
        url = self.textbox1.text().strip()

        if not url:
            self.textbox1.setPlaceholderText("Please enter a Youtube Link")
            self.textbox1.setStyleSheet("color: #ff0000;")
            return

        self.download_manager.url = url
        self.download_button.setEnabled(False)
        self.background_thread.start()
        self.progressBar.show()

    def finished_download(self):
        QMessageBox.information(self, "Success", "Download Completed")
        self.resetUI()

    def browse_folders(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if selected_folder:
            selected_folder = Path(selected_folder)
            if selected_folder.name != "Youtube Downloader":
                selected_folder = selected_folder / "Youtube Downloader"
            self.download_dir_label.setText(str(selected_folder))
            self.download_manager.downloads_folder = selected_folder

    def handle_errors(self, error):
        if "is not a valid URL" in error or "generic" in error:
            return

        error = str(error).lower()
        found_key = "default"
        for key in UI_MESSAGES:
            if key in error:
                found_key = key
                break

        icon, title, description = UI_MESSAGES[found_key]
        QMessageBox.critical(self, title, f"{description}\n\n {error}")
        self.resetUI()

    def initUI(self):
        #defining the UI's main characteristics
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setFixedSize(600, 600)
        self.setStyleSheet(self.main_style())

        #Setting up the main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20,20,20,20)
        self.main_layout.setSpacing(20)

        self.setup_download_section()
        self.setup_dir_section()
        self.setup_progress_section()

        self.main_layout.addStretch(1)
        self.setCentralWidget(self.main_widget)

    def setup_download_section(self):
        self.download_layout = QGridLayout()
        self.download_group = QGroupBox("Download Settings")
        self.download_group.setStyleSheet(self.group_style())

        self.textbox1 = QLineEdit()
        self.textbox1.setPlaceholderText("Enter a Youtube Link...")
        self.textbox1.setFixedWidth(500)

        #download_button
        self.download_button = QPushButton("Download")
        self.download_button.setFixedWidth(150)
        self.download_button.setCursor(Qt.PointingHandCursor)

        # Adding widgets to the download_layout
        self.download_layout.addWidget(self.textbox1, 0, 0)
        self.download_layout.addWidget(self.download_button, 1, 0, alignment=Qt.AlignCenter)

        self.download_group.setLayout(self.download_layout)
        self.main_layout.addWidget(self.download_group)

    def setup_dir_section(self):
        self.dir_layout = QGridLayout()
        self.dir_group = QGroupBox("Storage Settings")
        self.dir_group.setLayout(self.dir_layout)
        self.dir_group.setStyleSheet(self.group_style())

        self.download_dir_caption = QLabel("Save files to")

        #download_dir_label
        self.download_dir_label = QLineEdit()
        self.download_dir_label.setReadOnly(True)
        self.download_dir_label.setFixedSize(420, 32)

        #download_dir_button
        self.download_dir_button = QPushButton("Browse...")
        self.download_dir_button.setFixedSize(80, 32)
        self.download_dir_button.setCursor(Qt.PointingHandCursor)

        # Adding widgets to the dir_Layout
        self.dir_layout.addWidget(self.download_dir_caption, 0, 0)
        self.dir_layout.addWidget(self.download_dir_label, 1, 0)
        self.dir_layout.addWidget(self.download_dir_button, 1, 1)

        self.main_layout.addWidget(self.dir_group)

    def setup_progress_section(self):
        self.progress_layout = QGridLayout()
        self.statusLabel = QLabel()

        self.progressBar = QProgressBar()
        self.progressBar.setFixedWidth(500)
        self.progressBar.hide()

        # Adding widgets to the progress_layout
        self.progress_layout.addWidget(self.progressBar, 0, 0)
        self.progress_layout.addWidget(self.statusLabel, 1, 0)
        self.progress_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.main_layout.addLayout(self.progress_layout)

    def main_style(self):
        return """
            QMainWindow {
                background-color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e5e5e5;
            }
            QProgressBar {
                border: 1px solid #dcdcdc;
                border-radius: 5px;
                text-align: center;
                background-color: #f9f9f9;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 4px;
            }
            QMessageBox {
            background-color: #ffffff;
            border: 1px solid #dcdcdc;
            }
            QMessageBox QLabel {
            color: #333333;
            font-size: 13px;
            font-weight: 500;
            padding-left: 10px;
            }
            QMessageBox QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            padding: 6px 20px;
            min-width: 70px;
            min-height: 24px;          
            }
            QMessageBox QPushButton:hover {
            background-color: #e5e5e5;
            }
        """
    def group_style(self):
        return """
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                margin-top: 15px;
                padding: 10px;
                background-color: #f9f9f9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                color: #555;
            }
        """