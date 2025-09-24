FROM python:3.11-slim

# 安装FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt ./
COPY main.py ./

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建临时目录
RUN mkdir -p temp

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]