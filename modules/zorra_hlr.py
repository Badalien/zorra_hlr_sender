import requests
import json


class ZorraHLR:

    def __init__(self, user_email: str, user_password: str) -> None:
        self.email = user_email
        self.password = user_password
        self.zorra_hlr_url = 'http://module.hlr.zorra.com/api/v1/'
        self.zorra_core_url = 'https://my.zorra.com/api/'
        self.token = None
        self.user_id = None
        pass

    def get_token(self) -> None:
        method = 'auth/login'
        url = self.zorra_core_url + method
        payload = {'email': self.email, 'password': self.password}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            self.token = response.json()['access_token']
        else:
            print('Error on login: ')
            print(response.text)
            print('Check your credentials.')
            return None

    def get_user_id(self) -> None:
        method = 'auth/me'
        url = self.zorra_core_url + method
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.post(url, headers=headers)
        if response.status_code == 200:        
            self.user_id = response.json()['id']
        else:
            print('Error on getting user id: ')
            print(response.text)
            return None

    def send_hlr(self, method: str, phone_number: str) -> str:
        if self.token is None:
            self.get_token()
        url = self.zorra_hlr_url + method
        payload = json.dumps({
            "numbers": [
                f'{phone_number}'
            ]
        })
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('Error on sending HLR: ')
            print(response.text)
            return None

    def send_hlr_instant(self, phone_number: str) -> str:
        method = "lookups/instant"
        return self.send_hlr(method, phone_number)

    def send_hlr_background(self, phone_number: str) -> str:
        method = "lookups/background"
        result = self.send_hlr(method, phone_number)
        if result:
            return result['request_id']
        else:
            return None

    def get_hlr_stat(self, limit: int, date_from: str, request_id: str = None) -> list:  # noqa: E501
        if self.token is None:
            self.get_token()
        if self.user_id is None:
            self.get_user_id()

        method = 'stats/detailed'
        url = self.zorra_hlr_url + method
        payload = {
            "client_id": self.user_id,
            "sort_column": "id",
            "sort_direction": "desc",
            "items_per_page": limit,
            "date_from": date_from,
        }
        if request_id:
            payload['request_id'] = request_id
        payload = json.dumps(payload)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        print(url)
        print(payload)
        response = requests.get(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['data'][0]
        else:
            print('Error on getting HLR stat: ')
            print(response.text)
            return None

    def get_stat_by_id(self, request_id: int) -> str:
        if self.token is None:
            self.get_token()
        if self.user_id is None:
            self.get_user_id()

        method = 'stats/detailed'
        url = self.zorra_hlr_url + method
        payload = {
            "client_id": self.user_id,
            "request_id": request_id
        }
        payload = json.dumps(payload)
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['data'][0]
        else:
            print('Error on getting HLR stat: ')
            print(response.text)
            return None
