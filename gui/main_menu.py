import tkinter as tk
from tkinter import filedialog, messagebox
from gui.user_management import user_management_menu
from gui.jira_menu import jira_menu
from gui.settings_menu import settings_menu
from gui.window_utils import center_window, set_close_behavior
from utils.excel_handler import select_excel_file

def main_menu():
    """메인 메뉴 GUI를 생성합니다."""
    root = tk.Tk()
    root.title("Atlassian Cloud 관리 프로그램")
    root.geometry("400x250")
    center_window(root)

    def show_user_management_menu():
        root.withdraw()  # 메인 메뉴 숨기기
        user_management_menu(root)

    def show_jira_menu():
        root.withdraw()  # 메인 메뉴 숨기기
        jira_menu(root)

    def show_settings_menu():
        root.withdraw()  # 메인 메뉴 숨기기
        settings_menu(root)

    tk.Label(root, text="Atlassian 관리 작업을 선택하세요:", font=("Arial", 14)).pack(pady=20)

    #tk.Button(root, text="Jira 작업 관리", width=20, command=show_jira_menu).pack(pady=5)
    #tk.Button(root, text="Confluence 관리", width=20, command=lambda: select_excel_file("Confluence 관리")).pack(pady=5)
    tk.Button(root, text="유저 관리", width=20, command=show_user_management_menu).pack(pady=5)
    tk.Button(root, text="설정", width=20, command=show_settings_menu).pack(pady=5)
    tk.Button(root, text="종료", width=20, command=root.destroy).pack(pady=5)

    root.mainloop()
