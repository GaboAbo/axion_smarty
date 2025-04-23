import os
from dotenv import load_dotenv

from django.shortcuts import redirect
from django.http import HttpRequest, JsonResponse
from rest_framework.exceptions import AuthenticationFailed

from msal import PublicClientApplication

from .validation import validate_microsoft_token

load_dotenv()

# Environment Variables
TENANT = os.getenv("MICROSOFT_TENANT", "")
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "")
REDIRECT_URI_MOBILE = os.getenv("MICROSOFT_REDIRECT_URI_MOBILE", "")

# Singleton Instances
_public_client = None


def set_public_client() -> None:
    global _public_client

    if _public_client is None:
        _public_client = PublicClientApplication(CLIENT_ID, authority=TENANT)
    

def get_flow(request):
    set_public_client()
    auth_flow = _public_client.initiate_device_flow(
        scopes=[f"api://{CLIENT_ID}/User.Read"],
    )
    return JsonResponse(auth_flow)


def get_auth_uri(request: HttpRequest):
    auth_flow = get_flow(request)

    user_code = auth_flow.get("user_code")

    request.session["auth_flow"] = auth_flow

    return JsonResponse({"auth_url": "https://microsoft.com/devicelogin", "user_code": user_code})


def get_token(request: HttpRequest):
    claims_challenge = request.data
    auth_flow = request.session.get("auth_flow")

    if claims_challenge and auth_flow:
        response = _public_client.acquire_token_by_device_flow(
            flow=auth_flow,
            claims_challenge=claims_challenge
        )

        if response:
            access_token = response.get("access_token")
            try:
                decoded_token = validate_microsoft_token(access_token)
                credentials = {
                    "decoded_token": decoded_token,
                    "user_email": decoded_token.get("preferred_username"),
                    "full_name": decoded_token.get("name"),
                    "refresh_token": response.get("refresh_token"),
                    "expires_in": response.get("expires_in"),
                }
                return credentials
            except AuthenticationFailed as e:
                print(e)
                return JsonResponse({'error': 'Error al validar el token'}, status=400)

    