import os
import requests
from telem_cli.config import get_token_path

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token_path = get_token_path()
        self.token = self._load_token()

    def _load_token(self):
        if os.path.exists(self.token_path):
            with open(self.token_path, "r") as f:
                return f.read().strip()
        return None

    def _save_token(self, token):
        with open(self.token_path, "w") as f:
            f.write(token)

    def _auth_headers(self):
        if not self.token:
            raise RuntimeError("Not authenticated. Please run 'sensor login' first.")
        return {"Authorization": f"Bearer {self.token}"}

    def login(self, email, password):
        res = requests.post(f"{self.base_url}/auth/login", json={
            "email": email,
            "password": password
        })
        res.raise_for_status()
        token = res.json().get("access_token")
        if not token:
            raise RuntimeError("No token received from API.")
        self._save_token(token)
        self.token = token
        return {"status": "success", "token_saved": True}

    def register_sensor(self, type, latitude, longitude, description):
        headers = self._auth_headers()
        res = requests.post(f"{self.base_url}/sensors", json={
            "type": type,
            "latitude": latitude,
            "longitude": longitude,
            "description": description,
        }, headers=headers)
        res.raise_for_status()
        return res.json()
    
    def get_sensor_data(self, sensor_id):
        headers = self._auth_headers()
        res = requests.get(f"{self.base_url}/sensors/{sensor_id}/data", headers=headers)
        res.raise_for_status()
        return res.json()

    def push_sensor_data(self, sensor_id, unit, value):
        headers = self._auth_headers()
        res = requests.post(f"{self.base_url}/sensors/{sensor_id}/data", json={
            "unit": unit,
            "value": value
        }, headers=headers)
        res.raise_for_status()
        return res.json()
