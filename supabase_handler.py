import json
import os
from supabase import create_client, Client


class SupabaseHandler:

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    def get_supabase_client(self):
        supabase: Client = create_client(self.url, self.key)
        return supabase

    def do_signup(self, email, password):
        supabase = self.get_supabase_client()
        response = supabase.auth.sign_up(
            {
                'email': email,
                'password': password
            }
        )
        return json.loads(response.json())

    def do_login(self, email, password):
        supabase = self.get_supabase_client()
        response = supabase.auth.sign_in_with_password(
            {
                'email': email,
                'password': password
            }
        )
        return json.loads(response.json())


