from pynput import keyboard, mouse
import time
import sys

start_time = float(sys.argv[1])
output_path = sys.argv[2]

# 添加组合键状态跟踪
current_keys = set()
last_x, last_y = None, None

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
    global last_x, last_y
    log_event(f"MouseMoveAbsolute: ({x}, {y})")
    
    # 计算相对移动量
    if last_x is not None and last_y is not None:
        dx = x - last_x
        dy = y - last_y
        if dx != 0 or dy != 0:  # 只记录有实际移动的情况
            log_event(f"MouseMoveRelative: ({dx}, {dy})")
    
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