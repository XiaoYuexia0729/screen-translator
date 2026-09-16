# Screen Translator - 快速开始指南

一个实时识别屏幕英文并翻译为中文的实用工具

## 系统要求

- Windows 7/10/11
- Python 3.9 或更高版本
- 互联网连接（用于翻译服务）

---

## 安装步骤（首次使用）

### 步骤 1: 安装 Python（如果还没有）

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.9 或更高版本
3. 安装时**务必勾选 "Add Python to PATH"**

### 步骤 2: 安装 Python 依赖库

**方式 A: 自动安装（推荐）**
- 直接运行 `run.bat`，程序会自动检查并安装依赖

**方式 B: 手动安装**
- 运行 `install-dependencies.bat`

### 步骤 3: 安装 Tesseract OCR

**选项 A: 使用安装脚本**
1. 运行 `install-tesseract.bat`
2. 浏览器会打开下载页面
3. 下载并运行安装程序
4. 安装时选择 English 语言包
5. 安装到默认路径：`C:\Program Files\Tesseract-OCR`

**选项 B: 手动下载**
1. 访问 https://github.com/UB-Mannheim/tesseract/wiki
2. 下载 Windows 安装程序
3. 运行安装程序
4. 选择 English 语言包
5. 安装到：`C:\Program Files\Tesseract-OCR`

### 步骤 4: 验证安装（可选）

运行 `test-dependencies.bat` 检查所有依赖是否正确安装

如果所有项目显示 `[OK]`，说明安装成功！

### 步骤 5: 启动翻译器

运行 `run.bat`

---

## 使用方法

1. 点击 **"鼠标选择区域"** 按钮
2. 用鼠标拖动选择包含英文的屏幕区域
3. 点击 **"开始翻译"** 进行实时翻译
   或
   点击 **"手动截图"** 进行单次翻译
4. 查看结果：
   - 上方：英文原文
   - 下方：中文翻译（蓝色背景）

---

## 常见问题

**"Tesseract not found" / 找不到 Tesseract**
- 按照上面步骤安装 Tesseract
- 确认安装路径为：`C:\Program Files\Tesseract-OCR`

**"No text detected" / 未检测到文本**
- 确保选择区域包含清晰的英文文本
- 文字大小应足够大（12像素以上）
- 避免复杂背景

**"Translation failed" / 翻译失败**
- 检查互联网连接
- 程序会自动尝试多个翻译服务（Bing、Google、百度等）

**Python 版本过低**
- 本程序需要 Python 3.9 或更高版本
- 从 https://www.python.org/downloads/ 下载最新版本
- 重新安装时勾选 "Add Python to PATH"

**依赖安装失败**
- 检查网络连接是否正常
- 尝试升级 pip：`python -m pip install --upgrade pip`
- 确认防火墙没有阻止 pip

---

## 文件说明

- `run.bat` - 启动翻译器（推荐使用）
- `install-dependencies.bat` - 安装 Python 依赖库
- `test-dependencies.bat` - 测试依赖是否正确安装
- `install-tesseract.bat` - Tesseract OCR 安装助手
- `build-exe.bat` - 构建独立 EXE 文件（高级用户）
- `main.py` - 主程序
- `translator_utils.py` - 翻译功能
- `area_selector.py` - 区域选择功能
- `overlay_window.py` - 翻译悬浮窗
- `config.py` - 配置文件
- `requirements.txt` - Python 依赖列表

---

## 技术细节

### Python 版本兼容性
- **最低要求**: Python 3.9
- **推荐版本**: Python 3.10 或更高
- **已测试**: Python 3.9, 3.10, 3.11, 3.12, 3.13, 3.14

### 依赖库版本
所有依赖库版本已优化，确保在 Python 3.9+ 上稳定运行：
- PyQt5 >= 5.15.0
- pytesseract >= 0.3.10
- Pillow >= 9.0.0
- mss >= 6.1.0
- deep-translator >= 1.11.0
- numpy >= 1.21.0
- translators >= 5.8.0

### 翻译服务
程序会按顺序尝试以下翻译服务：
1. Bing Translator（最稳定）
2. Google Translate
3. Deep Translator
4. Alibaba Translator
5. Baidu Translator

如果一个服务不可用，会自动切换到下一个。

---

## 其他文档

- `COMPATIBILITY.md` - 详细的兼容性说明和技术细节

---

开始使用吧！🎉

如有问题，请检查上面的常见问题部分。
