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
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'serverconfig.ini')

    try:
        config.read(config_path)
        key_path = config['Server']['key_path']
        # 如果密钥路径是相对路径，则转换为绝对路径
        if not os.path.isabs(key_path):
            key_path = os.path.join(base_dir, key_path)

        return {
            'HOST': config['Server']['host'],
            'USERNAME': config['Server']['username'],
            'KEY_PATH': key_path,  # 使用处理后的路径
            'PORT': int(config['Server']['port']),
            'REMOTE_PATH': config['Server']['remote_path']
        }
    except Exception as e:
        print(f"使用默认配置")
        # 使用默认配置
        return {
            'HOST': '47.121.221.247',
            'USERNAME': 'newuser',
            'KEY_PATH': os.path.join(base_dir, 'id_rsa'),
            'PORT': 22,
            'REMOTE_PATH': '/home/newuser/jie/'
        }


# 加载配置
config = load_config()
HOST = config['HOST']
USERNAME = config['USERNAME']
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

        # 使用密钥创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 加载私钥
        private_key = paramiko.RSAKey.from_private_key_file(config['KEY_PATH'])

        # 使用私钥连接
        ssh.connect(hostname=HOST,
                    username=USERNAME,
                    pkey=private_key,
                    port=PORT)

        # 创建SFTP客户端
        sftp = ssh.open_sftp()

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
            ssh.close()
        except:
            pass


def on_hotkey_pressed():
    image = take_screenshot()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"screenshot_{timestamp}.png"
    upload_to_server(image, filename)


# 需要重新添加 current_keys 用于 macOS 的组合键检测
current_keys = set()


def on_press(key):
    try:
        # macOS 使用 Ctrl+E
        if sys.platform == 'darwin':
            if keyboard.Key.ctrl in current_keys:
                if isinstance(key, keyboard.KeyCode
                              ) and key.char and key.char.lower() == 'e':
                    print("检测到快捷键 Ctrl+E")
                    on_hotkey_pressed()
        # Windows 使用 F9
        else:
            if key == keyboard.Key.f9:
                print("检测到快捷键 F9")
                on_hotkey_pressed()

        # ESC 退出
        if key == keyboard.Key.esc:
            return False
    except AttributeError as e:
        print(f"按键检测错误: {e}")
        pass


def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass


def test_server_connection():
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 加载私钥
        private_key = paramiko.RSAKey.from_private_key_file(config['KEY_PATH'])

        # 使用私钥连接
        ssh.connect(hostname=HOST,
                    username=USERNAME,
                    pkey=private_key,
                    port=PORT)
        ssh.close()
        print("服务器连接测试成功")
        return True
    except Exception as e:
        print(f"服务器连接测试失败: {e}")
        return False


def main():
    if not test_server_connection():
        print("程序退出：无法连接到服务器")
        return

    # 根据系统显示对应的提示
    hotkey = "Ctrl+E" if sys.platform == 'darwin' else "F9"

    with keyboard.Listener(on_press=on_press,
                           on_release=on_release) as listener:
        print(f"截图工具已启动，使用 {hotkey} 进行截图，ESC 退出")
        listener.join()


if __name__ == "__main__":
    main()
