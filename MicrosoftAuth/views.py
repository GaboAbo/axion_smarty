import os
from dotenv import load_dotenv

from msal import ConfidentialClientApplication

from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .functions import validate_microsoft_token

from AuthUser.models import Engineer

from rest_framework.exceptions import AuthenticationFailed

load_dotenv()

# Environment Variables
TENANT = os.getenv("MICROSOFT_TENANT", "")
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("MICROSOFT_REDIRECT_URI", "")

_confidential_client = None


def set_client():
    global _confidential_client
    if _confidential_client is None:
        _confidential_client = ConfidentialClientApplication(
            CLIENT_ID,
            CLIENT_SECRET,
            authority=TENANT,
        )
    return _confidential_client


def microsoft_login(request: HttpRequest) -> HttpResponseRedirect:
    """
    Initiates the Microsoft OAuth2 login flow based on the application type.
    Selects between ConfidentialClientApplication or PublicClientApplication 
    depending on the app_type parameter.

    Args:
        request (HttpRequest): The Django HTTP request object.
        app_type (str): The type of the application. Use 'server' for server-side apps
                        (ConfidentialClientApplication) or 'mobile' for client-side apps
                        (PublicClientApplication). Default is 'server'.

    Returns:
        JsonResponse: A JSON response containing the authorization URL.

    Raises:
        KeyError: If required environment variables are missing.

    Notes:
        - Ensure `MICROSOFT_CLIENT_ID`, `MICROSOFT_CLIENT_SECRET`, and `MICROSOFT_TENANT` are set in the environment.
        - `server` app type requires `ConfidentialClientApplication` (with client secret).
        - `mobile` app type uses `PublicClientApplication` (no client secret).
        - The `auth_flow` stored in the session should not contain sensitive information.
        - Consider storing the redirect URI in an environment variable instead of hardcoding it.
    """   
    _confidential_client = set_client()
    auth_flow = _confidential_client.initiate_auth_code_flow(
        scopes=[f"api://{CLIENT_ID}/User.Read"],
        redirect_uri=REDIRECT_URI,
    )

    auth_url = auth_flow.get("auth_uri")

    request.session["auth_flow"] = auth_flow

    return redirect(auth_url)


def microsoft_callback(request):
    _confidential_client = set_client()
    auth_flow = request.session.get("auth_flow")
    auth_response = request.GET

    result = _confidential_client.acquire_token_by_auth_code_flow(
        auth_flow, auth_response,
        scopes=[f"api://{CLIENT_ID}/User.Read"]
    )
    
    if not result or "id_token_claims" not in result:
        messages.error(request, "Error al autenticar con Microsoft")
        return redirect("error")
    
    access_token = result.get("access_token")
    claims = result.get("id_token_claims")
    
    try:
        decoded_token = validate_microsoft_token(access_token)
        user_email = claims.get("preferred_username")
        full_name = claims.get("name")
    except AuthenticationFailed as e:
        messages.error(request, f"Error al validar el token: {str(e)}")
        return redirect("error")

    user = Engineer.objects.filter(email=user_email).first()
    if user:
        request.session["user_email"] = user_email
        request.session["full_name"] = full_name
        request.session["token"] = result["refresh_token"]

        login(request, user)

        return redirect("home")


def microsoft_logout(request: HttpRequest, app_type: str = "server"):
    logout(request)
    
    request.session.flush()

    if app_type == "server":
        return redirect("index")
    elif app_type == "mobile":
        return JsonResponse({"status": 200})


def error(request):
    return render(request, "error.html")
