import requests

from django.contrib.auth import login

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .functions import validate_microsoft_token


class microsoftOauth2Authentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        access_token = auth_header.split(" ")[1]

        response = validate_microsoft_token(access_token)
        
        if response != "success":
            raise AuthenticationFailed("Invalid or expired Microsoft token")

        userinfo_url = "https://graph.microsoft.com/v1.0/me"

        response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code != 200:
            raise AuthenticationFailed("Invalid or expired Microsoft token")
        
        user_data = response.json()
        email = user_data["mail"] or user_data["userPrincipalName"]

        from django.contrib.auth import get_user_model
        User = get_user_model()
        user, _ = User.objects.get_or_create(username="rmendoza.abd@hotmail.com")

        return (user, access_token)