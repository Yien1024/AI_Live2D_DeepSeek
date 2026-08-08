"""
voice.py - 语音合成与播放模块
Edge-TTS 合成 + winsound 播放，语音角色从 config 读取
"""

import asyncio
import winsound
import edge_tts
import soundfile as sf
import config


async def text_to_speech(text: str, save_path: str) -> float:
    """
    文字转语音
    返回: 音频时长（秒）
    """
    comm = edge_tts.Communicate(text, config.TTS_VOICE)
    await comm.save(save_path)
    data, sr = sf.read(save_path)
    return len(data) / sr


def play_audio(audio_path: str):
    """异步播放 WAV（Windows），立即返回"""
    winsound.PlaySound(audio_path, winsound.SND_ASYNC | winsound.SND_FILENAME)


def stop_audio():
    """停止当前播放"""
    winsound.PlaySound(None, winsound.SND_PURGE)