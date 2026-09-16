"""
实时屏幕英文翻译程序
功能：
1. 截取屏幕区域
2. OCR 识别英文文本
3. 翻译成中文
4. 在窗口中显示翻译结果
"""

import sys
import threading
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QSpinBox, QGroupBox, QCheckBox, QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon
import mss
import pytesseract
from PIL import Image
import numpy as np
import io
from area_selector import AreaSelector
from translator_utils import translate_text_cached
from overlay_window import TranslationOverlay

# Import config to set Tesseract path
import config


class TranslationSignals(QObject):
    """信号类，用于线程间通信"""
    translation_ready = pyqtSignal(str, str)  # 原文, 译文
    error_occurred = pyqtSignal(str)
    status_update = pyqtSignal(str)  # 状态更新


class ScreenTranslator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = TranslationSignals()
        self.signals.translation_ready.connect(self.update_translation)
        self.signals.error_occurred.connect(self.show_error)
        self.signals.status_update.connect(self.update_status)

        self.is_running = False
        self.capture_thread = None
        self.last_text = ""

        # 创建悬浮窗口
        self.overlay = TranslationOverlay()

        # 截图区域设置（默认值 - 未设置状态）
        self.capture_region = {
            'left': 0,
            'top': 0,
            'width': 0,
            'height': 0
        }

        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('实时屏幕翻译器')
        self.setGeometry(100, 100, 900, 700)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 标题
        title_label = QLabel('📺 实时屏幕英文翻译')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 悬浮显示选项
        overlay_layout = QHBoxLayout()
        self.overlay_checkbox = QCheckBox('在屏幕上悬浮显示翻译（推荐）')
        self.overlay_checkbox.setChecked(True)
        self.overlay_checkbox.setStyleSheet("font-size: 12px; padding: 5px;")
        overlay_layout.addWidget(self.overlay_checkbox)
        overlay_layout.addStretch()
        main_layout.addLayout(overlay_layout)

        # 控制面板
        control_group = QGroupBox('控制面板')
        control_layout = QVBoxLayout()

        # 截图区域设置 - 改为更友好的方式
        region_layout = QVBoxLayout()

        # 区域信息显示
        info_layout = QHBoxLayout()
        info_layout.addWidget(QLabel('📍 当前截图区域:'))
        self.region_info_label = QLabel('未设置')
        self.region_info_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        info_layout.addWidget(self.region_info_label)
        info_layout.addStretch()
        region_layout.addLayout(info_layout)

        # 选择区域按钮
        select_area_btn = QPushButton('🎯 鼠标框选截图区域')
        select_area_btn.clicked.connect(self.open_area_selector)
        select_area_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 13px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        region_layout.addWidget(select_area_btn)

        # 提示文字
        hint_label = QLabel('💡 提示: 点击按钮后，用鼠标在屏幕上拖动框选需要翻译的区域')
        hint_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        hint_label.setWordWrap(True)
        region_layout.addWidget(hint_label)

        control_layout.addLayout(region_layout)

        # 更新间隔设置
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel('更新间隔:'))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 10)
        self.interval_spin.setValue(2)
        self.interval_spin.setSuffix(' 秒')
        interval_layout.addWidget(self.interval_spin)
        interval_layout.addStretch()
        control_layout.addLayout(interval_layout)

        # 按钮
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton('▶ 开始翻译')
        self.start_btn.clicked.connect(self.toggle_translation)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.start_btn)

        self.capture_btn = QPushButton('📷 手动截图翻译')
        self.capture_btn.clicked.connect(self.manual_capture)
        button_layout.addWidget(self.capture_btn)

        control_layout.addLayout(button_layout)
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)

        # 显示区域
        display_group = QGroupBox('翻译结果')
        display_layout = QVBoxLayout()

        # 原文
        display_layout.addWidget(QLabel('原文 (English):'))
        self.original_text = QTextEdit()
        self.original_text.setReadOnly(True)
        self.original_text.setMaximumHeight(150)
        self.original_text.setStyleSheet("background-color: #f5f5f5;")
        display_layout.addWidget(self.original_text)

        # 译文
        display_layout.addWidget(QLabel('译文 (中文):'))
        self.translated_text = QTextEdit()
        self.translated_text.setReadOnly(True)
        self.translated_text.setFont(QFont('Microsoft YaHei', 11))
        self.translated_text.setStyleSheet("background-color: #e3f2fd; font-weight: bold;")
        display_layout.addWidget(self.translated_text)

        display_group.setLayout(display_layout)
        main_layout.addWidget(display_group)

        # 状态栏
        status_layout = QHBoxLayout()
        self.status_label = QLabel('状态: 请先框选截图区域')
        self.status_label.setStyleSheet("padding: 5px; background-color: #fff3cd; color: #856404;")
        status_layout.addWidget(self.status_label, 3)

        # 进度指示器
        self.progress_label = QLabel('⚪ 就绪')
        self.progress_label.setStyleSheet("padding: 5px; font-weight: bold;")
        status_layout.addWidget(self.progress_label, 1)

        main_layout.addLayout(status_layout)

        # 更新区域信息显示
        self.update_region_display()

    def update_status(self, status):
        """更新状态指示器"""
        if "识别中" in status:
            self.progress_label.setText('🔵 识别中...')
        elif "翻译中" in status:
            self.progress_label.setText('🟡 翻译中...')
        elif "完成" in status:
            self.progress_label.setText('🟢 完成')
        else:
            self.progress_label.setText('⚪ 就绪')

    def open_area_selector(self):
        """打开区域选择器"""
        self.hide()  # 隐藏主窗口
        self.selector = AreaSelector()
        self.selector.area_selected.connect(self.on_area_selected)
        self.selector.show()

    def on_area_selected(self, region):
        """区域选择完成"""
        if region and region.get('width', 0) > 0 and region.get('height', 0) > 0:
            self.capture_region = region
            self.update_region_display()
            self.status_label.setText('状态: 区域已设置，点击"开始翻译"或"手动截图翻译"')
            self.status_label.setStyleSheet("padding: 5px; background-color: #d4edda; color: #155724;")
        self.show()  # 显示主窗口

    def update_region_display(self):
        """更新区域信息显示"""
        if self.capture_region['width'] > 0:
            info = f"左上角({self.capture_region['left']}, {self.capture_region['top']}) 尺寸: {self.capture_region['width']} × {self.capture_region['height']} 像素"
            self.region_info_label.setText(info)
        else:
            self.region_info_label.setText('未设置 - 请先框选区域')

    def toggle_translation(self):
        """切换翻译状态"""
        if not self.is_running:
            self.start_translation()
        else:
            self.stop_translation()

    def start_translation(self):
        """开始实时翻译"""
        # 检查区域是否已设置
        if self.capture_region['width'] <= 0 or self.capture_region['height'] <= 0:
            self.status_label.setText('错误: 请先框选截图区域！')
            self.status_label.setStyleSheet("padding: 5px; background-color: #f8d7da; color: #721c24;")
            return

        self.is_running = True
        self.start_btn.setText('⏸ 停止翻译')
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        self.status_label.setText('状态: 运行中...')
        self.status_label.setStyleSheet("padding: 5px; background-color: #d1ecf1; color: #0c5460;")

        # 启动截图翻译线程
        self.capture_thread = threading.Thread(target=self.capture_and_translate_loop, daemon=True)
        self.capture_thread.start()

    def stop_translation(self):
        """停止实时翻译"""
        self.is_running = False
        self.start_btn.setText('▶ 开始翻译')
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.status_label.setText('状态: 已停止')

    def capture_and_translate_loop(self):
        """循环截图和翻译"""
        with mss.mss() as sct:
            while self.is_running:
                try:
                    self.signals.status_update.emit("识别中")

                    # 截取屏幕区域
                    monitor = {
                        'left': self.capture_region['left'],
                        'top': self.capture_region['top'],
                        'width': self.capture_region['width'],
                        'height': self.capture_region['height']
                    }
                    screenshot = sct.grab(monitor)

                    # 转换为 PIL Image
                    img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

                    # OCR 识别文本
                    text = pytesseract.image_to_string(img, lang='eng')
                    text = text.strip()

                    # 如果文本有变化且不为空，则翻译
                    if text and text != self.last_text:
                        self.last_text = text

                        self.signals.status_update.emit("翻译中")

                        # 翻译文本（使用缓存优化速度）
                        translated_text = translate_text_cached(text)

                        self.signals.status_update.emit("完成")

                        # 发送信号更新 UI
                        self.signals.translation_ready.emit(text, translated_text)
                    else:
                        self.signals.status_update.emit("就绪")

                    # 等待指定的间隔
                    time.sleep(self.interval_spin.value())

                except Exception as e:
                    self.signals.error_occurred.emit(f'错误: {str(e)}')
                    time.sleep(2)

    def manual_capture(self):
        """手动截图翻译一次"""
        # 检查区域是否已设置
        if self.capture_region['width'] <= 0 or self.capture_region['height'] <= 0:
            self.status_label.setText('错误: 请先框选截图区域！')
            self.status_label.setStyleSheet("padding: 5px; background-color: #f8d7da; color: #721c24;")
            return

        self.status_label.setText('状态: 正在截图翻译...')

        # 在新线程中执行，避免阻塞 UI
        thread = threading.Thread(target=self.do_manual_capture, daemon=True)
        thread.start()

    def do_manual_capture(self):
        """执行手动截图翻译"""
        try:
            self.signals.status_update.emit("识别中")

            with mss.mss() as sct:
                monitor = {
                    'left': self.capture_region['left'],
                    'top': self.capture_region['top'],
                    'width': self.capture_region['width'],
                    'height': self.capture_region['height']
                }
                screenshot = sct.grab(monitor)
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

                # OCR
                text = pytesseract.image_to_string(img, lang='eng').strip()

                if text:
                    self.signals.status_update.emit("翻译中")

                    # 翻译（使用缓存优化速度）
                    translated_text = translate_text_cached(text)

                    self.signals.status_update.emit("完成")
                    self.signals.translation_ready.emit(text, translated_text)
                else:
                    self.signals.status_update.emit("就绪")
                    self.signals.error_occurred.emit('未识别到文本')

        except Exception as e:
            self.signals.status_update.emit("就绪")
            self.signals.error_occurred.emit(f'错误: {str(e)}')

    def update_translation(self, original, translated):
        """更新翻译显示"""
        self.original_text.setPlainText(original)
        self.translated_text.setPlainText(translated)
        self.status_label.setText(f'状态: 翻译完成 - {time.strftime("%H:%M:%S")}')

        # 如果启用悬浮显示
        if self.overlay_checkbox.isChecked():
            self.overlay.update_position(self.capture_region)
            self.overlay.show_translation(translated)

    def show_error(self, error_msg):
        """显示错误信息"""
        self.status_label.setText(error_msg)
        self.status_label.setStyleSheet("padding: 5px; background-color: #ffebee; color: #c62828;")
        QTimer.singleShot(3000, lambda: self.status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0;"))


def main():
    app = QApplication(sys.argv)
    window = ScreenTranslator()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
