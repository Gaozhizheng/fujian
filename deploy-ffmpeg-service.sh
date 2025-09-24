#!/bin/bash

# FFmpeg服务部署脚本
# 支持多种部署平台

echo "🚀 FFmpeg服务部署脚本"
echo "========================"

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法: $0 [platform]"
    echo "可用平台: docker, heroku, railway, render, digitalocean, aws"
    exit 1
fi

PLATFORM=$1

case $PLATFORM in
    "docker")
        echo "🐳 部署到Docker..."
        
        # 检查Docker是否安装
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker未安装"
            exit 1
        fi
        
        # 构建镜像
        docker build -t ffmpeg-video-converter .
        
        # 运行容器
        docker run -d \
            -p 8000:8000 \
            -v $(pwd)/temp:/app/temp \
            --name video-converter \
            ffmpeg-video-converter
        
        echo "✅ Docker部署完成"
        echo "🌐 服务地址: http://localhost:8000"
        ;;
    
    "heroku")
        echo "🦸 部署到Heroku..."
        
        # 检查Heroku CLI是否安装
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI未安装"
            exit 1
        fi
        
        # 创建Heroku应用
        heroku create your-ffmpeg-service-name
        
        # 添加FFmpeg buildpack
        heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
        heroku buildpacks:add heroku/python
        
        # 部署
        git init
        git add .
        git commit -m "Deploy FFmpeg service"
        git push heroku main
        
        echo "✅ Heroku部署完成"
        ;;
    
    "railway")
        echo "🚄 部署到Railway..."
        echo "请参考: https://railway.app/"
        echo "1. 连接GitHub仓库"
        echo "2. 选择此项目"
        echo "3. 部署自动开始"
        ;;
    
    "render")
        echo "🎨 部署到Render..."
        echo "请参考: https://render.com/"
        echo "1. 创建Web Service"
        echo "2. 连接GitHub"
        echo "3. 使用Docker部署"
        ;;
    
    "digitalocean")
        echo "🐠 部署到DigitalOcean..."
        echo "请参考: https://www.digitalocean.com/"
        echo "1. 创建Droplet"
        echo "2. 安装Docker"
        echo "3. 部署服务"
        ;;
    
    "aws")
        echo "☁️ 部署到AWS..."
        echo "请参考: https://aws.amazon.com/"
        echo "选项: ECS, EKS, EC2, Lambda"
        ;;
    
    *)
        echo "❌ 不支持的平台: $PLATFORM"
        exit 1
        ;;
esac

echo ""
echo "📋 部署完成后，请更新Cloudflare配置:"
echo "在 wrangler.toml 中设置:"
echo "EXTERNAL_FFMPEG_SERVICE = 'https://your-deployed-service.com/convert'"