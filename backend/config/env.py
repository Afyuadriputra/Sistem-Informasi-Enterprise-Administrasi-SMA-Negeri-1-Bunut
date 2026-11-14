"""Centralized Environment Configuration Loader & Validator for Django.

Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut
Acuan: TRD Bab 9, PRD, BSD, dan Master Integration Plan
"""

import os
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

KNOWN_INSECURE_KEYS = {
    "dev-insecure-secret-key-change-in-production-bunut-2026-xyz",
    "django-insecure-default",
    "change-me",
    "insecure",
}


def load_environment(base_dir: Path) -> Dict[str, Any]:
    """Loads environment variables based on explicit DJANGO_ENV or ENV_FILE."""
    django_env = os.environ.get("DJANGO_ENV", "development").lower().strip()
    explicit_env_file = os.environ.get("ENV_FILE")

    if explicit_env_file:
        env_path = Path(explicit_env_file)
        if not env_path.is_absolute():
            env_path = base_dir / env_path
    elif django_env == "integration":
        env_path = base_dir / ".env.integration"
    elif django_env == "production":
        env_path = base_dir / ".env.production"
    elif django_env == "test":
        env_path = base_dir / ".env.test"
    else:
        env_path = base_dir / ".env"

    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
    elif django_env != "development" and (base_dir / ".env").exists():
        # Fallback to .env if specific environment file does not exist
        load_dotenv(dotenv_path=base_dir / ".env", override=False)

    return {
        "django_env": django_env,
        "loaded_file": str(env_path) if env_path.exists() else None,
    }


def validate_environment(
    env_name: str,
    secret_key: str,
    debug: bool,
    allowed_hosts: List[str],
    database_url: str,
    redis_url: str,
    private_media_root: Path,
) -> None:
    """Performs fail-fast validation on critical environment configurations."""
    # 1. Secret Key Validation
    if not secret_key or not secret_key.strip():
        raise ImproperlyConfigured("DJANGO_SECRET_KEY tidak boleh kosong.")

    if env_name == "production":
        if secret_key in KNOWN_INSECURE_KEYS or len(secret_key) < 32:
            raise ImproperlyConfigured(
                "DJANGO_SECRET_KEY tidak aman untuk environment production. "
                "Gunakan kunci kriptografi acak minimal 32 karakter."
            )

    # 2. Debug Mode Validation
    if env_name == "production" and debug:
        raise ImproperlyConfigured("DJANGO_DEBUG wajib disetel bernilai False pada environment production.")

    # 3. Allowed Hosts Validation
    if not allowed_hosts:
        raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS tidak boleh kosong.")

    if env_name == "production" and "*" in allowed_hosts:
        raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS dilarang menggunakan wildcard '*' pada environment production.")

    # 4. Database URL Validation
    if not database_url or not database_url.strip():
        raise ImproperlyConfigured("DATABASE_URL tidak boleh kosong.")

    parsed_db = urlparse(database_url)
    if parsed_db.scheme not in ("sqlite", "postgresql", "postgres"):
        raise ImproperlyConfigured(
            f"Skema DATABASE_URL '{parsed_db.scheme}' tidak didukung. "
            "Gunakan format standar sqlite:/// atau postgresql://."
        )

    # 5. Redis URL Validation (Fail-closed for integration & production)
    if env_name in ("integration", "production"):
        if not redis_url or not redis_url.strip():
            raise ImproperlyConfigured(
                f"REDIS_URL wajib dikonfigurasi pada environment '{env_name}'. "
                "Penggantian diam-diam dengan LocMemCache dilarang untuk menjamin persistensi sesi dan blacklist token."
            )
        parsed_redis = urlparse(redis_url)
        if parsed_redis.scheme not in ("redis", "rediss"):
            raise ImproperlyConfigured(
                f"Skema REDIS_URL '{parsed_redis.scheme}' tidak valid. Gunakan skema redis:// atau rediss://."
            )

    # 6. Private Media Root Validation
    if not private_media_root:
        raise ImproperlyConfigured("PRIVATE_MEDIA_ROOT wajib dikonfigurasi.")
