# 腾讯云部署脚本 - PowerShell版本

Write-Host "🚀 腾讯云视频转换服务部署脚本" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# 检查参数
if ($args.Count -eq 0) {
    Write-Host "使用方法: .\tencent-cloud-deploy.ps1 <服务器IP> [SSH端口]" -ForegroundColor Yellow
    Write-Host "示例: .\tencent-cloud-deploy.ps1 123.123.123.123" -ForegroundColor Yellow
    Write-Host "示例: .\tencent-cloud-deploy.ps1 123.123.123.123 2222" -ForegroundColor Yellow
    exit 1
}

$SERVER_IP = $args[0]
$SSH_PORT = if ($args.Count -gt 1) { $args[1] } else { 22 }

Write-Host "📋 部署信息:" -ForegroundColor Cyan
Write-Host "- 服务器IP: $SERVER_IP" -ForegroundColor White
Write-Host "- SSH端口: $SSH_PORT" -ForegroundColor White
Write-Host "- 服务端口: 8000" -ForegroundColor White
Write-Host ""

# 检查本地文件
Write-Host "🔍 检查本地文件..." -ForegroundColor Cyan
$requiredFiles = @("Dockerfile", "requirements.txt", "main.py")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ 错误: 未找到 $file" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ 所有必要文件都存在" -ForegroundColor Green
Write-Host ""

# 部署选项
Write-Host "📝 选择部署方式:" -ForegroundColor Cyan
Write-Host "1. Docker容器部署 (推荐)" -ForegroundColor Yellow
Write-Host "2. 直接Python部署" -ForegroundColor Yellow
$deployChoice = Read-Host "请选择 (1/2)"

Write-Host ""

if ($deployChoice -eq "1") {
    Write-Host "🐳 选择Docker容器部署" -ForegroundColor Green
    
    # 检查Docker是否安装
    try {
        docker --version | Out-Null
    } catch {
        Write-Host "❌ Docker未安装，请先安装Docker Desktop" -ForegroundColor Red
        exit 1
    }
    
    # 构建Docker镜像
    Write-Host "🔨 构建Docker镜像..." -ForegroundColor Cyan
    docker build -t video-converter .
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker构建失败" -ForegroundColor Red
        exit 1
    }
    
    # 保存镜像为tar文件
    Write-Host "💾 保存镜像..." -ForegroundColor Cyan
    docker save video-converter -o video-converter.tar
    
    # 检查ssh命令是否可用
    try {
        ssh -V 2>&1 | Out-Null
    } catch {
        Write-Host "❌ SSH客户端未安装，请安装Git Bash或OpenSSH" -ForegroundColor Red
        exit 1
    }
    
    # 传输到服务器
    Write-Host "📤 传输镜像到服务器..." -ForegroundColor Cyan
    scp -P $SSH_PORT video-converter.tar root@${SERVER_IP}:/tmp/
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 文件传输失败" -ForegroundColor Red
        exit 1
    }
    
    # 执行部署脚本
    Write-Host "🚀 在服务器上部署..." -ForegroundColor Cyan
    $deployScript = @"
        # 加载镜像
        docker load -i /tmp/video-converter.tar
        
        # 停止现有容器
        docker stop video-converter 2>/dev/null || true
        docker rm video-converter 2>/dev/null || true
        
        # 启动新容器
        docker run -d \\
            --name video-converter \\
            -p 8000:8000 \\
            --restart unless-stopped \\
            video-converter
        
        # 清理
        rm -f /tmp/video-converter.tar
        
        echo "✅ 部署完成!"
        echo "🌐 服务地址: http://$SERVER_IP:8000"
        echo "📋 检查状态: docker logs video-converter"
"@
    
    # 保存临时脚本
    $tempScript = "deploy-temp.sh"
    $deployScript | Out-File -Encoding UTF8 $tempScript
    
    # 传输并执行
    scp -P $SSH_PORT $tempScript root@${SERVER_IP}:/tmp/
    ssh -p $SSH_PORT root@${SERVER_IP} "bash /tmp/deploy-temp.sh"
    
    # 清理
    Remove-Item $tempScript -Force
    Remove-Item video-converter.tar -Force
    
} else {
    Write-Host "🐍 选择直接Python部署" -ForegroundColor Green
    
    # 检查ssh命令是否可用
    try {
        ssh -V 2>&1 | Out-Null
    } catch {
        Write-Host "❌ SSH客户端未安装，请安装Git Bash或OpenSSH" -ForegroundColor Red
        exit 1
    }
    
    # 创建部署目录
    Write-Host "📁 创建服务器目录..." -ForegroundColor Cyan
    ssh -p $SSH_PORT root@${SERVER_IP} "mkdir -p /opt/video-converter"
    
    # 传输文件到服务器
    Write-Host "📤 传输文件到服务器..." -ForegroundColor Cyan
    # 使用Git Bash的scp或者系统scp
    $filesToTransfer = @("main.py", "requirements.txt", "Dockerfile", "cloudflare_deploy.py")
    
    foreach ($file in $filesToTransfer) {
        if (Test-Path $file) {
            scp -P $SSH_PORT $file root@${SERVER_IP}:/opt/video-converter/
        }
    }
    
    # 执行部署脚本
    Write-Host "🚀 在服务器上部署..." -ForegroundColor Cyan
    $pythonDeployScript = @"
        cd /opt/video-converter
        
        # 安装系统依赖
        echo "📦 安装系统依赖..."
        if command -v yum &> /dev/null; then
            yum install -y python3 python3-pip ffmpeg
        elif command -v apt-get &> /dev/null; then
            apt-get update && apt-get install -y python3 python3-pip ffmpeg
        else
            echo "❌ 不支持的包管理器"
            exit 1
        fi
        
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
        echo "📋 检查日志: tail -f /opt/video-converter/app.log"
"@
    
    # 保存临时脚本
    $tempScript = "python-deploy-temp.sh"
    $pythonDeployScript | Out-File -Encoding UTF8 $tempScript
    
    # 传输并执行
    scp -P $SSH_PORT $tempScript root@${SERVER_IP}:/tmp/
    ssh -p $SSH_PORT root@${SERVER_IP} "bash /tmp/python-deploy-temp.sh"
    
    # 清理
    Remove-Item $tempScript -Force
}

Write-Host ""
Write-Host "🎉 部署完成!" -ForegroundColor Green
Write-Host "📋 下一步:" -ForegroundColor Cyan
Write-Host "1. 测试服务: curl http://${SERVER_IP}:8000/health" -ForegroundColor White
Write-Host "2. 更新Cloudflare配置中的EXTERNAL_FFMPEG_SERVICE变量" -ForegroundColor White
Write-Host "3. 部署Cloudflare Workers: npm run deploy" -ForegroundColor White
Write-Host ""
Write-Host "💡 提示: 确保服务器的安全组开放了8000端口" -ForegroundColor Yellow
Write-Host "🔗 腾讯云控制台: https://console.cloud.tencent.com" -ForegroundColor Blue