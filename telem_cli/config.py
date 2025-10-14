import os

DEFAULT_API_URL = "http://127.0.0.1:5000/api"

def get_api_url():
    """Get the base API URL from env or fallback to default."""
    return os.getenv("API_URL", DEFAULT_API_URL)

def get_token_path():
    """Local path to save access token."""
    return os.path.expanduser("~/.telem_token")
