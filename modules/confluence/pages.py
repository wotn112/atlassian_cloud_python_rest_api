from utils.api_handler import send_request
from utils.logger import log_info

def create_page(space_key, title, content):
    endpoint = "/wiki/rest/api/content"
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {"storage": {"value": content, "representation": "storage"}}
    }
    response = send_request(endpoint, method="POST", payload=payload)
    log_info(f"Page created: {response['id']}")
    return response