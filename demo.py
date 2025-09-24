#!/usr/bin/env python3
"""
演示脚本 - 视频链接转MP4服务使用示例
"""

import requests
import json

def demo():
    """演示服务功能"""
    
    base_url = "http://localhost:8000"
    
    print("🎬 视频链接转MP4服务演示")
    print("=" * 50)
    
    # 1. 检查服务状态
    print("1. 检查服务状态...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("   ✅ 服务状态正常")
        else:
            print("   ❌ 服务异常")
            return
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return
    
    # 2. 获取服务信息
    print("2. 获取服务信息...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            info = response.json()
            print(f"   📝 服务名称: {info.get('message')}")
            print(f"   🔗 可用接口: {list(info.get('endpoints', {}).keys())}")
        else:
            print("   ❌ 获取信息失败")
    except Exception as e:
        print(f"   ❌ 获取信息失败: {e}")
    
    # 3. 演示转换功能（需要真实URL）
    print("\n3. 视频转换演示")
    print("   ℹ️  请提供一个真实的视频URL进行测试")
    print("   示例命令:")
    print("   curl -o output.mp4 \"http://localhost:8000/convert?url=YOUR_VIDEO_URL\"")
    print("   ")
    print("   或者使用Python:")
    print("   ")
    print("   import requests")
    print("   url = \"http://localhost:8000/convert\"")
    print("   params = {")
    print("       \"url\": \"YOUR_VIDEO_URL\",")
    print("       \"filename\": \"my_video.mp4\"  # 可选")
    print("   }")
    print("   response = requests.get(url, params=params)")
    print("   with open(\"downloaded_video.mp4\", \"wb\") as f:")
    print("       f.write(response.content)")
    
    # 4. API文档信息
    print("\n4. API文档")
    print("   📖 访问 http://localhost:8000/docs 查看完整的API文档")
    print("   📖 包含详细的参数说明和测试界面")
    
    # 5. 注意事项
    print("\n5. 使用注意事项")
    print("   ⚠️  确保FFmpeg已安装（转换功能需要）")
    print("   ⚠️  使用真实的视频URL进行测试")
    print("   ⚠️  大文件转换可能需要较长时间")
    
    print("\n" + "=" * 50)
    print("🎉 演示完成！服务已准备就绪")
    print("   现在您可以开始使用视频转换功能了！")

if __name__ == "__main__":
    demo()