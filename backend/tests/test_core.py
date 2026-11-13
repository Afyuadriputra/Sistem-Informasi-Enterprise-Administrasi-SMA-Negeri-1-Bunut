import pytest
from django.db import connection
from django.test import Client

from apps.core.exceptions import BusinessValidationError, ConcurrencyConflictError, PermissionDeniedError
from apps.core.schemas import ErrorEnvelope


@pytest.mark.django_db
def test_sqlite_connection_and_wal():
    """Verify SQLite connection, foreign keys, and WAL journal mode."""
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys;")
        fk_status = cursor.fetchone()[0]
        cursor.execute("PRAGMA journal_mode;")
        journal_mode = cursor.fetchone()[0]

    assert fk_status == 1
    # SQLite in-memory during tests returns 'memory', file-based returns 'wal'
    assert journal_mode.lower() in ("wal", "memory")


def test_health_check_endpoint(client: Client):
    """Verify GET /api/health returns 200 and expected payload."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.1.0"
    assert "X-Request-ID" in response.headers


def test_request_id_propagation(client: Client):
    """Verify incoming X-Request-ID is preserved in response headers."""
    custom_req_id = "req-custom-client-id-999"
    response = client.get("/api/health", HTTP_X_REQUEST_ID=custom_req_id)
    assert response.status_code == 200
    assert response.headers.get("X-Request-ID") == custom_req_id


def test_error_envelope_schema():
    """Verify ErrorEnvelope adheres to OpenAPI contract."""
    envelope = ErrorEnvelope(
        code="VALIDATION_ERROR",
        message="Validasi gagal",
        details=[{"field": "username", "message": "Wajib diisi"}],
        request_id="req-12345",
    )
    dumped = envelope.model_dump()
    assert dumped["code"] == "VALIDATION_ERROR"
    assert dumped["message"] == "Validasi gagal"
    assert len(dumped["details"]) == 1
    assert dumped["request_id"] == "req-12345"


def test_custom_exception_classes():
    """Verify custom exception inheritance and HTTP status codes."""
    val_err = BusinessValidationError("Input tidak valid")
    assert val_err.status_code == 422
    assert val_err.code == "VALIDATION_ERROR"

    conflict_err = ConcurrencyConflictError()
    assert conflict_err.status_code == 409
    assert conflict_err.code == "CONCURRENCY_CONFLICT"

    perm_err = PermissionDeniedError()
    assert perm_err.status_code == 403
    assert perm_err.code == "PERMISSION_DENIED"
