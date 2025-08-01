from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '..' /'.env')

SECRET_KEY = 'django-insecure-do3_ychdntoxyn#=yoh1)_4p8b5q2=%m9qr3cspjaj7cc^5yna'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
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

ROOT_URLCONF = 'admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'admin.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DBNAME'),
        'USER': os.getenv('DBUSER'),
        'PASSWORD': os.getenv('DBPASSWORD'),
        'HOST': os.getenv('DBADRESS', 'localhost'),
        'PORT': '5432',
    }
}


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


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Minsk'

USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = 'static/'

MEDIA_URL = ''
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_title': 'Админ панель Yummy',
    'site_header': 'Админ панель Yummy',
    'site_brand': 'Yummy',
    'welcome_sign': 'Добро пожаловать',

    "top_menu_links": [
        {"name": "Главная",
         "url": "admin:index",
         "permissions": ["auth.view_user"]},
    ],
    "icons": {
        "dashboard.Users": "fas fa-user",
        "dashboard.Categories": "fas fa-tag",
        "dashboard.Products": "fas fa-cookie"
    },
    'show_sidebar': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'order_with_respect_to': ['dashboard', 'auth']
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",  # другие: darkly, cyborg, journal, lux, minty, solar, etc, flatly
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_colour": "navbar-green",
    "accent": "accent-green",
    "navbar": "navbar-black navbar-green",
    "no_navbar_border": False,
    "sidebar": "sidebar-light-blue",
    "sidebar_nav_small_text": False,
   # "custom_css": "css/custom_admin.css",
}