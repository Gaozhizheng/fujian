#!/usr/bin/env python3
"""
启动脚本 - 视频链接转MP4服务
"""

import os
import sys
import subprocess

def check_ffmpeg():
    """检查FFmpeg是否安装"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_dependencies():
    """安装Python依赖"""
    print("正在安装依赖包...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("依赖安装完成!")
        return True
    except subprocess.CalledProcessError:
        print("依赖安装失败，请手动运行: pip install -r requirements.txt")
        return False

def main():
    print("=" * 50)
    print("视频链接转MP4服务")
    print("=" * 50)
    
    # 检查依赖
    if not os.path.exists('requirements.txt'):
        print("错误: 未找到requirements.txt文件")
        return
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 检查FFmpeg
    if not check_ffmpeg():
        print("\n⚠️  警告: FFmpeg未安装或未在PATH中")
        print("请先安装FFmpeg:")
        print("1. Windows: 下载 https://ffmpeg.org/download.html")
        print("2. Linux: sudo apt install ffmpeg")
        print("3. macOS: brew install ffmpeg")
        print("\n安装后请确保ffmpeg命令可用")
        print("\n继续启动服务（转换功能将不可用）...")
    else:
        print("✅ FFmpeg检测正常")
    
    # 启动服务
    print("\n🚀 启动服务...")
    print("服务地址: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()