# FFmpeg服务部署指南

## 部署方案选择

### 🐳 方案A: Docker部署（推荐）
**支持平台**: 任何支持Docker的平台
- AWS ECS/EKS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Railway
- Render
- Heroku (with Docker)

### 🚀 方案B: 传统VPS部署
**支持平台**: 任何云服务器
- AWS EC2
- DigitalOcean Droplet
- Vultr VPS
- 阿里云/腾讯云服务器

### ☁️ 方案C: 无服务器部署（有限制）
**注意**: 大多数无服务器平台对FFmpeg支持有限

## 快速开始 - Docker部署

### 1. 本地测试
```bash
# 构建Docker镜像
docker build -t ffmpeg-video-converter .

# 运行容器
docker run -d -p 8000:8000 --name video-converter ffmpeg-video-converter

# 测试服务
curl http://localhost:8000/health
```

### 2. 部署到云平台

#### Railway (推荐)
1. 访问 https://railway.app/
2. 连接GitHub仓库
3. 选择此项目
4. 自动部署

#### Render
1. 访问 https://render.com/
2. 创建Web Service
3. 连接GitHub
4. 选择Docker部署

#### Heroku
```bash
# 安装Heroku CLI
heroku create your-app-name
heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
heroku buildpacks:add heroku/python
git push heroku main
```

## VPS服务器部署

### 1. 准备服务器
```bash
# 连接到您的VPS
ssh user@your-server-ip

# 安装必要软件
sudo apt update
sudo apt install -y python3-pip python3-venv ffmpeg

# 创建项目目录
mkdir -p ~/video-converter
cd ~/video-converter
```

### 2. 部署代码
```bash
# 上传代码或使用Git
git clone your-repo-url .

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建临时目录
mkdir -p temp
```

### 3. 配置服务
```bash
# 创建systemd服务
sudo tee /etc/systemd/system/video-converter.service > /dev/null <<EOF
[Unit]
Description=Video Converter Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/video-converter
ExecStart=/home/ubuntu/video-converter/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
sudo systemctl daemon-reload
sudo systemctl enable video-converter
sudo systemctl start video-converter

# 检查状态
sudo systemctl status video-converter
```

### 4. 配置Nginx（可选）
```bash
# 安装Nginx
sudo apt install -y nginx

# 创建Nginx配置
sudo tee /etc/nginx/sites-available/video-converter > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# 启用配置
sudo ln -s /etc/nginx/sites-available/video-converter /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 环境配置

### 必需配置
在部署后，设置外部服务URL：

```bash
# 对于Cloudflare Workers，更新wrangler.toml
[vars]
EXTERNAL_FFMPEG_SERVICE = "https://your-deployed-service.com"
```

### 可选配置
```python
# 环境变量支持
import os

# 最大文件大小（字节）
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "100000000"))  # 100MB

# 超时设置（秒）
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "30"))
CONVERT_TIMEOUT = int(os.getenv("CONVERT_TIMEOUT", "300"))

# 身份验证
API_KEY = os.getenv("API_KEY", "")
```

## 平台特定指南

### AWS部署
```bash
# 使用ECS
aws ecr create-repository --repository-name video-converter
aws ecr get-login-password | docker login --username AWS --password-stdin your-account-id.dkr.ecr.region.amazonaws.com

docker tag ffmpeg-video-converter:latest your-account-id.dkr.ecr.region.amazonaws.com/video-converter:latest
docker push your-account-id.dkr.ecr.region.amazonaws.com/video-converter:latest
```

### Google Cloud Run
```bash
# 构建和部署
gcloud builds submit --tag gcr.io/your-project-id/video-converter
gcloud run deploy video-converter --image gcr.io/your-project-id/video-converter --platform managed
```

### DigitalOcean App Platform
1. 创建App
2. 选择GitHub仓库
3. 配置Docker部署
4. 设置环境变量

## 监控和维护

### 日志查看
```bash
# Docker日志
docker logs video-converter

# Systemd日志
sudo journalctl -u video-converter -f

# 实时日志
tail -f /var/log/your-service.log
```

### 性能监控
- 设置监控警报
- 监控CPU和内存使用
- 设置自动扩展（如果平台支持）

### 备份策略
- 定期备份重要配置
- 设置日志轮转
- 监控磁盘空间

## 安全考虑

1. **防火墙配置**: 只开放必要端口
2. **SSL证书**: 启用HTTPS
3. **访问控制**: 设置身份验证
4. **速率限制**: 防止滥用
5. **输入验证**: 验证所有输入参数

## 故障排除

### 常见问题

1. **FFmpeg未找到**
   ```bash
   # 检查FFmpeg安装
   ffmpeg -version
   
   # 安装FFmpeg
   sudo apt install -y ffmpeg
   ```

2. **权限问题**
   ```bash
   # 检查目录权限
   ls -la temp/
   
   # 修复权限
   chmod 755 temp/
   chown www-data:www-data temp/  # 对于Web服务器用户
   ```

3. **内存不足**
   - 增加服务器内存
   - 优化FFmpeg参数
   - 设置文件大小限制

4. **网络问题**
   - 检查防火墙设置
   - 验证网络连接
   - 检查DNS解析

### 调试命令

```bash
# 检查服务状态
sudo systemctl status video-converter

# 查看日志
sudo journalctl -u video-converter --since "1 hour ago"

# 测试端点
curl http://localhost:8000/health
curl "http://localhost:8000/convert?url=https://example.com/video.mp4"

# 检查端口占用
netstat -tlnp | grep :8000

# 检查进程
ps aux | grep uvicorn
```

## 成本优化

1. **选择合适的实例类型**: 根据负载选择
2. **使用spot实例**: 对于非关键任务
3. **设置自动扩展**: 根据负载动态调整
4. **监控使用量**: 避免不必要的资源浪费
5. **使用CDN**: 优化文件分发

## 支持

如果遇到问题：
1. 检查日志文件
2. 验证FFmpeg安装
3. 测试网络连接
4. 查看平台文档

## 下一步

1. 选择部署平台
2. 部署FFmpeg服务
3. 测试服务功能
4. 更新Cloudflare配置
5. 进行端到端测试