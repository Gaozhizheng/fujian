# FFmpeg Windows安装脚本
# 运行方法: 右键点击 -> "使用PowerShell运行"

Write-Host "🚀 开始安装FFmpeg..." -ForegroundColor Green
Write-Host "=" * 50

# 创建ffmpeg目录
$ffmpegDir = "$PWD\ffmpeg"
if (-not (Test-Path $ffmpegDir)) {
    New-Item -ItemType Directory -Path $ffmpegDir | Out-Null
    Write-Host "✅ 创建ffmpeg目录: $ffmpegDir" -ForegroundColor Green
}

# 下载FFmpeg
Write-Host "📥 下载FFmpeg..." -ForegroundColor Yellow
$downloadUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
$zipFile = "$ffmpegDir\ffmpeg.zip"

try {
    # 使用Invoke-WebRequest下载
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipFile
    Write-Host "✅ FFmpeg下载完成" -ForegroundColor Green
} catch {
    Write-Host "❌ 下载失败，请手动下载:" -ForegroundColor Red
    Write-Host "   1. 访问: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    Write-Host "   2. 选择Windows版本下载" -ForegroundColor Yellow
    Write-Host "   3. 解压到当前目录的ffmpeg文件夹中" -ForegroundColor Yellow
    exit 1
}

# 解压文件
Write-Host "📦 解压FFmpeg..." -ForegroundColor Yellow
try {
    Expand-Archive -Path $zipFile -DestinationPath $ffmpegDir -Force
    Write-Host "✅ 解压完成" -ForegroundColor Green
} catch {
    Write-Host "❌ 解压失败，请手动解压" -ForegroundColor Red
    exit 1
}

# 查找ffmpeg.exe
$ffmpegExe = Get-ChildItem -Path $ffmpegDir -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
if ($ffmpegExe) {
    # 复制到项目目录
    Copy-Item -Path $ffmpegExe.FullName -Destination "$PWD\ffmpeg.exe" -Force
    Write-Host "✅ FFmpeg已安装到: $PWD\ffmpeg.exe" -ForegroundColor Green
    
    # 测试FFmpeg
    Write-Host "🧪 测试FFmpeg..." -ForegroundColor Yellow
    $version = & "$PWD\ffmpeg.exe" -version 2>&1 | Select-String "ffmpeg version"
    if ($version) {
        Write-Host "✅ FFmpeg测试成功: $version" -ForegroundColor Green
    } else {
        Write-Host "⚠️  FFmpeg测试异常" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ 未找到ffmpeg.exe，请手动安装" -ForegroundColor Red
}

# 清理
Remove-Item $zipFile -Force -ErrorAction SilentlyContinue

Write-Host "=" * 50
Write-Host "🎉 FFmpeg安装完成!" -ForegroundColor Green
Write-Host "📝 下一步:" -ForegroundColor Yellow
Write-Host "   1. 服务将自动使用当前目录的ffmpeg.exe" -ForegroundColor Cyan
Write-Host "   2. 您现在可以测试视频转换功能了" -ForegroundColor Cyan
Write-Host "   3. 访问 http://localhost:8000/docs 进行测试" -ForegroundColor Cyan

pause