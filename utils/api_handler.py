import requests
import base64
from configparser import ConfigParser
from utils.logger import log_info, log_error
import os
from pathlib import Path
# 실행 디렉토리 기준으로 config 폴더 경로 설정
execution_dir = Path().resolve()  # 실행 파일이 실행되는 디렉터리
config_dir = execution_dir / "config"
config_file = config_dir / "settings.properties"

# config 폴더가 없으면 생성
if not config_dir.exists():
    os.makedirs(config_dir)

CONFIG_FILE = config_file

class APIClient:
    def __init__(self):
        self.settings = self._load_settings()
        self.base_url = self.settings["BASE_URL"]
        self.user_token = self.settings["USER_TOKEN"]
        self.org_id = self.settings["ORG_ID"]
        self.org_token = self.settings["ORG_TOKEN"]
        self.username = self.settings["USERNAME"]

        # 설정값 유효성 검증
        self._validate_settings()

    @staticmethod
    def _load_settings():
        """설정 파일에서 값을 불러옵니다."""
        config = ConfigParser()
        config.read(CONFIG_FILE)
        return {
            "BASE_URL": config.get("DEFAULT", "BASE_URL", fallback=""),
            "USERNAME": config.get("DEFAULT", "USERNAME", fallback=""),
            "USER_TOKEN": config.get("DEFAULT", "USER_TOKEN", fallback=""),
            "ORG_ID": config.get("DEFAULT", "ORG_ID", fallback=""),
            "ORG_TOKEN": config.get("DEFAULT", "ORG_TOKEN", fallback=""),
            "LOG_FILE": config.get("DEFAULT", "LOG_FILE", fallback=""),
        }

    def _validate_settings(self):
        """필수 설정값 유효성 검증."""
        missing_settings = [
            key for key, value in self.settings.items() 
            if not value and key in ["BASE_URL", "USERNAME", "USER_TOKEN"]
        ]
        if missing_settings:
            error_message = f"필수 설정값이 누락되었습니다: {', '.join(missing_settings)}"
            log_error(error_message)
            raise ValueError(error_message)

    def _encode_credentials(self):
        """사용자 이름과 토큰을 Base64로 인코딩."""
        auth_string = f"{self.username}:{self.user_token}"
        return base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    def _get_auth_header(self, auth_type="user"):
        """인증 헤더를 생성합니다."""
        authHearder = "Basic"
        if auth_type == "user":
            authHearder = "Basic"
            credentials = self._encode_credentials()
        elif auth_type == "org":
            authHearder = "Bearer"
            credentials = self.org_token
        else:
            raise ValueError("Invalid auth type. Use 'user' or 'org'.")
        return {"Authorization": f"{authHearder} {credentials}", "Content-Type": "application/json;chartset=utf-8", 'Accept': 'application/json'}

    def build_url(self, endpoint, auth_type="user"):
        """기본 URL에 엔드포인트를 추가하여 URL을 생성합니다."""
        # auth_type에 따라 base_url 선택
        base_url = self.base_url if auth_type == "user" else "https://api.atlassian.com"

        if not base_url.endswith("/"):
            base_url += "/"

        return f"{base_url}{endpoint}"

    def send_request(self, method, endpoint, params=None, body=None, auth_type="user"):
        """API 요청 처리 메서드."""
        url = self.build_url(endpoint, auth_type)
        headers = self._get_auth_header(auth_type)
        
        log_info(f"Sending {method} request to {url} with params={params}, body={body}.")
        try:
            response = requests.request(method, url, headers=headers, params=params, json=body)
            response.raise_for_status()
            log_info(f"Response received: {response.status_code}")
            return response.json()
        except requests.RequestException as e:
            log_error(f"Error during {method} request to {url}: {e}")
            raise
