"""
INT-M4 Attendance Gate Integration Tests
Verifies:
1. Guru logs in, selects assigned class, loads roster (with roster_version).
2. Guru submits bulk attendance with valid expected_roster_version.
3. Stale roster version submission returns HTTP 409 Conflict.
4. Wali Kelas views class attendance recap (calculates summary and student counts).
5. Excel export of attendance records returns HTTP 200 with valid spreadsheet binary.
6. Negative authorization: unauthorized role attempting attendance submission returns 403.
"""
import json
import urllib.request
import urllib.error
from datetime import date
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


def test_m4_scenario_a1_full_attendance():
    guru_tok = get_token("guru")
    wali_tok = get_token("wali_kelas")
    tu_tok = get_token("tata_usaha")

    # 1. Guru finds assigned class
    # Get class list
    _, classes_res, _ = api_request("GET", "/api/master/classes", guru_tok)
    cls_items = classes_res.get("items", classes_res) if isinstance(classes_res, dict) else classes_res
    target_class = next((c for c in cls_items if c["name"] == "XI-MIPA-1"), cls_items[0])
    cls_id = target_class["id"]

    today_str = date.today().isoformat()

    # 2. Guru loads roster
    status, roster, _ = api_request("GET", f"/api/attendance/roster?class_id={cls_id}&date={today_str}", guru_tok)
    assert status == 200
    assert "students" in roster
    assert len(roster["students"]) >= 1
    current_roster_version = roster.get("roster_version", 0)
    print(f"Loaded roster with {len(roster['students'])} students, roster_version={current_roster_version}")

    # 3. Guru records bulk attendance
    bulk_items = []
    statuses = ["HADIR", "HADIR", "HADIR", "SAKIT", "IZIN"]
    for i, st in enumerate(roster["students"]):
        status_val = statuses[i % len(statuses)]
        bulk_items.append({
            "student_id": st["student_id"],
            "status": status_val,
            "note": f"Presensi terintegrasi {status_val}",
        })

    bulk_payload = {
        "class_id": cls_id,
        "date": today_str,
        "items": bulk_items,
        "expected_roster_version": current_roster_version,
    }
    status, save_res, _ = api_request("POST", "/api/attendance/bulk", guru_tok, bulk_payload)
    assert status == 200
    assert save_res["saved_count"] == len(bulk_items)
    print(f"PASS: Guru recorded {save_res['saved_count']} attendance entries")

    # 4. Stale roster version submission -> must return 409 Conflict
    stale_payload = {
        "class_id": cls_id,
        "date": today_str,
        "items": bulk_items,
        "expected_roster_version": 999999,  # Stale/mismatched version
    }
    try:
        api_request("POST", "/api/attendance/bulk", guru_tok, stale_payload)
        pytest.fail("Expected HTTP 409 Conflict for stale expected_roster_version")
    except urllib.error.HTTPError as e:
        assert e.code == 409
        err = json.loads(e.read().decode("utf-8"))
        assert err["code"] == "CONCURRENCY_CONFLICT"
        print("PASS: Stale roster submission rejected with HTTP 409 CONCURRENCY_CONFLICT")

    # 5. Wali Kelas views recap
    status, recap, _ = api_request(
        "GET",
        f"/api/attendance?class_id={cls_id}&date_from=2026-01-01&date_to=2026-12-31",
        wali_tok,
    )
    assert status == 200
    assert "summary" in recap
    assert "student_recaps" in recap
    summary = recap["summary"]
    assert summary["total_students"] >= 1
    assert summary["hadir_pct"] > 0
    print(f"PASS: Wali Kelas recap verified: {summary['total_students']} students, {summary['hadir_pct']}% hadir")

    # 6. Excel Report Download
    status, excel_bytes, hdrs = api_request(
        "GET",
        f"/api/reports/attendance.xlsx?start_date=2026-01-01&end_date=2026-12-31&class_id={cls_id}",
        wali_tok,
    )
    assert status == 200
    assert len(excel_bytes) > 500  # Valid binary Excel file
    # Check openxml header signature PK (ZIP container for XLSX)
    assert excel_bytes.startswith(b"PK")
    print("PASS: Attendance Excel export generated and verified (valid XLSX PK header)")

    # 7. Negative Authorization: Tata Usaha attempting attendance recording -> 403
    try:
        api_request("POST", "/api/attendance/bulk", tu_tok, bulk_payload)
        pytest.fail("Expected HTTP 403 for Tata Usaha recording attendance")
    except urllib.error.HTTPError as e:
        assert e.code == 403
        err = json.loads(e.read().decode("utf-8"))
        assert err["code"] == "PERMISSION_DENIED"
        print("PASS: Non-authorized role rejected with HTTP 403 PERMISSION_DENIED")


if __name__ == "__main__":
    test_m4_scenario_a1_full_attendance()
    print("ALL INT-M4 TESTS PASSED")
