from pynput import keyboard, mouse
import time
import sys
import json

start_time = float(sys.argv[1])
output_path = sys.argv[2]

# 从config.json读取配置
with open('config.json', 'r') as f:
    config = json.load(f)

# 添加组合键状态跟踪
current_keys = set()
last_x, last_y = None, None
# 新增累积位移变量
accumulated_dx = 0
accumulated_dy = 0
# 设置位移阈值(像素)
MOVE_THRESHOLD = config.get("mouse_move_threshold", 5)
# 新增时间阈值(秒)
TIME_THRESHOLD = config.get("mouse_time_threshold", 0.05)
last_move_time = 0

def log_event(event):
    timestamp = time.time() - start_time
    try:
        with open(output_path, "a") as f:
            f.write(f"[{timestamp:.6f}] {event}\n")
    except IOError as e:
        print(f"Error writing to log file: {e}")

def on_press(key):
    current_keys.add(key)
    try:
        log_event(f"KeyDown: {key.char}")
    except AttributeError:
        log_event(f"KeyDown: {key}")
    
    # 记录当前按下的所有键
    if len(current_keys) > 1:
        log_event(f"KeyCombination: {current_keys}")

def on_release(key):
    current_keys.discard(key)
    log_event(f"KeyUp: {key}")

def on_move(x, y):
    global last_x, last_y, accumulated_dx, accumulated_dy, last_move_time
    
    current_time = time.time()
    
    # 根据配置决定是否记录绝对坐标
    if config.get("log_absolute_position", True):
        log_event(f"MouseMoveAbsolute: ({x}, {y})")
    
    
    # 只有当超过时间阈值时才处理相对位移
    if current_time - last_move_time >= TIME_THRESHOLD:
        if last_x is not None and last_y is not None:
            dx = x - last_x
            dy = y - last_y
            
            accumulated_dx += dx
            accumulated_dy += dy
            
            if abs(accumulated_dx) >= MOVE_THRESHOLD or abs(accumulated_dy) >= MOVE_THRESHOLD:
                log_event(f"MouseMoveRelative: ({accumulated_dx}, {accumulated_dy})")
                accumulated_dx = 0
                accumulated_dy = 0
        
        last_move_time = current_time
    
    last_x, last_y = x, y

def on_click(x, y, button, pressed):
    action = "MouseDown" if pressed else "MouseUp"
    log_event(f"{action}: {button} at ({x}, {y})")

def on_scroll(x, y, dx, dy):
    log_event(f"MouseScroll: ({dx}, {dy}) at ({x}, {y})")

try:
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(
        on_click=on_click,
        on_move=on_move,
        on_scroll=on_scroll
    )

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()
except Exception as e:
    print(f"Error starting listeners: {e}")
    sys.exit(1)