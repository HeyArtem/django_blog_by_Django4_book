"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2(gp9p_83r!)g-zx0r28#bl%oi=r%0ns8(27!jdjrfy$y2-y8+'

# SECURITY WARNING: don't run with debug turned on in production!
"""
DEBUG – это булев параметр, который включает и выключает режим от-
ладки проекта. Если его значение установлено равным True, то Django
будет отображать подробные страницы ошибок в случаях, когда прило-
жение выдает неперехваченное исключение. При переходе в производ-
ственную среду следует помнить о том, что необходимо устанавливать
его значение равным False. Никогда не развертывайте свой сайт в про-
изводственной среде с включенной отладкой, поскольку вы предоста-
вите конфиденциальные данные, связанные с проектом.
"""
DEBUG = True


"""
ALLOWED_HOSTS не применяется при включенном режиме отладки или при
выполнении тестов. При перенесении своего сайта в производственную
среду и установке параметра DEBUG равным False в этот настроечный40
Разработка приложения для ведения блога
параметр следует добавлять свои домен/хост, чтобы разрешить ему раз-
давать ваш сайт Django.
"""
ALLOWED_HOSTS = []


# Application definition
"""
сообщает Django о приложениях, которые для этого сайта
являются активными

– django.contrib.admin: сайт администрирования;
– django.contrib.auth: фреймворк аутентификации;
– django.contrib.contenttypes: фреймворк типов контента;
– django.contrib.sessions: фреймворк сеансов;
– django.contrib.messages: фреймворк сообщений;
– django.contrib.staticfiles: фреймворк управления статическими
файлами
"""
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig', #Класс BlogConfig – это конфигурация приложения.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

"""
ROOT_URLCONF указывает модуль Python, в котором определены шаблоны
корневых URL-адресов приложения.
"""
ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
"""
DATABASES – словарь, содержащий настроечные параметры всех баз дан-
ных, которые будут использоваться в проекте. Всегда должна сущест-
вовать база данных, которая будет использоваться по умолчанию.
В стандартной конфигурации используется база данных SQLite3, если
не указана иная.
"""

# Определение типа БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
