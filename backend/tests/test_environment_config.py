"""Tests for Centralized Environment Configuration & Secret Management.

Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut
Acuan: TRD Bab 9, INT-M8.1 Addendum
"""

from pathlib import Path
import pytest
from django.core.exceptions import ImproperlyConfigured

from config.env import load_environment, validate_environment


def test_load_environment_default_development(monkeypatch, tmp_path):
    monkeypatch.delenv("DJANGO_ENV", raising=False)
    monkeypatch.delenv("ENV_FILE", raising=False)
    info = load_environment(tmp_path)
    assert info["django_env"] == "development"


def test_load_environment_respects_django_env(monkeypatch, tmp_path):
    int_file = tmp_path / ".env.integration"
    int_file.write_text("DJANGO_ENV=integration\nREDIS_URL=redis://127.0.0.1:6379/1\n", encoding="utf-8")

    monkeypatch.setenv("DJANGO_ENV", "integration")
    info = load_environment(tmp_path)
    assert info["django_env"] == "integration"
    assert info["loaded_file"] == str(int_file)


def test_load_environment_explicit_env_file(monkeypatch, tmp_path):
    custom_file = tmp_path / "custom.env"
    custom_file.write_text("DJANGO_DEBUG=False\n", encoding="utf-8")

    monkeypatch.setenv("ENV_FILE", str(custom_file))
    info = load_environment(tmp_path)
    assert info["loaded_file"] == str(custom_file)


def test_validation_valid_sqlite_configuration(tmp_path):
    # Valid dev SQLite setup should not raise
    validate_environment(
        env_name="development",
        secret_key="dev-insecure-key-for-local-testing-only",
        debug=True,
        allowed_hosts=["localhost", "127.0.0.1"],
        database_url="sqlite:///db.sqlite3",
        redis_url="redis://127.0.0.1:6379/1",
        private_media_root=tmp_path / "media",
    )


def test_validation_valid_postgresql_configuration(tmp_path):
    # Valid integration PostgreSQL setup should not raise
    validate_environment(
        env_name="integration",
        secret_key="integration-secret-key-sufficiently-long-for-test-32chars",
        debug=False,
        allowed_hosts=["localhost", "127.0.0.1"],
        database_url="postgresql://sie_app:Password123!@127.0.0.1:5432/sie_bunut",
        redis_url="redis://127.0.0.1:6379/1",
        private_media_root=tmp_path / "media",
    )


def test_validation_invalid_database_url_scheme(tmp_path):
    with pytest.raises(ImproperlyConfigured) as exc:
        validate_environment(
            env_name="development",
            secret_key="some-secret-key-value",
            debug=True,
            allowed_hosts=["localhost"],
            database_url="mysql://root:secret@localhost:3306/sie",
            redis_url="redis://127.0.0.1:6379/1",
            private_media_root=tmp_path / "media",
        )
    assert "tidak didukung" in str(exc.value)


def test_validation_empty_secret_key_rejected(tmp_path):
    with pytest.raises(ImproperlyConfigured) as exc:
        validate_environment(
            env_name="development",
            secret_key="",
            debug=True,
            allowed_hosts=["localhost"],
            database_url="sqlite:///db.sqlite3",
            redis_url="",
            private_media_root=tmp_path / "media",
        )
    assert "DJANGO_SECRET_KEY tidak boleh kosong" in str(exc.value)


def test_validation_production_insecure_secret_key_rejected(tmp_path):
    with pytest.raises(ImproperlyConfigured) as exc:
        validate_environment(
            env_name="production",
            secret_key="dev-insecure-secret-key-change-in-production-bunut-2026-xyz",
            debug=False,
            allowed_hosts=["sie.sman1bunut.sch.id"],
            database_url="postgresql://sie_app:pass@127.0.0.1:5432/sie_prod",
            redis_url="redis://127.0.0.1:6379/1",
            private_media_root=tmp_path / "media",
        )
    assert "tidak aman untuk environment production" in str(exc.value)


def test_validation_production_debug_true_rejected(tmp_path):
    with pytest.raises(ImproperlyConfigured) as exc:
        validate_environment(
            env_name="production",
            secret_key="valid-secure-random-long-production-key-with-high-entropy",
            debug=True,
            allowed_hosts=["sie.sman1bunut.sch.id"],
            database_url="postgresql://sie_app:pass@127.0.0.1:5432/sie_prod",
            redis_url="redis://127.0.0.1:6379/1",
            private_media_root=tmp_path / "media",
        )
    assert "DJANGO_DEBUG wajib disetel bernilai False" in str(exc.value)


def test_validation_production_wildcard_allowed_hosts_rejected(tmp_path):
    with pytest.raises(ImproperlyConfigured) as exc:
        validate_environment(
            env_name="production",
            secret_key="valid-secure-random-long-production-key-with-high-entropy",
            debug=False,
            allowed_hosts=["*", "sie.sman1bunut.sch.id"],
            database_url="postgresql://sie_app:pass@127.0.0.1:5432/sie_prod",
            redis_url="redis://127.0.0.1:6379/1",
            private_media_root=tmp_path / "media",
        )
    assert "wildcard '*'" in str(exc.value)


def test_validation_missing_redis_in_integration_or_production_rejected(tmp_path):
    # In integration/production, Redis is mandatory (fail-closed, no silent LocMemCache fallback)
    with pytest.raises(ImproperlyConfigured) as exc:
        validate_environment(
            env_name="integration",
            secret_key="integration-secret-key-sufficiently-long-for-test-32chars",
            debug=False,
            allowed_hosts=["localhost"],
            database_url="postgresql://sie_app:pass@127.0.0.1:5432/sie_int",
            redis_url="",
            private_media_root=tmp_path / "media",
        )
    assert "REDIS_URL wajib dikonfigurasi" in str(exc.value)
