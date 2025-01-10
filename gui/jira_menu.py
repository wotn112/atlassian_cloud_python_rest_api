import tkinter as tk
from tkinter import messagebox
from gui.window_utils import center_window, set_close_behavior

def jira_menu(main_window):
    """Jira 관리 메뉴를 생성합니다."""
    jira_window = tk.Toplevel()
    jira_window.title("Jira 관리")
    jira_window.geometry("400x250")
    center_window(jira_window)

    def close_jira_menu():
        jira_window.destroy()
        main_window.deiconify()  # 메인 메뉴 다시 표시
    set_close_behavior(jira_window, close_jira_menu, False)
    tk.Label(jira_window, text="Jira 관리 작업을 선택하세요:", font=("Arial", 14)).pack(pady=20)

    tk.Button(jira_window, text="Jira 이슈 추가", width=20, command=lambda: jira_action("Jira 추가")).pack(pady=5)
    tk.Button(jira_window, text="Jira 삭제", width=20, command=lambda: jira_action("Jira 삭제")).pack(pady=5)
    tk.Button(jira_window, text="Jira 목록 조회", width=20, command=lambda: jira_action("Jira 목록 조회")).pack(pady=5)

    tk.Frame(jira_window, height=10).pack()  # 여백 추가
    tk.Button(jira_window, text="닫기", width=15, command=close_jira_menu).pack(pady=10)

def jira_action(action_name):
    """jira 관리 작업을 수행합니다."""
    messagebox.showinfo("jira 관리", f"{action_name} 작업이 선택되었습니다.")
