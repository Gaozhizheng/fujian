#!/usr/bin/env python3
"""
测试脚本 - 视频链接转MP4服务
"""

import requests
import time

def test_service():
    """测试服务功能"""
    
    # 服务地址
    base_url = "http://localhost:8000"
    
    print("🧪 开始测试视频转换服务...")
    
    try:
        # 测试健康检查
        print("1. 测试健康检查...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ 健康检查正常")
        else:
            print("❌ 健康检查失败")
            return False
        
        # 测试根目录
        print("2. 测试根目录...")
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ 根目录访问正常")
        else:
            print("❌ 根目录访问失败")
            return False
        
        print("\n📋 服务基本信息:")
        info = response.json()
        print(f"   服务名称: {info.get('message', '未知')}")
        print(f"   可用端点: {list(info.get('endpoints', {}).keys())}")
        
        # 测试转换功能（使用示例URL）
        print("\n3. 测试视频转换功能...")
        print("   注意: 需要提供真实的视频URL进行测试")
        print("   示例: http://localhost:8000/convert?url=https://example.com/video.mp4")
        
        return True
        
    except requests.ConnectionError:
        print("❌ 无法连接到服务，请确保服务已启动")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

def create_example_usage():
    """创建使用示例"""
    
    print("\n📖 使用示例:")
    print("=" * 50)
    
    # Python使用示例
    print("Python客户端使用:")
    print("""
import requests

# 转换视频
url = "http://localhost:8000/convert"
params = {
    "url": "https://example.com/your-video.mp4",  # 替换为真实URL
    "filename": "converted_video.mp4"  # 可选
}

response = requests.get(url, params=params)
if response.status_code == 200:
    with open("downloaded_video.mp4", "wb") as f:
        f.write(response.content)
    print("视频下载成功!")
else:
    print(f"转换失败: {response.text}")
""")
    
    # cURL使用示例
    print("cURL命令使用:")
    print("""
# 转换并下载视频
curl -o output.mp4 "http://localhost:8000/convert?url=https://example.com/your-video.mp4"

# 带自定义文件名
curl -o my_video.mp4 "http://localhost:8000/convert?url=https://example.com/your-video.mp4&filename=my_video.mp4"
""")

if __name__ == "__main__":
    print("=" * 50)
    print("视频链接转MP4服务 - 测试工具")
    print("=" * 50)
    
    if test_service():
        create_example_usage()
        print("\n🎉 基本测试完成!")
        print("接下来您可以:")
        print("1. 使用真实视频URL测试转换功能")
        print("2. 访问 http://localhost:8000/docs 查看API文档")
    else:
        print("\n❌ 测试失败，请检查服务状态")