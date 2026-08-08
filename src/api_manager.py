"""
api_manager.py - API Key 管理器
将 API Key 保存在项目根目录的 .env 文件中
首次运行自动引导输入，无需手动编辑文件
"""

import os
from pathlib import Path


# .env 文件路径（项目根目录）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

# 支持的 API 提供商（可扩展）
PROVIDERS = {
    "dashscope": {
        "name": "通义千问（阿里百炼）",
        "key_label": "DASHSCOPE_API_KEY",
        "apply_url": "https://bailian.console.aliyun.com/#/api-key",
        "test_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    },
}


class ApiManager:
    """管理多个 API 提供商的 Key"""

    def __init__(self):
        self._keys: dict[str, str] = {}
        self._load()

    def _load(self):
        """从 .env 文件加载所有 Key"""
        self._keys.clear()
        if not ENV_FILE.exists():
            return
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    self._keys[k.strip()] = v.strip().strip('"').strip("'")

    def _save(self):
        """保存到 .env 文件"""
        lines = []
        lines.append("# AI Live2D 虚拟角色 - API Key 配置")
        lines.append("# 此文件由程序自动管理，也可以手动编辑")
        lines.append("")
        for provider_id, info in PROVIDERS.items():
            label = info["key_label"]
            val = self._keys.get(label, "")
            lines.append(f"{label}={val}")
        lines.append("")
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def get_key(self, provider_id: str) -> str:
        """获取指定提供商的 API Key"""
        info = PROVIDERS.get(provider_id)
        if not info:
            return ""
        return self._keys.get(info["key_label"], "")

    def set_key(self, provider_id: str, key: str):
        """设置 API Key 并保存"""
        info = PROVIDERS.get(provider_id)
        if not info:
            raise ValueError(f"未知的 API 提供商: {provider_id}")
        self._keys[info["key_label"]] = key
        self._save()

    def has_key(self, provider_id: str) -> bool:
        """检查是否已配置 Key"""
        key = self.get_key(provider_id)
        return bool(key) and "你的" not in key and key.startswith("sk-")

    def is_configured(self) -> bool:
        """是否有至少一个可用的 Key"""
        return any(self.has_key(p) for p in PROVIDERS)

    def setup_wizard(self):
        """首次运行引导：交互式输入 API Key"""
        print("=" * 55)
        print("🔑  API Key 配置向导（首次运行）")
        print("=" * 55)
        print()

        for provider_id, info in PROVIDERS.items():
            current = self.get_key(provider_id)
            masked = ""
            if current:
                masked = current[:6] + "****" + current[-4:] if len(current) > 10 else "****"
                print(f"  [{info['name']}] 当前 Key: {masked}")
            else:
                print(f"  [{info['name']}] 尚未配置")

            print(f"  申请地址: {info['apply_url']}")
            print()
            new_key = input(f"  请输入 {info['name']} API Key（直接回车跳过）: ").strip()

            if new_key:
                self.set_key(provider_id, new_key)
                print("  ✅ 已保存！")
            elif current:
                print("  (保持现有 Key)")
            else:
                print("  ⚠️  跳过，之后可在 .env 文件中手动配置")
            print()

        print("配置完成！之后修改 Key 请编辑项目根目录的 .env 文件")
        print("=" * 55)


# 全局单例
api = ApiManager()