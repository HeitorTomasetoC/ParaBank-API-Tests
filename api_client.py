import requests

class ParaBankClient:

    base_url = ""

    def login(self,username, password):
        url = f"{self.base_url}/login/{username}/{password}"
        response = requests.get(url)
        return response 

    def get_customer_account(self, customer_id):
        url = f"{self.base_url}/customers/{customer_id}/accounts"    
        response = requests.get(url)
        return response

    def get_account_by_id(self, account_id):
        url = f"{self.base_url}/accounts/{account_id}"
        response = requests.get(url)
        return response

    def transfer(self, from_account_id, to_account_id, amount):
        url = f"{self.base_url}/transfer"
        response = requests.post(url, params={
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": amount
        })
        return response

    def create_account(self, customer_id, new_account_type, from_account_id):
        url = f"{self.base_url}/createAccount"
        response = requests.post(url, params={
            "customerId": customer_id,
            "newAccountType": new_account_type,
            "fromAccountId": from_account_id
        })
        return response

    def get_transactions(self, account_id):
        url = f"{self.base_url}/accounts/{account_id}/transactions"
        response = requests.get(url)
        return response

    def request_loan(self, customer_id, amount, down_payment, from_account_id):
        url = f"{self.base_url}/requestLoan"
        response = requests.post(url, params={
            "customerId": customer_id,
            "amount": amount,
            "downPayment": down_payment,
            "fromAccountId": from_account_id
        })
        return response