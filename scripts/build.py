import os
import sys
import PyInstaller.__main__

# 基本配置
build_options = [
    'jt.py',
    '--onefile',
    '--name=截图工具',
    '--hidden-import=PIL._tkinter_finder',
    '--console',
    '--icon=screenshot.ico',
]

# 根据系统添加特定配置
if sys.platform in ['win32', 'win64']:  # Windows
    build_options.extend([
        '--add-binary=tcl86t.dll;.',
        '--add-binary=tk86t.dll;.',
    ])
    print("正在构建 Windows 版本...")
elif sys.platform == 'darwin':  # macOS
    print("正在构建 macOS 版本...")
else:
    print("正在构建 Linux 版本...")

# 执行打包
PyInstaller.__main__.run(build_options) 