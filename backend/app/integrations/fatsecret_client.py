import httpx
import base64
from app.core.config import settings


class FatSecretClient:
    TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
    API_URL = "https://platform.fatsecret.com/rest/server.api"

    def __init__(self):
        self.client_id = settings.FATSECRET_CLIENT_ID
        self.client_secret = settings.FATSECRET_CLIENT_SECRET
        self.access_token = self._get_token()

    def _get_token(self):
        auth = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()

        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}

        response = httpx.post(
            self.TOKEN_URL,
            headers=headers,
            data=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def search_food(self, query: str):
        params = {
            "method": "foods.search",
            "search_expression": query,
            "format": "json"
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = httpx.get(
            self.API_URL,
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
