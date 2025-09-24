"""
Cloudflare Workers兼容版本 - 视频链接转MP4服务
注意：Cloudflare Workers不支持FFmpeg，因此需要调用外部服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import os
from typing import Optional

app = FastAPI(title="视频链接转MP4服务 - Cloudflare版本", version="1.0.0")

# 外部FFmpeg服务配置（Render部署的服务）
EXTERNAL_FFMPEG_SERVICE = os.getenv("EXTERNAL_FFMPEG_SERVICE", "https://fujian.onrender.com/convert")

@app.get("/")
async def root():
    return {
        "message": "视频链接转MP4服务 (Vercel版本)",
        "note": "此版本需要外部FFmpeg服务支持",
        "endpoints": {
            "convert": "/convert?url=视频链接",
            "health": "/health",
            "info": "/info"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "platform": "vercel"}

@app.get("/info")
async def service_info():
    return {
        "service": "video-converter",
        "version": "1.0.0",
        "platform": "vercel",
        "external_ffmpeg_service": EXTERNAL_FFMPEG_SERVICE
    }

@app.get("/convert")
async def convert_video(url: str, filename: Optional[str] = None):
    """
    将视频链接转换为MP4格式文件（通过外部FFmpeg服务）
    
    - **url**: 视频文件的URL链接
    - **filename**: 可选的自定义输出文件名
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL参数不能为空")
    
    try:
        # 调用外部FFmpeg服务
        payload = {
            "url": url,
            "filename": filename or "converted_video.mp4"
        }
        
        response = requests.post(
            EXTERNAL_FFMPEG_SERVICE,
            json=payload,
            timeout=60,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            # 返回外部服务的响应
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "转换请求已提交",
                    "download_url": f"{EXTERNAL_FFMPEG_SERVICE}/download/{response.json().get('job_id')}"
                }
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"外部服务错误: {response.text}"
            )
            
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="外部服务响应超时")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"外部服务连接失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

# Vercel函数入口点
async def handler(request):
    """Vercel Serverless Function入口函数"""
    try:
        # 这里需要将Python请求转换为Vercel Serverless Function的格式
        # 实际部署时需要更复杂的适配代码
        return {
            "message": "Vercel Serverless Function已配置",
            "status": "info"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)