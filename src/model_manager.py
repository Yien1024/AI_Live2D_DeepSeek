"""
model_manager.py - Live2D 模型管理器
自动扫描 models/ 文件夹，发现所有可用模型
拖入模型文件夹即可自动识别，无需改配置
"""

import os
import json
from dataclasses import dataclass
from typing import Optional


# 模型根目录
MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")


@dataclass
class ModelInfo:
    """Live2D 模型信息"""
    name: str           # 显示名称（文件夹名）
    path: str           # model3.json 的绝对路径
    dir_path: str       # 模型文件夹路径
    model_json: str     # model3.json 文件名
    version: str = ""   # 模型版本（从 JSON 读取）


class ModelManager:
    """自动扫描 models/ 文件夹，发现所有 .model3.json"""

    def __init__(self):
        self._models: list[ModelInfo] = []
        self._current: Optional[ModelInfo] = None
        self._rescan()

    def _rescan(self):
        """扫描 models/ 目录，递归查找所有 .model3.json"""
        self._models.clear()
        if not os.path.isdir(MODELS_DIR):
            return

        for root, dirs, files in os.walk(MODELS_DIR):
            for fname in files:
                if fname.endswith(".model3.json"):
                    full_path = os.path.join(root, fname)
                    folder_name = os.path.basename(root)
                    version = self._read_version(full_path)
                    self._models.append(ModelInfo(
                        name=folder_name,
                        path=full_path,
                        dir_path=root,
                        model_json=fname,
                        version=version,
                    ))

    @staticmethod
    def _read_version(json_path: str) -> str:
        """尝试读取模型版本号"""
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return str(data.get("Version", ""))
        except Exception:
            return ""

    def list_all(self) -> list[ModelInfo]:
        """返回所有可用模型"""
        self._rescan()
        return list(self._models)

    def get_by_name(self, name: str) -> Optional[ModelInfo]:
        """按文件夹名获取模型"""
        for m in self._models:
            if m.name == name:
                return m
        return None

    def get_by_path(self, path: str) -> Optional[ModelInfo]:
        """按 model3.json 路径获取模型"""
        for m in self._models:
            if m.path == path:
                return m
        return None

    def set_current(self, model: ModelInfo):
        self._current = model

    @property
    def current(self) -> Optional[ModelInfo]:
        return self._current

    @property
    def count(self) -> int:
        return len(self._models)

    def pick_best(self) -> Optional[ModelInfo]:
        """自动选择最合适的模型（第一个可用）"""
        self._rescan()
        if self._models:
            self._current = self._models[0]
            return self._current
        return None

    def print_list(self):
        """打印模型列表"""
        self._rescan()
        if not self._models:
            print("  (未找到 Live2D 模型，请将模型放入 models/ 文件夹)")
            return
        for i, m in enumerate(self._models):
            current_mark = "▶" if self._current and m.path == self._current.path else " "
            ver = f"v{m.version}" if m.version else ""
            print(f" {current_mark} [{i + 1}] {m.name}  {ver}")
            print(f"      {os.path.relpath(m.path, MODELS_DIR)}")


# 全局单例
model_manager = ModelManager()