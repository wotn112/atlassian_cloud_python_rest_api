import tkinter as tk
import os
from pathlib import Path
from tkinter import messagebox
from configparser import ConfigParser
from gui.window_utils import center_window, set_close_behavior


# 실행 디렉토리 기준으로 config 폴더 경로 설정
execution_dir = Path().resolve()  # 실행 파일이 실행되는 디렉터리
config_dir = execution_dir / "config"
config_file = config_dir / "settings.properties"

# config 폴더가 없으면 생성
if not config_dir.exists():
    os.makedirs(config_dir)

CONFIG_FILE = config_file

def load_settings():
    """설정 파일에서 값을 불러옵니다."""
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return {
        "base_url": config.get("DEFAULT", "base_url", fallback=""),
        "username": config.get("DEFAULT", "username", fallback=""),
        "user_token": config.get("DEFAULT", "user_token", fallback=""),
        "org_id": config.get("DEFAULT", "org_id", fallback=""),
        "org_token": config.get("DEFAULT", "org_token", fallback=""),
        "log_file": config.get("DEFAULT", "log_file", fallback=""),
    }

def save_settings_to_file(base_url, username, user_token, org_id, org_token, log_file):
    """설정 값을 파일에 저장합니다."""
    config = ConfigParser()  
    config["DEFAULT"] = {
        "base_url": base_url,
        "username": username,
        "user_token": user_token,
        "org_id": org_id,
        "org_token": org_token,
        "log_file": log_file,
    }
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

def settings_menu(main_window):
    """설정 메뉴 GUI를 생성합니다."""
    settings_window = tk.Toplevel()
    settings_window.title("설정")
    settings_window.geometry("450x450")
    center_window(settings_window)

    settings = load_settings()  # 기존 설정 불러오기

    def save_settings():
        """입력한 설정을 저장."""
        base_url = base_url_entry.get()
        username = username_entry.get()
        user_token = user_token_entry.get()
        org_id = org_id_entry.get()
        org_token = org_token_entry.get()
        log_file = log_file_entry.get()

        save_settings_to_file(base_url, username, user_token, org_id, org_token, log_file)
        messagebox.showinfo("저장 완료", "설정이 저장되었습니다.")

    def close_settings_menu():
        """설정 메뉴 닫기."""
        settings_window.destroy()
        main_window.deiconify()

    set_close_behavior(settings_window, close_settings_menu, False)

    tk.Label(settings_window, text="설정을 입력하세요:", font=("Arial", 14)).pack(pady=10)

    # GUI 필드 매핑
    fields = {
        "base_url": "Base URL",
        "username": "Username",
        "user_token": "User Token",
        "org_id": "Org ID",
        "org_token": "Org Token",
        "log_file": "Log File",
    }

    input_fields = {}
    for key, label in fields.items():
        tk.Label(settings_window, text=f"{label}:").pack(anchor="w", padx=20)
        entry = tk.Entry(settings_window, width=40, show="*" if "token" in key else "")
        entry.insert(0, settings.get(key, ""))  # 정확히 매칭된 키 값 삽입
        entry.pack(pady=5, padx=20)
        input_fields[key] = entry

    # 필드 참조 변수 할당
    base_url_entry = input_fields["base_url"]
    username_entry = input_fields["username"]
    user_token_entry = input_fields["user_token"]
    org_id_entry = input_fields["org_id"]
    org_token_entry = input_fields["org_token"]
    log_file_entry = input_fields["log_file"]

    tk.Button(settings_window, text="저장", width=15, command=save_settings).pack(pady=10)
    tk.Button(settings_window, text="닫기", width=15, command=close_settings_menu).pack(pady=10)
