@echo off
echo 🚀 正在安装FFmpeg...
echo ==================================================

REM 创建ffmpeg目录
if not exist "ffmpeg" mkdir ffmpeg

REM 下载FFmpeg（使用更稳定的源）
echo 📥 下载FFmpeg...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg\ffmpeg.zip'"

if errorlevel 1 (
    echo ❌ 下载失败
    echo 请手动下载FFmpeg:
    echo 1. 访问 https://ffmpeg.org/download.html
    echo 2. 下载Windows版本
    echo 3. 解压到ffmpeg文件夹
    pause
    exit /b 1
)

REM 解压文件
echo 📦 解压FFmpeg...
powershell -Command "Expand-Archive -Path 'ffmpeg\ffmpeg.zip' -DestinationPath 'ffmpeg' -Force"

REM 查找并复制ffmpeg.exe
for /r ffmpeg %%i in (ffmpeg.exe) do (
    copy "%%i" .\ffmpeg.exe >nul
    goto :found
)

:found
echo ✅ FFmpeg安装完成！
echo 📍 位置: %CD%\ffmpeg.exe

REM 测试FFmpeg
echo 🧪 测试FFmpeg版本...
ffmpeg.exe -version 2>&1 | findstr "version"

if errorlevel 1 (
    echo ⚠️  FFmpeg测试失败
) else (
    echo ✅ FFmpeg测试成功
)

echo ==================================================
echo 🎉 安装完成！现在可以测试视频转换功能了
echo 📝 访问 http://localhost:8000/docs 进行测试
pause