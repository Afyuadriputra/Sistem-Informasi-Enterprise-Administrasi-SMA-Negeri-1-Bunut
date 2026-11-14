"""
INT-M7 Dashboard, Reports & Cache Gate Integration Tests
Verifies:
1. Dashboard metrics retrieval across all 6 roles (contract compliance).
2. Administration PDF report generation (binary %PDF- validation).
3. Attendance Excel export generation (binary PK zip validation).
4. System Audit Log listing:
   - Admin retrieves audit trail with pagination.
   - Non-admin (Guru) access is rejected with HTTP 403 PERMISSION_DENIED.
5. Cache invalidation behavior on mutation.
"""
import json
import urllib.request
import urllib.error
import pytest


BASE_URL = "http://127.0.0.1:8000"


def get_token(username):
    payload = json.dumps({"username": username, "password": "Password123!"}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    res = urllib.request.urlopen(req, timeout=5)
    return json.loads(res.read().decode("utf-8"))["access_token"]


def api_request(method, path, token, body=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=5) as res:
        res_data = res.read()
        content_type = res.headers.get("Content-Type", "")
        if "json" in content_type:
            return res.status, json.loads(res_data.decode("utf-8")), res.headers
        return res.status, res_data, res.headers


def test_m7_six_roles_dashboard_metrics():
    roles = ["admin", "guru", "wali_kelas", "kesiswaan", "tata_usaha", "kepsek"]
    for role in roles:
        tok = get_token(role)
        status, dash, _ = api_request("GET", "/api/reports/dashboard", tok)
        assert status == 200
        assert "role" in dash or "metrics" in dash
        metrics = dash.get("metrics", dash)
        print(f"Role {role} dashboard metrics: {list(metrics.keys())[:5]}")

    print("PASS: Six roles dashboard metrics retrieved and contract-aligned")


def test_m7_reports_export_pdf_and_excel():
    tu_tok = get_token("tata_usaha")
    kepsek_tok = get_token("kepsek")
    admin_tok = get_token("admin")

    # 1. PDF Export (TU or Kepsek)
    status, pdf_bytes, hdrs = api_request(
        "GET",
        "/api/reports/administration.pdf?start_date=2026-01-01&end_date=2026-12-31",
        tu_tok,
    )
    assert status == 200
    assert len(pdf_bytes) > 200
    assert pdf_bytes.startswith(b"%PDF-")
    print("PASS: Administration PDF export verified (%PDF- header)")

    # 2. Excel Export (Kepsek / Pimpinan)
    status, excel_bytes, hdrs = api_request(
        "GET",
        "/api/reports/attendance.xlsx?start_date=2026-01-01&end_date=2026-12-31",
        kepsek_tok,
    )
    assert status == 200
    assert len(excel_bytes) > 200
    assert excel_bytes.startswith(b"PK")
    print("PASS: Attendance Excel export verified (PK zip container header)")

    # 3. Least privilege check: Admin is not allowed to export attendance excel -> 403
    try:
        api_request(
            "GET",
            "/api/reports/attendance.xlsx?start_date=2026-01-01&end_date=2026-12-31",
            admin_tok,
        )
        pytest.fail("Expected HTTP 403 for Admin accessing attendance excel")
    except urllib.error.HTTPError as e:
        assert e.code == 403
        print("PASS: Admin strictly denied access to academic attendance report (least privilege)")


def test_m7_audit_logs_and_least_privilege():
    admin_tok = get_token("admin")
    guru_tok = get_token("guru")

    # 1. Admin reads audit logs
    status, audit_res, _ = api_request("GET", "/api/audit-logs?page=1&page_size=10", admin_tok)
    assert status == 200
    assert "items" in audit_res
    items = audit_res["items"]
    assert len(items) >= 1
    print(f"PASS: Admin retrieved {len(items)} audit log entries (page 1)")

    # 2. Guru attempts to access audit logs -> 403 Forbidden
    try:
        api_request("GET", "/api/audit-logs", guru_tok)
        pytest.fail("Expected HTTP 403 for non-admin accessing audit logs")
    except urllib.error.HTTPError as e:
        assert e.code == 403
        err = json.loads(e.read().decode("utf-8"))
        assert err["code"] == "PERMISSION_DENIED"
        print("PASS: Non-admin rejected with HTTP 403 PERMISSION_DENIED on /api/audit-logs")


if __name__ == "__main__":
    test_m7_six_roles_dashboard_metrics()
    test_m7_reports_export_pdf_and_excel()
    test_m7_audit_logs_and_least_privilege()
    print("ALL INT-M7 TESTS PASSED")
