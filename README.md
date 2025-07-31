# RecTool

## 项目简介

屏幕录制工具，可同时录制屏幕操作和键盘鼠标输入事件，并生成带时间戳的输出文件。

## 更新日志

### 0.0.0 (2025-05-20)

- 初始发布，支持基本的屏幕录制和输入事件记录。

### 0.0.0 (2025-05-25)

- 新增功能：支持自定义配置开始和停止录制的按键。
- 修复了一些已知问题。

### 0.0.0 (2025-06-10)

- 移除了 MouseMoveAbsolute 的绝对坐标记录
- 相对位移记录( MouseMoveRelative )现在同时受时间阈值(TIME_THRESHOLD)和位移阈值(MOVE_THRESHOLD)控制
- 只有当两次移动的时间间隔超过 50 毫秒(TIME_THRESHOLD)且累积位移超过 5 像素(MOVE_THRESHOLD)时，才会记录相对位移，可以根据实际需要调整这两个阈值参数。

### 0.0.0 (2025-06-15)

- 新增功能：支持自定义配置是否记录鼠标的绝对坐标
- 优化功能：操作开始就记录时间戳，而不是操作完成后再记录

## 功能特性

- 录制屏幕为 MP4 视频
- 记录键盘按键和鼠标操作
- 支持组合键记录
- 自动生成带时间戳的输出文件
- 支持自定义输出目录和文件名
- 支持用户自定义配置开始和停止录制的按键
- 支持自定义配置是否记录鼠标的绝对坐标

## 安装指南

### 前置要求

- Python 3.x
- FFmpeg (需配置环境变量或指定路径)
- pynput (pip install pynput)

### 安装步骤

1. 克隆仓库

```bash
git clone https://github.com/Maimai-snowcapped/RecTool.git
```

2. 安装 Python 依赖

```bash
pip install pynput
```

3. 配置 FFmpeg 路径(可选)
   修改`tool/config.json`中的`ffmpeg_path`

## 使用说明

1. 进入项目目录

```bash
cd RecTool
```

2. 开始录制

```bash
cd tool
start_record.bat
```

3. 按 Ctrl+C 停止录制

## 配置选项

修改`tool/config.json`文件：

```json
{
  "ffmpeg_path": "C:/ffmpeg/bin/ffmpeg.exe",
  "output_dir": "output",
  "video_filename": "video",
  "start_key": "F9",
  "stop_key": "F10",
  "mouse_move_threshold": 5,
  "mouse_time_threshold": 0.05,
  "log_absolute_position": false
}
```

- `ffmpeg_path`: FFmpeg 可执行文件路径
- `output_dir`: 输出目录(相对于 tool 目录)
- `video_filename`: 视频文件名前缀
- `start_key` : 开始录制的按键，默认为 F9
- `stop_key` : 停止录制的按键，默认为 F10
- `mouse_move_threshold` : 鼠标移动的位移阈值，单位为像素，默认为 5
- `mouse_time_threshold` : 鼠标移动的时间阈值，单位为秒，默认为 0.05
- `log_absolute_position` : 是否记录鼠标的绝对坐标，默认为 false

## 输出文件

- `video_YYYYMMDD_HHMMSS.mp4`: 屏幕录制视频
- `input_YYYYMMDD_HHMMSS.txt`: 输入事件日志

## 开发

### 依赖

- pynput

### 运行测试

```bash
python tool/recorder.py
```

## 贡献指南

欢迎通过 Issues 报告问题或提交 Pull Request。

## 许可证

MIT License
