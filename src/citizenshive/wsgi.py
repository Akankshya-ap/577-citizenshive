"""
WSGI config for citizenshive project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


sys.path.append('/Users/kranthi_nuthalapati/Desktop/577/577-citizenshive/src/citizenshive')
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings.py'

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citizenshive.settings')

application = get_wsgi_application()


