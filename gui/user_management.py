import tkinter as tk
from tkinter import messagebox
from gui.window_utils import center_window, set_close_behavior
from gui.sheet_navigator import SheetNavigator
from modules.user import UserClient
from utils.api_handler import APIClient
from utils.logger import log_info, log_error

def user_management_menu(main_window):
    """유저 관리 메뉴를 생성합니다."""
    user_window = tk.Toplevel()
    user_window.title("유저 관리")
    user_window.geometry("400x250")
    center_window(user_window)

    def close_user_menu():
        user_window.destroy()
        main_window.deiconify()  # 메인 메뉴 다시 표시

    set_close_behavior(user_window, close_user_menu, False)

    tk.Label(user_window, text="유저 관리 작업을 선택하세요:", font=("Arial", 14)).pack(pady=20)

    tk.Button(user_window, text="유저 추가", width=20, command=lambda: show_user_add_view(user_window)).pack(pady=5)
   #tk.Button(user_window, text="유저 삭제", width=20, command=lambda: user_action("유저 삭제")).pack(pady=5)
    tk.Button(user_window, text="유저 목록 조회", width=20, command=lambda: show_user_list_view(user_window)).pack(pady=5)

    tk.Frame(user_window, height=10).pack()  # 여백 추가
    tk.Button(user_window, text="닫기", width=15, command=close_user_menu).pack(pady=10)

def show_user_add_view(parent_window):
    """유저 추가 뷰."""
    add_window = tk.Toplevel()
    add_window.title("유저 추가")
    add_window.geometry("800x550")
    center_window(add_window)

    def close_add_view():
        add_window.destroy()
        parent_window.deiconify()

    set_close_behavior(add_window, close_add_view, False)

    tk.Label(add_window, text="유저 및 그룹 추가", font=("Arial", 14)).pack(pady=10)

    # SheetNavigator 삽입
    sheet = SheetNavigator(add_window, headers=["유저 이메일", "그룹1", "그룹2", "그룹3"], rows=20)
    sheet.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    def process_user_creation(email, groups):
        """사용자 생성 및 그룹 추가 처리."""
        try:
            api_client = APIClient()
            user_client = UserClient(api_client)

            # 이메일로 사용자 존재 확인
            account_id = user_client.search_user_by_email(email, auth_type="user")
            if account_id:
                messagebox.showinfo("확인", f"사용자가 이미 존재합니다: {email}")
                return

            # 사용자 생성
            created_user = user_client.create_user(email)
            account_id = created_user.get("accountId")
            if not account_id:
                log_error(f"Failed to create user: {email}")
                messagebox.showerror("오류", f"사용자 생성에 실패했습니다: {email}")
                return

            # 그룹 추가
            for group in groups:
                if group.strip():  # 그룹명이 비어 있지 않을 때만 추가
                    user_client.add_user_to_group(account_id, group)
                    log_info(f"User {email} added to group {group}")

            messagebox.showinfo("성공", f"{email} 사용자가 성공적으로 추가되고 그룹에 할당되었습니다.")
        except Exception as e:
            log_error(f"Error processing user {email}: {e}")
            messagebox.showerror("오류", f"{email} 사용자를 처리하는 중 오류가 발생했습니다: {e}")

    def add_user_to_groups(email, groups):
        """이메일을 통해 사용자 그룹에 추가."""
        try:
            api_client = APIClient()
            user_client = UserClient(api_client)

            # 이메일로 accountId 검색
            account_id = user_client.search_user_by_email(email, auth_type="user")
            if not account_id:
                messagebox.showerror("오류", f"사용자를 찾을 수 없습니다: {email}")
                return

            # 그룹 추가
            for group in groups:
                if group.strip():  # 그룹명이 비어 있지 않을 때만 추가
                    user_client.add_user_to_group(account_id, group)
                    log_info(f"User {email} added to group {group}")
            messagebox.showinfo("성공", f"{email} 사용자가 그룹 {', '.join(groups)}에 추가되었습니다.")
        except Exception as e:
            log_error(f"Error adding user {email} to groups: {e}")
            messagebox.showerror("오류", f"{email} 사용자를 그룹에 추가하는 데 실패했습니다: {e}")

    def only_group_add():
        """기존 이메일을 기준으로 그룹에만 추가."""
        data = sheet.get_data()
        for row in data:
            email = row[0].strip()
            groups = row[1:]  # 첫 번째 열 이후는 그룹 목록
            if email:  # 이메일이 비어 있지 않을 때만 처리
                add_user_to_groups(email, groups)

    def add_users():
        """이메일 및 그룹 데이터를 기반으로 사용자 추가."""
        data = sheet.get_data()
        for row in data:
            email = row[0]
            groups = row[1:]
            if email:  # 이메일이 비어 있지 않을 때만 처리
                process_user_creation(email, groups)

    def resend_invitations():
        """사용자를 강제로 생성하고 그룹에 추가."""
        data = sheet.get_data()
        for row in data:
            email = row[0]
            groups = row[1:]
            if email:  # 이메일이 비어 있지 않을 때만 처리
                try:
                    api_client = APIClient()
                    user_client = UserClient(api_client)

                    # 사용자 생성
                    created_user = user_client.create_user(email)
                    account_id = created_user.get("accountId")

                    if not account_id:
                        log_error(f"Failed to create user for resend: {email}")
                        continue

                    # 그룹 추가
                    for group in groups:
                        if group.strip():  # 그룹명이 비어 있지 않을 때만 추가
                            user_client.add_user_to_group(account_id, group)

                    log_info(f"Resent invitation and added {email} to groups {groups}")
                    messagebox.showinfo("성공", f"{email}로 초대 메일이 재전송되고 그룹에 추가되었습니다.")
                except Exception as e:
                    log_error(f"Error resending invitation to {email}: {e}")
                    messagebox.showerror("오류", f"{email}로 초대 메일을 재전송하는 중 오류가 발생했습니다: {e}")

    # 버튼 추가
    tk.Button(add_window, text="추가", width=15, command=add_users).pack(pady=5)
    tk.Button(add_window, text="추가(재전송)", width=15, command=resend_invitations).pack(pady=5)
    tk.Button(add_window, text="그룹 추가", width=15, command=only_group_add).pack(pady=5)
    tk.Button(add_window, text="닫기", width=15, command=close_add_view).pack(pady=10)


def show_user_list_view(parent_window):
    """유저 목록 조회 뷰."""
    list_window = tk.Toplevel()
    list_window.title("유저 목록")
    list_window.geometry("800x600")
    center_window(list_window)

    def close_list_view():
        list_window.destroy()
        parent_window.deiconify()

    set_close_behavior(list_window, close_list_view, False)

    tk.Label(list_window, text="유저 목록", font=("Arial", 14)).pack(pady=10)

    # SheetNavigator 삽입
    sheet = SheetNavigator(
        list_window,
        headers=["AccountId", "DisplayName", "EmailAddress", "Active", "TimeZone", "Groups"],
        rows=0
    )
    sheet.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def fetch_users():
        """유저 데이터를 한 줄씩 시트에 추가."""
        try:
            api_client = APIClient()
            user_client = UserClient(api_client)
            users = user_client.get_all_users()
            
            if not users:
                log_info("No users found.")
                messagebox.showinfo("정보", "조회된 유저가 없습니다.")
                return

            # 시트 초기화
            sheet.clear_sheet()  # 기존 데이터를 제거하여 중복 방지

            for user in users:
                try:
                    # 기본 필드 처리
                    account_id = user.get("accountId", "")
                    display_name = user.get("displayName", "N/A")
                    email_address = user.get("emailAddress", "N/A")
                    active = str(user.get("active", ""))
                    time_zone = user.get("timeZone", "N/A")

                    # 프로필 정보 조회
                    profile = user_client.get_user_profile(account_id)
                    groups = profile.get("groups", {}).get("items", [])
                    groups_str = ", ".join(group.get("name", "Unknown") for group in groups if isinstance(group, dict))

                    # 각 유저 데이터를 행으로 변환
                    row_data = [
                        account_id,
                        display_name,
                        email_address,
                        active,
                        time_zone,
                        groups_str
                    ]
                    print("추가할 데이터 행:", row_data)  # 디버깅용 출력

                    # 시트에 데이터 추가
                    sheet.insert_row(row_data)  # 기존 add_row 대신 insert_row 사용
                except Exception as e:
                    log_error(f"Error processing user {account_id}: {e}")
                    continue

            messagebox.showinfo("완료", "모든 유저 정보를 불러왔습니다.")
        except Exception as e:
            log_error(f"Error fetching users: {e}")
            messagebox.showerror("Error", f"유저 목록을 가져오는 데 실패했습니다.\n{e}")
    import threading

    def fetch_users_async():
        threading.Thread(target=fetch_users).start()

    # 버튼으로 유저 불러오기
    tk.Button(list_window, text="유저 불러오기", width=15, command=fetch_users_async).pack(pady=10)
    tk.Button(list_window, text="닫기", width=15, command=close_list_view).pack(pady=10)


def user_action(action_name):
    """유저 관리 작업을 수행합니다."""
    messagebox.showinfo("유저 관리", f"{action_name} 작업이 선택되었습니다.")
