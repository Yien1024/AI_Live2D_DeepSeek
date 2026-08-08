"""
config.py - 全局配置
所有配置通过 character_manager / model_manager / api_manager 管理
修改角色人设 → 编辑 characters/*.json
修改模型     → 拖入 models/ 文件夹自动识别
修改 API Key  → 编辑项目根目录 .env 文件
"""

import os

# ============================================================
# 项目根目录
# ============================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 路径
# ============================================================
CHARACTERS_DIR = os.path.join(PROJECT_ROOT, "characters")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
TEMP_AUDIO_PATH = os.path.join(PROJECT_ROOT, "temp_voice.wav")

# ============================================================
# 窗口设置
# ============================================================
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# ============================================================
# LLM 设置
# ============================================================
# 模型选择：qwen-turbo（最快） / qwen-plus（平衡） / qwen-max（最强）
LLM_MODEL = "qwen-turbo"
# 通义千问 OpenAI 兼容接口
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# ============================================================
# 运行时状态（由 main.py 初始化）
# ============================================================
WINDOW_TITLE = "AI Live2D - 加载中..."
DASHSCOPE_API_KEY = ""  # 由 api_manager 在运行时注入
CHARACTER_NAME = ""
CHARACTER_PERSONALITY = ""
SYSTEM_PROMPT = ""
TTS_VOICE = "zh-CN-XiaoxiaoNeural"
MODEL_PATH = ""
GREETING = ""
FAREWELL = ""
EMOTION_PARAMS = {}