"""
Overlay window for displaying translations on screen
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont


class TranslationOverlay(QWidget):
    """Transparent overlay window to show translations on screen"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the overlay window"""
        # Make window frameless and always on top
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )

        # Semi-transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        # Translation label
        self.translation_label = QLabel()
        self.translation_label.setWordWrap(True)
        self.translation_label.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        self.translation_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 120, 215, 220);
                color: white;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 150);
            }
        """)

        layout.addWidget(self.translation_label)
        self.setLayout(layout)

        # Default size and position
        self.resize(400, 100)

    def show_translation(self, text, x=None, y=None):
        """Show translation at specified position or below selected region"""
        self.translation_label.setText(text)
        self.adjustSize()

        if x is not None and y is not None:
            self.move(x, y)

        self.show()

    def hide_translation(self):
        """Hide the overlay"""
        self.hide()

    def update_position(self, region):
        """Update position based on selected region"""
        # Position below the selected region
        x = region['left']
        y = region['top'] + region['height'] + 10

        # Make sure it's within screen bounds
        screen = QApplication.desktop().screenGeometry()
        if x + self.width() > screen.width():
            x = screen.width() - self.width() - 10
        if y + self.height() > screen.height():
            y = region['top'] - self.height() - 10

        self.move(x, y)
