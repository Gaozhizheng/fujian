"""
Vercel Serverless Function - 视频链接转MP4服务
注意：Vercel不支持FFmpeg，因此需要调用外部服务
"""

from http.server import BaseHTTPRequestHandler
import json
import requests
import os
import urllib.parse
from typing import Optional

# 外部FFmpeg服务配置（Render部署的服务）
EXTERNAL_FFMPEG_SERVICE = os.getenv("EXTERNAL_FFMPEG_SERVICE", "https://fujian.onrender.com/convert")

# Vercel API路由处理
class handler(BaseHTTPRequestHandler):
    """Vercel Serverless Function处理类"""
    
    def do_GET(self):
        """处理GET请求"""
        try:
            # 解析路径和查询参数
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # 处理根路径
            if path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "message": "视频链接转MP4服务 (Vercel版本)",
                    "note": "此版本需要外部FFmpeg服务支持",
                    "endpoints": {
                        "convert": "/convert?url=视频链接",
                        "health": "/health",
                        "info": "/info"
                    }
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # 处理健康检查
            elif path == "/health":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "healthy", "platform": "vercel"}
                self.wfile.write(json.dumps(response).encode())
                return
            
            # 处理服务信息
            elif path == "/info":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "service": "video-converter",
                    "version": "1.0.0",
                    "platform": "vercel",
                    "external_ffmpeg_service": EXTERNAL_FFMPEG_SERVICE
                }
                self.wfile.write(json.dumps(response).encode())
                return
            
            # 处理视频转换
            elif path == "/convert":
                url = query_params.get('url', [None])[0]
                filename = query_params.get('filename', [None])[0]
                
                if not url:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"error": "URL参数不能为空"}
                    self.wfile.write(json.dumps(response).encode())
                    return
                
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
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response_data = {
                            "status": "success",
                            "message": "转换请求已提交",
                            "download_url": f"{EXTERNAL_FFMPEG_SERVICE}/download/{response.json().get('job_id')}"
                        }
                        self.wfile.write(json.dumps(response_data).encode())
                        return
                    else:
                        self.send_response(response.status_code)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_response = {"error": f"外部服务错误: {response.text}"}
                        self.wfile.write(json.dumps(error_response).encode())
                        return
                        
                except requests.exceptions.Timeout:
                    self.send_response(504)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    error_response = {"error": "外部服务响应超时"}
                    self.wfile.write(json.dumps(error_response).encode())
                    return
                except requests.exceptions.RequestException as e:
                    self.send_response(502)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    error_response = {"error": f"外部服务连接失败: {str(e)}"}
                    self.wfile.write(json.dumps(error_response).encode())
                    return
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    error_response = {"error": f"处理失败: {str(e)}"}
                    self.wfile.write(json.dumps(error_response).encode())
                    return
            
            # 处理未找到的路径
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "未找到路径"}
                self.wfile.write(json.dumps(response).encode())
                return
                
        except Exception as e:
            # 全局异常处理
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": f"服务器内部错误: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())
            return

# 本地测试代码
if __name__ == "__main__":
    from http.server import HTTPServer
    
    class TestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # 创建handler实例并处理请求
            handler_instance = handler
            handler_instance.__init__(self, None, None, None)
            handler_instance.do_GET()
    
    server = HTTPServer(('localhost', 8000), TestHandler)
    print("测试服务器运行在 http://localhost:8000")
    server.serve_forever()