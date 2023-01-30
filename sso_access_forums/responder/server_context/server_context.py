from django.http import HttpRequest
from ...app_settings import JSCONNECT_CLIENT_ID, JSCONNECT_SECRET

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
        username = cls.get_user_forum_username(request.user)
        vanilla_id = cls.generate_vanilla_id(request.user.id)
        
        user_data['uniqueid'] = vanilla_id
        user_data['name'] = username
        user_data['email'] = f"{vanilla_id}@goosegoo.se"
        user_data['photourl'] = ""
        user_data['roles'] = cls.get_user_roles(request.user)

        return user_data

    @classmethod
    def generate_vanilla_id(cls, user_id):
        #Ideally we don't send the plaintext ID, but we'll have to see
        raise NotImplementedError()

    @classmethod
    def get_user_forum_username(cls, user):
        # Either from Services module name format config model or user-specified
        raise NotImplementedError()

    @classmethod
    def get_user_roles(cls, user):
        # Look at AA's admin panel docs for what to set for this.
        raise NotImplementedError()

