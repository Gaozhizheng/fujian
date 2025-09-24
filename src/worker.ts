// Cloudflare Workers入口文件
import { Router } from 'itty-router'

// 创建路由器
const router = Router()

// 环境变量接口
interface Env {
  EXTERNAL_FFMPEG_SERVICE: string
}

// 根路径
router.get('/', () => {
  return Response.json({
    message: "视频链接转MP4服务 (Cloudflare Workers版本)",
    note: "此版本需要外部FFmpeg服务支持",
    endpoints: {
      convert: "/convert?url=视频链接",
      health: "/health",
      info: "/info"
    }
  })
})

// 健康检查
router.get('/health', () => {
  return Response.json({ status: "healthy", platform: "cloudflare" })
})

// 服务信息
router.get('/info', (request, env: Env) => {
  return Response.json({
    service: "video-converter",
    version: "1.0.0",
    platform: "cloudflare-workers",
    external_ffmpeg_service: env.EXTERNAL_FFMPEG_SERVICE
  })
})

// 视频转换接口
router.get('/convert', async (request, env: Env) => {
  const url = new URL(request.url)
  const videoUrl = url.searchParams.get('url')
  const filename = url.searchParams.get('filename') || 'converted_video.mp4'

  if (!videoUrl) {
    return Response.json(
      { error: "URL参数不能为空" },
      { status: 400 }
    )
  }

  try {
    // 调用外部FFmpeg服务
    const response = await fetch(env.EXTERNAL_FFMPEG_SERVICE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: videoUrl,
        filename: filename
      })
    })

    if (response.ok) {
      const data = await response.json()
      return Response.json({
        status: "success",
        message: "转换请求已提交",
        job_id: data.job_id,
        download_url: `${env.EXTERNAL_FFMPEG_SERVICE}/download/${data.job_id}`
      })
    } else {
      return Response.json(
        { error: `外部服务错误: ${await response.text()}` },
        { status: response.status }
      )
    }

  } catch (error) {
    return Response.json(
      { error: `服务调用失败: ${error.message}` },
      { status: 502 }
    )
  }
})

// 404处理
router.all('*', () => {
  return Response.json(
    { error: "路由未找到" },
    { status: 404 }
  )
})

// Workers入口点
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    return router.handle(request, env, ctx)
  }
}