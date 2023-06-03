import requests
import pytest

# RUN TEST
# pytest test_token.py
# pytest test_token.py -s
from fastapi.security import OAuth2PasswordRequestForm

url = "http://localhost:8000/token"

test_data = [
    ("username1", "password1", 200),
    ("username2", "password2", 200),
    ("charlie", "password3", 401),
    ("dave", "password4", 401),
    ("", "", 422)
]


@pytest.mark.parametrize("username,password,expected_status_code", test_data)
def test_get_token(username, password, expected_status_code):
    response = requests.post(url, data={"grant_type": "password",
                                        "username": username,
                                        "password": password})

    print(response.status_code)
    print(response.headers)
    print(response.json())

    assert response.status_code == expected_status_code
    if response.status_code == 200:
        assert "access_token" in response.json()
