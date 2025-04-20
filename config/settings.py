import environ
import structlog
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
    _DEFAULT_DB = env.db(default="sqlite:///" + str(BASE_DIR / "db.sqlite3"))
else:
    SECRET_KEY = env.str("SECRET_KEY")
    _DEFAULT_DB = env.db()

DATABASES = {"default": _DEFAULT_DB}

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
    INSTALLED_APPS += ["debug_toolbar"]
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

# This configures django-allauth with reasonably secure defaults
# for an email-based account.
#
# TODO: Document other common configurations.
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

# Logging Config ---------

# default to not capturing data we don't know we need (re-enable as needed)
DJANGO_STRUCTLOG_IP_LOGGING_ENABLED = False
DJANGO_STRUCTLOG_USER_ID_FIELD = None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"]
            ),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        },
        "json_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "_logs/log.json",
            "formatter": "json_formatter",
        },
        "flat_line_file": {
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "_logs/flat.log",
            "formatter": "key_value",
        },
    },
    "loggers": {
        "django_structlog": {
            "handlers": ["console", "flat_line_file", "json_file"],
            "level": "INFO",
        },
        # Modify this to match the name of your application.
        # to configure different logging for your app vs. Django's
        # internals.
        # "YOUR_APP": {
        #    "handlers": ["console", "flat_line_file", "json_file"],
        #    "level": "INFO",
        # },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


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

