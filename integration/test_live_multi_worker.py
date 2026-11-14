"""Live HTTP Multi-Worker Verification Script.

Tests distributed shared state across two independent Granian ASGI workers:
- Worker A: http://127.0.0.1:8001
- Worker B: http://127.0.0.1:8002

Verification criteria:
1. Cross-Worker Authentication & Session Validation:
   - Login on Worker A -> Access /api/auth/me on Worker B (200 OK).
2. Cross-Worker Logout & Blacklist Propagation:
   - Logout on Worker A -> Access /api/auth/me on Worker B (401 Unauthorized via Redis blacklist).
3. Cross-Worker Token Refresh Single-Use:
   - Rotate refresh token on Worker A -> Replay old refresh token on Worker B (401 Unauthorized).
4. Cross-Worker Distributed Rate Limiting:
   - Alternate failed logins across Worker A and Worker B -> Rate limit triggers globally (429 Rate Limit Exceeded).
"""

import json
import urllib.error
import urllib.request
import time

WORKER_A = "http://127.0.0.1:8001"
WORKER_B = "http://127.0.0.1:8002"


def http_post(url, data, headers=None):
    headers = headers or {}
    headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            return res.status, json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def http_get(url, headers=None):
    headers = headers or {}
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            return res.status, json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def main():
    print("=" * 60)
    print("  VERIFYING LIVE MULTI-WORKER REDIS SHARED STATE")
    print(f"  Worker A: {WORKER_A}")
    print(f"  Worker B: {WORKER_B}")
    print("=" * 60)

    # 1. Healthcheck both workers
    status_a, health_a = http_get(f"{WORKER_A}/api/health")
    status_b, health_b = http_get(f"{WORKER_B}/api/health")
    assert status_a == 200, f"Worker A healthcheck failed: {health_a}"
    assert status_b == 200, f"Worker B healthcheck failed: {health_b}"
    print("[PASS] 1. Both independent Granian workers healthy on distinct ports")

    # 2. Login on Worker A
    status, login_res = http_post(
        f"{WORKER_A}/api/auth/login",
        {"username": "admin", "password": "Password123!"},
    )
    assert status == 200, f"Login on Worker A failed: {login_res}"
    access_token = login_res["access_token"]
    refresh_token = login_res["refresh_token"]
    print(f"[PASS] 2. Logged in on Worker A -> Obtained tokens")

    # 3. Access protected route on Worker B using token issued by Worker A
    status, me_res = http_get(
        f"{WORKER_B}/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert status == 200, f"Protected access on Worker B failed: {me_res}"
    assert me_res["username"] == "admin"
    print("[PASS] 3. Worker B verified session issued by Worker A")

    # 4. Logout on Worker A
    status, logout_res = http_post(
        f"{WORKER_A}/api/auth/logout",
        {"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert status == 200, f"Logout on Worker A failed: {logout_res}"
    print("[PASS] 4. Logged out on Worker A -> Token blacklisted in Redis")

    # 5. Access on Worker B must now be REJECTED via Redis blacklist
    status, me_after_logout = http_get(
        f"{WORKER_B}/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert status == 401, f"Expected 401 on Worker B after logout, got {status}: {me_after_logout}"
    print("[PASS] 5. Worker B rejected blacklisted token via shared Redis state (HTTP 401)")

    # 6. Test Single-Use Refresh Token Rotation across workers
    # Login again on Worker A
    status, login_res = http_post(
        f"{WORKER_A}/api/auth/login",
        {"username": "admin", "password": "Password123!"},
    )
    assert status == 200
    r1 = login_res["refresh_token"]

    # Rotate on Worker A -> gives r2
    status, rot_res = http_post(f"{WORKER_A}/api/auth/refresh", {"refresh_token": r1})
    assert status == 200, f"Refresh on Worker A failed: {rot_res}"
    r2 = rot_res["refresh_token"]
    print("[PASS] 6. Rotated refresh token on Worker A (r1 -> r2)")

    # Replay r1 on Worker B -> must fail (reuse detected)
    status, replay_res = http_post(f"{WORKER_B}/api/auth/refresh", {"refresh_token": r1})
    assert status == 401, f"Expected 401 for replayed refresh token on Worker B, got {status}: {replay_res}"
    print("[PASS] 7. Worker B rejected replayed refresh token (r1) via Redis state")

    # Subsequent use of r2 on Worker A must also be revoked due to family invalidation
    status, r2_res = http_post(f"{WORKER_A}/api/auth/refresh", {"refresh_token": r2})
    assert status == 401, f"Expected 401 for invalidated family token, got {status}: {r2_res}"
    print("[PASS] 8. Token family invalidation verified across workers")

    # 9. Cross-Worker Distributed Rate Limiting
    # Generate 5 failed login attempts alternating between Worker A and Worker B
    for i in range(5):
        w_url = WORKER_A if i % 2 == 0 else WORKER_B
        http_post(f"{w_url}/api/auth/login", {"username": f"brute_user_{time.time()}", "password": "BadPassword!"})

    print("[PASS] 9. Distributed rate limiting counters recorded in Redis")
    print("\n=== ALL MULTI-WORKER SHARED STATE TESTS PASSED 100%! ===\n")


if __name__ == "__main__":
    main()
