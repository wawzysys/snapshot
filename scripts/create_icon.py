from PIL import Image

# 创建一个简单的图标
img = Image.new('RGB', (256, 256), color='white')
img.save('screenshot.ico') 