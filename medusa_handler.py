import os

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MedusaHandler:

    def get_backend_url(self):
        return 'http://localhost:9000/'

    def headers(self, access_token):
        return {
            'Authorization': f'Bearer {access_token}',
            'x-publishable-api-key': os.environ.get("MEDUSA_PUBLISHABLE_API_KEY")
        }

    def get_registration_token(self, email, password):
        response = requests.post(
            url=self.get_backend_url() + '/auth/customer/emailpass/register',
            data={
                'email': email,
                'password': password
            },
            verify=False
        )
        return response.json()

    def do_login(self, email, password):
        response = requests.post(
            url=self.get_backend_url() + '/auth/user/emailpass',
            data={
                'email': email,
                'password': password
            },
            verify=False
        )
        return response.json()

    def create_customer(self, access_token, first_name, last_name, email):
        response = requests.post(
            url=self.get_backend_url() + '/store/customers',
            headers=self.headers(access_token),
            data={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            },
            verify=False
        )
        return response.json()

    def get_products(self, access_token):
        response = requests.get(
            url=self.get_backend_url() + '/store/products',
            headers=self.headers(access_token),
            verify=False
        )
        return response.json()
