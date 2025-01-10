import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def select_excel_file(task_name):
    """엑셀 파일 선택 창을 열고 작업 이름을 출력합니다."""
    file_path = filedialog.askopenfilename(
        title=f"{task_name} - 엑셀 파일 선택",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )

    if file_path:
        messagebox.showinfo("파일 선택됨", f"선택한 파일 경로: {file_path}")
    else:
        messagebox.showwarning("파일 없음", "파일을 선택하지 않았습니다.")

def read_excel(file_path):
    """엑셀 파일을 읽어 데이터프레임으로 반환합니다."""
    return pd.read_excel(file_path)

def save_to_excel(data, file_path):
    """데이터프레임을 엑셀 파일로 저장합니다."""
    data.to_excel(file_path, index=False)
