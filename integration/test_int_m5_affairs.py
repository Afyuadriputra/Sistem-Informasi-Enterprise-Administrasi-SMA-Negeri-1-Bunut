"""
INT-M5 Student Affairs & Privacy Gate Integration Tests
Verifies:
1. Kesiswaan creates a new student case (BARU / DILAPORKAN).
2. Status transitions:
   - MULAI_PENANGANAN -> DIPROSES (version incremented)
   - CATAT_TINDAKAN -> DIPROSES with confidential counseling note (version incremented)
   - SELESAIKAN -> SELESAI terminal status (version incremented)
3. Optimistic locking on transitions (stale expected_version returns HTTP 409 Conflict).
4. DEC-TECH-18 Privacy Masking:
   - Kesiswaan reads case -> full unmasked counseling note containing synthetic canary.
   - Guru / Wali Kelas reads case -> note is masked as '[CATATAN RAHASIA KONSELING]'
     and synthetic canary is strictly absent from the payload.
"""
import json
import urllib.request
import urllib.error
import pytest


BASE_URL = "http://127.0.0.1:8000"
CANARY_STRING = "CANARY_CONFIDENTIAL_BK_NOTE_SECURE_2026"


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
        res_data = res.read().decode("utf-8")
        return res.status, json.loads(res_data) if res_data else None


def test_m5_scenario_a2_student_affairs_and_privacy():
    kesiswaan_tok = get_token("kesiswaan")
    wali_tok = get_token("wali_kelas")

    # 1. Get a student to attach case to
    _, std_list = api_request("GET", "/api/master/students?page_size=1", kesiswaan_tok)
    items = std_list.get("items", std_list) if isinstance(std_list, dict) else std_list
    assert len(items) >= 1
    std_id = items[0]["id"]

    # 2. Kesiswaan creates case
    case_payload = {
        "student_id": std_id,
        "title": "Evaluasi Kedisiplinan dan Konseling Terpadu",
        "summary": "Siswa memerlukan bimbingan konseling komprehensif terkait kehadiran.",
    }
    status, case_res = api_request("POST", "/api/student-affairs/cases", kesiswaan_tok, case_payload)
    assert status == 201
    case_id = case_res["id"]
    assert case_res["status"] in ["BARU", "DILAPORKAN"]
    v1 = case_res.get("version", 1)
    print(f"Case created: id={case_id}, status={case_res['status']}, version={v1}")

    # 3. Transition: MULAI_PENANGANAN -> DIPROSES
    trans1_payload = {
        "action": "MULAI_PENANGANAN",
        "expected_version": v1,
        "note": "Memulai proses konseling awal dengan siswa",
    }
    status, t1_res = api_request("POST", f"/api/student-affairs/cases/{case_id}/transitions", kesiswaan_tok, trans1_payload)
    assert status == 200
    assert t1_res["status"] == "DIPROSES"
    v2 = t1_res["version"]
    assert v2 == v1 + 1
    print(f"Transition 1 successful: status={t1_res['status']}, version={v2}")

    # 4. Action: CATAT_TINDAKAN with synthetic canary note
    trans2_payload = {
        "action": "CATAT_TINDAKAN",
        "expected_version": v2,
        "note": f"{CANARY_STRING}: Siswa mengutarakan kendala transportasi dan disepakati solusi tindak lanjut.",
    }
    status, t2_res = api_request("POST", f"/api/student-affairs/cases/{case_id}/transitions", kesiswaan_tok, trans2_payload)
    assert status == 200
    v3 = t2_res["version"]
    assert v3 == v2 + 1
    print(f"Transition 2 successful (CATAT_TINDAKAN): version={v3}")

    # 5. Optimistic Locking Test: Attempt transition with stale expected_version (v1 instead of v3) -> 409
    stale_payload = {
        "action": "SELESAIKAN",
        "expected_version": v1,
        "note": "Mencoba selesaikan dengan versi basi",
    }
    try:
        api_request("POST", f"/api/student-affairs/cases/{case_id}/transitions", kesiswaan_tok, stale_payload)
        pytest.fail("Expected HTTP 409 for stale expected_version")
    except urllib.error.HTTPError as e:
        assert e.code == 409
        err = json.loads(e.read().decode("utf-8"))
        assert err["code"] == "CONCURRENCY_CONFLICT"
        print("PASS: Stale transition rejected with HTTP 409 CONCURRENCY_CONFLICT")

    # 6. Complete case: SELESAIKAN -> SELESAI
    trans3_payload = {
        "action": "SELESAIKAN",
        "expected_version": v3,
        "note": "Penanganan selesai dengan hasil pemantauan positif",
    }
    status, t3_res = api_request("POST", f"/api/student-affairs/cases/{case_id}/transitions", kesiswaan_tok, trans3_payload)
    assert status == 200
    assert t3_res["status"] == "SELESAI"
    v4 = t3_res["version"]
    assert v4 == v3 + 1
    print(f"Case finalized: status={t3_res['status']}, version={v4}")

    # 7. DEC-TECH-18 Privacy Check:
    # 7a. Kesiswaan fetches case detail: canary string MUST be visible in timeline action note
    status, kesiswaan_case = api_request("GET", f"/api/student-affairs/cases/{case_id}", kesiswaan_tok)
    assert status == 200
    kesiswaan_json_str = json.dumps(kesiswaan_case)
    assert CANARY_STRING in kesiswaan_json_str, "Kesiswaan MUST see unmasked canary counseling note"
    print("PASS: Kesiswaan received unmasked counseling note containing canary")

    # 7b. Wali Kelas fetches case detail: canary string MUST NOT appear! Note MUST be masked!
    status, wali_case = api_request("GET", f"/api/student-affairs/cases/{case_id}", wali_tok)
    assert status == 200
    wali_json_str = json.dumps(wali_case)
    assert CANARY_STRING not in wali_json_str, "Canary string MUST NOT be leaked to Wali Kelas!"
    assert (
        "[Catatan konseling privat - Terproteksi]" in wali_json_str
        or "[CATATAN RAHASIA KONSELING]" in wali_json_str
    ), "Wali Kelas MUST receive masked private counseling note"
    print("PASS: DEC-TECH-18 privacy masking verified: Wali Kelas received masked text, zero canary leak")

    # 7c. Pimpinan Sekolah denied from reading case detail -> HTTP 403
    kepsek_tok = get_token("kepsek")
    try:
        api_request("GET", f"/api/student-affairs/cases/{case_id}", kepsek_tok)
        pytest.fail("Expected HTTP 403 for Pimpinan accessing case detail")
    except urllib.error.HTTPError as e:
        assert e.code == 403
        print("PASS: Pimpinan strictly denied from reading case detail (HTTP 403 per RBAC)")

    # 7d. Administrator denied from reading case detail -> HTTP 403
    admin_tok = get_token("admin")
    try:
        api_request("GET", f"/api/student-affairs/cases/{case_id}", admin_tok)
        pytest.fail("Expected HTTP 403 for Administrator accessing case detail")
    except urllib.error.HTTPError as e:
        assert e.code == 403
        print("PASS: Administrator strictly denied from reading case detail (HTTP 403 per RBAC)")


if __name__ == "__main__":
    test_m5_scenario_a2_student_affairs_and_privacy()
    print("ALL INT-M5 TESTS PASSED")
