import tkinter as tk
from tkinter import filedialog, messagebox

def center_window(window):
    """창을 화면 중앙에 배치합니다."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = screen_width // 2 - size[0] // 2
    y = screen_height // 2 - size[1] // 2
    window.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

def set_close_behavior(window, on_close_callback=None, confirm_exit=True):
    """창 닫기 버튼 동작 설정."""
    def on_closing():
        if confirm_exit:
            if messagebox.askokcancel("종료", "프로그램을 종료하시겠습니까?"):
                if on_close_callback:
                    on_close_callback()
                window.destroy()
        else:
            if on_close_callback:
                on_close_callback()
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)