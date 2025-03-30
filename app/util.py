import os, sys
import ctypes
import ctypes.wintypes as wintypes
import threading


def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = ""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def buildPath(*args: str):
    rel_path = ""
    for level in args:
        rel_path = os.path.join(rel_path, level)
    return rel_path

def createHotkeyListener(onEvent):
    # Run the hotkey listener in a separate daemon thread so it doesn't block the main app
    listener_thread = threading.Thread(target=lambda: hotkeyListener(onEvent), daemon=True)
    listener_thread.start()

def hotkeyListener(eventCallback):
    user32 = ctypes.windll.user32

    # Constants for modifiers and key codes
    MOD_ALT = 0x0001
    MOD_SHIFT = 0x0004
    VK_Q = 0x51  # Virtual key codes (Q and S)
    VK_S = 0x53
    WM_HOTKEY = 0x0312

    # Register the global hotkey: Alt + Shift + S
    if not user32.RegisterHotKey(None, 1, MOD_ALT | MOD_SHIFT, VK_S):
        print("Failed to register hotkey.")
        return

    try:
        msg = wintypes.MSG()
        while user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == WM_HOTKEY:
                # Activate search bar
                eventCallback()
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageA(ctypes.byref(msg))
    finally:
        user32.UnregisterHotKey(None, 1)







