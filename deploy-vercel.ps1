# Vercel免费部署脚本 - PowerShell版本

Write-Host "🚀 Vercel免费部署脚本" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green

Write-Host "📋 Vercel免费层优势:" -ForegroundColor Cyan
Write-Host "✅ 完全免费，无需信用卡" -ForegroundColor Green
Write-Host "✅ 100GB带宽/月" -ForegroundColor Green  
Write-Host "✅ 全球CDN加速" -ForegroundColor Green
Write-Host "✅ 国内访问友好" -ForegroundColor Green
Write-Host "✅ 自动SSL证书" -ForegroundColor Green
Write-Host ""

# 检查必要文件
Write-Host "🔍 检查部署文件..." -ForegroundColor Cyan
$requiredFiles = @("vercel.json", "cloudflare_deploy.py", "requirements.txt")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ 找到 $file" -ForegroundColor Green
    } else {
        Write-Host "❌ 未找到 $file" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# 部署选项
Write-Host "📝 选择部署方式:" -ForegroundColor Cyan
Write-Host "1. Vercel CLI部署 (推荐)" -ForegroundColor Yellow
Write-Host "2. GitHub集成部署" -ForegroundColor Yellow
Write-Host "3. Vercel网页端部署" -ForegroundColor Yellow
$deployChoice = Read-Host "请选择 (1/2/3)"

Write-Host ""

switch ($deployChoice) {
    "1" {
        Write-Host "🖥️ 选择Vercel CLI部署" -ForegroundColor Green
        
        # 检查Node.js和npm
        try {
            node --version | Out-Null
            npm --version | Out-Null
        } catch {
            Write-Host "❌ 需要安装Node.js和npm" -ForegroundColor Red
            Write-Host "📥 下载: https://nodejs.org/" -ForegroundColor Yellow
            exit 1
        }
        
        # 安装Vercel CLI
        Write-Host "📦 安装Vercel CLI..." -ForegroundColor Cyan
        npm install -g vercel
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Vercel安装失败" -ForegroundColor Red
            exit 1
        }
        
        # 登录Vercel
        Write-Host "🔐 登录Vercel..." -ForegroundColor Cyan
        Write-Host "💡 请在浏览器中完成登录授权" -ForegroundColor Yellow
        vercel login
        
        # 部署
        Write-Host "🚀 开始部署到Vercel..." -ForegroundColor Cyan
        $deployResult = vercel --prod
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "🎉 部署成功!" -ForegroundColor Green
            Write-Host "🌐 服务地址: $deployResult" -ForegroundColor White
            
            # 更新Cloudflare配置
            Write-Host ""
            Write-Host "📝 更新Cloudflare配置:" -ForegroundColor Cyan
            Write-Host "请将 wrangler.toml 中的 EXTERNAL_FFMPEG_SERVICE 更新为:" -ForegroundColor White
            Write-Host "EXTERNAL_FFMPEG_SERVICE = \"$deployResult/convert\"" -ForegroundColor Yellow
        } else {
            Write-Host "❌ 部署失败" -ForegroundColor Red
        }
    }
    
    "2" {
        Write-Host "🐙 选择GitHub集成部署" -ForegroundColor Green
        
        Write-Host "📋 步骤:" -ForegroundColor Cyan
        Write-Host "1. 创建GitHub仓库" -ForegroundColor White
        Write-Host "2. 推送代码到GitHub" -ForegroundColor White
        Write-Host "3. 在Vercel中连接GitHub仓库" -ForegroundColor White
        Write-Host "4. 自动部署" -ForegroundColor White
        Write-Host ""
        
        Write-Host "🔗 Vercel控制台: https://vercel.com/new" -ForegroundColor Blue
        Write-Host "🔗 GitHub: https://github.com/new" -ForegroundColor Blue
    }
    
    "3" {
        Write-Host "🌐 选择网页端部署" -ForegroundColor Green
        
        Write-Host "📋 步骤:" -ForegroundColor Cyan
        Write-Host "1. 访问 https://vercel.com" -ForegroundColor White
        Write-Host "2. 注册/登录账号" -ForegroundColor White
        Write-Host "3. 点击'New Project'" -ForegroundColor White
        Write-Host "4. 导入Git仓库或拖拽文件" -ForegroundColor White
        Write-Host "5. 配置部署" -ForegroundColor White
        Write-Host ""
        
        Write-Host "🔗 立即开始: https://vercel.com/new" -ForegroundColor Blue
    }
    
    default {
        Write-Host "❌ 无效选择" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎯 下一步行动:" -ForegroundColor Cyan
Write-Host "1. 测试部署的服务" -ForegroundColor White
Write-Host "2. 更新Cloudflare Workers配置" -ForegroundColor White
Write-Host "3. 部署Cloudflare Workers" -ForegroundColor White
Write-Host ""

Write-Host "🧪 测试命令:" -ForegroundColor Cyan
Write-Host "curl https://your-app.vercel.app/health" -ForegroundColor White
Write-Host "curl https://your-app.vercel.app/info" -ForegroundColor White
Write-Host ""

Write-Host "🔧 Cloudflare部署:" -ForegroundColor Cyan
Write-Host "npm run deploy" -ForegroundColor White
Write-Host ""

Write-Host "💡 提示:" -ForegroundColor Yellow
Write-Host "• Vercel完全免费，适合个人项目" -ForegroundColor White
Write-Host "• 国内访问速度良好" -ForegroundColor White
Write-Host "• 自动HTTPS和CDN" -ForegroundColor White
Write-Host "• 无需服务器维护" -ForegroundColor White