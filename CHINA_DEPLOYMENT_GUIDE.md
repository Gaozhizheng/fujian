# 🇨🇳 国内可访问部署方案

由于国际平台访问问题，以下是完全在国内可用的部署方案：

## 🚀 国内云平台推荐

### 1. **阿里云** (推荐)
- **产品**: 容器服务ACK / 函数计算FC / 轻量应用服务器
- **网址**: https://www.aliyun.com
- **优势**: 稳定可靠、文档完善、国内访问快

### 2. **腾讯云** 
- **产品**: 容器服务TKE / 云函数SCF / 轻量应用服务器
- **网址**: https://cloud.tencent.com
- **优势**: 性价比高、生态丰富

### 3. **百度智能云**
- **产品**: CCE容器引擎 / 函数计算CFC
- **网址**: https://cloud.baidu.com
- **优势**: AI能力集成

### 4. **华为云**
- **产品**: 容器引擎CCE / 函数工作流FunctionGraph
- **网址**: https://www.huaweicloud.com
- **优势**: 企业级服务

## 💻 本地部署方案

### 方案A: Docker本地部署 + 内网穿透
```bash
# 1. 本地Docker部署
docker build -t video-converter .
docker run -d -p 8000:8000 --name video-converter video-converter

# 2. 使用内网穿透工具
# 可选: frp, ngrok, ssh隧道等
```

### 方案B: 本地服务器 + 端口转发
```bash
# 在本地服务器或NAS上部署
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# 配置路由器端口转发
```

## 📋 各方案对比

| 方案 | 成本 | 难度 | 访问性 | 推荐度 |
|------|------|------|--------|--------|
| 阿里云 | 💰💰 | ⭐⭐ | ✅✅ | ⭐⭐⭐⭐⭐ |
| 腾讯云 | 💰💰 | ⭐⭐ | ✅✅ | ⭐⭐⭐⭐ |
| 本地Docker | 💰 | ⭐⭐⭐ | ⚠️ | ⭐⭐⭐ |
| 内网穿透 | 💰 | ⭐⭐⭐⭐ | ✅ | ⭐⭐ |

## 🎯 立即开始 - 阿里云部署

### 步骤1: 准备阿里云账号
1. 访问 https://www.aliyun.com
2. 注册/登录账号
3. 实名认证

### 步骤2: 选择产品
- **简单版**: 轻量应用服务器 (¥24/月起)
- **进阶版**: 容器服务ACK
- **无服务器**: 函数计算FC

### 步骤3: 部署应用

#### 轻量应用服务器部署:
```bash
# 连接到服务器
ssh root@your-server-ip

# 安装依赖
yum install -y python3 python3-pip ffmpeg

# 部署代码
cd /opt
git clone your-repo-url video-converter
cd video-converter

# 安装Python依赖
pip3 install -r requirements.txt

# 启动服务
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
```

#### 容器服务部署:
```bash
# 构建镜像
docker build -t video-converter .

# 推送到阿里云容器镜像服务
docker tag video-converter registry.cn-hangzhou.aliyuncs.com/your-namespace/video-converter
docker push registry.cn-hangzhou.aliyuncs.com/your-namespace/video-converter

# 在ACK中部署
```

## 🔧 本地快速测试

### Windows本地测试:
```powershell
# 确保FFmpeg已安装
ffmpeg -version

# 启动服务
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# 测试访问
curl http://localhost:8000/health
```

### Docker本地测试:
```powershell
# 构建镜像
docker build -t video-converter .

# 运行容器
docker run -d -p 8000:8000 --name video-converter video-converter

# 查看日志
docker logs video-converter

# 测试服务
curl http://localhost:8000/health
```

## 🌐 网络配置

### 安全组配置（云平台）:
- 开放端口: 8000 (HTTP)
- 可选: 80/443 (Nginx反向代理)
- 设置访问白名单

### 域名配置（可选）:
1. 备案域名
2. 解析到服务器IP
3. 配置SSL证书

## 💰 成本估算

### 阿里云轻量应用服务器:
- ¥24/月 (1核1G)
- ¥34/月 (1核2G) - 推荐
- ¥60/月 (2核4G)

### 腾讯云轻量应用服务器:
- ¥38/月 (1核2G)
- ¥58/月 (2核4G)

## 🛡️ 安全建议

1. **修改默认端口**: 不使用8000端口
2. **设置防火墙**: 只允许必要IP访问
3. **使用HTTPS**: 配置SSL证书
4. **定期更新**: 保持系统和依赖更新
5. **监控日志**: 设置日志监控

## 🆘 遇到问题？

### 常见问题:
1. **端口不通** - 检查安全组和防火墙
2. **FFmpeg问题** - 验证FFmpeg安装
3. **依赖问题** - 检查Python包版本
4. **权限问题** - 检查文件权限

### 获取帮助:
- 云平台文档和技术支持
- 查看服务日志
- 本地测试验证

## 🎉 下一步行动

1. **选择平台**: 阿里云或腾讯云
2. **购买服务器**: 轻量应用服务器
3. **部署应用**: 按照上述步骤
4. **测试服务**: 验证功能正常
5. **配置Cloudflare**: 更新外部服务URL

## 📞 需要具体帮助？

如果您需要我帮您：
- 具体的云平台部署步骤
- 本地Docker问题排查  
- 网络配置指导
- 或者其他特定问题

请告诉我您选择哪个方案，或者遇到的具体问题！