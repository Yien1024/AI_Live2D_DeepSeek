"""
main.py - AI Live2D 虚拟角色主程序
流程：用户输入 → AI 对话 → 语音合成 → 音频播放 + Live2D 口型/表情同步

【系统设计】
- 角色人设 → characters/*.json（编辑 JSON 即可切换角色）
- Live2D 模型 → 拖入 models/ 文件夹自动识别
- API Key   → 编辑项目根目录 .env 文件
- 渲染线程 → 独立线程持续渲染，input 不阻塞窗口
"""

import asyncio
import time
import math
import os
import sys
import threading

# 确保 src 目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from brain import chat_with_ai
from voice import text_to_speech, play_audio, stop_audio
from live2d_render import Live2DWindow
from character_manager import manager as char_mgr
from model_manager import model_manager
from api_manager import api


# ============================================================
# 渲染线程
# ============================================================

def render_thread(window: Live2DWindow):
    """独立线程持续渲染，保持窗口响应"""
    # 关键：在渲染线程中绑定 OpenGL 上下文
    import glfw
    glfw.make_context_current(window.window)
    while window.running:
        window.render_frame()
        time.sleep(0.016)  # ~60fps


# ============================================================
# 初始化阶段
# ============================================================

def init_api_key():
    if not api.is_configured():
        print()
        api.setup_wizard()
        print()
    config.DASHSCOPE_API_KEY = api.get_key("dashscope")


def init_character():
    chars = char_mgr.list_all()
    if not chars:
        print("❌ 没有找到角色配置！请在 characters/ 文件夹中创建 .json 文件")
        sys.exit(1)

    print()
    print("=" * 50)
    print("🎭  可用角色：")
    char_mgr.print_roster()
    print("=" * 50)

    if len(chars) == 1:
        char = chars[0]
        print(f"  自动选择: {char.avatar} {char.name}")
    else:
        while True:
            try:
                choice = input(f"  选择角色 (1-{len(chars)}，默认 1): ").strip()
            except (EOFError, KeyboardInterrupt):
                choice = ""
            if not choice:
                choice = "1"
            try:
                idx = int(choice) - 1
                char = chars[idx]
                break
            except (ValueError, IndexError):
                print(f"  请输入 1-{len(chars)}")

    char_mgr.set_current(char.id)
    _apply_character(char)


def _apply_character(char):
    config.CHARACTER_NAME = char.name
    config.CHARACTER_PERSONALITY = char.personality
    config.SYSTEM_PROMPT = char.system_prompt
    config.TTS_VOICE = char.voice
    config.GREETING = char.greeting
    config.FAREWELL = char.farewell
    config.EMOTION_PARAMS = char.emotion_params
    config.WINDOW_TITLE = f"AI {char.name} - 通义千问驱动"


def init_model():
    models = model_manager.list_all()

    print()
    print("=" * 50)
    print("🎨  可用 Live2D 模型：")
    model_manager.print_list()
    print("=" * 50)

    if not models:
        print()
        print("❌ 没有找到 Live2D 模型！")
        print("   请将模型文件夹放入 models/ 目录，结构如下：")
        print("   models/")
        print("     └── 你的模型名/")
        print("           ├── 模型名.model3.json")
        print("           ├── 模型名.moc3")
        print("           └── textures/")
        print()
        print("   免费模型获取：Live2D Cubism SDK 自带示例模型")
        print("   https://www.live2d.com/download/cubism-sdk-download-native/")
        sys.exit(1)

    if len(models) == 1:
        model = models[0]
        print(f"  自动选择: {model.name}")
    else:
        while True:
            try:
                choice = input(f"  选择模型 (1-{len(models)}，默认 1): ").strip()
            except (EOFError, KeyboardInterrupt):
                choice = ""
            if not choice:
                choice = "1"
            try:
                idx = int(choice) - 1
                model = models[idx]
                break
            except (ValueError, IndexError):
                print(f"  请输入 1-{len(models)}")

    model_manager.set_current(model)
    config.MODEL_PATH = model.path


# ============================================================
# 音频播放 + 口型同步
# ============================================================

def play_audio_with_lipsync(window: Live2DWindow, audio_path: str, duration: float, emotion: str):
    window.apply_emotion(emotion)
    play_audio(audio_path)

    start_time = time.time()
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        mouth = abs(math.sin(elapsed * 10)) * 0.5 + 0.15
        window.update(mouth_open=mouth)
        time.sleep(0.03)

    window.update(mouth_open=0.0)


# ============================================================
# 主循环
# ============================================================

async def main_loop():
    # ---- 初始化 ----
    init_api_key()
    init_character()
    init_model()

    char = char_mgr.current

    # ---- 启动 Live2D 窗口 ----
    print(f"\n  正在加载 Live2D 模型: {os.path.basename(config.MODEL_PATH)}...")
    try:
        window = Live2DWindow(config.MODEL_PATH, char.emotion_params)
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return

    # 更新窗口标题为角色名
    window.set_title(config.WINDOW_TITLE)

    # 启动独立渲染线程，input 阻塞时窗口依然响应
    render_t = threading.Thread(target=render_thread, args=(window,), daemon=True)
    render_t.start()

    print()
    print("=" * 50)
    print(f"✨ AI {char.avatar} {char.name} 已苏醒！")
    print(f"   {char.greeting}")
    print()
    print("   命令: 输入文字聊天 | /角色 切换角色 | /模型 切换模型")
    print("        /key 修改API Key  | /帮助 更多命令 | exit 退出")
    print("=" * 50)

    # ---- 主循环 ----
    while window.running:
        try:
            user = input("\n你: ")
        except (EOFError, KeyboardInterrupt):
            break

        if not user.strip():
            continue

        # ---- 内置命令 ----
        if user.startswith("/"):
            handled = await handle_command(user, window, char)
            if handled:
                char = char_mgr.current
            continue

        if user.lower() in ("exit", "quit", "退出"):
            print(f"{char.name}: {char.farewell}")
            break

        # ① AI 对话
        print("  思考中...", end="\r")
        emotion, reply = chat_with_ai(user)
        print(f"{char.name}【{emotion}】: {reply}")

        # ② 文字转语音
        print("  合成语音中...", end="\r")
        duration = await text_to_speech(reply, config.TEMP_AUDIO_PATH)
        print(" " * 20, end="\r")

        # ③ 播放 + 口型同步
        play_audio_with_lipsync(window, config.TEMP_AUDIO_PATH, duration, emotion)

    # ---- 清理 ----
    stop_audio()
    window.close()
    if os.path.exists(config.TEMP_AUDIO_PATH):
        os.remove(config.TEMP_AUDIO_PATH)
    print("\n已退出，再见！")


async def handle_command(cmd: str, window, char) -> bool:
    parts = cmd.strip().split()
    cmd = parts[0].lower()

    if cmd == "/角色":
        print()
        print("🎭 可用角色：")
        char_mgr.print_roster()
        choice = input("切换角色 (输入 ID，取消按回车): ").strip()
        if choice:
            try:
                new_char = char_mgr.set_current(choice)
                _apply_character(new_char)
                window.set_title(config.WINDOW_TITLE)
                window.apply_emotion("平静")
                print(f"✅ 已切换为 {new_char.avatar} {new_char.name}")
                print(f"   {new_char.greeting}")
            except ValueError as e:
                print(f"❌ {e}")
        return True

    elif cmd == "/模型":
        models = model_manager.list_all()
        if not models:
            print("❌ 没有可用模型")
            return True
        print()
        print("🎨 可用模型：")
        model_manager.print_list()
        choice = input("切换模型 (输入编号，取消按回车): ").strip()
        if choice:
            try:
                idx = int(choice) - 1
                model = models[idx]
                model_manager.set_current(model)
                config.MODEL_PATH = model.path
                print(f"✅ 已切换模型: {model.name}")
                print("   请重启程序以加载新模型")
            except (ValueError, IndexError):
                print("❌ 无效选择")
        return True

    elif cmd == "/key":
        api.setup_wizard()
        config.DASHSCOPE_API_KEY = api.get_key("dashscope")
        return True

    elif cmd == "/帮助" or cmd == "/help":
        print()
        print("  📋 可用命令：")
        print("  /角色    - 切换角色人设")
        print("  /模型    - 切换 Live2D 模型（需重启）")
        print("  /key     - 修改 API Key（保存到 .env）")
        print("  /情绪    - 手动切换表情")
        print("  /帮助    - 显示此帮助")
        print("  exit     - 退出程序")
        return True

    elif cmd == "/情绪":
        if len(parts) > 1:
            emo = parts[1]
            window.apply_emotion(emo)
            print(f"  已切换情绪: {emo}")
        else:
            print("  用法: /情绪 开心|愤怒|害羞|悲伤|惊讶|平静")
        return True

    return False


if __name__ == "__main__":
    asyncio.run(main_loop())