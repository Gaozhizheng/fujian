from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
import os
import subprocess
import uuid
from pathlib import Path
from typing import Optional

app = FastAPI(title="视频链接转MP4服务", version="1.0.0")

# 创建临时目录用于存储文件
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

def download_video(url: str, output_path: Path) -> bool:
    """下载视频文件"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False

def convert_to_mp4(input_path: Path, output_path: Path) -> bool:
    """使用FFmpeg转换视频格式为MP4"""
    try:
        # 检查FFmpeg是否可用
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("FFmpeg未安装，请先安装FFmpeg")
        
        # 转换视频格式
        cmd = [
            "ffmpeg", "-i", str(input_path), 
            "-c", "copy",  # 直接复制流，不重新编码
            "-movflags", "+faststart",  # 优化网络播放
            "-y",  # 覆盖输出文件
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"FFmpeg错误: {result.stderr}")
            return False
            
        return True
        
    except subprocess.TimeoutExpired:
        print("转换超时")
        return False
    except Exception as e:
        print(f"转换失败: {e}")
        return False

@app.get("/")
async def root():
    return {
        "message": "视频链接转MP4服务",
        "endpoints": {
            "convert": "/convert?url=视频链接",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/convert")
async def convert_video(url: str, filename: Optional[str] = None):
    """
    将视频链接转换为MP4格式文件
    
    - **url**: 视频文件的URL链接
    - **filename**: 可选的自定义输出文件名
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL参数不能为空")
    
    # 生成唯一文件名
    file_id = str(uuid.uuid4())
    temp_input = TEMP_DIR / f"input_{file_id}"
    temp_output = TEMP_DIR / f"output_{file_id}.mp4"
    
    try:
        # 1. 下载视频
        print(f"开始下载: {url}")
        if not download_video(url, temp_input):
            raise HTTPException(status_code=400, detail="视频下载失败")
        
        # 2. 转换格式
        print("开始转换格式...")
        if not convert_to_mp4(temp_input, temp_output):
            raise HTTPException(status_code=500, detail="视频格式转换失败")
        
        # 3. 返回文件
        output_filename = filename or f"converted_video_{file_id}.mp4"
        
        return FileResponse(
            path=temp_output,
            filename=output_filename,
            media_type="video/mp4",
            headers={
                "Content-Disposition": f"attachment; filename={output_filename}"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")
    
    finally:
        # 清理临时文件
        try:
            if temp_input.exists():
                temp_input.unlink()
            # 输出文件由FileResponse自动清理
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)