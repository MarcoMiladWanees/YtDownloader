# constants.py

UI_MESSAGES = {

    # Success State
    "success"           : ("✅", "Success", "Download completed successfully!"),

    # URL / Content Errors
    "is not a valid url": ("❌", "Link Error", "Check the address and try again."),
    "unavailable"       : ("🔒", "Video Unavailable", "This video is private or deleted."),
    "403"               : ("🚫", "Access Denied", "YouTube blocked this. (Age or Region restricted)"),

    # System / Hardware Errors
    "getaddrinfo failed": ("🌐", "Network Error", "I can't find YouTube. Please check your internet connection and try again."),
    "connection"        : ("🌐", "Network Error", "Check your internet connection."),
    "timeout"           : ("⏱️", "Timed Out", "YouTube took too long to respond."),
    "permission denied" : ("📂", "Folder Error", "I don't have permission to save to this folder."),
    "no space left"     : ("💾", "Disk Full", "Your hard drive is full!"),
    "ffmpeg"            : ("⚙️", "System Tool Missing", "FFmpeg not found. Please check your installation."),

    # Fallback
    "default"           : ("⚠️", "Unexpected Error", "Something went wrong. Please try again.")
}


class UIConfig:
    # Window
    WINDOW_WIDTH = 850
    WINDOW_HEIGHT = 550

    # download widgets
    URL_BAR_WIDTH = 796
    DOWNLOAD_WIDGETS_HEIGHT = 35
    DOWNLOAD_WIDGETS_WIDTH = 150

    # Spacing
    MARGIN = 15
    SPACING = 10

    # Colors
    PRIMARY_COLOR = "#2ecc71"
    BORDER_COLOR = "#dcdcdc"
    BG_COLOR = "#f9f9f9"

