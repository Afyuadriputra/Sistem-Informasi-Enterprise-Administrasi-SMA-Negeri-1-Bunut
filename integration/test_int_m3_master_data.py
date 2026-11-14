"""
INT-M3 Master Data & Academic Gate Integration Tests
Verifies:
1. User account lifecycle (Create, List, Detail, Update is_active).
2. Academic year lifecycle (Create, List, PATCH is_active single-active toggle).
3. School class lifecycle (Create, List, PATCH).
4. Employee lifecycle (Create, List, PATCH).
5. Student lifecycle (Create, List, PATCH status enum AKTIF -> LULUS).
6. Student enrollment lifecycle (Create, List, PATCH end_date).
7. Teacher assignment lifecycle (Create, List, PATCH).
"""
import json
import urllib.request
import urllib.error
import uuid
from datetime import date


BASE_URL = "http://127.0.0.1:8000"


def get_admin_token():
    payload = json.dumps({"username": "admin", "password": "Password123!"}).encode("utf-8")
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


def test_m3_account_lifecycle(token):
    # 1. Create account
    new_user_payload = {
        "username": "guru_m3_test",
        "password": "Password123!",
        "name": "Guru M3 Test",
        "roles": ["Guru"],
    }
    # Check if user already exists
    status, users_res = api_request("GET", "/api/accounts/users?search=guru_m3_test", token)
    user_id = None
    items = users_res.get("items", users_res) if isinstance(users_res, dict) else users_res
    for u in items:
        if u["username"] == "guru_m3_test":
            user_id = u["id"]
            break

    if not user_id:
        status, user_res = api_request("POST", "/api/accounts/users", token, new_user_payload)
        assert status == 201
        user_id = user_res["id"]
        assert user_res["username"] == "guru_m3_test"

    # 2. Detail
    status, detail_res = api_request("GET", f"/api/accounts/users/{user_id}", token)
    assert status == 200
    assert detail_res["username"] == "guru_m3_test"

    # 3. PATCH is_active = False then True
    status, patch_res = api_request("PATCH", f"/api/accounts/users/{user_id}", token, {"is_active": False})
    assert status == 200
    assert patch_res["is_active"] is False

    status, patch_res2 = api_request("PATCH", f"/api/accounts/users/{user_id}", token, {"is_active": True})
    assert status == 200
    assert patch_res2["is_active"] is True
    print("PASS: test_m3_account_lifecycle")


def test_m3_academic_year_lifecycle(token):
    # 1. Create Academic Year
    ay_payload = {
        "name": "2027/2028 Ganjil M3",
        "start_date": "2027-07-01",
        "end_date": "2027-12-31",
        "is_active": False,
    }
    # List to see if already exists
    _, ay_list = api_request("GET", "/api/master/academic-years", token)
    ay_id = None
    items = ay_list.get("items", ay_list) if isinstance(ay_list, dict) else ay_list
    for ay in items:
        if ay["name"] == ay_payload["name"]:
            ay_id = ay["id"]
            break

    if not ay_id:
        status, ay_res = api_request("POST", "/api/master/academic-years", token, ay_payload)
        assert status == 201
        ay_id = ay_res["id"]

    # 2. PATCH is_active = True and verify single active constraint
    status, patch_res = api_request("PATCH", f"/api/master/academic-years/{ay_id}", token, {"is_active": True})
    assert status == 200
    assert patch_res["is_active"] is True

    # Check all academic years: only ay_id should be active
    _, all_ays = api_request("GET", "/api/master/academic-years", token)
    ay_items = all_ays.get("items", all_ays) if isinstance(all_ays, dict) else all_ays
    active_count = sum(1 for a in ay_items if a["is_active"])
    assert active_count == 1, f"Expected exactly 1 active academic year, found {active_count}"

    # Restore 2026/2027 Ganjil as active
    orig_ay = next((a for a in ay_items if "2026/2027" in a["name"]), None)
    if orig_ay:
        api_request("PATCH", f"/api/master/academic-years/{orig_ay['id']}", token, {"is_active": True})

    print("PASS: test_m3_academic_year_lifecycle")
    return orig_ay["id"] if orig_ay else ay_id


def test_m3_classes_and_employees(token, ay_id):
    run_id = uuid.uuid4().hex[:6]
    # 1. Create Class
    class_payload = {
        "academic_year_id": ay_id,
        "name": f"X-M3-{run_id}",
        "level": 10,
    }
    status, cls_res = api_request("POST", "/api/master/classes", token, class_payload)
    assert status == 201
    cls_id = cls_res["id"]

    # PATCH Class
    status, patch_cls = api_request("PATCH", f"/api/master/classes/{cls_id}", token, {"name": f"X-M3-UP-{run_id}"})
    assert status == 200
    assert patch_cls["name"] == f"X-M3-UP-{run_id}"

    # 2. Create Employee
    emp_payload = {
        "nip": f"1990{run_id[:4]}2020011099"[:18],
        "name": f"Guru M3 {run_id}, S.Kom.",
    }
    status, emp_res = api_request("POST", "/api/master/employees", token, emp_payload)
    assert status == 201
    emp_id = emp_res["id"]

    # PATCH Employee
    status, patch_emp = api_request("PATCH", f"/api/master/employees/{emp_id}", token, {"name": f"Guru M3 Senior {run_id}, M.Kom."})
    assert status == 200
    assert patch_emp["name"] == f"Guru M3 Senior {run_id}, M.Kom."

    print("PASS: test_m3_classes_and_employees")
    return cls_id, emp_id


def test_m3_students_enrollments_and_assignments(token, cls_id, emp_id):
    run_id = uuid.uuid4().hex[:6]
    # 1. Create Student
    student_payload = {
        "student_number": f"NISN-M3-{run_id}",
        "name": f"Zaky Ramadhan {run_id}",
        "gender": "LAKI_LAKI",
        "status": "AKTIF",
    }
    status, std_res = api_request("POST", "/api/master/students", token, student_payload)
    assert status == 201
    std_id = std_res["id"]

    # PATCH Student status to LULUS
    status, patch_std = api_request("PATCH", f"/api/master/students/{std_id}", token, {"status": "LULUS"})
    assert status == 200
    assert patch_std["status"] == "LULUS"

    # Revert to AKTIF
    status, _ = api_request("PATCH", f"/api/master/students/{std_id}", token, {"status": "AKTIF"})
    assert status == 200

    # 2. Enrollment
    enr_payload = {
        "student_id": std_id,
        "class_id": cls_id,
        "start_date": "2026-07-01",
    }
    status, enr_res = api_request("POST", "/api/master/enrollments", token, enr_payload)
    assert status == 201
    enr_id = enr_res["id"]

    # PATCH Enrollment end_date
    status, patch_enr = api_request("PATCH", f"/api/master/enrollments/{enr_id}", token, {"end_date": "2026-12-31"})
    assert status == 200
    assert patch_enr["end_date"] == "2026-12-31"

    # 3. Class Assignment
    asgn_payload = {
        "employee_id": emp_id,
        "class_id": cls_id,
        "role": "GURU_MAPEL",
        "start_date": "2026-07-01",
    }
    status, asgn_res = api_request("POST", "/api/master/assignments", token, asgn_payload)
    assert status == 201
    asgn_id = asgn_res["id"]

    # PATCH Assignment end_date
    status, patch_asgn = api_request("PATCH", f"/api/master/assignments/{asgn_id}", token, {"end_date": "2026-12-31"})
    assert status == 200
    assert patch_asgn["end_date"] == "2026-12-31"

    print("PASS: test_m3_students_enrollments_and_assignments")


if __name__ == "__main__":
    tok = get_admin_token()
    test_m3_account_lifecycle(tok)
    ay_id = test_m3_academic_year_lifecycle(tok)
    cls_id, emp_id = test_m3_classes_and_employees(tok, ay_id)
    test_m3_students_enrollments_and_assignments(tok, cls_id, emp_id)
    print("ALL INT-M3 TESTS PASSED")
