from pynput import keyboard

def on_press(key):
    try:
        # For regular characters
        print(f'Key pressed: {key.char}')
    except AttributeError:
        # For special keys
        print(f'Special key pressed: {key}')

def on_release(key):
    try:
        print(f'Key released: {key.char}')
    except AttributeError:
        print(f'Special key released: {key}')
    
    # Stop listener if ESC is pressed
    if key == keyboard.Key.esc:
        print("Stopping keyboard monitor...")
        return False

# Create and start the listener
print("Keyboard monitor started. Press ESC to exit.")
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()