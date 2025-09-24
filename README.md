# 视频链接转MP4服务

一个基于FastAPI的视频链接转换服务，可以将任意视频链接转换为MP4格式并提供下载。

## 功能特性

- ✅ 支持HTTP视频链接下载
- ✅ 自动转换为MP4格式
- ✅ 提供RESTful API接口
- ✅ 支持自定义输出文件名
- ✅ 自动清理临时文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 安装FFmpeg

### Windows
1. 运行项目中的安装脚本：
   ```bash
   # PowerShell
   .\install_ffmpeg.ps1
   
   # 或使用批处理文件
   .\simple_install_ffmpeg.bat
   ```
2. 或手动下载FFmpeg: https://ffmpeg.org/download.html
3. 解压并添加到系统PATH环境变量

### Linux/Ubuntu
```bash
sudo apt update
sudo apt install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

## 启动服务

### 方法1：使用run.py脚本（推荐）
```bash
python run.py
```

### 方法2：直接使用uvicorn
```bash
# 开发模式
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API接口

### 1. 根目录
```
GET /
```
返回服务信息和可用端点

### 2. 健康检查
```
GET /health
```
返回服务状态

### 3. 视频转换
```
GET /convert?url=<视频链接>&filename=<可选文件名>
```

**参数:**
- `url`: 视频文件的URL链接（必需）
- `filename`: 自定义输出文件名（可选）

**示例:**
```
http://localhost:8000/convert?url=https://example.com/video.mp4&filename=my_video.mp4
```

## 使用示例

### Python客户端
```python
import requests

url = "http://localhost:8000/convert"
params = {
    "url": "https://example.com/video.mp4",
    "filename": "converted_video.mp4"
}

response = requests.get(url, params=params)
with open("downloaded_video.mp4", "wb") as f:
    f.write(response.content)
```

### cURL命令
```bash
curl -o output.mp4 "http://localhost:8000/convert?url=https://example.com/video.mp4"
```

## 测试服务

### 运行演示脚本
```bash
python demo.py
```

## 技术栈

- **FastAPI**: Web框架
- **FFmpeg**: 视频处理
- **Requests**: HTTP客户端
- **Uvicorn**: ASGI服务器

## 注意事项

1. 确保FFmpeg已正确安装并添加到PATH
2. 视频转换可能需要较长时间，取决于视频大小和网络速度
3. 服务会自动清理临时文件，无需手动干预
4. 支持大多数常见视频格式的转换

## 项目结构

```
├── main.py                    # 主程序文件
├── requirements.txt           # 依赖文件
├── README.md                  # 说明文档
├── run.py                     # 启动脚本
├── demo.py                    # 演示和测试脚本
├── install_ffmpeg.ps1        # FFmpeg安装脚本(PowerShell)
├── simple_install_ffmpeg.bat  # FFmpeg安装脚本(批处理)
├── .gitignore                 # Git忽略文件
└── temp/                      # 临时文件目录（自动创建）
```

## 故障排除

### FFmpeg相关问题
1. 如果提示FFmpeg未找到，请运行安装脚本或手动安装
2. 确保FFmpeg可执行文件在系统PATH中或项目目录中

### 服务启动问题
1. 确保所有Python依赖已安装：`pip install -r requirements.txt`
2. 确保端口8000未被其他程序占用

### 视频转换问题
1. 确保提供的视频URL是有效的
2. 某些网站可能有访问限制，导致下载失败
3. 大文件转换可能需要较长时间，请耐心等待