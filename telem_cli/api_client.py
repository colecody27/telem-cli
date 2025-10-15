import os
import requests
from telem_cli.config import get_token_path

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token_path = get_token_path()
        self.token = self._load_token()

    ################ AUTHENTICATION ####################
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

    ################ USERS ####################
    def login(self, username, password):
        res = requests.post(f"{self.base_url}/auth/login", json={
            "username": username,
            "password": password
        })
        res.raise_for_status()
        token = res.json().get("access_token")
        if not token:
            raise RuntimeError("No token received from API.")
        self._save_token(token)
        self.token = token
        return {"status": "success", "token_saved": True}
    
    def register(self, email, username, password):
        res = requests.post(f"{self.base_url}/auth/register", json={
            "email": email,
            "username": username,
            "password": password
        })
        res.raise_for_status()
        return res.json()

    ################ SENSORS ####################
    def register_sensor(self, type, latitude, longitude, description, is_active):
        headers = self._auth_headers()
        res = requests.post(f"{self.base_url}/sensors", json={
            "type": type,
            "latitude": latitude,
            "longitude": longitude,
            "description": description,
            "is_active": is_active,
        }, headers=headers)
        res.raise_for_status()
        return res.json()
    
    def update_sensor(self, sensor_id, type, latitude, longitude, is_active, description):
        headers = self._auth_headers()
        res = requests.put(f"{self.base_url}/sensors/{sensor_id}", json={
            "type": type,
            "latitude": latitude,
            "longitude": longitude,
            "description": description,
            "is_active": is_active,
        }, headers=headers)
        res.raise_for_status()
        return res.json()
    
    def get_sensor(self, sensor_id):
        headers = self._auth_headers()
        res = requests.get(f"{self.base_url}/sensors/{sensor_id}", headers=headers)
        res.raise_for_status()
        return res.json()
    
    def get_sensors(self):
        headers = self._auth_headers()
        res = requests.get(f"{self.base_url}/sensors", headers=headers)
        res.raise_for_status()
        return res.json()
    
    ################ DATA ####################
    def get_sensor_data(self, sensor_id):
        headers = self._auth_headers()
        res = requests.get(f"{self.base_url}/sensors/{sensor_id}/data", headers=headers)
        res.raise_for_status()
        return res.json()

    def push_sensor_data(self, sensor_id, data):
        headers = self._auth_headers()
        res = requests.post(f"{self.base_url}/sensors/{sensor_id}/data", json=data, headers=headers)
        res.raise_for_status()
        return res.json()
