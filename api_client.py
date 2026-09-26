import requests

class ParaBankClient:

    base_url = ""

    def login(self,username, password):
        url = f"{self.base_url}/login/{username}/{password}"
        response = requests.get(url)
        return response 

    def get_account(self, customer_id):
        url = f"{self.base_url}/customers/{customer_id}/accounts"    
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