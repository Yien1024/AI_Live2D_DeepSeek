"""
character_manager.py - 角色人设管理器
自动扫描 characters/ 文件夹，加载/切换角色人设
修改角色只需编辑 JSON 文件，无需改代码
"""

import json
import os
from dataclasses import dataclass, field
from typing import Optional


# JSON 文件所在目录
CHARACTERS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "characters")


@dataclass
class Character:
    """角色人设数据类"""
    id: str
    name: str
    avatar: str
    personality: str
    voice: str
    system_prompt: str
    model: Optional[str] = None
    greeting: str = "你好呀！"
    farewell: str = "再见啦！"
    emotion_params: dict = field(default_factory=dict)


class CharacterManager:
    """角色管理器：扫描、加载、切换角色"""

    def __init__(self):
        self._characters: dict[str, Character] = {}
        self._current: Optional[Character] = None
        self._refresh()

    def _refresh(self):
        """重新扫描 characters/ 文件夹"""
        self._characters.clear()
        if not os.path.isdir(CHARACTERS_DIR):
            return
        for fname in sorted(os.listdir(CHARACTERS_DIR)):
            if fname.endswith(".json"):
                path = os.path.join(CHARACTERS_DIR, fname)
                try:
                    char = self._load_from_json(path)
                    self._characters[char.id] = char
                except Exception:
                    pass  # 跳过损坏的 JSON

    @staticmethod
    def _load_from_json(path: str) -> Character:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Character(
            id=data["id"],
            name=data["name"],
            avatar=data.get("avatar", ""),
            personality=data.get("personality", ""),
            voice=data.get("voice", "zh-CN-XiaoxiaoNeural"),
            system_prompt=data.get("system_prompt", ""),
            model=data.get("model"),
            greeting=data.get("greeting", "你好呀！"),
            farewell=data.get("farewell", "再见啦！"),
            emotion_params=data.get("emotion_params", {}),
        )

    def list_all(self) -> list[Character]:
        """返回所有可用角色"""
        self._refresh()
        return list(self._characters.values())

    def get(self, char_id: str) -> Optional[Character]:
        """按 ID 获取角色"""
        self._refresh()
        return self._characters.get(char_id)

    def set_current(self, char_id: str) -> Character:
        """切换当前角色，返回新角色"""
        char = self.get(char_id)
        if char is None:
            raise ValueError(f"角色 '{char_id}' 不存在，可用角色: {list(self._characters.keys())}")
        self._current = char
        return char

    @property
    def current(self) -> Optional[Character]:
        return self._current

    @property
    def default_id(self) -> str:
        """默认角色 ID（第一个可用角色，或 'default'）"""
        if "default" in self._characters:
            return "default"
        ids = list(self._characters.keys())
        return ids[0] if ids else "default"

    def print_roster(self):
        """打印角色列表"""
        self._refresh()
        if not self._characters:
            print("  (没有找到角色配置文件)")
            return
        for char in self._characters.values():
            current_mark = " ▶" if self._current and char.id == self._current.id else "  "
            print(f"{current_mark} {char.avatar} {char.name} ({char.id}) - {char.personality[:20]}...")


# 全局单例
manager = CharacterManager()