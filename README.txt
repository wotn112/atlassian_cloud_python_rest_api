# My Project

이 프로젝트는 Python과 Tkinter를 사용하여 Atlassian Cloud 제품(Jira, Confluence 등)의 사용자와 그룹을 관리할 수 있는 데스크톱 애플리케이션입니다. 엑셀 스타일의 인터페이스를 제공하며, API를 통해 Atlassian 서비스와 연동합니다.

---

## 주요 기능

- **사용자 관리**:
  - 이메일을 통해 사용자 추가.
  - 사용자를 여러 그룹에 할당.
  - 사용자 초대 메일 재전송.
- **그룹 관리**:
  - 이메일 주소를 사용하여 사용자 그룹 추가.
- **설정 관리**:
  - API 토큰, Base URL, 로그 설정을 설정 메뉴에서 관리.
- **엑셀 스타일 인터페이스**:
  - `SheetNavigator`를 활용한 직관적인 그리드 UI.
- **로그 관리**:
  - 애플리케이션 로그가 `logs` 폴더에 저장.

---

## 설치 방법

```bash
# Python 3.11 이상 설치 필요
pip install -r requirements.txt

# PyInstaller 설치
pip install pyinstaller

# 애플리케이션 실행
python app.py

# 실행 파일 빌드
pyinstaller --onefile --add-data "config/*:config" --add-data "data/*:data" --add-data "gui/*:gui" --add-data "modules/*:modules" --add-data "utils/*:utils" --noconsole app.py
