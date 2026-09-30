import data
import api_client

client = api_client.ParaBankClient()

def test_get_customer_accounts_valid():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    response = client.get_customer_accounts(customer_id)
    assert response.status_code == 200

def test_get_customer_accounts_nonexistent():
    response = client.get_customer_accounts(999999)
    assert response.status_code != 200

def test_get_account_by_id_valid():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    response = client.get_customer_accounts(customer_id)
    account_id = response.json()[0]["id"]
    account_response = client.get_account_by_id(account_id)
    assert account_response.status_code == 200

def test_get_account_by_id_nonexistent():
    response = client.get_account_by_id(999999)
    assert response.status_code != 200
    