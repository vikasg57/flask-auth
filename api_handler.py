import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApiHandler:

    def get_backend_url(self):
        return 'http://localhost:9000/'

    def headers(self, access_token):
        return {
            'Authorization': f'Bearer {access_token}'
        }

    def create_customer(self, access_token, first_name, last_name, email, password):
        response = requests.post(
            url=self.get_backend_url() + 'v1/customers',
            headers=self.headers(access_token),
            data={
                'password': password,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            },
            verify=False
        )
        print(response)
        return response.json()
