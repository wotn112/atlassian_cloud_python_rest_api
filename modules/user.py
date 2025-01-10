from utils.api_handler import APIClient
from utils.logger import log_info, log_error

class UserClient:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_all_users(self):
        """
        모든 유저를 조회합니다.
        Atlassian REST API를 사용하여 페이지네이션을 처리합니다.
        """
        endpoint = "rest/api/3/users/search"
        all_users = []
        start_at = 0
        max_results = 100

        while True:
            params = {
                "startAt": start_at,
                "maxResults": max_results,
            }
            response = self.api_client.send_request("GET", endpoint, params=params)

            if not response:
                log_error(f"Failed to fetch users at startAt: {start_at}")
                break

            all_users.extend(response)

            if len(response) < max_results:
                break

            start_at += max_results

        log_info(f"Fetched {len(all_users)} users from the API.")
        return all_users

    def search_user_by_email(self, email, auth_type="user"):
        """
        이메일로 accountId를 검색합니다.
        """
        endpoint = f"rest/api/2/user/search?query={email}"
        response = self.api_client.send_request("GET", endpoint, auth_type=auth_type)

        if not response:
            log_error(f"No user found with email: {email}")
            return None

        log_info(f"User found for email {email}: {response[0].get('accountId')}")
        return response[0].get("accountId")

    def create_user(self, email):
        """사용자를 생성합니다."""
        try:
            endpoint = "rest/api/3/user"
            payload = {
                "emailAddress": email,
                "products": []  # 빈 배열로 설정
            }
            response = self.api_client.send_request(
                method="POST",
                endpoint=endpoint,
                body=payload,
                auth_type="user"
            )
            log_info(f"User created successfully: {email}")
            print(response)
            return response  # Created user details returned
        except Exception as e:
            log_error(f"Failed to create user {email}: {e}")
            raise
    def add_user_to_group(self, account_id, group_name):
        """사용자를 그룹에 추가합니다."""
        try:
            endpoint = f"rest/api/3/group/user?groupname={group_name}"
            payload = {
                "accountId": account_id
            }
            response = self.api_client.send_request(
                method="POST",
                endpoint=endpoint,
                body=payload,
                auth_type="user"
            )
            log_info(f"User {account_id} added to group {group_name}")
            return response
        except Exception as e:
            log_error(f"Failed to add user {account_id} to group {group_name}: {e}")
            raise
        
    def get_user_profile(self, account_id, auth_type="org"):
        """
        사용자의 프로필 정보를 accountId를 기반으로 가져옵니다.
        """
        #account_id = account_id.split(":")[-1]
        endpoint = f"users/{account_id}/manage/profile"
        try:
            response = self.api_client.send_request("GET", endpoint, auth_type="org")
            if not response:
                log_error(f"Failed to retrieve profile for accountId: {account_id}")
                raise Exception(f"Profile retrieval failed for account ID: {account_id}")
            log_info(f"Successfully retrieved profile for account ID: {account_id}")
            return response
        except Exception as e:
            log_error(f"Error retrieving user profile for account ID {account_id}: {e}")
            raise        
