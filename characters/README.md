# 角色人设文件夹

**编辑 JSON 文件即可修改角色，无需改代码！**

每个 `.json` 文件代表一个角色，支持多角色切换。

## 文件格式

```json
{
    "id": "唯一标识",
    "name": "角色名",
    "avatar": "🌸",
    "personality": "一句话性格描述",
    "voice": "zh-CN-XiaoxiaoNeural",
    "system_prompt": "给 AI 的 system prompt...",
    "model": null,
    "greeting": "开场白",
    "farewell": "告别语",
    "emotion_params": {
        "开心": { "ParamMouthForm": 0.8, "ParamEyeLSmile": 1.0 },
        "愤怒": { "ParamBrowLY": -0.6 },
        "害羞": { "ParamCheek": 1.0 },
        "悲伤": { "ParamBrowLY": 0.4, "ParamMouthForm": -0.5 },
        "惊讶": { "ParamEyeLOpen": 1.3, "ParamMouthOpenY": 0.4 },
        "平静": {}
    }
}
```

## 字段说明

| 字段 | 说明 |
|------|------|
| `id` | 唯一标识符，用于 `/角色` 命令切换 |
| `name` | 显示名称 |
| `avatar` | 终端显示的 emoji 头像 |
| `personality` | 性格描述（简短） |
| `voice` | Edge-TTS 语音角色名 |
| `system_prompt` | 发给 AI 的系统提示词 |
| `model` | 绑定的模型路径（null=不绑定） |
| `greeting` | 登场问候语 |
| `farewell` | 离场告别语 |
| `emotion_params` | 六种情绪对应的 Live2D 参数 |

## 可用 Edge-TTS 语音

| 语音 ID | 风格 |
|---------|------|
| `zh-CN-XiaoxiaoNeural` | 活泼少女 |
| `zh-CN-XiaoyiNeural` | 温柔少女 |
| `zh-CN-YunxiNeural` | 阳光少年 |
| `zh-CN-YunjianNeural` | 稳重男声 |
| `zh-CN-YunyangNeural` | 新闻播报 |
| `zh-CN-XiaochenNeural` | 知性女声 |

## 添加新角色

1. 复制 `default.json` 重命名为新文件
2. 修改 JSON 内容
3. 重启程序，自动识别

## 运行中切换

输入 `/角色` 命令即可在运行中切换角色人设。