import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.mark.django_db
def test_real_http_granian_server_smoke_test():
    """Verify that Granian ASGI server runs on an isolated port and serves real HTTP requests.
    Validates infrastructure healthcheck, real HTTP response envelopes, and error handling.
    """
    port = find_free_port()
    backend_dir = Path(__file__).resolve().parent.parent
    venv_granian = backend_dir / ".venv" / "Scripts" / "granian.exe"

    if not venv_granian.exists():
        pytest.skip("granian executable not found in .venv")

    cmd = [
        str(venv_granian),
        "--interface",
        "asgi",
        "config.asgi:application",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--workers",
        "1",
    ]

    env = dict(sys.modules["os"].environ)
    env["DJANGO_SETTINGS_MODULE"] = "config.settings"

    proc = subprocess.Popen(
        cmd,
        cwd=str(backend_dir),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    base_url = f"http://127.0.0.1:{port}"
    server_started = False

    try:
        # Wait up to 10 seconds for Granian to start
        for _ in range(20):
            try:
                with urllib.request.urlopen(f"{base_url}/api/health", timeout=1) as res:
                    if res.status == 200:
                        server_started = True
                        break
            except Exception:
                time.sleep(0.5)

        assert server_started, "Granian ASGI server failed to start within timeout"

        # 1. Real HTTP GET /api/health
        with urllib.request.urlopen(f"{base_url}/api/health", timeout=2) as res:
            assert res.status == 200
            data = json.loads(res.read().decode("utf-8"))
            assert data["status"] == "ok"
            assert data["service"] == "sie-sman1-bunut-backend"

        # 2. Real HTTP POST /api/auth/login with invalid payload -> 422 Unprocessable Entity
        login_url = f"{base_url}/api/auth/login"
        bad_req = urllib.request.Request(
            login_url,
            data=b'{"username": "test"}',
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urllib.request.urlopen(bad_req, timeout=2)
            pytest.fail("Expected HTTP 422 for missing password")
        except urllib.error.HTTPError as e:
            assert e.code == 422
            err_data = json.loads(e.read().decode("utf-8"))
            assert err_data["code"] == "VALIDATION_ERROR"
            assert "message" in err_data
            assert "details" in err_data

        # 3. Real HTTP GET 404
        try:
            urllib.request.urlopen(f"{base_url}/api/non_existent_route", timeout=2)
            pytest.fail("Expected HTTP 404")
        except urllib.error.HTTPError as e:
            assert e.code == 404

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
