from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """应用运行配置。

    从系统环境变量读取 DashScope 服务所需配置。项目启动前可以先由外部工具
    将 ``.env`` 文件中的变量注入到系统环境变量中。

    :ivar dashscope_api_key: DashScope API Key。
    :ivar dashscope_uploads_url: DashScope 上传凭证接口地址。
    :ivar dashscope_video_synthesis_url: DashScope 视频合成接口地址。
    :ivar dashscope_tasks_url: DashScope 任务查询接口地址。
    :ivar dashscope_request_timeout_seconds: HTTP 请求超时时间，单位为秒。
    :ivar dashscope_poll_interval_seconds: 任务轮询间隔时间，单位为秒。
    :ivar dashscope_verify_ssl: 是否校验 HTTPS 证书。
    :ivar dashscope_watermark: 是否生成水印。
    :ivar dashscope_check_image: 是否启用图片检查。
    :ivar dashscope_generation_mode: 视频生成模式。
    """

    model_config = SettingsConfigDict(extra="ignore")

    dashscope_api_key: SecretStr = Field(validation_alias="DASHSCOPE_API_KEY")
    dashscope_uploads_url: str = Field(
        default="https://dashscope.aliyuncs.com/api/v1/uploads",
        validation_alias="DASHSCOPE_UPLOADS_URL",
    )
    dashscope_video_synthesis_url: str = Field(
        default="https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis",
        validation_alias="DASHSCOPE_VIDEO_SYNTHESIS_URL",
    )
    dashscope_tasks_url: str = Field(
        default="https://dashscope.aliyuncs.com/api/v1/tasks",
        validation_alias="DASHSCOPE_TASKS_URL",
    )
    dashscope_request_timeout_seconds: int = Field(
        default=1800,
        validation_alias="DASHSCOPE_REQUEST_TIMEOUT_SECONDS",
    )
    dashscope_poll_interval_seconds: int = Field(
        default=15,
        validation_alias="DASHSCOPE_POLL_INTERVAL_SECONDS",
    )
    dashscope_verify_ssl: bool = Field(
        default=False,
        validation_alias="DASHSCOPE_VERIFY_SSL",
    )
    dashscope_watermark: bool = Field(
        default=False,
        validation_alias="DASHSCOPE_WATERMARK",
    )
    dashscope_check_image: bool = Field(
        default=True,
        validation_alias="DASHSCOPE_CHECK_IMAGE",
    )
    dashscope_generation_mode: str = Field(
        default="wan-pro",
        validation_alias="DASHSCOPE_GENERATION_MODE",
    )

    @property
    def dashscope_api_key_value(self) -> str:
        """获取 DashScope API Key 明文值。

        :return: DashScope API Key 字符串。
        """

        return self.dashscope_api_key.get_secret_value()


@lru_cache
def get_settings() -> AppSettings:
    """获取缓存后的应用配置。

    :return: 应用配置实例。
    """

    return AppSettings()
