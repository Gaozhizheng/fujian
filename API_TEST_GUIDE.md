# API 测试指南

## 如何在API文档页面测试视频转换功能

### 1. 访问API文档
打开浏览器，访问: http://localhost:8000/docs

### 2. 找到转换接口
- 在页面中找到 `/convert` 接口（GET方法）
- 点击该接口展开详细信息

### 3. 填写测试参数

#### 必需参数：
- **url**: 视频链接地址
  示例：
  ```
  https://lf9-bot-platform-tos-sign.coze.cn/bot-studio-bot-platform/bot_files/2162074399288379/video/quicktime/7553106305146306594/3b6bca88-0e8b-44ab-9344-bed5495ac926.mp4?lk3s=50ccb0c5&x-expires=1759199480&x-signature=lE5IXkWV1Z34D3ftvh1gonizp9Y%3D
  ```

- **filename**: 输出文件名（带.mp4扩展名）
  示例：`test_video.mp4`

### 4. 执行测试
1. 点击 "Try it out" 按钮
2. 填写参数值
3. 点击 "Execute" 按钮

### 5. 查看结果
- **成功响应 (200)**: 
  - 显示文件下载信息
  - 包含文件大小和内容类型

- **错误响应**: 
  - 显示具体的错误信息
  - 常见错误：网络连接问题、视频链接无效、FFmpeg处理失败

### 6. 其他测试接口

#### 健康检查
- 接口：`/health`
- 方法：GET
- 用途：检查服务状态

#### 服务信息
- 接口：`/info`
- 方法：GET
- 用途：获取服务信息

### 测试示例

#### 示例1：基本转换测试
```
url: https://example.com/video/sample.mp4
filename: output_video.mp4
```

#### 示例2：使用您提供的链接
```
url: https://lf9-bot-platform-tos-sign.coze.cn/bot-studio-bot-platform/bot_files/2162074399288379/video/quicktime/7553106305146306594/3b6bca88-0e8b-44ab-9344-bed5495ac926.mp4?lk3s=50ccb0c5&x-expires=1759199480&x-signature=lE5IXkWV1Z34D3ftvh1gonizp9Y%3D
filename: converted_video.mp4
```

### 注意事项
1. 确保视频链接可公开访问
2. 网络连接稳定
3. 大文件转换需要较长时间
4. 转换后的文件会保存在服务器的temp目录中