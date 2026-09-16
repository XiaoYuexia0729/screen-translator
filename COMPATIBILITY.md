# 兼容性说明 / Compatibility Notes

## Python 版本 / Python Version

### 支持的版本 / Supported Versions
- **最低要求 / Minimum**: Python 3.9
- **推荐版本 / Recommended**: Python 3.10 或更高 / or higher
- **已测试 / Tested**: Python 3.9, 3.10, 3.11, 3.12, 3.13, 3.14

### 为什么需要 Python 3.9+ / Why Python 3.9+
- PyQt5 需要 Python 3.7+ / PyQt5 requires Python 3.7+
- numpy 现代版本需要 Python 3.9+ / Modern numpy requires Python 3.9+
- 某些依赖库在 Python 3.9+ 上更稳定 / Some dependencies are more stable on Python 3.9+

## 操作系统 / Operating System

### Windows
- ✅ Windows 7 SP1 (需要更新) / (with updates)
- ✅ Windows 10
- ✅ Windows 11
- ⚠️ Windows Server (未测试但理论支持) / (untested but should work)

### Linux / macOS
- ❌ 当前版本仅支持 Windows / Current version is Windows-only
- 主要原因：使用了 Windows 特定的 UTF-8 编码处理 / Due to Windows-specific UTF-8 handling
- 如需跨平台支持，需要修改 `translator_utils.py` / For cross-platform support, modify `translator_utils.py`

## 依赖库兼容性 / Dependencies Compatibility

所有依赖库版本已设置为较低的最低要求，确保广泛兼容：
All dependency versions are set to lower minimum requirements for broad compatibility:

| 库 / Library | 最低版本 / Min Version | Python 3.9 | Python 3.10+ |
|--------------|----------------------|------------|--------------|
| PyQt5        | 5.15.0              | ✅         | ✅           |
| pytesseract  | 0.3.10              | ✅         | ✅           |
| Pillow       | 9.0.0               | ✅         | ✅           |
| mss          | 6.1.0               | ✅         | ✅           |
| deep-translator | 1.11.0           | ✅         | ✅           |
| numpy        | 1.21.0              | ✅         | ✅           |
| translators  | 5.8.0               | ✅         | ✅           |

## 外部依赖 / External Dependencies

### Tesseract OCR
- **版本 / Version**: 任何现代版本 / Any modern version (4.0+)
- **安装路径 / Install Path**: `C:\Program Files\Tesseract-OCR\`
- **必需语言包 / Required Language**: English (eng)
- **下载地址 / Download**: https://github.com/UB-Mannheim/tesseract/wiki

## 网络要求 / Network Requirements

### 翻译服务 / Translation Services
程序依赖以下在线翻译服务（按优先级）：
Program depends on these online translation services (in priority order):

1. **Bing Translator** (bing.com) - 最稳定 / Most stable
2. **Google Translate** (translate.google.com)
3. **Alibaba Translator** (alibaba.com)
4. **Baidu Translator** (fanyi.baidu.com)

### 防火墙设置 / Firewall Settings
- 确保 Python 可以访问互联网 / Ensure Python can access internet
- 如果使用企业代理，可能需要配置环境变量 / For corporate proxies, may need environment variables:
  - `HTTP_PROXY`
  - `HTTPS_PROXY`

## 已知问题 / Known Issues

### 1. 中文显示乱码 / Chinese Characters Display as Garbage
**问题 / Issue**: Windows 控制台编码问题
**解决方案 / Solution**: 已在 `translator_utils.py` 中自动处理 UTF-8 编码
**状态 / Status**: ✅ 已修复 / Fixed

### 2. PyInstaller 命令找不到 / PyInstaller Command Not Found
**问题 / Issue**: PyInstaller Scripts 目录不在 PATH 中
**解决方案 / Solution**: 使用 `python -m PyInstaller` 而不是直接调用 `pyinstaller`
**状态 / Status**: ✅ 已修复 / Fixed in `build-exe.bat`

### 3. numpy 版本冲突 / numpy Version Conflicts
**问题 / Issue**: 某些 Python 版本对 numpy 版本有特定要求
**解决方案 / Solution**: 使用 `numpy>=1.21.0` 确保兼容 Python 3.9+
**状态 / Status**: ✅ 已优化 / Optimized

## 兼容性检查 / Compatibility Check

运行以下脚本检查您的系统：
Run these scripts to check your system:

1. **Python 版本检查 / Python Version Check**:
   ```bash
   python --version
   ```
   应显示 3.9.0 或更高 / Should show 3.9.0 or higher

2. **完整依赖检查 / Full Dependency Check**:
   ```bash
   test-dependencies.bat
   ```
   所有项应显示 [OK] / All items should show [OK]

3. **导入测试 / Import Test**:
   ```bash
   python -c "from translator_utils import translate_text; print('OK')"
   ```

## 升级建议 / Upgrade Recommendations

如果您使用较旧的 Python 版本：
If you're using an older Python version:

- **Python 3.8 及以下 / 3.8 and below**: 
  - ❌ 不支持 / Not supported
  - 请升级到 Python 3.9+ / Please upgrade to Python 3.9+
  
- **Python 3.9**:
  - ✅ 支持但建议升级 / Supported but upgrade recommended
  - 某些依赖库可能需要编译 / Some dependencies may require compilation
  
- **Python 3.10+**:
  - ✅ 完全支持，推荐使用 / Fully supported, recommended

## 技术支持 / Technical Support

如果遇到兼容性问题：
If you encounter compatibility issues:

1. 运行 `test-dependencies.bat` 查看具体错误
2. 检查 Python 版本：`python --version`
3. 确认所有依赖已安装：`pip list`
4. 尝试重新安装依赖：`pip install -r requirements.txt --force-reinstall`
