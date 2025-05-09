import os
from pathlib import Path

# === Корневая директория проекта ===
# BASE_DIR указывает на папку, где лежат manage.py и папка templates/
BASE_DIR = Path(__file__).resolve().parent.parent

# === Безопасность ===
# В продакшене храните SECRET_KEY в окружении и никогда не коммите его в репозиторий
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-replace-me-with-secure-key')

DEBUG = True  # Для продакшена поставьте False

ALLOWED_HOSTS = []  # Например: ['yourdomain.com', 'www.yourdomain.com']

# === Установленные приложения ===
INSTALLED_APPS = [
    # Стандартные Django-приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Ваши приложения
    'users',
    'pages',
    'booking',
]

# === Смена модели пользователя на свою ===
AUTH_USER_MODEL = 'users.CustomUser'

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === Корневой URLConf ===
ROOT_URLCONF = 'hotel_booking.urls'

# === Шаблоны ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Здесь Django будет искать ваш base.html
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,  # также ищет <app>/templates/
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

# === WSGI ===
WSGI_APPLICATION = 'hotel_booking.wsgi.application'
# (если используете ASGI, можно добавить: ASGI_APPLICATION = 'hotel_booking.asgi.application')

# === База данных ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === Парольные валидаторы ===
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

# === Локализация ===
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Tallinn'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === Статика и медиа ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# === Переадресации после логина/логаута ===
LOGIN_REDIRECT_URL = 'pages:home'
LOGOUT_REDIRECT_URL = 'pages:home'
