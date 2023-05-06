"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/

wsgi.py: конфигурация для выполнения проекта в качестве прило-
жения, работающего по протоколу интерфейса шлюза веб-сервера
(WSGI) 1 с WSGI-совместимыми веб-серверами.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
