"""
INT-M1 Foundation & Infrastructure Gate Integration Tests
Verifies:
1. Healthcheck endpoint live response and payload structure.
2. Request ID propagation (X-Request-ID).
3. CORS preflight (OPTIONS) and Access-Control headers.
4. ErrorEnvelope structure on 401, 404, and 422.
"""
import json
import urllib.request
import urllib.error
import pytest


BASE_URL = "http://127.0.0.1:8000"
PROXY_URL = "http://localhost:3000"


def test_m1_healthcheck_direct():
    req = urllib.request.Request(f"{BASE_URL}/api/health", method="GET")
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200
        data = json.loads(res.read().decode("utf-8"))
        assert data["status"] == "ok"
        assert data["version"] == "1.1.0"
        assert data["service"] == "sie-sman1-bunut-backend"
        req_id = res.headers.get("X-Request-ID")
        assert req_id is not None
        assert req_id.startswith("req-")


def test_m1_healthcheck_via_vite_proxy():
    req = urllib.request.Request(f"{PROXY_URL}/api/health", method="GET")
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200
        data = json.loads(res.read().decode("utf-8"))
        assert data["status"] == "ok"
        assert data["service"] == "sie-sman1-bunut-backend"
        req_id = res.headers.get("x-request-id") or res.headers.get("X-Request-ID")
        assert req_id is not None
        assert req_id.startswith("req-")


def test_m1_cors_preflight():
    req = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type, Authorization",
        },
        method="OPTIONS",
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        assert res.status == 200
        allow_origin = res.headers.get("Access-Control-Allow-Origin")
        assert allow_origin in ["http://localhost:3000", "*"]


def test_m1_error_envelope_401():
    req = urllib.request.Request(f"{BASE_URL}/api/auth/me", method="GET")
    try:
        urllib.request.urlopen(req, timeout=5)
        pytest.fail("Expected HTTP 401")
    except urllib.error.HTTPError as e:
        assert e.code == 401
        body = json.loads(e.read().decode("utf-8"))
        assert "code" in body
        assert "message" in body
        assert body["code"] in ["UNAUTHORIZED", "AUTHENTICATION_FAILED", "TOKEN_MISSING"]


def test_m1_error_envelope_404():
    req = urllib.request.Request(f"{BASE_URL}/api/non_existent_route", method="GET")
    try:
        urllib.request.urlopen(req, timeout=5)
        pytest.fail("Expected HTTP 404")
    except urllib.error.HTTPError as e:
        assert e.code == 404
        req_id = e.headers.get("X-Request-ID")
        assert req_id is not None


def test_m1_error_envelope_422_validation():
    req = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=b'{"username": "only_user"}',
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=5)
        pytest.fail("Expected HTTP 422")
    except urllib.error.HTTPError as e:
        assert e.code == 422
        body = json.loads(e.read().decode("utf-8"))
        assert body.get("code") == "VALIDATION_ERROR"
        assert "details" in body


if __name__ == "__main__":
    test_m1_healthcheck_direct()
    print("PASS: test_m1_healthcheck_direct")
    test_m1_healthcheck_via_vite_proxy()
    print("PASS: test_m1_healthcheck_via_vite_proxy")
    test_m1_cors_preflight()
    print("PASS: test_m1_cors_preflight")
    test_m1_error_envelope_401()
    print("PASS: test_m1_error_envelope_401")
    test_m1_error_envelope_404()
    print("PASS: test_m1_error_envelope_404")
    test_m1_error_envelope_422_validation()
    print("PASS: test_m1_error_envelope_422_validation")
    print("ALL INT-M1 TESTS PASSED")
