from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚙️ Базовые настройки
SECRET_KEY = 'dev-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

# 📦 Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # DRF
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    # Локальные приложения
    'employees',
    'users',
    'api',
    # tailwind
    "tailwind",
    "theme",
    "django_browser_reload",
]

TAILWIND_APP_NAME = "theme"

# ⚙️ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

ROOT_URLCONF = 'ksk_project.urls'

# 📂 Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ksk_project.wsgi.application'

# 💾 База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 Пароли
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

# 🌍 Язык и время
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# 📂 Статика
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# 📩 Email (пишем в файл)
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================
# 🔹 DRF НАСТРОЙКИ
# ==========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

# ==========================
# 🔹 ЛОГГИРОВАНИЕ
# ==========================
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # Общий лог для приложения
        'app_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'app.log',
            'formatter': 'verbose',
        },
        # Лог действий пользователей
        'actions_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'actions.log',
            'formatter': 'verbose',
        },
        # Лог для ошибок и системных событий
        'employees_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'employees.log',
            'formatter': 'verbose',
        },
        # Консоль
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        # Лог всего приложения
        'app': {
            'handlers': ['console', 'app_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Лог действий (создание, редактирование, удаление сотрудников и т.д.)
        'actions': {
            'handlers': ['console', 'actions_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Лог ошибок и системных событий
        'employees': {
            'handlers': ['console', 'employees_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django системный
        'django': {
            'handlers': ['console', 'employees_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


LOGIN_URL = '/login/'  # куда редиректить при @login_required
LOGIN_REDIRECT_URL = '/'  # куда редиректить после успешного логина
LOGOUT_REDIRECT_URL = '/login/'  # куда редиректить после logout

AUTH_USER_MODEL = 'users.User'
