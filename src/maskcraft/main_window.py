import json
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, QThread, QUrl, Signal, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from maskcraft.dashscope_client import DashScopeClient
from maskcraft.ui.main_window_ui import Ui_MainWindow


class VideoGenerationWorker(QObject):
    """视频生成后台任务。

    在独立线程中调用 DashScope API，避免界面在上传和轮询期间失去响应。

    :param image_path: 本地图片路径。
    :param video_path: 本地视频路径。
    """

    status_changed = Signal(str)
    finished = Signal(str, object)
    failed = Signal(str)

    def __init__(self, image_path: Path, video_path: Path) -> None:
        """初始化后台任务。

        :param image_path: 本地图片路径。
        :param video_path: 本地视频路径。
        """

        super().__init__()
        self.image_path = image_path
        self.video_path = video_path

    @Slot()
    def run(self) -> None:
        """执行视频生成任务。

        上传素材、创建异步任务并等待 API 返回最终结果。
        """

        try:
            client = DashScopeClient()
            self.status_changed.emit("正在上传素材")
            task_id = client.start_video_synthesis(self.image_path, self.video_path)
            self.status_changed.emit(f"任务已创建: {task_id}")
            result = client.wait_for_task_result(task_id, self.status_changed.emit)
            video_url = extract_video_url(result)
            self.finished.emit(video_url, result)
        except Exception as error:
            self.failed.emit(str(error))


class MainWindow(QMainWindow, Ui_MainWindow):
    """MaskCraft 主窗口。

    提供图片和视频选择、任务提交、状态反馈以及结果链接复制和打开能力。
    """

    def __init__(self) -> None:
        """初始化主窗口并设置默认状态。"""

        super().__init__()
        self.setupUi(self)

        self._worker_thread: QThread | None = None
        self._generation_worker: VideoGenerationWorker | None = None
        self._set_busy(False)

    @Slot()
    def on_selectImageButton_clicked(self) -> None:
        """响应选择图片按钮点击事件。"""

        image_path = self._select_file(
            "选择图片",
            "图片文件 (*.jpg *.jpeg *.png *.webp *.bmp);;所有文件 (*.*)",
        )
        if image_path:
            self.imagePathLineEdit.setText(str(image_path))
            self._append_log(f"已选择图片: {image_path}")
            self._refresh_ready_state()

    @Slot()
    def on_selectVideoButton_clicked(self) -> None:
        """响应选择视频按钮点击事件。"""

        video_path = self._select_file(
            "选择视频",
            "视频文件 (*.mp4 *.mov *.m4v *.avi *.mkv);;所有文件 (*.*)",
        )
        if video_path:
            self.videoPathLineEdit.setText(str(video_path))
            self._append_log(f"已选择视频: {video_path}")
            self._refresh_ready_state()

    @Slot()
    def on_generateButton_clicked(self) -> None:
        """响应开始生成按钮点击事件。"""

        image_path = Path(self.imagePathLineEdit.text().strip())
        video_path = Path(self.videoPathLineEdit.text().strip())

        if not image_path.is_file() or not video_path.is_file():
            QMessageBox.warning(self, "素材不完整", "请先选择有效的图片和视频文件。")
            return

        self.resultUrlLineEdit.clear()
        self.copyResultButton.setEnabled(False)
        self.openResultButton.setEnabled(False)
        self._set_busy(True)
        self._append_log("开始创建生成任务")

        self._worker_thread = QThread(self)
        self._generation_worker = VideoGenerationWorker(image_path, video_path)
        self._generation_worker.moveToThread(self._worker_thread)

        self._worker_thread.started.connect(self._generation_worker.run)
        self._generation_worker.status_changed.connect(self._handle_status_changed)
        self._generation_worker.finished.connect(self._handle_generation_finished)
        self._generation_worker.failed.connect(self._handle_generation_failed)
        self._generation_worker.finished.connect(self._worker_thread.quit)
        self._generation_worker.failed.connect(self._worker_thread.quit)
        self._worker_thread.finished.connect(self._generation_worker.deleteLater)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)
        self._worker_thread.finished.connect(self._clear_worker_refs)
        self._worker_thread.start()

    @Slot()
    def on_copyResultButton_clicked(self) -> None:
        """响应复制链接按钮点击事件。"""

        video_url = self.resultUrlLineEdit.text().strip()
        if video_url:
            QApplication.clipboard().setText(video_url)
            self._handle_status_changed("视频链接已复制")

    @Slot()
    def on_openResultButton_clicked(self) -> None:
        """响应打开链接按钮点击事件。"""

        video_url = self.resultUrlLineEdit.text().strip()
        if video_url:
            QDesktopServices.openUrl(QUrl(video_url))

    @Slot(str)
    def _handle_status_changed(self, message: str) -> None:
        """处理后台任务状态变化。

        :param message: 状态消息。
        """

        self.statusLabel.setText(message)
        self._append_log(message)

    @Slot(str, object)
    def _handle_generation_finished(self, video_url: str, raw_result: object) -> None:
        """处理视频生成成功事件。

        :param video_url: API 返回的视频链接。
        :param raw_result: API 返回的原始结果数据。
        """

        self.resultUrlLineEdit.setText(video_url)
        self.copyResultButton.setEnabled(bool(video_url))
        self.openResultButton.setEnabled(bool(video_url))
        self._set_busy(False)
        self._handle_status_changed("任务完成")
        self._append_log("原始结果:")
        self._append_log(json.dumps(raw_result, ensure_ascii=False, indent=2))

    @Slot(str)
    def _handle_generation_failed(self, error_message: str) -> None:
        """处理视频生成失败事件。

        :param error_message: 错误消息。
        """

        self._set_busy(False)
        self._handle_status_changed("任务失败")
        self._append_log(error_message)
        QMessageBox.critical(self, "生成失败", error_message)

    @Slot()
    def _clear_worker_refs(self) -> None:
        """清理后台线程引用。"""

        self._worker_thread = None
        self._generation_worker = None

    def _select_file(self, title: str, file_filter: str) -> Path | None:
        """打开文件选择对话框。

        :param title: 对话框标题。
        :param file_filter: 文件类型过滤器。
        :return: 用户选择的文件路径；取消选择时返回 ``None``。
        """

        file_name, _ = QFileDialog.getOpenFileName(self, title, "", file_filter)
        if not file_name:
            return None

        return Path(file_name)

    def _set_busy(self, is_busy: bool) -> None:
        """设置界面忙碌状态。

        :param is_busy: 是否正在执行生成任务。
        """

        self.selectImageButton.setEnabled(not is_busy)
        self.selectVideoButton.setEnabled(not is_busy)
        self.generateButton.setText("生成中" if is_busy else "开始生成")
        self.taskProgressBar.setRange(0, 0 if is_busy else 100)
        self.taskProgressBar.setValue(0)
        self.generateButton.setEnabled(False)
        if not is_busy:
            self._refresh_ready_state()

    def _refresh_ready_state(self) -> None:
        """刷新素材选择状态。"""

        image_ready = Path(self.imagePathLineEdit.text().strip()).is_file()
        video_ready = Path(self.videoPathLineEdit.text().strip()).is_file()
        is_busy = self._worker_thread is not None and self._worker_thread.isRunning()

        self.generateButton.setEnabled(image_ready and video_ready and not is_busy)

        if image_ready and video_ready:
            self.statusLabel.setText("素材已就绪")
        elif image_ready or video_ready:
            self.statusLabel.setText("请继续选择另一个素材")
        else:
            self.statusLabel.setText("等待选择素材")

    def _append_log(self, message: str) -> None:
        """追加界面日志。

        :param message: 日志消息。
        """

        self.logTextEdit.append(message)


def extract_video_url(result: Any) -> str:
    """从 API 结果中提取视频链接。

    兼容字符串、字典和列表结构，优先读取常见的视频链接字段。

    :param result: API 返回的结果数据。
    :return: 提取到的视频链接。
    :raises ValueError: 未找到视频链接。
    """

    if isinstance(result, str) and result.startswith(("http://", "https://")):
        return result

    if isinstance(result, dict):
        for key in ("video_url", "url", "result_url", "output_url", "video"):
            value = result.get(key)
            if isinstance(value, str) and value.startswith(("http://", "https://")):
                return value

        for value in result.values():
            try:
                return extract_video_url(value)
            except ValueError:
                continue

    if isinstance(result, list):
        for item in result:
            try:
                return extract_video_url(item)
            except ValueError:
                continue

    raise ValueError("API 结果中没有找到视频链接")


def run_gui() -> None:
    """运行 MaskCraft 图形界面。"""

    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
