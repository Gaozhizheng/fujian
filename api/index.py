"""
Vercel Serverless Function - 视频链接转MP4服务
注意：Vercel不支持FFmpeg，因此需要调用外部服务
"""

import json
import requests
import os
from typing import Optional

# 外部FFmpeg服务配置（Render部署的服务）
EXTERNAL_FFMPEG_SERVICE = os.getenv("EXTERNAL_FFMPEG_SERVICE", "https://fujian.onrender.com/convert")

def handler(request):
    """Vercel Serverless Function入口函数"""
    try:
        # 解析请求路径和方法
        path = request.path
        method = request.method
        
        # 处理根路径
        if path == "/" and method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
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
        elif path == "/health" and method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"status": "healthy", "platform": "vercel"})
            }
        
        # 处理服务信息
        elif path == "/info" and method == "GET":
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({
                    "service": "video-converter",
                    "version": "1.0.0",
                    "platform": "vercel",
                    "external_ffmpeg_service": EXTERNAL_FFMPEG_SERVICE
                })
            }
        
        # 处理视频转换
        elif path == "/convert" and method == "GET":
            # 解析查询参数
            from urllib.parse import parse_qs
            query_string = request.query_string.decode('utf-8')
            query_params = parse_qs(query_string)
            
            url = query_params.get('url', [None])[0]
            filename = query_params.get('filename', [None])[0]
            
            if not url:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
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
                    return {
                        "statusCode": 200,
                        "headers": {"Content-Type": "application/json"},
                        "body": json.dumps({
                            "status": "success",
                            "message": "转换请求已提交",
                            "download_url": f"{EXTERNAL_FFMPEG_SERVICE}/download/{response.json().get('job_id')}"
                        })
                    }
                else:
                    return {
                        "statusCode": response.status_code,
                        "headers": {"Content-Type": "application/json"},
                        "body": json.dumps({"error": f"外部服务错误: {response.text}"})
                    }
                    
            except requests.exceptions.Timeout:
                return {
                    "statusCode": 504,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "外部服务响应超时"})
                }
            except requests.exceptions.RequestException as e:
                return {
                    "statusCode": 502,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": f"外部服务连接失败: {str(e)}"})
                }
            except Exception as e:
                return {
                    "statusCode": 500,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": f"处理失败: {str(e)}"})
                }
        
        # 处理未找到的路径
        else:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "未找到路径"})
            }
    except Exception as e:
        # 全局异常处理
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": f"服务器内部错误: {str(e)}"})
        }

# 本地测试代码
if __name__ == "__main__":
    import json
    from http.server import BaseHTTPRequestHandler, HTTPServer
    
    class MockRequest:
        def __init__(self, path, method, query_string=""):
            self.path = path
            self.method = method
            self.query_string = query_string.encode('utf-8')
    
    class TestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # 解析路径和查询参数
            path = self.path.split('?')[0]
            query_string = self.path.split('?')[1] if '?' in self.path else ""
            
            request = MockRequest(path, "GET", query_string)
            response = handler(request)
            
            self.send_response(response['statusCode'])
            for header, value in response['headers'].items():
                self.send_header(header, value)
            self.end_headers()
            self.wfile.write(response['body'].encode('utf-8'))
    
    server = HTTPServer(('localhost', 8000), TestHandler)
    print("测试服务器运行在 http://localhost:8000")
    server.serve_forever()