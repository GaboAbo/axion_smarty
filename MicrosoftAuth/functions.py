import jwt, requests, base64, environ, logging
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger(__name__)

env = environ.Env()

if env.str('ENV', default='development') != 'production':
    environ.Env.read_env()

# Environment Variables
TENANT = env("MICROSOFT_TENANT", default="")


def get_microsoft_public_keys():
    url = f"https://login.microsoftonline.com/{TENANT}/discovery/v2.0/keys"
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

        return "success"

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired.")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token.")
