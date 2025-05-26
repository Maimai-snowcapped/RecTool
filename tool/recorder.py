import subprocess
import time
import json
import os
import sys

ffmpeg_proc = None
input_proc = None

timestamp_file = "record_start_time.txt"

with open("config.json", "r") as f:
    config = json.load(f)

ffmpeg_path = config["ffmpeg_path"]
output_dir = config["output_dir"]
video_filename = config["video_filename"]
input_logger_script = "input_logger.py"

def start_recording():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    video_path = os.path.join(output_dir, f"{video_filename}_{timestamp}.mp4")
    input_log_path = os.path.join(output_dir, f"input_{timestamp}.txt")

    start_time = time.time()
    with open(timestamp_file, "w") as f:
        f.write(str(start_time))

    # 启动 FFmpeg
    global ffmpeg_proc

    # 启动 ffmpeg 录屏（全屏）
    ffmpeg_cmd = [
        ffmpeg_path,
        "-y",
        "-f", "gdigrab",
        "-framerate", "30",
        "-video_size", "1920x1080",  # 使用标准分辨率
        "-i", "desktop",
        "-vcodec", "libx264",
        "-pix_fmt", "yuv420p",  # 使用兼容性更好的色彩空间
        "-preset", "medium",
        "-crf", "23",
        "-movflags", "+faststart",  # 优化MP4文件头
        video_path
    ]
    ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    print(f"[*] FFmpeg started with PID {ffmpeg_proc.pid}")

    # 启动键鼠记录器
    global input_proc
    input_proc = subprocess.Popen(["python", input_logger_script, str(start_time), input_log_path])
    print(f"[*] Input logger started with PID {input_proc.pid}")

    print("[*] 正在录制中，按 Ctrl+C 停止...")

def stop_recording():
    print("[*] 正在终止录制，请稍候...")

    if ffmpeg_proc:
        try:
            ffmpeg_proc.stdin.write(b"q\n")
            ffmpeg_proc.stdin.flush()
            ffmpeg_proc.wait(timeout=10)
            print("[*] FFmpeg 已终止")
        except Exception as e:
            print("[!] 无法优雅终止 FFmpeg:", e)

    if input_proc:
        try:
            input_proc.terminate()
            input_proc.wait(timeout=5)
            print("[*] Input logger 已终止")
        except Exception as e:
            print("[!] 无法终止 input logger:", e)

if __name__ == "__main__":
    try:
        start_recording()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] 收到 Ctrl+C")
        stop_recording()
        print("[*] 录制已停止")
