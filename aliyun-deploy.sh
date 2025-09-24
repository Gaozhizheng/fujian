#!/bin/bash
# 阿里云部署脚本 - 适用于轻量应用服务器

echo "🚀 阿里云视频转换服务部署脚本"
echo "================================"

# 检查参数
if [ $# -eq 0 ]; then
    echo "使用方法: $0 <服务器IP> [SSH端口]"
    echo "示例: $0 123.123.123.123"
    echo "示例: $0 123.123.123.123 2222"
    exit 1
fi

SERVER_IP=$1
SSH_PORT=${2:-22}

echo "📋 部署信息:"
echo "- 服务器IP: $SERVER_IP"
echo "- SSH端口: $SSH_PORT"
echo "- 服务端口: 8000"
echo ""

# 检查本地文件
echo "🔍 检查本地文件..."
if [ ! -f "Dockerfile" ]; then
    echo "❌ 错误: 未找到Dockerfile"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误: 未找到requirements.txt"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ 错误: 未找到main.py"
    exit 1
fi

echo "✅ 所有必要文件都存在"
echo ""

# 部署选项
echo "📝 选择部署方式:"
echo "1. Docker容器部署 (推荐)"
echo "2. 直接Python部署"
read -p "请选择 (1/2): " DEPLOY_CHOICE

echo ""

if [ "$DEPLOY_CHOICE" = "1" ]; then
    echo "🐳 选择Docker容器部署"
    
    # 构建Docker镜像
    echo "🔨 构建Docker镜像..."
    docker build -t video-converter .
    
    if [ $? -ne 0 ]; then
        echo "❌ Docker构建失败"
        exit 1
    fi
    
    # 保存镜像为tar文件
    echo "💾 保存镜像..."
    docker save video-converter -o video-converter.tar
    
    # 传输到服务器
    echo "📤 传输镜像到服务器..."
    scp -P $SSH_PORT video-converter.tar root@$SERVER_IP:/tmp/
    
    # 执行部署脚本
    echo "🚀 在服务器上部署..."
    ssh -p $SSH_PORT root@$SERVER_IP << 'EOF'
        # 加载镜像
        docker load -i /tmp/video-converter.tar
        
        # 停止现有容器
        docker stop video-converter || true
        docker rm video-converter || true
        
        # 启动新容器
        docker run -d \
            --name video-converter \
            -p 8000:8000 \
            --restart unless-stopped \
            video-converter
        
        # 清理
        rm -f /tmp/video-converter.tar
        
        echo "✅ 部署完成!"
        echo "🌐 服务地址: http://$SERVER_IP:8000"
        echo "📋 检查状态: docker logs video-converter"
EOF
    
    # 清理本地文件
    rm -f video-converter.tar
    
else
    echo "🐍 选择直接Python部署"
    
    # 传输文件到服务器
    echo "📤 传输文件到服务器..."
    scp -P $SSH_PORT -r ./* root@$SERVER_IP:/opt/video-converter/
    
    # 执行部署脚本
    echo "🚀 在服务器上部署..."
    ssh -p $SSH_PORT root@$SERVER_IP << 'EOF'
        cd /opt/video-converter
        
        # 安装系统依赖
        echo "📦 安装系统依赖..."
        yum install -y python3 python3-pip ffmpeg || \
        apt-get update && apt-get install -y python3 python3-pip ffmpeg
        
        # 安装Python依赖
        echo "🐍 安装Python依赖..."
        pip3 install -r requirements.txt
        
        # 停止现有服务
        pkill -f "uvicorn main:app" || true
        
        # 启动服务
        echo "🚀 启动服务..."
        nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
        
        echo "✅ 部署完成!"
        echo "🌐 服务地址: http://$SERVER_IP:8000"
        echo "📋 检查日志: tail -f app.log"
EOF
fi

echo ""
echo "🎉 部署完成!"
echo "📋 下一步:"
echo "1. 测试服务: curl http://$SERVER_IP:8000/health"
echo "2. 更新Cloudflare配置中的EXTERNAL_FFMPEG_SERVICE变量"
echo "3. 部署Cloudflare Workers: npm run deploy"
echo ""
echo "💡 提示: 确保服务器的安全组开放了8000端口"