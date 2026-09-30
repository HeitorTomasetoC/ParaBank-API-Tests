import data
import api_client

client = api_client.ParaBankClient()

def test_transfer_valid_amount():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    accounts_response = client.get_customer_accounts(customer_id)
    from_account_id = accounts_response.json()[0]["id"]
    new_account_response = client.create_account(customer_id, 1, from_account_id)
    to_account_id = new_account_response.json()["id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, data.VALID_AMOUNT)
    account_after = client.get_account_by_id(from_account_id)
    balance_after = account_after.json()["balance"]
    assert balance_after == balance_before - data.VALID_AMOUNT

def test_transfer_negative_amount():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    accounts_response = client.get_customer_accounts(customer_id)
    from_account_id = accounts_response.json()[0]["id"]
    new_account_response = client.create_account(customer_id, 1, from_account_id)
    to_account_id = new_account_response.json()["id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, data.NEGATIVE_AMOUNT)
    assert transfer_response.status_code != 200

def test_transfer_amount_exceeds_balance():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    accounts_response = client.get_customer_accounts(customer_id)
    from_account_id = accounts_response.json()[0]["id"]
    new_account_response = client.create_account(customer_id, 1, from_account_id)
    to_account_id = new_account_response.json()["id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, balance_before + 9999)
    assert transfer_response.status_code != 200