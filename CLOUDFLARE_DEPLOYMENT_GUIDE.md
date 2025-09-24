# Cloudflare Workers 部署指南

## 部署方案选择

### 方案1: Cloudflare Workers + 外部FFmpeg服务（推荐）
- **优点**: 利用Cloudflare的全球网络，响应快
- **缺点**: 需要单独部署FFmpeg服务
- **文件**: `src/worker.ts`, `wrangler.toml`, `package.json`

### 方案2: 纯Python部署（需要支持FFmpeg的平台）
- **优点**: 代码无需大改
- **缺点**: 需要找到支持FFmpeg的云平台
- **文件**: `cloudflare_deploy.py`

## 部署步骤 - 方案1（推荐）

### 1. 安装必要工具
```bash
# 安装Node.js和npm
# 然后安装Wrangler (Cloudflare CLI)
npm install -g wrangler

# 登录Cloudflare
wrangler login
```

### 2. 安装项目依赖
```bash
npm install
```

### 3. 配置环境变量
编辑 `wrangler.toml` 文件：
```toml
[vars]
EXTERNAL_FFMPEG_SERVICE = "https://your-actual-ffmpeg-service.com/convert"
```

### 4. 部署到Cloudflare
```bash
# 测试部署
wrangler dev

# 正式部署
wrangler deploy
```

### 5. 配置自定义域名（可选）
在Cloudflare Dashboard中配置您的域名路由。

## 外部FFmpeg服务部署

您需要部署一个支持FFmpeg的服务，可以选择：

### 选项A: VPS/云服务器
- AWS EC2
- DigitalOcean Droplet
- Vultr VPS
- 阿里云/腾讯云服务器

### 选项B: 容器平台
- Docker + 任何支持容器的平台
- Kubernetes
- Railway
- Render

### 选项C: 无服务器平台（支持FFmpeg的）
- AWS Lambda with EFS
- Google Cloud Run
- Azure Container Instances

## HTTP调用示例

部署成功后，您可以通过以下方式调用：

### 1. 直接HTTP请求
```bash
# 健康检查
curl https://your-worker.workers.dev/health

# 转换视频
curl "https://your-worker.workers.dev/convert?url=https://example.com/video.mp4&filename=output.mp4"
```

### 2. Python客户端
```python
import requests

# 配置端点
endpoint = "https://your-worker.workers.dev"

# 健康检查
response = requests.get(f"{endpoint}/health")
print(response.json())

# 转换视频
params = {
    "url": "https://example.com/video.mp4",
    "filename": "my_video.mp4"
}
response = requests.get(f"{endpoint}/convert", params=params)
print(response.json())
```

### 3. JavaScript客户端
```javascript
// 健康检查
fetch('https://your-worker.workers.dev/health')
  .then(response => response.json())
  .then(data => console.log(data));

// 转换视频
const params = new URLSearchParams({
  url: 'https://example.com/video.mp4',
  filename: 'output.mp4'
});

fetch(`https://your-worker.workers.dev/convert?${params}`)
  .then(response => response.json())
  .then(data => console.log(data));
```

## 环境变量配置

### 必需的环境变量
- `EXTERNAL_FFMPEG_SERVICE`: 外部FFmpeg服务的URL

### 可选的环境变量
- `API_KEY`: 用于身份验证（如果需要）
- `RATE_LIMIT`: 请求频率限制

## 监控和日志

### 查看日志
```bash
wrangler tail
```

### 性能监控
- 使用Cloudflare Dashboard监控请求量
- 设置警报规则
- 查看错误率和响应时间

## 安全考虑

1. **API密钥验证**: 为外部FFmpeg服务添加身份验证
2. **速率限制**: 防止滥用
3. **输入验证**: 验证URL格式和文件类型
4. **CORS配置**: 根据需要配置跨域请求

## 故障排除

### 常见问题
1. **构建失败**: 检查Node.js版本和依赖
2. **部署失败**: 检查wrangler配置和权限
3. **运行时错误**: 查看日志 `wrangler tail`
4. **外部服务连接失败**: 检查网络连接和URL配置

### 调试命令
```bash
# 本地测试
wrangler dev

# 查看部署状态
wrangler whoami

# 查看日志
wrangler tail

# 更新环境变量
wrangler secret put EXTERNAL_FFMPEG_SERVICE
```

## 成本估算

- **Cloudflare Workers**: 免费套餐包含10万次请求/天
- **外部FFmpeg服务**: 根据使用的云平台定价
- **带宽费用**: 根据视频大小和请求量计算

## 下一步

1. 部署外部FFmpeg服务
2. 配置环境变量
3. 测试部署
4. 配置自定义域名
5. 设置监控和警报

## 支持

如果遇到问题，请参考：
- [Cloudflare Workers文档](https://developers.cloudflare.com/workers/)
- [Wrangler CLI文档](https://developers.cloudflare.com/workers/wrangler/)
- [外部FFmpeg服务部署指南](FFMPEG_SERVICE_DEPLOYMENT.md)