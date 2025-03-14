import os
import sys
import shutil
import PyInstaller.__main__

# 检查是否在 Windows 环境
if not sys.platform in ['win32', 'win64']:
    print("错误：此脚本只能在 Windows 系统上运行")
    sys.exit(1)

# 获取项目根目录的路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义所有相关路径
PATHS = {
    'src': os.path.join(ROOT_DIR, 'src', 'jt.py'),
    'icon': os.path.join(ROOT_DIR, 'assets', 'screenshot.ico'),
    'config': os.path.join(ROOT_DIR, 'src', 'serverconfig.ini'),
    'key': os.path.join(ROOT_DIR, 'src', 'id_rsa'),  # 添加密钥文件路径
    'dist': os.path.join(ROOT_DIR, 'build', 'windows')
}

# 确保输出目录存在
os.makedirs(PATHS['dist'], exist_ok=True)

print("开始构建 Windows 版本...")

# Windows 构建配置
build_options = [
    PATHS['src'],
    '--onefile',
    '--name=截图工具',
    '--console',  # 显示控制台窗口
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
    f'--icon={PATHS["icon"]}',
    f'--add-data={PATHS["config"]};.',  # 修改配置文件添加方式
    f'--add-data={PATHS["key"]};.',  # 添加密钥文件
    f'--distpath={PATHS["dist"]}',
    '--clean',
]

try:
    # 执行打包
    PyInstaller.__main__.run(build_options)

    # 复制配置文件到输出目录
    shutil.copy2(PATHS['config'], PATHS['dist'])

    print("\n构建成功！")
    print(f"可执行文件位置：{os.path.join(PATHS['dist'], '截图工具.exe')}")
    print(f"配置文件位置：{os.path.join(PATHS['dist'], 'serverconfig.ini')}")

except Exception as e:
    print(f"\n构建失败：{str(e)}")
    sys.exit(1)
