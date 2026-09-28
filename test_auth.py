import data
import api_client

client = api_client.ParaBankClient()

def test_login_valid_credentials():
    response = client.login(data.USERNAME, data.PASSWORD)
    assert response.status_code == 200
    assert "id" in response.json()

def test_login_wrong_password():
    response = client.login(data.USERNAME, "wrongpassword")
    assert response.status_code == 400
    assert "Invalid" in response.text

def test_login_nonexistent_user():
    response = client.login("nonexistentuser", data.PASSWORD)
    assert response.status_code == 400
    assert "Invalid" in response.text