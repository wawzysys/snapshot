# 截图上传工具

一个简单的截图并自动上传到服务器的工具。支持 Windows 和 macOS 系统。

## 功能特点

- 一键截图并自动上传
- 支持快捷键操作
- 自动适配不同操作系统的快捷键
- 实时显示上传状态
- 支持 ESC 快速退出

## 快捷键

- Windows: `Ctrl + M` 截图
- macOS: `Command + M` 截图
- 所有系统: `ESC` 退出

## 安装说明

### 环境要求

- Python 3.9 或更高版本
- 必需的 Python 包：
  ```bash
  pip install pyautogui paramiko pynput pillow pyinstaller
  ```

### 目录结构 

## 配置说明

程序使用 `serverconfig.ini` 配置文件来存储服务器信息：

```ini
[Server]
host = 你的服务器地址
username = 用户名
password = 密码
port = 22
remote_path = /上传/目录/路径/
```

配置文件位置：`src/serverconfig.ini`

如果配置文件不存在，程序会使用默认配置。 

## 使用说明

1. 运行程序前，确保 `serverconfig.ini` 和程序在同一目录下
2. 根据需要修改 `serverconfig.ini` 中的服务器配置
3. 运行 `截图工具.exe`（Windows）或 `截图工具`（Mac）
4. 使用对应系统的快捷键进行截图
5. 截图会自动上传到服务器
6. 按 ESC 键退出程序

### 配置文件说明

`serverconfig.ini` 文件应与程序放在同一目录下：
```
程序目录/
├── 截图工具.exe     # Windows可执行文件
└── serverconfig.ini  # 配置文件
``` 