from custom_auth.serializers import UserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'id': user.id,
        'created': user.date_joined,
        'modified': user.modified,
        'last_login': user.last_login,
        'token': token
    }