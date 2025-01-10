from utils.api_handler import send_request
from utils.logger import log_info

def create_issue(project_key, summary, issue_type="Task"):
    endpoint = "/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": issue_type},
        }
    }
    response = send_request(endpoint, method="POST", payload=payload)
    log_info(f"Issue created: {response['key']}")
    return response