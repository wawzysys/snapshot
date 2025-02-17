import pyautogui
import paramiko
from io import BytesIO
import time
from PIL import Image
from datetime import datetime
from pynput import keyboard
import threading
import sys
import configparser
import os

def load_config():
    config = configparser.ConfigParser()
    # 获取配置文件的路径
    config_path = os.path.join(os.path.dirname(__file__), 'serverconfig.ini')
    
    try:
        config.read(config_path)
        return {
            'HOST': config['Server']['host'],
            'USERNAME': config['Server']['username'],
            'PASSWORD': config['Server']['password'],
            'PORT': int(config['Server']['port']),
            'REMOTE_PATH': config['Server']['remote_path']
        }
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        # 使用默认配置
        return {
            'HOST': '47.121.221.247',
            'USERNAME': 'newuser',
            'PASSWORD': '0',
            'PORT': 22,
            'REMOTE_PATH': '/home/newuser/jie/'
        }

# 加载配置
config = load_config()
HOST = config['HOST']
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']
PORT = config['PORT']
REMOTE_PATH = config['REMOTE_PATH']

def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot
def upload_to_server(image, filename):
    try:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        transport = paramiko.Transport((HOST, PORT))
        transport.connect(username=USERNAME, password=PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        with BytesIO(img_byte_arr) as fl:
            sftp.putfo(fl, REMOTE_PATH + filename)
        print(f'上传成功')
        
    except paramiko.SSHException as ssh_error:
        print(f'SSH连接错误: {ssh_error}')
    except Exception as e:
        print(f'发生错误: {e}')
    finally:
        try:
            sftp.close()
            transport.close()
        except:
            pass
def on_hotkey_pressed():
    image = take_screenshot()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"screenshot_{timestamp}.png"
    upload_to_server(image, filename)

# 添加一个集合来跟踪当前按下的键
current_keys = set()

def on_press(key):
    current_keys.add(key)
    try:
        # 判断系统类型并使用对应的快捷键
        if hasattr(key, 'char') and key.char == 'e':
            if sys.platform == 'darwin' and keyboard.Key.cmd in current_keys:  # macOS
                on_hotkey_pressed()
            elif sys.platform in ['win32', 'win64'] and keyboard.Key.ctrl in current_keys:  # Windows
                on_hotkey_pressed()
            elif sys.platform.startswith('linux') and keyboard.Key.ctrl in current_keys:  # Linux
                on_hotkey_pressed()
        elif key == keyboard.Key.esc:
            return False
    except AttributeError:
        pass

def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

def test_server_connection():
    try:
        transport = paramiko.Transport((HOST, PORT))
        transport.connect(username=USERNAME, password=PASSWORD)
        transport.close()
        print("服务器连接测试成功")
        return True
    except Exception as e:
        print(f"服务器连接测试失败: {e}")
        return False

def main():
    if not test_server_connection():
        print("程序退出：无法连接到服务器")
        return
    
    # 根据系统显示对应的快捷键提示
    if sys.platform == 'darwin':
        hotkey = "Command+E"
    else:
        hotkey = "Ctrl+M"
        
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print(f"截图工具已启动，使用 {hotkey} 进行截图，ESC 退出")
        listener.join()

if __name__ == "__main__":
    main()  
