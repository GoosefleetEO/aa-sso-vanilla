from cryptography.fernet import Fernet

from django.http import HttpRequest

from ...app_settings import JSCONNECT_CLIENT_ID, JSCONNECT_SECRET, ENCRYPTION_SECRET

class ServerContext:
    def __init__(self, user_data):
        self.user_data = user_data
        self.client_id = JSCONNECT_CLIENT_ID
        self.secret = JSCONNECT_SECRET

    @classmethod
    def get_server_context(cls, request: HttpRequest):
        user_data = {}

        if request.user.is_authenticated():
            cls._populate_user_data(user_data)

        return cls(user_data)

    @classmethod
    def _populate_user_data(cls, request: HttpRequest, user_data: dict):
        fernet_system = Fernet(ENCRYPTION_SECRET)
        vanilla_id = fernet_system.encrypt(request.user.id)
        
        user_data['uniqueid'] = vanilla_id
        user_data['name'] = request.user.username
        user_data['email'] = f"{vanilla_id}@goosegoo.se"
        user_data['photourl'] = ""
        user_data['roles'] = request.user.groups.order_by("name")

        return user_data