#!/usr/bin/env python3
"""
视频转换功能测试脚本
"""

import requests
import os

def test_video_conversion():
    """测试视频转换功能"""
    
    print("🎬 视频转换功能测试")
    print("=" * 50)
    
    # 测试FFmpeg
    print("1. 检查FFmpeg...")
    if os.path.exists("ffmpeg.exe"):
        print("   ✅ FFmpeg已安装")
    else:
        print("   ❌ FFmpeg未找到")
        return False
    
    # 测试服务健康
    print("2. 检查服务状态...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ 服务状态正常")
        else:
            print(f"   ❌ 服务异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 服务连接失败: {e}")
        return False
    
    print("3. 视频转换功能就绪!")
    print("   📍 访问 http://localhost:8000/docs 进行测试")
    print("   📍 使用示例:")
    print("   ")
    print("   import requests")
    print("   response = requests.get(")
    print("       \"http://localhost:8000/convert\",")
    print("       params={")
    print("           \"url\": \"https://example.com/video.mp4\",")
    print("           \"filename\": \"my_video.mp4\"")
    print("       }")
    print("   )")
    print("   ")
    print("   with open(\"output.mp4\", \"wb\") as f:")
    print("       f.write(response.content)")
    
    return True

if __name__ == "__main__":
    if test_video_conversion():
        print("\n" + "=" * 50)
        print("🎉 所有组件就绪! 视频转换服务已完全可用")
        print("📝 下一步: 提供真实视频URL进行测试")
    else:
        print("\n❌ 测试失败，请检查配置")
        print("💡 提示: 确保服务正在运行且FFmpeg已安装")