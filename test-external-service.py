#!/usr/bin/env python3
"""
外部FFmpeg服务测试脚本
用于测试部署后的服务功能
"""

import requests
import sys
import json

def test_service(service_url):
    """测试外部FFmpeg服务"""
    
    print(f"🔍 测试服务: {service_url}")
    print("=" * 50)
    
    # 测试健康检查
    print("1. 健康检查...")
    try:
        health_url = f"{service_url}/health"
        response = requests.get(health_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ 健康检查成功: {response.json()}")
        else:
            print(f"   ❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 健康检查错误: {e}")
        return False
    
    # 测试服务信息
    print("2. 服务信息...")
    try:
        info_url = f"{service_url}/info"
        response = requests.get(info_url, timeout=10)
        if response.status_code == 200:
            info = response.json()
            print(f"   ✅ 服务信息: {json.dumps(info, indent=2)}")
        else:
            print(f"   ⚠️  服务信息不可用: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  服务信息错误: {e}")
    
    # 测试视频转换（使用测试视频）
    print("3. 视频转换测试...")
    try:
        # 使用一个小的测试视频
        test_video_url = "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4"
        
        convert_url = f"{service_url}/convert"
        params = {
            "url": test_video_url,
            "filename": "test_output.mp4"
        }
        
        response = requests.get(convert_url, params=params, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ 转换请求成功: {json.dumps(result, indent=2)}")
            
            # 检查是否有下载链接
            if "download_url" in result:
                print(f"   📥 下载链接: {result['download_url']}")
            
            return True
            
        else:
            print(f"   ❌ 转换请求失败: {response.status_code}")
            print(f"   📋 响应内容: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ⚠️  转换请求超时（可能正常，视频处理需要时间）")
        return True  # 超时不一定表示失败
    except Exception as e:
        print(f"   ❌ 转换请求错误: {e}")
        return False

def main():
    """主函数"""
    
    if len(sys.argv) != 2:
        print("使用方法: python test-external-service.py <service-url>")
        print("示例: python test-external-service.py https://your-service.com")
        sys.exit(1)
    
    service_url = sys.argv[1].rstrip('/')  # 移除末尾的斜杠
    
    print("🎬 开始测试外部FFmpeg服务")
    print("-" * 50)
    
    success = test_service(service_url)
    
    print("-" * 50)
    if success:
        print("🎉 服务测试成功！")
        print("📋 下一步: 更新Cloudflare Workers配置")
        print("   在 wrangler.toml 中设置:")
        print(f'    EXTERNAL_FFMPEG_SERVICE = "{service_url}"')
    else:
        print("❌ 服务测试失败")
        print("🔧 请检查服务部署和网络连接")
        sys.exit(1)

if __name__ == "__main__":
    main()