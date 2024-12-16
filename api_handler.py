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

    def validate_access_token(self, access_token):
        response = requests.get(
            url=self.get_backend_url() + 'v1/validate-token',
            headers=self.headers(access_token),
            verify=False
        )
        print(response)
        return response.json()
