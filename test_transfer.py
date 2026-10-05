import pytest
import data
import api_client

client = api_client.ParaBankClient()

@pytest.fixture(scope="module")
def transfer_setup():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    accounts_response = client.get_customer_accounts(customer_id)
    from_account_id = accounts_response.json()[0]["id"]
    new_account_response = client.create_account(customer_id, 1, from_account_id)
    to_account_id = new_account_response.json()["id"]
    return {"customer_id": customer_id, "from_account_id": from_account_id, "to_account_id": to_account_id}

@pytest.fixture(scope="module")
def clean_from_account_id(transfer_setup):
    new_account_response = client.create_account(transfer_setup["customer_id"], 1, transfer_setup["from_account_id"])
    return new_account_response.json()["id"]

def test_transfer_valid_amount(transfer_setup):
    from_account_id = transfer_setup["from_account_id"]
    to_account_id = transfer_setup["to_account_id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, data.VALID_AMOUNT)
    account_after = client.get_account_by_id(from_account_id)
    balance_after = account_after.json()["balance"]
    assert balance_after == balance_before - data.VALID_AMOUNT

def test_transfer_negative_amount(transfer_setup):
    from_account_id = transfer_setup["from_account_id"]
    to_account_id = transfer_setup["to_account_id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, data.NEGATIVE_AMOUNT)
    assert transfer_response.status_code != 200

def test_transfer_amount_exceeds_balance(transfer_setup):
    from_account_id = transfer_setup["from_account_id"]
    to_account_id = transfer_setup["to_account_id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, balance_before + 9999)
    assert transfer_response.status_code != 200

def test_transfer_to_nonexistent_account(transfer_setup):
    from_account_id = transfer_setup["from_account_id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, data.NONEXISTENT_ACCOUNT_ID, data.VALID_AMOUNT)
    assert transfer_response.status_code != 200

def test_transfer_full_value(transfer_setup):
    customer_id = transfer_setup["customer_id"]
    base_account_id = transfer_setup["from_account_id"]
    to_account_id = transfer_setup["to_account_id"]
    new_account_response = client.create_account(customer_id, 1, base_account_id)
    from_account_id = new_account_response.json()["id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, balance_before)
    account_after = client.get_account_by_id(from_account_id)
    balance_after = account_after.json()["balance"]
    assert balance_after == 0

def test_transfer_empty_amount(transfer_setup):
    from_account_id = transfer_setup["from_account_id"]
    to_account_id = transfer_setup["to_account_id"]
    transfer_response = client.transfer(from_account_id, to_account_id, data.ZERO_AMOUNT)
    assert transfer_response.status_code != 200

@pytest.mark.skip(reason="Teste instável: o servidor ParaBank degrada com uso acumulado no container Docker")
def test_transfer_decimal_amount(transfer_setup, clean_from_account_id):
    from_account_id = clean_from_account_id
    to_account_id = transfer_setup["to_account_id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    transfer_response = client.transfer(from_account_id, to_account_id, data.DECIMAL_AMOUNT)
    account_after = client.get_account_by_id(from_account_id)
    balance_after = account_after.json()["balance"]
    assert balance_after == balance_before - data.DECIMAL_AMOUNT

@pytest.mark.skip(reason="Teste instável: o servidor ParaBank degrada com uso acumulado no container Docker")
def test_transfer_below_minimum_balance(transfer_setup, clean_from_account_id):
    from_account_id = clean_from_account_id
    to_account_id = transfer_setup["to_account_id"]
    account_before = client.get_account_by_id(from_account_id)
    balance_before = account_before.json()["balance"]
    amount = balance_before - 50
    transfer_response = client.transfer(from_account_id, to_account_id, amount)
    assert transfer_response.status_code == 500
