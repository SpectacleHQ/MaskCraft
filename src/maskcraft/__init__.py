from maskcraft.config import AppSettings, get_settings
from maskcraft.dashscope_client import DashScopeClient, DashScopeClientError
from maskcraft.main_window import MainWindow, run_gui

__all__ = [
    "AppSettings",
    "DashScopeClient",
    "DashScopeClientError",
    "MainWindow",
    "get_settings",
    "main",
    "run_gui",
]


def main() -> None:
    """运行包级命令行入口。

    延迟导入真正的命令行入口，避免 ``python -m maskcraft`` 执行时提前加载
    ``maskcraft.__main__``。
    """

    run_gui()
