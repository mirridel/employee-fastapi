import pytest
import requests

url = "http://localhost:8000/token"


@pytest.fixture()
def get_token(username: str, password: str):
    response = requests.post(url, data={"grant_type": "password",
                                        "username": username,
                                        "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    return None
