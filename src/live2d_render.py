"""
live2d_render.py - Live2D 渲染模块
基于 glfw 窗口 + live2d-py + OpenGL 渲染，独立线程运行
"""

import glfw
import threading
import live2d.v3 as live2d
from live2d.v3 import StandardParams
import config


class Live2DWindow:
    """Live2D 渲染窗口，封装 glfw + live2d-py 的初始化、渲染、参数控制"""

    def __init__(self, model_path: str, emotion_params: dict = None):
        # ---------- 初始化 GLFW ----------
        if not glfw.init():
            raise RuntimeError("GLFW 初始化失败")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_COMPAT_PROFILE)
        glfw.window_hint(glfw.SAMPLES, 4)
        # 兼容低端集显：允许向后兼容的上下文
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 0)

        self.width = config.WINDOW_WIDTH
        self.height = config.WINDOW_HEIGHT
        self.window = glfw.create_window(
            self.width, self.height, config.WINDOW_TITLE, None, None
        )
        if not self.window:
            glfw.terminate()
            raise RuntimeError("GLFW 窗口创建失败")

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        # ---------- 初始化 Live2D ----------
        live2d.init()
        live2d.glInit()

        # ---------- 加载模型 ----------
        self.model = live2d.LAppModel()
        self.model.LoadModelJson(model_path)
        self.model.Resize(self.width, self.height)
        self.model.SetAutoBlinkEnable(True)
        self.model.SetAutoBreathEnable(True)

        # ---------- 释放主线程的 OpenGL 上下文 (渲染线程会重新绑定) ----------
        glfw.make_context_current(None)

        # ---------- 状态 ----------
        self.running = True
        self.mouth_open = 0.0
        self.current_emotion = "平静"
        self._lock = threading.Lock()

        # ---------- 情绪参数 ----------
        self.emotion_map = emotion_params or self._default_emotion_map()

    @staticmethod
    def _default_emotion_map() -> dict:
        return {
            "开心": {
                "ParamMouthForm": 0.8, "ParamEyeLSmile": 1.0,
                "ParamEyeRSmile": 1.0, "ParamCheek": 0.5,
            },
            "愤怒": {
                "ParamBrowLY": -0.6, "ParamBrowRY": -0.6,
                "ParamBrowLAngle": -0.5, "ParamBrowRAngle": -0.5,
                "ParamEyeLOpen": 0.5, "ParamEyeROpen": 0.5,
            },
            "害羞": {
                "ParamCheek": 1.0, "ParamEyeLSmile": 0.5,
                "ParamEyeRSmile": 0.5, "ParamMouthForm": 0.3,
            },
            "悲伤": {
                "ParamBrowLY": 0.4, "ParamBrowRY": 0.4,
                "ParamBrowLAngle": 0.3, "ParamBrowRAngle": 0.3,
                "ParamMouthForm": -0.5, "ParamEyeLOpen": 0.6,
                "ParamEyeROpen": 0.6,
            },
            "惊讶": {
                "ParamEyeLOpen": 1.3, "ParamEyeROpen": 1.3,
                "ParamMouthOpenY": 0.4, "ParamBrowLY": -0.3,
                "ParamBrowRY": -0.3,
            },
            "平静": {},
        }

    def set_title(self, title: str):
        """更新窗口标题"""
        glfw.set_window_title(self.window, title)

    def apply_emotion(self, emotion: str):
        with self._lock:
            self.current_emotion = emotion
            params = self.emotion_map.get(emotion, {})
            for param_id, value in params.items():
                self.model.SetParameterValue(param_id, value)

    def update(self, mouth_open: float = None, emotion: str = None):
        with self._lock:
            if mouth_open is not None:
                self.mouth_open = mouth_open
            if emotion is not None:
                self.current_emotion = emotion
                params = self.emotion_map.get(emotion, {})
                for param_id, value in params.items():
                    self.model.SetParameterValue(param_id, value)
            self.model.SetParameterValue(StandardParams.ParamMouthOpenY, self.mouth_open)

    def render_frame(self) -> bool:
        """渲染一帧，线程安全"""
        if glfw.window_should_close(self.window):
            self.running = False
            return False
        with self._lock:
            live2d.clearBuffer(0.94, 0.94, 0.98, 1.0)
            self.model.Update()
            self.model.Draw()
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        return self.running

    def close(self):
        self.running = False
        live2d.dispose()
        live2d.glRelease()
        glfw.terminate()
