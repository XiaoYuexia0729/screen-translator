"""
截图区域选择器
允许用户通过鼠标框选屏幕区域
"""

from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
import sys


class AreaSelector(QWidget):
    """全屏透明窗口，用于选择截图区域"""

    area_selected = pyqtSignal(dict)  # 发送选中的区域

    def __init__(self):
        super().__init__()
        self.begin = QPoint()
        self.end = QPoint()
        self.is_selecting = False
        self.init_ui()

    def init_ui(self):
        """初始化全屏透明窗口"""
        self.setWindowTitle('选择截图区域')
        # 设置为全屏无边框窗口
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        # 设置窗口透明度
        self.setWindowOpacity(0.3)
        # 全屏显示
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.showFullScreen()
        self.setCursor(Qt.CrossCursor)

    def paintEvent(self, event):
        """绘制选择框"""
        if self.is_selecting:
            painter = QPainter(self)

            # 设置半透明背景
            painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

            # 绘制选择框
            rect = QRect(self.begin, self.end).normalized()

            # 选择框内部透明
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(rect, QColor(0, 0, 0, 0))

            # 绘制边框
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            pen = QPen(QColor(0, 255, 0), 3, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(rect)

            # 显示尺寸信息
            font = QFont('Arial', 12, QFont.Bold)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            info_text = f'区域: {rect.width()} x {rect.height()} 像素'
            painter.drawText(rect.x(), rect.y() - 10, info_text)

    def mousePressEvent(self, event):
        """鼠标按下，开始选择"""
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.is_selecting = True
            self.update()

    def mouseMoveEvent(self, event):
        """鼠标移动，更新选择框"""
        if self.is_selecting:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放，完成选择"""
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.is_selecting = False
            rect = QRect(self.begin, self.end).normalized()

            # 发送选中的区域
            region = {
                'left': rect.x(),
                'top': rect.y(),
                'width': rect.width(),
                'height': rect.height()
            }
            self.area_selected.emit(region)
            self.close()

    def keyPressEvent(self, event):
        """按 ESC 键取消选择"""
        if event.key() == Qt.Key_Escape:
            self.close()


def select_area():
    """打开区域选择器并返回选中的区域"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    selector = AreaSelector()
    selector.show()

    selected_region = {}

    def on_area_selected(region):
        nonlocal selected_region
        selected_region = region

    selector.area_selected.connect(on_area_selected)
    app.exec_()

    return selected_region


if __name__ == '__main__':
    # 测试
    region = select_area()
    if region:
        print(f"选中的区域: {region}")
