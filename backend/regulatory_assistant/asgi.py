"""
ASGI config for regulatory_assistant project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'regulatory_assistant.settings')

application = get_asgi_application()
