import requests
import pytest

# RUN TEST
# pytest test_token.py
# RUN TEST WITH OUTPUT
# pytest test_token.py -s

url = "http://localhost:8000/users/me/promotion/"

test_data = [
    ("username1", "password1", 200),
    ("username2", "password2", 200),
    ("charlie", "password3", 401),
    ("dave", "password4", 401),
    ("", "", 401)
]


@pytest.mark.parametrize("username,password,expected_status_code", test_data)
def test_get_token(username, password, get_token, expected_status_code):
    headers = {"Authorization": "Bearer {}".format(get_token)}
    response = requests.get(url, headers=headers)

    print(response.status_code)
    print(response.headers)
    print(response.json())

    assert response.status_code == expected_status_code
    if response.status_code == 200:
        assert "id" in response.json()
        assert "employee_id" in response.json()
        assert "created_at" in response.json()
        assert "received_at" in response.json()
        assert "is_received" in response.json()
