from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QProgressBar, QMessageBox, QGridLayout, QGroupBox, QFileDialog, QComboBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
import re
from constants import *
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

        #backend signals
        self.download_manager.progressSignal.connect(self.progressBar.setValue)
        self.download_manager.statusSignal.connect(self.statusLabel.setText)
        self.download_manager.finishedSignal.connect(self.finished_download)
        self.download_manager.errorSignal.connect(self.handle_errors)
        self.download_manager.metadata.connect(self.list_metadata)


        #frontend signals
        self.download_dir_label.setText(str(self.download_manager.downloads_folder))
        self.download_dir_button.clicked.connect(self.browse_folders)
        self.fetch_info_button.clicked.connect(self.fetch_info)
        self.download_button.clicked.connect(self.start_download)

        #tell the thread what to do when it starts
        self.background_thread.started.connect(self.download_manager.download)

    def resetUI(self):
        self.url_box.clear()
        self.download_button.setEnabled(True)
        self.progressBar.hide()
        self.statusLabel.clear()
        self.formats_dropdown.clear()
        self.background_thread.quit()

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

    def fetch_info(self):
        url = self.url_box.text().strip()
        if not url:
            return
        self.download_manager.url = url
        self.download_manager.fetch_info()

    def list_metadata(self, options):
        self.formats_dropdown.clear()
        for option in options:
            format, id = option
            self.formats_dropdown.addItem(format,id)

    def start_download(self):
        url = self.url_box.text().strip()
        self.download_manager.format_id = self.formats_dropdown.currentData()
        self.download_manager.label = self.formats_dropdown.currentText()
        if not url:
            return

        self.download_manager.url = url
        self.download_button.setEnabled(False)
        self.background_thread.start()
        self.progressBar.show()

    def finished_download(self):
        QMessageBox.information(self, "Success", "Download Completed")
        self.resetUI()

    def initUI(self):
        #defining the UI's main characteristics
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setFixedSize(UIConfig.WINDOW_WIDTH,UIConfig.WINDOW_HEIGHT)
        self.setStyleSheet(self.main_style())

        #Setting up the main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(UIConfig.MARGIN,UIConfig.MARGIN,UIConfig.MARGIN,UIConfig.MARGIN)
        self.main_layout.setSpacing(UIConfig.SPACING)

        self.setup_download_section()
        self.setup_dir_section()
        self.setup_progress_section()

        self.main_layout.addStretch(1)
        self.setCentralWidget(self.main_widget)

    def setup_download_section(self):
        self.download_layout = QVBoxLayout()
        self.actions_layout = QHBoxLayout()
        self.download_group = QGroupBox("Download Settings")
        self.download_group.setStyleSheet(self.main_style())

        #url_box
        self.url_box = QLineEdit()
        self.url_box.setPlaceholderText("Enter a Youtube Link...")
        self.url_box.setFixedSize(UIConfig.URL_BAR_WIDTH, UIConfig.DOWNLOAD_WIDGETS_HEIGHT)

        #download_button
        self.download_button = QPushButton("Download")
        self.download_button.setFixedSize(UIConfig.DOWNLOAD_WIDGETS_WIDTH, UIConfig.DOWNLOAD_WIDGETS_HEIGHT)
        self.download_button.setCursor(Qt.PointingHandCursor)

        #fetch_info_button
        self.fetch_info_button = QPushButton("Fetch Info")
        self.fetch_info_button.setFixedSize(UIConfig.DOWNLOAD_WIDGETS_WIDTH, UIConfig.DOWNLOAD_WIDGETS_HEIGHT)
        self.fetch_info_button.setCursor(Qt.PointingHandCursor)

        #formats_dropdown
        self.formats_dropdown = QComboBox()
        self.formats_dropdown.setFixedSize(UIConfig.DOWNLOAD_WIDGETS_WIDTH, UIConfig.DOWNLOAD_WIDGETS_HEIGHT)
        self.formats_dropdown.setStyleSheet(self.main_style())

        # Adding widgets to the layouts
        self.download_layout.addWidget(self.url_box)
        self.actions_layout.addWidget(self.download_button)
        self.actions_layout.addWidget(self.fetch_info_button)
        self.actions_layout.addStretch(1)
        self.actions_layout.addWidget(self.formats_dropdown)


        self.download_group.setLayout(self.download_layout)
        self.download_layout.addLayout(self.actions_layout)
        self.main_layout.addWidget(self.download_group)

    def setup_dir_section(self):
        self.dir_layout = QGridLayout()
        self.dir_group = QGroupBox("Storage Settings")
        self.dir_group.setLayout(self.dir_layout)
        self.dir_group.setStyleSheet(self.main_style())

        self.download_dir_caption = QLabel("Save files to")

        #download_dir_label
        self.download_dir_label = QLineEdit()
        self.download_dir_label.setReadOnly(True)
        self.download_dir_label.setFixedSize(UIConfig.URL_BAR_WIDTH - 100, UIConfig.DOWNLOAD_WIDGETS_HEIGHT)

        #download_dir_button
        self.download_dir_button = QPushButton("Browse...")
        self.download_dir_button.setFixedSize(90, UIConfig.DOWNLOAD_WIDGETS_HEIGHT)
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
        return f"""
    QMainWindow {{
        background-color: {UIConfig.BG_COLOR};
    }}


    QLineEdit {{
        padding: 8px;
        border: 1px solid {UIConfig.BORDER_COLOR};
        border-radius: 4px;
        background-color: white;
        color: #333333;
    }}
    QLineEdit:focus {{
        border: 1px solid {UIConfig.PRIMARY_COLOR};
    }}

    QPushButton {{
        background-color: #fcfcfc;
        border: 1px solid {UIConfig.BORDER_COLOR};
        border-radius: 6px;
        padding: 5px 10px;
        font-weight: 450;
        color: #444444;
    }}
    QPushButton:hover {{
        background-color: #f0f0f0;
        border-color: #bcbcbc;
    }}
    QPushButton:pressed {{
        background-color: #e5e5e5;
    }}

    QComboBox {{
        border: 1px solid {UIConfig.BORDER_COLOR};
        border-radius: 4px;
        padding: 5px 10px;
        background-color: white;
        color: #333333;
    }}
    QComboBox:hover {{
        border-color: {UIConfig.PRIMARY_COLOR};
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left: 1px solid #eeeeee;
    }}
    
    QProgressBar {{
        border: 1px solid {UIConfig.BORDER_COLOR};
        border-radius: 4px;
        text-align: center;
        background-color: #f3f3f3;
        font-weight: bold;
        color: #333;
    }}
    QProgressBar::chunk {{
        background-color: {UIConfig.PRIMARY_COLOR};
        border-radius: 3px;
    }}

    QMessageBox {{
        background-color: #ffffff;
    }}
    QMessageBox QLabel {{
        color: #333333;
        font-size: 13px;
    }}
    QAbstractItemView {{
        border: 1px solid {UIConfig.BORDER_COLOR};
        selection-background-color: {UIConfig.PRIMARY_COLOR};
        selection-color: white;
        background-color: white;
        outline: none;
    }}
    QGroupBox {{
        font-weight: bold;
        border: 1px solid {UIConfig.BORDER_COLOR};
        border-radius: 6px;
        margin-top: 1.2em;
        background-color: white;
        padding-top: 10px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
        padding: 0 5px;
        color: #555555;
    }}
    """