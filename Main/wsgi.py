"""
WSGI config for Main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

from .settings import BASE_DIR


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')

application = get_wsgi_application()

# Wrap the application with WhiteNoise to serve static files
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))
