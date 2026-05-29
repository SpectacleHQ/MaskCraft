import time
from pathlib import Path
from typing import Any, Callable

import requests
import urllib3

from maskcraft.config import AppSettings, get_settings

MODEL_NAME = "wan2.2-animate-mix"


class DashScopeClientError(RuntimeError):
    """DashScope 客户端异常。

    当 DashScope 请求失败、响应结构异常或任务执行失败时抛出。
    """


class DashScopeClient:
    """DashScope 视频生成客户端。

    封装上传凭证获取、OSS 临时文件上传、视频生成任务创建和任务结果轮询。

    :param settings: 应用配置。未传入时从系统环境变量读取。
    :param session: 可复用的 HTTP 会话。未传入时创建新的 ``requests.Session``。
    """

    def __init__(
        self,
        settings: AppSettings | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """初始化 DashScope 客户端。

        :param settings: 应用配置。
        :param session: HTTP 会话。
        """

        self.settings = settings or get_settings()
        self.session = session or requests.Session()

        if not self.settings.dashscope_verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_upload_policy(self) -> dict[str, Any]:
        """获取文件上传凭证。

        :return: DashScope 返回的上传凭证数据。
        :raises DashScopeClientError: 上传凭证获取失败或响应数据异常。
        """

        response = self.session.get(
            self.settings.dashscope_uploads_url,
            headers=self._authorization_headers(),
            params={
                "action": "getPolicy",
                "model": MODEL_NAME,
            },
            timeout=self.settings.dashscope_request_timeout_seconds,
            verify=self.settings.dashscope_verify_ssl,
        )
        payload = self._parse_json_response(response, "获取上传凭证失败")

        try:
            return payload["data"]
        except KeyError as error:
            raise DashScopeClientError("上传凭证响应缺少 data 字段") from error

    def upload_file_to_oss(self, upload_policy: dict[str, Any], file_path: str | Path) -> str:
        """将本地文件上传到 DashScope 临时 OSS。

        :param upload_policy: 上传凭证数据。
        :param file_path: 待上传的本地文件路径。
        :return: 上传后的 OSS 地址。
        :raises DashScopeClientError: 文件不存在、凭证字段缺失或上传失败。
        """

        source_path = Path(file_path)
        if not source_path.is_file():
            raise DashScopeClientError(f"文件不存在: {source_path}")

        object_key = self._build_oss_object_key(upload_policy, source_path.name)

        try:
            file_fields = {
                "OSSAccessKeyId": (None, upload_policy["oss_access_key_id"]),
                "Signature": (None, upload_policy["signature"]),
                "policy": (None, upload_policy["policy"]),
                "x-oss-object-acl": (None, upload_policy["x_oss_object_acl"]),
                "x-oss-forbid-overwrite": (None, upload_policy["x_oss_forbid_overwrite"]),
                "key": (None, object_key),
                "success_action_status": (None, "200"),
            }
            upload_host = upload_policy["upload_host"]
        except KeyError as error:
            raise DashScopeClientError(f"上传凭证缺少字段: {error.args[0]}") from error

        with source_path.open("rb") as file_stream:
            files = {
                **file_fields,
                "file": (source_path.name, file_stream),
            }
            response = self.session.post(
                upload_host,
                files=files,
                timeout=self.settings.dashscope_request_timeout_seconds,
                verify=self.settings.dashscope_verify_ssl,
            )

        if response.status_code != 200:
            raise DashScopeClientError(f"上传文件失败: {response.text}")

        return f"oss://{object_key}"

    def upload_image_and_video(self, image_path: str | Path, video_path: str | Path) -> tuple[str, str]:
        """上传图片和视频并返回 OSS 地址。

        :param image_path: 本地图片路径。
        :param video_path: 本地视频路径。
        :return: 图片 OSS 地址和视频 OSS 地址。
        """

        upload_policy = self.get_upload_policy()
        image_url = self.upload_file_to_oss(upload_policy, image_path)
        video_url = self.upload_file_to_oss(upload_policy, video_path)
        return image_url, video_url

    def create_video_synthesis_task(self, image_url: str, video_url: str) -> str:
        """创建视频合成任务。

        :param image_url: 图片 OSS 地址。
        :param video_url: 视频 OSS 地址。
        :return: DashScope 异步任务 ID。
        :raises DashScopeClientError: 任务创建失败或响应数据异常。
        """

        response = self.session.post(
            self.settings.dashscope_video_synthesis_url,
            headers={
                **self._authorization_headers(),
                "Content-Type": "application/json",
                "X-DashScope-Async": "enable",
                "X-DashScope-OssResourceResolve": "enable",
            },
            json={
                "model": MODEL_NAME,
                "input": {
                    "image_url": image_url,
                    "video_url": video_url,
                    "watermark": self.settings.dashscope_watermark,
                },
                "parameters": {
                    "check_image": self.settings.dashscope_check_image,
                    "mode": self.settings.dashscope_generation_mode,
                },
            },
            timeout=self.settings.dashscope_request_timeout_seconds,
            verify=self.settings.dashscope_verify_ssl,
        )
        payload = self._parse_json_response(response, "创建视频合成任务失败")

        try:
            return payload["output"]["task_id"]
        except KeyError as error:
            raise DashScopeClientError("视频合成任务响应缺少 task_id 字段") from error

    def start_video_synthesis(self, image_path: str | Path, video_path: str | Path) -> str:
        """上传素材并启动视频合成任务。

        :param image_path: 本地图片路径。
        :param video_path: 本地视频路径。
        :return: DashScope 异步任务 ID。
        """

        image_url, video_url = self.upload_image_and_video(image_path, video_path)
        return self.create_video_synthesis_task(image_url, video_url)

    def wait_for_task_result(self, task_id: str, status_callback: Callable[[str], None] | None = None) -> Any:
        """轮询任务状态并返回成功结果。

        :param task_id: DashScope 异步任务 ID。
        :param status_callback: 任务状态回调函数。
        :return: DashScope 任务成功后的结果数据。
        :raises DashScopeClientError: 任务查询失败、任务失败或响应数据异常。
        """

        task_url = f"{self.settings.dashscope_tasks_url}/{task_id}"

        while True:
            response = self.session.get(
                task_url,
                headers=self._authorization_headers(),
                timeout=self.settings.dashscope_request_timeout_seconds,
                verify=self.settings.dashscope_verify_ssl,
            )
            payload = self._parse_json_response(response, "查询任务结果失败")

            try:
                output = payload["output"]
                task_status = output["task_status"]
            except KeyError as error:
                raise DashScopeClientError("任务查询响应缺少 output.task_status 字段") from error

            match task_status:
                case "PENDING":
                    self._emit_status("任务排队中", status_callback)
                case "RUNNING":
                    self._emit_status("任务处理中", status_callback)
                case "SUCCEEDED":
                    self._emit_status("任务成功", status_callback)
                    return output.get("results")
                case _:
                    raise DashScopeClientError(f"任务执行失败: {payload}")

            time.sleep(self.settings.dashscope_poll_interval_seconds)

    def _authorization_headers(self) -> dict[str, str]:
        """生成 DashScope 授权请求头。

        :return: 包含 Bearer Token 的请求头。
        """

        return {
            "Authorization": f"Bearer {self.settings.dashscope_api_key_value}",
        }

    def _emit_status(self, message: str, status_callback: Callable[[str], None] | None) -> None:
        """发送任务状态消息。

        :param message: 状态消息。
        :param status_callback: 状态回调函数。
        """

        if status_callback is None:
            print(message)
            return

        status_callback(message)

    def _parse_json_response(self, response: requests.Response, error_message: str) -> dict[str, Any]:
        """解析 HTTP JSON 响应。

        :param response: HTTP 响应对象。
        :param error_message: 请求失败时使用的错误描述。
        :return: JSON 字典响应。
        :raises DashScopeClientError: 状态码异常或响应不是 JSON 字典。
        """

        if not response.ok:
            raise DashScopeClientError(f"{error_message}: {response.text}")

        try:
            payload = response.json()
        except ValueError as error:
            raise DashScopeClientError(f"{error_message}: 响应不是合法 JSON") from error

        if not isinstance(payload, dict):
            raise DashScopeClientError(f"{error_message}: 响应不是 JSON 对象")

        return payload

    def _build_oss_object_key(self, upload_policy: dict[str, Any], file_name: str) -> str:
        """构建 OSS 对象路径。

        :param upload_policy: 上传凭证数据。
        :param file_name: 本地文件名。
        :return: OSS 对象路径。
        :raises DashScopeClientError: 上传凭证缺少上传目录字段。
        """

        try:
            upload_dir = upload_policy["upload_dir"]
        except KeyError as error:
            raise DashScopeClientError("上传凭证缺少 upload_dir 字段") from error

        return f"{upload_dir}/{file_name}"
