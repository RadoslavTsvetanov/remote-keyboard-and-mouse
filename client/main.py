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



class KeyBoardKey:
    def __init__(self, v):
        if self.__check_if_it_a_char(v) or self.is_custom_key(v):
            self.v = v
        else:
            raise ValueError(f"Invalid key: {v}")

    def __check_if_it_a_char(self, v):
        return isinstance(v, str) and len(v) == 1 and ('a' <= v <= 'z' or 'A' <= v <= 'Z')

    def is_custom_key(self,v):
        return v in KEY_MAP  # `v in KEY_MAP` is cleaner than `KEY_MAP.get(v) != None`


class KeyBoard:
    def __init__(self):

        self.keyboard = Controller()

    def press_keys(self,keyList: list[KeyBoardKey]):
        """
        presses keys in the order they are passed

        Note that even though they are pressed in order the first key is not released until all keys have been pressed
        """
        keys = []
        for key in keyList:
            keys.append(key.v) 
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
                self.keyboard.press(key)
            
            for key in reversed(keys_to_press):
                self.keyboard.release(key)
        except Exception as e:
            print(f"Error pressing keys: {e}")
        
        for key in keys_to_press:
            try:
                self.keyboard.release(key)
            except:
                pass


class Mouse:
    def __init__(self):
        self.mouse = C() 

    def click(self,x: X, y: Y, phone_dimensions: Dimensions = None):
        print("clicking",x,y,phone_dimensions)
    
        self.move_mouse(x,y,phone_dimensions)

        time.sleep(0.01)
        self.mouse.click(Button.left)
    

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



# def scale(x: X, y: Y, phone_dimensions: Dimensions):

#     d = display.Display()
#     screen = d.screen()
#     screen_width = screen.width_in_pixels
#     screen_height = screen.height_in_pixels

#     d.flush()
#     return (int(x.v * (screen_width / phone_dimensions.width.v)), int(y.v * (screen_height / phone_dimensions.height.v)))

SERVER_URL = "http://164.92.142.166:8899/"
REQUEST_TIMEOUT = 5  # seconds
RETRY_DELAY = 1  # seconds

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
    mouse = Mouse()
    keyboard = KeyBoard()
    signal.signal(signal.SIGINT, signal_handler)
    
    while True:
        input_data = fetch_keys()
        keyStringCodes = input_data.get("keys").get("pressedkeys")
        keys = []

        for code in keyStringCodes:
            keys.append(KeyBoardKey(code).v)
        keyboard.press_keys()

        mouse_action = input_data.get("mouse").get("action")
        if(mouse_action == ""):
            pass
        elif mouse_action == "click":
            mouse.click(X(int(input_data.get("mouse").get("x"))), Y(int(input_data.get("mouse").get("y"))))
        elif mouse_action == "move":
            mouse.move_mouse(X(int(input_data.get("mouse").get("x"))), Y(int(input_data.get("mouse").get("y"))))
        else:
            
            print(input_data.mouse.action)
        time.sleep(0.05)

if __name__ == "__main__":

# Connect to X server
    
    main()
