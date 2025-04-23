import jwt, requests, os, base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from rest_framework.exceptions import AuthenticationFailed
from msal import ConfidentialClientApplication, PublicClientApplication

load_dotenv()

# Environment Variables
TENANT = os.getenv("MICROSOFT_TENANT", "")
CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("MICROSOFT_REDIRECT_URI", "")
REDIRECT_URI_MOBILE = os.getenv("MICROSOFT_REDIRECT_URI_MOBILE", "")


def get_microsoft_public_keys():
    url = f"{os.getenv('MICROSOFT_TENANT')}/discovery/v2.0/keys"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad status codes
        keys = response.json().get("keys", [])
        if not keys:
            raise AuthenticationFailed("No keys found in the response.")
        return keys
    except requests.RequestException as e:
        raise AuthenticationFailed(f"Error fetching Microsoft public keys: {str(e)}")


def base64url_decode(base64url):
    padding = '=' * (4 - len(base64url) % 4)
    base64url += padding
    return base64.urlsafe_b64decode(base64url)


def jwk_to_pem(jwk):
    e = int.from_bytes(base64url_decode(jwk["e"]), byteorder='big')
    n = int.from_bytes(base64url_decode(jwk["n"]), byteorder='big')

    rsa_key = rsa.RSAPublicNumbers(e=e, n=n).public_key(default_backend())

    pem = rsa_key.public_bytes(
        Encoding.PEM,
        PublicFormat.SubjectPublicKeyInfo
    )
    return pem


def get_token(request):
    pass


def validate_microsoft_token(token):
    try:
        header = jwt.get_unverified_header(token)

        # Fetch public keys
        public_keys = get_microsoft_public_keys()

        # Find the correct key based on the key ID (kid)
        rsa_key = {}
        for key in public_keys:
            if key["kid"] == header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            raise AuthenticationFailed("Unable to find appropriate key.")

        # Convert JWK to PEM format
        pem = jwk_to_pem(rsa_key)

        # Decode and verify the token
        payload = jwt.decode(
            token,
            pem,
            algorithms=["RS256"],
            audience=os.getenv("MICROSOFT_CLIENT_ID"),
            issuer=f"{os.getenv('MICROSOFT_TENANT')}/v2.0",
        )
        return payload

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        raise AuthenticationFailed("Token has expired.")
    except jwt.InvalidTokenError:
        print("Invalid token.")
        raise AuthenticationFailed("Invalid token.")
