import base64
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

    def admin_request_headers(self):
        medusa_response = self.do_login(os.environ.get("MEDUSA_ADMIN_EMAIL"), os.environ.get("MEDUSA_ADMIN_PASSWORD"))
        access_token = medusa_response.get('token')
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

    def create_customer(self, first_name, last_name, email, password):
        token_response = self.get_registration_token(email, password)
        if token_response.get('token'):
            access_token = token_response['token']
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

    def generate_customer_password(self, email):
        salt = os.environ.get("PASSWORD_SALT")
        email_salt_combo = f"{email}{salt}"
        string_bytes = email_salt_combo.encode('ascii')
        base64_bytes = base64.b64encode(string_bytes)
        encoded_string = base64_bytes.decode('ascii')
        return encoded_string[:4] + encoded_string[-4:]

    def get_customer_by_email(self, email):
        response = requests.post(
            url=self.get_backend_url() + '/v1/customers?email=' + email,
            headers=self.admin_request_headers(),
            data={
                'email': email
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
