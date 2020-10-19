import sys
import platform
from typing import Optional

import tkinter as tk
from tkinter import messagebox as mg
from PIL import Image, ImageTk

isWindows = platform.system().lower() == "windows"

if isWindows:
    import ctypes
    import win32api
    import win32event
    from winerror import ERROR_ALREADY_EXISTS


def getImg(name: str, imgDATA: dict) -> Optional[tk.PhotoImage]:
    if name in imgDATA:
        if imgDATA[name][1] is None:
            imgDATA[name][1] = ImageTk.PhotoImage(Image.open(imgDATA[name][0]))
        return imgDATA[name][1]
    return None


def _checkInstance(img: Optional[tk.PhotoImage] = None) -> None:
    if isWindows:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
        _ = win32event.CreateMutex(None, False, "name")
        isAlready = win32api.GetLastError() == ERROR_ALREADY_EXISTS
        if not isAdmin or isAlready:
            msg = tk.Tk()
            msg.withdraw()
            msg.attributes("-topmost", 1)
            msg.title("Error")
            if img != None:
                msg.iconphoto(False, img)
            if not isAdmin:
                mg.showwarning(
                    "Error",
                    "This App requires Administrator Privileges to function properly.\nPlease Retry with Run As Administrator.",
                    parent=msg,
                )
            if isAlready:
                mg.showwarning("Error", "App instance already running.", parent=msg)
            msg.destroy()
            sys.exit(1)
