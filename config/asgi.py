"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django

from channels.routing import get_default_application


environment = os.getenv('ENV', 'local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'config.settings.' + environment)
django.setup()
application = get_default_application()
