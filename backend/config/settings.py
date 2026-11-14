import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

from config.env import load_environment, validate_environment

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Centralized environment loader (supports DJANGO_ENV and explicit ENV_FILE)
ENV_INFO = load_environment(BASE_DIR)
DJANGO_ENV = ENV_INFO["django_env"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-insecure-secret-key-change-in-production-bunut-2026-xyz")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("true", "1", "yes")

allowed_hosts_raw = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_raw.split(",") if h.strip()]

database_url = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
REDIS_URL = os.environ.get("REDIS_URL", "")
_raw_media_root = os.environ.get("PRIVATE_MEDIA_ROOT", "private_media")
if os.path.isabs(_raw_media_root):
    PRIVATE_MEDIA_ROOT = Path(_raw_media_root).resolve()
else:
    PRIVATE_MEDIA_ROOT = (BASE_DIR / _raw_media_root).resolve()
PRIVATE_MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

# Fail-fast validation of critical settings per environment
validate_environment(
    env_name=DJANGO_ENV,
    secret_key=SECRET_KEY,
    debug=DEBUG,
    allowed_hosts=ALLOWED_HOSTS,
    database_url=database_url,
    redis_url=REDIS_URL,
    private_media_root=PRIVATE_MEDIA_ROOT,
)

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "simple_history",
    "ninja_extra",
    "ninja_jwt",
    "ninja_jwt.token_blacklist",
    "apps.core.apps.CoreConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.master_data.apps.MasterDataConfig",
    "apps.attendance.apps.AttendanceConfig",
    "apps.student_affairs.apps.StudentAffairsConfig",
    "apps.administration.apps.AdministrationConfig",
    "apps.reports.apps.ReportsConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "apps.core.middleware.RequestIDMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "apps.core.middleware.RequestLoggingMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database Strategy: SQLite with WAL mode by default, support for PostgreSQL
if database_url.startswith("postgresql://") or database_url.startswith("postgres://"):
    parsed = urlparse(database_url)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "postgres",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "127.0.0.1",
            "PORT": parsed.port or 5432,
            "TEST": {
                "NAME": f"test_{parsed.path.lstrip('/') or 'sie_bunut'}",
            },
        }
    }
elif database_url.startswith("sqlite:///"):
    # SQLite WAL mode
    sqlite_path = database_url.replace("sqlite:///", "")
    if sqlite_path == "" or sqlite_path == ":memory:":
        db_file = ":memory:"
    elif Path(sqlite_path).is_absolute():
        db_file = str(Path(sqlite_path))
    else:
        db_file = str((BASE_DIR / sqlite_path).resolve())

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": db_file,
            "OPTIONS": {
                "timeout": 20,
                "init_command": "PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL;",
            },
            "TEST": {
                "NAME": str((BASE_DIR / "test_db.sqlite3").resolve()),
            },
        }
    }
else:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(f"DATABASE_URL tidak valid: skema '{database_url}' tidak didukung.")

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Password validation and Argon2 Hasher
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "id-id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS configuration
cors_origins_raw = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173",
)
CORS_ALLOWED_ORIGINS = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["X-Request-ID"]

# Cache & Redis configuration
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
            "KEY_PREFIX": os.environ.get("CACHE_KEY_PREFIX", "sie_bunut"),
        }
    }
else:
    # Use LocMemCache for local dev/testing if Redis is not explicitly configured
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "sie-bunut-cache",
        }
    }

# Ninja JWT Settings
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS256",
}

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "api.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
