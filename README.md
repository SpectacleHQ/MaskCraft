# MaskCraft

MaskCraft 是一个基于 PySide6 的桌面工具，用于选择一张图片和一段参考视频，并通过阿里云 DashScope `wan2.2-animate-mix` 模型创建视频生成任务。任务完成后，界面会展示 API 返回的视频链接，并支持复制或在浏览器中打开。

## 功能特性

- 图形界面选择图片素材和参考视频。
- 自动获取 DashScope 上传凭证并上传素材到临时 OSS。
- 创建异步视频生成任务并轮询任务状态。
- 在界面中展示任务日志、原始返回结果和最终视频链接。

## 环境要求

- Python 3.14 或更高版本。
- 推荐使用 `uv` 管理依赖和运行项目。
- 可用的 DashScope API Key。

## 快速开始

1. 克隆项目并进入目录。

```powershell
git clone <repository-url>
cd MaskCraft
```

2. 安装依赖。

```powershell
uv sync
```

3. 准备环境变量示例文件。

```powershell
Copy-Item .env.example .env
```

编辑 `.env`，将 `DASHSCOPE_API_KEY` 改为你自己的 DashScope API Key。`.env` 已被 `.gitignore` 忽略，不要提交真实密钥。

当前应用从系统环境变量读取配置。如果你的启动方式不会自动加载 `.env`，请先在当前终端中设置必填变量：

```powershell
$env:DASHSCOPE_API_KEY = "your_dashscope_api_key_here"
```

4. 启动应用。

```powershell
uv run maskcraft
```

也可以使用模块方式启动：

```powershell
uv run python -m maskcraft
```

## 配置说明

| 变量名 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DASHSCOPE_API_KEY` | 是 | 无 | DashScope API Key。 |
| `DASHSCOPE_UPLOADS_URL` | 否 | `https://dashscope.aliyuncs.com/api/v1/uploads` | 上传凭证接口地址。 |
| `DASHSCOPE_VIDEO_SYNTHESIS_URL` | 否 | `https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis` | 视频合成任务接口地址。 |
| `DASHSCOPE_TASKS_URL` | 否 | `https://dashscope.aliyuncs.com/api/v1/tasks` | 任务查询接口地址。 |
| `DASHSCOPE_REQUEST_TIMEOUT_SECONDS` | 否 | `1800` | HTTP 请求超时时间，单位为秒。 |
| `DASHSCOPE_POLL_INTERVAL_SECONDS` | 否 | `15` | 任务状态轮询间隔，单位为秒。 |
| `DASHSCOPE_VERIFY_SSL` | 否 | `false` | 是否校验 HTTPS 证书。 |
| `DASHSCOPE_WATERMARK` | 否 | `false` | 是否生成水印。 |
| `DASHSCOPE_CHECK_IMAGE` | 否 | `true` | 是否启用图片检查。 |
| `DASHSCOPE_GENERATION_MODE` | 否 | `wan-pro` | 视频生成模式。 |

## 使用流程

1. 启动 MaskCraft。
2. 点击“选择图片”，选择 JPG、PNG、BMP 或 WebP 图片。
3. 点击“选择视频”，选择 MP4、AVI、MOV 等参考视频。
4. 点击“开始生成”，等待素材上传、任务创建和轮询完成。
5. 任务成功后复制或打开返回的视频链接。

## 项目结构

```text
src/maskcraft/
├── __init__.py              # 包入口和公开 API
├── __main__.py              # python -m maskcraft 入口
├── config.py                # 应用配置和环境变量读取
├── dashscope_client.py      # DashScope API 封装
├── main_window.py           # PySide6 主窗口逻辑
└── ui/
    ├── main_window.ui       # Qt Designer UI 文件
    └── main_window_ui.py    # 生成后的 UI Python 文件
```

## 开发说明

- 依赖声明位于 `pyproject.toml`，锁定文件为 `uv.lock`。
- 本地虚拟环境、缓存、日志和真实 `.env` 文件不会提交到仓库。
- 修改 `main_window.ui` 后，需要重新生成对应的 `main_window_ui.py`。
