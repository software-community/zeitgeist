"""
WSGI config for zeitgeist_2019_website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import subprocess

try:
    shellscript = subprocess.Popen(["zeitgeist_2019/.env.production"])
    shellscript.wait()
except:
    print("aplying env variables error!")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zeitgeist_2019_website.settings')

application = get_wsgi_application()
