from pynput import keyboard, mouse
import time
import sys

start_time = float(sys.argv[1])
output_path = sys.argv[2]

# 添加组合键状态跟踪
current_keys = set()

def log_event(event):
    timestamp = time.time() - start_time
    with open(output_path, "a") as f:
        f.write(f"[{timestamp:.3f}] {event}\n")

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

# 添加鼠标移动记录
def on_move(x, y):
    log_event(f"MouseMove: ({x}, {y})")

def on_click(x, y, button, pressed):
    action = "MouseDown" if pressed else "MouseUp"
    log_event(f"{action}: {button} at ({x}, {y})")

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()