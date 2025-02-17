import pyautogui
import requests
from io import BytesIO
import time
from PIL import Image
from datetime import datetime
from pynput import keyboard
import threading
import sys
import configparser
import os
import base64

def load_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'github_config.ini')
    
    try:
        config.read(config_path)
        return {
            'GITHUB_TOKEN': config['GitHub']['token'],
            'REPO_OWNER': config['GitHub']['owner'],
            'REPO_NAME': config['GitHub']['repo'],
            'BRANCH': config['GitHub']['branch']
        }
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        sys.exit(1)

def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

def upload_to_github(image, filename):
    try:
        config = load_config()
        
        # 将图片转换为base64
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        content = base64.b64encode(img_byte_arr).decode()

        # GitHub API endpoint
        url = f"https://api.github.com/repos/{config['REPO_OWNER']}/{config['REPO_NAME']}/contents/screenshots/{filename}"
        
        headers = {
            "Authorization": f"token {config['GITHUB_TOKEN']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "message": f"Upload screenshot {filename}",
            "content": content,
            "branch": config['BRANCH']
        }

        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in [201, 200]:
            print(f'上传成功！图片URL: https://raw.githubusercontent.com/{config["REPO_OWNER"]}/{config["REPO_NAME"]}/{config["BRANCH"]}/screenshots/{filename}')
        else:
            print(f'上传失败: {response.status_code} - {response.text}')
            
    except Exception as e:
        print(f'发生错误: {e}')

def on_hotkey_pressed():
    image = take_screenshot()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"screenshot_{timestamp}.png"
    upload_to_github(image, filename)

current_keys = set()

def on_press(key):
    current_keys.add(key)
    try:
        if hasattr(key, 'char') and key.char == 'm':
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

def test_github_connection():
    try:
        config = load_config()
        headers = {
            "Authorization": f"token {config['GITHUB_TOKEN']}",
            "Accept": "application/vnd.github.v3+json"
        }
        response = requests.get(f"https://api.github.com/repos/{config['REPO_OWNER']}/{config['REPO_NAME']}", headers=headers)
        if response.status_code == 200:
            print("GitHub连接测试成功")
            return True
        else:
            print(f"GitHub连接测试失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"GitHub连接测试失败: {e}")
        return False

def main():
    if not test_github_connection():
        print("程序退出：无法连接到GitHub")
        return
    
    if sys.platform == 'darwin':
        hotkey = "Command+M"
    else:
        hotkey = "Ctrl+M"
        
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print(f"截图工具已启动，使用 {hotkey} 进行截图，ESC 退出")
        listener.join()

if __name__ == "__main__":
    main() 