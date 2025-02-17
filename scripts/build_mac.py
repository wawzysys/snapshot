import PyInstaller.__main__
import sys
import os

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PyInstaller.__main__.run([
    'src/jt.py',  # 主脚本
    '--onefile',  # 打包成单个文件
    '--noconsole',  # 不显示控制台
    '--name=截图工具',  # 可执行文件名
    '--hidden-import=PIL',
    '--hidden-import=PIL._imagingtk',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=pyautogui',
    '--hidden-import=pynput',
    '--hidden-import=paramiko',
    '--hidden-import=cryptography',
    '--hidden-import=bcrypt',
    '--hidden-import=nacl',
    '--collect-all=paramiko',
    '--collect-all=pynput',
    '--collect-all=cryptography',
]) 