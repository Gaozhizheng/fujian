"""
Vercel Serverless Function - 视频链接转MP4服务
注意：Vercel不支持FFmpeg，因此需要调用外部服务
"""

import json
import requests
import os
from typing import Dict, Any

# 外部FFmpeg服务配置（Render部署的服务）
EXTERNAL_FFMPEG_SERVICE = os.getenv("EXTERNAL_FFMPEG_SERVICE", "https://fujian.onrender.com/convert")

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Vercel Serverless Function处理函数"""
    
    try:
        # 获取请求路径和查询参数
        path = event.get("path", "/")
        query_parameters = event.get("queryParameters", {})
        
        # 处理根路径
        if path == "/":
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "message": "视频链接转MP4服务 (Vercel版本)",
                    "note": "此版本需要外部FFmpeg服务支持",
                    "endpoints": {
                        "convert": "/convert?url=视频链接",
                        "health": "/health",
                        "info": "/info"
                    }
                })
            }
        
        # 处理健康检查
        elif path == "/health":
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"status": "healthy", "platform": "vercel"})
            }
        
        # 处理服务信息
        elif path == "/info":
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "service": "video-converter",
                    "version": "1.0.0",
                    "platform": "vercel",
                    "external_ffmpeg_service": EXTERNAL_FFMPEG_SERVICE
                })
            }
        
        # 处理视频转换
        elif path == "/convert":
            url = query_parameters.get("url")
            filename = query_parameters.get("filename")
            
            if not url:
                return {
                    "statusCode": 400,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"error": "URL参数不能为空"})
                }
            
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
                    response_data = {
                        "status": "success",
                        "message": "转换请求已提交",
                        "download_url": f"{EXTERNAL_FFMPEG_SERVICE}/download/{response.json().get('job_id')}"
                    }
                    return {
                        "statusCode": 200,
                        "headers": {
                            "Content-Type": "application/json"
                        },
                        "body": json.dumps(response_data)
                    }
                else:
                    return {
                        "statusCode": response.status_code,
                        "headers": {
                            "Content-Type": "application/json"
                        },
                        "body": json.dumps({"error": f"外部服务错误: {response.text}"})
                    }
                    
            except requests.exceptions.Timeout:
                return {
                    "statusCode": 504,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"error": "外部服务响应超时"})
                }
            except requests.exceptions.RequestException as e:
                return {
                    "statusCode": 502,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"error": f"外部服务连接失败: {str(e)}"})
                }
            except Exception as e:
                return {
                    "statusCode": 500,
                    "headers": {
                        "Content-Type": "application/json"
                    },
                    "body": json.dumps({"error": f"处理失败: {str(e)}"})
                }
        
        # 处理未找到的路径
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "未找到路径"})
            }
            
    except Exception as e:
        # 全局异常处理
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": f"服务器内部错误: {str(e)}"})
        }