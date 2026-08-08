# AI Live2D 虚拟角色

一个基于 **通义千问（阿里百炼）** 大语言模型驱动的桌面虚拟角色程序。角色会说话、有表情、有性格，像桌宠一样陪伴你日常聊天。

## 功能

- **AI 对话** — 接入通义千问 API，角色会根据人设回答你的每一句话，支持多种情绪切换
- **Live2D 动画** — 加载 Live2D 模型，角色会眨眼、呼吸、随情绪变化表情
- **语音合成** — 使用 Edge-TTS 将回复朗读出来，配合口型同步，就像真人在说话
- **角色系统** — 通过 JSON 配置文件定义角色人设、性格、语气，无需改代码即可切换
- **模型管理** — 自动识别 `models/` 目录下的 Live2D 模型，支持多个模型切换
- **情绪驱动** — 根据对话内容自动切换表情（开心 / 愤怒 / 害羞 / 悲伤 / 惊讶 / 平静）

## 快速开始

### 环境要求

- Windows 10 / 11（依赖 `winsound` 播放音频）
- Python 3.10 – 3.12（推荐 3.12）
- 网络连接（调用阿里百炼 API 和 Edge-TTS）

### 1. 下载项目

```bash
git clone https://github.com/Yien1024/AI_Live2D_DeepSeek.git
cd AI_Live2D_DeepSeek
```

### 2. 创建虚拟环境

```bash
python -m venv env
```

### 3. 安装依赖

```bash
env\Scripts\pip install -r requirements.txt
```

> 如果 `live2d-py` 安装较慢，可以指定国内镜像源：
> ```bash
> env\Scripts\pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
> ```

### 4. 获取 API Key

1. 打开 [阿里百炼 API Key 管理](https://bailian.console.aliyun.com/#/api-key)
2. 登录阿里云账号，创建一个 API Key（以 `sk-` 开头）
3. 首次运行程序时会引导你输入，程序会自动保存到 `.env` 文件

### 5. 准备 Live2D 模型

将 Live2D 模型文件夹放入 `models/` 目录，结构如下：

```
models/
└── 你的模型名/
    ├── 模型名.model3.json
    ├── 模型名.moc3
    └── textures/
        ├── texture_00.png
        └── ...
```

项目自带一个 Allium 企划的 ariu 模型，可直接使用。

### 6. 启动

```bash
env\Scripts\python src\main.py
```

## 使用方法

### 启动流程

1. 运行 `src/main.py`
2. 首次运行会提示输入阿里百炼 API Key（之后可在 `.env` 文件中修改）
3. 选择角色（如有多个）
4. 选择 Live2D 模型（如有多个）
5. 角色加载完成后即可开始对话

### 内置命令

| 命令 | 功能 |
|------|------|
| 输入文字 | 与角色聊天 |
| `/角色` | 切换角色人设 |
| `/模型` | 切换 Live2D 模型（需重启） |
| `/情绪 开心` | 手动切换表情 |
| `/key` | 修改 API Key |
| `/帮助` | 显示帮助信息 |
| `exit` / `退出` | 退出程序 |

### 角色切换

编辑 `characters/` 目录下的 JSON 文件即可自定义角色。每个角色文件包含：

- `name` — 角色名字
- `personality` — 性格描述
- `system_prompt` — 控制 AI 回复风格的系统提示词
- `voice` — Edge-TTS 语音角色
- `greeting` / `farewell` — 见面 / 告别语
- `emotion_params` — 每种情绪对应的 Live2D 参数

示例角色 `default.json`（小樱）已预置，可直接使用。

## 项目结构

```
AI_Live2D_DeepSeek/
├── src/
│   ├── main.py               # 主程序入口
│   ├── config.py              # 全局配置
│   ├── brain.py               # AI 对话模块（调用通义千问）
│   ├── voice.py               # 语音合成与播放
│   ├── live2d_render.py       # Live2D 渲染窗口
│   ├── api_manager.py         # API Key 管理
│   ├── character_manager.py   # 角色管理
│   └── model_manager.py       # 模型管理
├── characters/
│   ├── default.json           # 默认角色（小樱）
│   └── kuudere.json           # 冷娇角色
├── models/                    # Live2D 模型文件夹
├── requirements.txt           # Python 依赖
├── .gitignore
└── README.md
```

## 技术栈

| 组件 | 技术 |
|------|------|
| AI 对话 | 通义千问（阿里百炼 OpenAI 兼容接口） |
| 语音合成 | Edge-TTS（微软语音引擎） |
| Live2D 渲染 | live2d-py + GLFW + OpenGL |
| 音频播放 | winsound（Windows 原生） |

## 常见问题

### Q: 启动后窗口黑屏 / 没有反应

确保使用虚拟环境的 Python 运行，OpenGL 上下文需要正确绑定：

```bash
env\Scripts\python src\main.py
```

### Q: 语音没有声音

- 检查系统音量是否开启
- 确认网络能访问 edge-tts 的服务器

### Q: 模型加载失败

- 确保模型文件夹结构正确（包含 `.model3.json` 和 `.moc3` 文件）
- 模型文件路径不能包含中文或特殊字符

### Q: API Key 在哪里修改

运行程序后输入 `/key` 命令，或直接编辑项目根目录的 `.env` 文件。
