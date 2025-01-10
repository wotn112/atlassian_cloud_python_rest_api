import logging
from configparser import ConfigParser
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

def load_settings():
    """설정 파일에서 값을 불러옵니다."""
    config = ConfigParser()
    config.read(CONFIG_FILE)
    return {
        "BASE_URL": config.get("DEFAULT", "BASE_URL", fallback=""),
        "USERNAME": config.get("DEFAULT", "USERNAME", fallback=""),
        "USER_TOKEN": config.get("DEFAULT", "USER_TOKEN", fallback=""),
        "ORG_ID": config.get("DEFAULT", "ORG_ID", fallback=""),
        "ORG_TOKEN": config.get("DEFAULT", "ORG_TOKEN", fallback=""),
        "LOG_FILE": config.get("DEFAULT", "LOG_FILE", fallback="logs/application.log"),
    }

def setup_logging():
    """로그 설정"""
    settings = load_settings()
    log_file = settings["LOG_FILE"]

    if not log_file:
        log_file = "logs/application.log"  # 기본 로그 파일 경로 설정

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # 핸들러 생성
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        console_handler = logging.StreamHandler()

        # 포맷터 설정
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 루트 로거에 핸들러 추가
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # 기존 핸들러 제거 후 새로 추가
        if root_logger.hasHandlers():
            root_logger.handlers.clear()
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        logging.info("Logging initialized successfully.")
    except Exception as e:
        print(f"Error initializing logging: {e}")
        raise

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

# 로깅 초기화
setup_logging()
