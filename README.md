# RecTool

## 项目简介
屏幕录制工具，可同时录制屏幕操作和键盘鼠标输入事件，并生成带时间戳的输出文件。

## 功能特性
- 录制屏幕为MP4视频
- 记录键盘按键和鼠标操作
- 支持组合键记录
- 自动生成带时间戳的输出文件
- 支持自定义输出目录和文件名
- 支持用户自定义配置开始和停止录制的按键

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
2. 安装Python依赖
```bash
pip install pynput
```
3. 配置FFmpeg路径(可选)
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
3. 按Ctrl+C停止录制

## 配置选项
修改`tool/config.json`文件：
```json
{
    "ffmpeg_path": "C:/ffmpeg/bin/ffmpeg.exe",
    "output_dir": "output",
    "video_filename": "video",
    "start_key": "F9",
    "stop_key": "F10"
}
```
- `ffmpeg_path`: FFmpeg可执行文件路径
- `output_dir`: 输出目录(相对于tool目录)
- `video_filename`: 视频文件名前缀
- `start_key` : 开始录制的按键，默认为 F9
- `stop_key` : 停止录制的按键，默认为 F10

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
欢迎通过Issues报告问题或提交Pull Request。

## 许可证
MIT License
        