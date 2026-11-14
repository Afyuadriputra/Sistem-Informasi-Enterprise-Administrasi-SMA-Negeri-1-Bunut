"""Centralized Configuration for Integration Test Suite.

Sistem Informasi Enterprise Administrasi SMA Negeri 1 Bunut
Acuan: INT-M8.1 Addendum - Centralized Environment & Secret Management
"""

import os

BASE_URL = os.environ.get("INTEGRATION_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
PROXY_URL = os.environ.get("INTEGRATION_PROXY_URL", "http://localhost:3000").rstrip("/")
DEFAULT_PASSWORD = os.environ.get("INTEGRATION_TEST_PASSWORD", "Password123!")
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3")
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1")
