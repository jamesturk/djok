import environ
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
)


env.read_env(BASE_DIR / ".env")

# Environment Variables ------
DEBUG = env.bool("DEBUG", False)

print("debug", DEBUG)

if DEBUG:
    SECRET_KEY = env.str("SECRET_KEY", "needs-to-be-set-in-prod")
else:
    SECRET_KEY = env.str("SECRET_KEY")

DATABASES = {"default": env.db()}


ALLOWED_HOSTS = []
INTERNAL_IPS = ["127.0.0.1"]

# Debug Toolbar
IS_TESTING = "test" in sys.argv or "pytest" in sys.argv


# Static Settings ------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "django_structlog",
    "django_typer",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

if DEBUG and not IS_TESTING:
    INSTALLED_APPS += "debug_toolbar"
    MIDDLEWARE.insert(
        2,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "config.wsgi.application"
ROOT_URLCONF = "config.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Authentication -----

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = True
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = "user_name"
ACCOUNT_USERNAME_BLACKLIST = ["admin"]
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_SIGNUP_FORM_CLASS = ""
# ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Site] "
# ACCOUNT_LOGIN_BY_CODE_REQUIRED = False
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# Static File Config (per whitenoise) -----

# TODO: make configurable
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_ROOT = BASE_DIR / "_staticfiles"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# this directory is served at project root (for favicon.ico/robots.txt/etc.)
WHITENOISE_ROOT = BASE_DIR / "static" / "root"
