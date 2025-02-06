import requests
from pynput.mouse import Button, Controller as C
from Xlib import display
import json
import time
import signal
import sys
from pynput.keyboard import Controller, Key
class Width():
    def __init__(self, v: int):
        self.v = v 

    def __str__(self):
        return self.v


mouse = C()

class Height():
    def __init__(self, v: int):
        self.v = v

    def __str__(self):
        return self.v


class X:
    def __init__(self, v: int):
        self.v = v

class Y:
    def __init__(self, v: int):
        self.v = v

class Dimensions:
    def __init__(self, width: Width, height: Height):
        self.width = width
        self.height = height

def click(x: X, y: Y, phone_dimensions: Dimensions = None):
    print("clicking",x,y,phone_dimensions)
    
    move_mouse(x,y,phone_dimensions)

    time.sleep(0.01)
    mouse.click(Button.left)
    
def scale(x: X, y: Y, phone_dimensions: Dimensions):

    d = display.Display()
    screen = d.screen()
    screen_width = screen.width_in_pixels
    screen_height = screen.height_in_pixels

    d.flush()
    return (int(x.v * (screen_width / phone_dimensions.width.v)), int(y.v * (screen_height / phone_dimensions.height.v)))

def move_mouse(x: X, y: Y, phone_dimensions: Dimensions = None):
    d = display.Display()
    root = d.screen().root
    screen = d.screen()


    if phone_dimensions == None:
        phone_dimensions = Dimensions(Width(412), Height(915))
    screen_width = screen.width_in_pixels
    screen_height = screen.height_in_pixels
    print((screen_width / phone_dimensions.width.v))
    print((x.v * (screen_width / phone_dimensions.width.v)))
    root.warp_pointer(int(x.v * (screen_width / phone_dimensions.width.v)) , int(y.v * (  screen_height // phone_dimensions.height.v)))
    d.flush()

SERVER_URL = "http://localhost:8080/"
REQUEST_TIMEOUT = 5  # seconds
RETRY_DELAY = 1  # seconds

KEY_MAP = {
    "enter": Key.enter,
    "space": Key.space,
    "shift": Key.shift,
    "ctrl": Key.ctrl,
    "alt": Key.alt,
    "backspace": Key.backspace,
    "esc": Key.esc,
    "tab": Key.tab,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "win": Key.cmd_r
}

keyboard = Controller()

def press_keys(keys):
    if not keys:
        return
    
    keys_to_press = []
    for k in keys:
        if k in KEY_MAP:
            keys_to_press.append(KEY_MAP[k])
        elif len(k) == 1:
            keys_to_press.append(k)
    
    try:
        for key in keys_to_press:
            keyboard.press(key)
            
        for key in reversed(keys_to_press):
            keyboard.release(key)
    except Exception as e:
        print(f"Error pressing keys: {e}")
        for key in keys_to_press:
            try:
                keyboard.release(key)
            except:
                pass

def fetch_keys():
    try:
        response = requests.get(SERVER_URL+"/keys", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching keys: {e}")
        return []

def get_mouse_data():
    try:
        response = requests.get(SERVER_URL+"/mouse", timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("")
    except:
        print("Error fetching mouse data")
        return None



def main():
    def signal_handler(sig, frame):
        print("\nShutting down gracefully...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        input_data = fetch_keys()
        press_keys(input_data.get("keys").get("pressedkeys"))

        mouse_action = input_data.get("mouse").get("action")
        if(mouse_action == ""):
            pass
        elif mouse_action == "click":
            click(X(int(input_data.get("mouse").get("x"))), Y(int(input_data.get("mouse").get("y"))))
        elif mouse_action == "move":
            move_mouse(X(int(input_data.get("mouse").get("x"))), Y(int(input_data.get("mouse").get("y"))))
        else:
            
            print(input_data.mouse.action)
        time.sleep(0.05)

if __name__ == "__main__":

# Connect to X server
    
    main()
