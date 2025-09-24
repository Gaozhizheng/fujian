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

# 外部FFmpeg服务配置（需要您自己部署）
EXTERNAL_FFMPEG_SERVICE = os.getenv("EXTERNAL_FFMPEG_SERVICE", "https://your-ffmpeg-service.com/convert")

@app.get("/")
async def root():
    return {
        "message": "视频链接转MP4服务 (Cloudflare Workers版本)",
        "note": "此版本需要外部FFmpeg服务支持",
        "endpoints": {
            "convert": "/convert?url=视频链接",
            "health": "/health",
            "info": "/info"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "platform": "cloudflare"}

@app.get("/info")
async def service_info():
    return {
        "service": "video-converter",
        "version": "1.0.0",
        "platform": "cloudflare-workers",
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

# Cloudflare Workers入口点
async def fetch(request, env):
    """Cloudflare Workers兼容的入口函数"""
    from js import Response
    
    try:
        # 这里需要将Python请求转换为Cloudflare Workers的格式
        # 实际部署时需要更复杂的适配代码
        return Response.json({
            "message": "请在wrangler.toml中配置正确的入口点",
            "status": "info"
        })
    except Exception as e:
        return Response.json({
            "error": str(e),
            "status": "error"
        }, status=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)