# 🆓 完全免费云平台部署方案

针对您的需求，以下是多个完全免费的云平台部署方案：

## 🌟 推荐免费方案

### 方案一：Vercel + Cloudflare Workers（最佳组合）
**完全免费** | **无需信用卡** | **国内访问友好**

#### Vercel 优势：
- 🆓 永远免费层
- ⚡ 自动全球CDN
- 🔧 简单Git集成
- 🌐 国内访问较快

#### 部署步骤：
```bash
# 1. 安装Vercel CLI
npm i -g vercel

# 2. 登录Vercel
vercel login

# 3. 部署到Vercel
vercel --prod

# 4. 获取部署URL（类似：https://your-app.vercel.app）
```

### 方案二：Netlify Functions + Cloudflare Workers
**免费** | **100GB带宽/月** | **简单易用**

#### Netlify 优势：
- 🆓 125k函数调用/月
- 📦 自动构建部署
- 🔗 自定义域名
- 📊 详细监控

### 方案三：GitHub Pages + Cloudflare Workers  
**完全免费** | **GitHub集成** | **开发者友好**

## 🚀 立即开始 - Vercel免费部署

### 步骤1: 准备Vercel账号
1. 访问 https://vercel.com
2. 使用GitHub账号登录
3. **无需信用卡**

### 步骤2: 创建部署配置
创建 `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "cloudflare_deploy.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/cloudflare_deploy.py"
    }
  ],
  "functions": {
    "cloudflare_deploy.py": {
      "maxDuration": 30
    }
  }
}
```

### 步骤3: 环境变量配置
在Vercel控制台设置：
- `EXTERNAL_FFMPEG_SERVICE`: 您的服务URL
- `FFMPEG_ENABLED`: `true`

### 步骤4: 一键部署
```bash
# 部署到Vercel
vercel --prod

# 或通过GitHub自动部署
 git push origin main
```

## 📦 免费容器平台方案

### 方案四: Railway (免费额度)
**每月5美元免费额度** | **简单部署**

```bash
# 安装Railway CLI
npm i -g @railway/cli

# 登录并部署
railway login
railway link
railway deploy
```

### 方案五: Render (免费Web服务)
**免费静态网站** | **简单配置**

创建 `render.yaml`:
```yaml
services:
  - type: web
    name: video-converter
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn cloudflare_deploy:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: EXTERNAL_FFMPEG_SERVICE
        value: https://your-ffmpeg-service.com
```

## 🔧 配置Cloudflare Workers使用免费服务

### 更新 wrangler.toml:
```toml
[vars]
EXTERNAL_FFMPEG_SERVICE = "https://your-vercel-app.vercel.app/convert"
```

### 或者使用多个环境:
```toml
[env.production.vars]
EXTERNAL_FFMPEG_SERVICE = "https://production-app.vercel.app/convert"

[env.staging.vars]  
EXTERNAL_FFMPEG_SERVICE = "https://staging-app.vercel.app/convert"
```

## 💰 免费额度详情

### Vercel 免费层:
- ✅ 无限个人项目
- ✅ 100GB带宽/月  
- ✅ 无限部署
- ✅ 自动SSL证书
- ✅ 全球CDN

### Netlify 免费层:
- ✅ 100GB带宽/月
- ✅ 300分钟构建时间/月
- ✅ 125k函数调用/月

### GitHub Pages:
- ✅ 完全免费
- ✅ 自定义域名
- ✅ 自动SSL

## 🛠️ 本地开发与测试

### 使用本地服务测试:
```bash
# 启动本地服务（您已经在运行）
uvicorn main:app --host 0.0.0.0 --port 8000

# 测试转换功能
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{"video_url":"https://example.com/video.mp4"}'
```

### 更新本地测试配置:
```toml
# 在 wrangler.toml 中添加开发环境
[env.development.vars]
EXTERNAL_FFMPEG_SERVICE = "http://localhost:8000/convert"
```

## 📊 免费方案对比

| 平台 | 免费额度 | 带宽 | 函数调用 | 易用性 | 推荐度 |
|------|---------|------|----------|--------|--------|
| Vercel | ⭐⭐⭐⭐⭐ | 100GB | 无限 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Netlify | ⭐⭐⭐⭐ | 100GB | 125k | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GitHub Pages | ⭐⭐⭐⭐ | 100GB | - | ⭐⭐⭐ | ⭐⭐⭐ |
| Railway | ⭐⭐⭐ | $5/月 | - | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Render | ⭐⭐ | 有限 | - | ⭐⭐⭐ | ⭐⭐ |

## 🚨 重要注意事项

1. **流量限制**: 免费层有带宽限制，适合中小流量
2. **超时限制**: 函数执行有时间限制（通常10-30秒）
3. **冷启动**: 免费服务可能有冷启动延迟
4. **监控报警**: 设置使用量提醒

## 🎯 推荐部署流程

1. **首选**: Vercel + Cloudflare Workers
2. **备选**: Netlify + Cloudflare Workers  
3. **测试**: 本地开发环境

## 🔍 验证部署

部署后验证服务：

```bash
# 健康检查
curl https://your-app.vercel.app/health

# 服务信息
curl https://your-app.vercel.app/info

# 测试转换（小文件）
curl -X POST https://your-app.vercel.app/convert \
  -H "Content-Type: application/json" \
  -d '{"video_url":"https://small-video.com/sample.mp4"}'
```

## 📝 下一步行动

1. **立即注册** Vercel 账号
2. **安装** Vercel CLI
3. **部署** 到Vercel
4. **测试** 服务功能
5. **更新** Cloudflare 配置

## 🆘 需要帮助？

如果您在部署过程中遇到任何问题：

1. 检查服务日志
2. 验证环境变量
3. 测试本地功能
4. 查看平台文档

选择Vercel开始免费部署吧！ 🚀