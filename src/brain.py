"""
brain.py - AI 大脑模块
调用通义千问（阿里百炼）API，结合当前角色人设进行对话
"""

import requests
import config


def chat_with_ai(user_input: str) -> tuple[str, str]:
    """
    调用通义千问对话（使用当前角色人设）
    返回: (emotion, reply)
    """
    headers = {
        "Authorization": f"Bearer {config.DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": config.LLM_MODEL,
        "messages": [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "temperature": 1.0,
        "max_tokens": 300
    }

    try:
        resp = requests.post(
            f"{config.DASHSCOPE_BASE_URL}/chat/completions",
            json=body,
            headers=headers,
            timeout=30
        )
        resp.raise_for_status()
        full_reply = resp.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError:
        if resp.status_code == 401:
            return "悲伤", "呜呜，API Key 好像不对...用 /key 命令修改一下"
        elif resp.status_code == 429:
            return "惊讶", "啊，免费额度用完了...等一会再试吧"
        else:
            return "平静", "网络出问题了..."
    except Exception:
        return "悲伤", "唔，好像出了点问题..."

    # 提取情绪标签
    emotion = "平静"
    if full_reply.startswith("【"):
        end = full_reply.find("】")
        if end != -1:
            emotion = full_reply[1:end]
            full_reply = full_reply[end + 1:].strip()

    return emotion, full_reply