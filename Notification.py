from win32api import *
from win32gui import *
import win32con
import sys, os
import time
from random import randint

class WindowsBalloonTip:

    def __init__(self, title, msg):
        
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"

        # Could also specify a wndproc.
        wc.lpfnWndProc = message_map
        class_atom = RegisterClass(wc)
        
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(
                            class_atom,
                            "Taskbar",
                            style,
                            0, 0,
                            win32con.CW_USEDEFAULT,
                            win32con.CW_USEDEFAULT,
                            0, 0,
                            hinst,
                            None
                        )

        UpdateWindow(self.hwnd)
        
        icon_path_name = os.path.abspath(os.path.join( sys.path[0], "Googleeyes.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        
        try:
            hicon = LoadImage( hinst, icon_path_name, win32con.IMAGE_ICON,  0, 0, icon_flags )
        except Exception as e:
            hicon = LoadIcon( 0, win32con.IDI_APPLICATION )

        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (   
                                self.hwnd,
                                0,
                                NIF_INFO,
                                win32con.WM_USER + 20,
                                hicon,
                                "Balloon tooltip",
                                msg,
                                200,
                                title,
                                NIIF_NOSOUND
                            )
                        )
        
        # self.show_balloon(title, msg)
        time.sleep(5)
        DestroyWindow(self.hwnd)
    
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        
        # Terminate the app.
        PostQuitMessage(0) 

def balloon_tip(title, msg):

    WindowsBalloonTip(title, msg)

if __name__ == '__main__':

    messages = [
        "The time has come when I will have to ask you to move your eyes as constantly staring at your screen would harm them!",
        "It's been 15 minutes!! How could you still be looking at your screen!!",
        "See, Let me shout you this again. MOVE YOUR EYES! STOP STARING AT YOUR SCREEN.",
        "This is the time when you should give your eyes some rest."
    ]

    balloon_tip( "Hey! You studious nerd!", messages[randint(0,len(messages)-1)])