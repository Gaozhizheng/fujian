# FFmpeg 安装指南

## 🎯 安装方法选择

### 方法1: 自动安装（推荐）
运行 `install_ffmpeg.ps1` 脚本：

```powershell
# 右键点击 install_ffmpeg.ps1 -> "使用PowerShell运行"
# 或执行:
.\install_ffmpeg.ps1
```

### 方法2: 手动安装

#### Windows 手动安装步骤:

1. **下载FFmpeg**
   - 访问: https://ffmpeg.org/download.html
   - 选择 "Windows builds from gyan.dev" 或 "Windows builds by BtbN"
   - 下载最新版本ZIP文件

2. **解压文件**
   - 将下载的ZIP文件解压到项目目录的 `ffmpeg` 文件夹中
   - 或者直接解压到项目根目录

3. **放置ffmpeg.exe**
   - 找到解压后的 `bin` 文件夹中的 `ffmpeg.exe`
   - 复制 `ffmpeg.exe` 到项目根目录

#### 目录结构示例:
```
e:\project\fujian\
├── ffmpeg.exe          # FFmpeg主程序
├── main.py
├── requirements.txt
└── ...其他文件
```

### 方法3: 使用包管理器

#### Chocolatey (Windows):
```powershell
# 安装Chocolatey（如果未安装）
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装FFmpeg
choco install ffmpeg
```

#### Scoop (Windows):
```powershell
# 安装Scoop（如果未安装）
irm get.scoop.sh | iex

# 安装FFmpeg
scoop install ffmpeg
```

## ✅ 验证安装

安装完成后，运行以下命令验证：

```powershell
# 检查FFmpeg版本
.\ffmpeg.exe -version

# 或在项目目录中运行
python -c "import subprocess; subprocess.run(['./ffmpeg', '-version'], capture_output=True, text=True)"
```

## 🔧 项目配置

您的视频转换服务会自动检测FFmpeg：
- 优先使用项目根目录的 `ffmpeg.exe`
- 其次查找系统PATH中的 `ffmpeg` 命令
- 如果找不到会显示错误信息

## 🌐 测试视频转换

安装FFmpeg后，您可以测试视频转换功能：

```python
import requests

# 测试转换功能
response = requests.get(
    "http://localhost:8000/convert",
    params={
        "url": "https://example.com/sample-video.mp4",
        "filename": "test_output.mp4"
    }
)

if response.status_code == 200:
    with open("test_output.mp4", "wb") as f:
        f.write(response.content)
    print("✅ 视频转换成功!")
else:
    print(f"❌ 转换失败: {response.text}")
```

## ❗ 常见问题

### Q: FFmpeg安装后仍然报错？
A: 确保 `ffmpeg.exe` 在项目根目录或系统PATH中

### Q: 下载速度慢？
A: 可以尝试不同的下载源，或者使用迅雷等下载工具

### Q: 权限问题？
A: 以管理员身份运行PowerShell

## 📞 支持

如果安装遇到问题，可以：
1. 查看FFmpeg官方文档: https://ffmpeg.org/
2. 检查项目日志输出
3. 确保网络连接正常

---

**安装完成后，您的视频转换服务将具备完整的格式转换功能！** 🎉