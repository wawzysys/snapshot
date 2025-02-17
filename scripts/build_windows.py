import os
import sys
import shutil

# 检查是否在 Windows 环境
if not sys.platform in ['win32', 'win64']:
    print("错误：此脚本只能在 Windows 系统上运行")
    sys.exit(1)

import PyInstaller.__main__

# 获取项目根目录的路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 源文件路径
SRC_FILE = os.path.join(ROOT_DIR, 'src', 'jt.py')
# 图标文件路径
ICON_FILE = os.path.join(ROOT_DIR, 'assets', 'screenshot.ico')
# 配置文件路径
CONFIG_FILE = os.path.join(ROOT_DIR, 'src', 'serverconfig.ini')
# 输出目录
DIST_PATH = os.path.join(ROOT_DIR, 'build', 'windows')

# 确保输出目录存在
os.makedirs(DIST_PATH, exist_ok=True)

print("开始构建 Windows 版本...")

# Windows 构建配置
build_options = [
    SRC_FILE,
    '--onefile',
    '--name=截图工具.exe',  # 明确指定 .exe 后缀
    '--hidden-import=PIL._tkinter_finder',
    '--console',
    f'--icon={ICON_FILE}',
    f'--distpath={DIST_PATH}',
    '--clean',
    '--add-binary=tcl86t.dll;.',
    '--add-binary=tk86t.dll;.',
]

# 执行打包
PyInstaller.__main__.run(build_options)

# 复制配置文件到输出目录
shutil.copy2(CONFIG_FILE, DIST_PATH)

print(f"构建完成！")
print(f"可执行文件位置：{os.path.join(DIST_PATH, '截图工具.exe')}")
print(f"配置文件位置：{os.path.join(DIST_PATH, 'serverconfig.ini')}") 