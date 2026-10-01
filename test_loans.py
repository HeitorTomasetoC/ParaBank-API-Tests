import api_client
import data

client = api_client.ParaBankClient()

def test_request_loan_valid():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    accounts_response = client.get_customer_accounts(customer_id)
    from_account_id = accounts_response.json()[0]["id"]
    loan_response = client.request_loan(customer_id, 500, 100, from_account_id)
    assert loan_response.status_code == 200
    assert "approved" in loan_response.json()

def test_request_loan_payment_exceeds_amount():
    login_response = client.login(data.USERNAME, data.PASSWORD)
    customer_id = login_response.json()["id"]
    accounts_response = client.get_customer_accounts(customer_id)
    from_account_id = accounts_response.json()[0]["id"]
    loan_response = client.request_loan(customer_id, 100, 500, from_account_id)
    if loan_response.status_code == 200:
        assert loan_reponse.json().get("approved") == False
    else:
        assert loan_response.status_code != 200

