from django.urls import path

from .views import (
    microsoft_login,
    microsoft_callback,
    microsoft_logout,
    error,
    BackendAuth,
)

from .Client.public import (
    set_public_client,
    get_flow,
    get_auth_uri,
    get_token,
)

urlpatterns = [
    path("login/", microsoft_login, name="login"),
    path("callback/", microsoft_callback, name="callback"),
    path("logout/", microsoft_logout, name="logout"),
    path("error/", error, name="error"),

    path("backendAuth", BackendAuth),

    path("set_public_client/", set_public_client),
    path("get_flow/", get_flow),
    path("get_auth_uri/", get_auth_uri),
    path("get_token/", get_token),
]
