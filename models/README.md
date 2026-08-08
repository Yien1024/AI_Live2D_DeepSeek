# Live2D 模型文件夹

**拖入模型文件夹即可自动识别，无需修改任何代码！**

程序启动时会自动扫描此目录下所有 `.model3.json` 文件。

## 目录结构

```
models/
  └── 你的模型名/              ← 直接拖入整个文件夹
        ├── 模型名.model3.json  ← 程序自动识别
        ├── 模型名.moc3
        ├── textures/
        │     └── texture_00.png
        ├── motions/            ← 可选
        └── expressions/        ← 可选
```

## 获取免费模型

1. **Live2D 官方 SDK 示例模型**
   - 下载 Cubism SDK for Native：https://www.live2d.com/download/cubism-sdk-download-native/
   - SDK 中自带 Haru、Hiyori 等示例模型

2. **社区免费模型**
   - 在 Bilibili 搜索 "免费 Live2D 模型"
   - 确认格式为 Cubism 3.0+（.model3.json）

## 多模型管理

放入多个模型文件夹后，启动时程序会列出所有可用模型供你选择。
运行中也可以随时用 `/模型` 命令切换。