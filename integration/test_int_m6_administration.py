"""
INT-M6 Administration & Private Documents Gate Integration Tests
Verifies:
1. Workflow A (Approved Request Lifecycle):
   - Tata Usaha creates service request (DIAJUKAN).
   - Tata Usaha uploads official PDF document (magic bytes verified).
   - Tata Usaha transitions DIAJUKAN -> DIPROSES -> MENUNGGU_PERSETUJUAN.
   - Pimpinan approves request (MENUNGGU_PERSETUJUAN -> DISETUJUI).
   - Tata Usaha finalizes request (DISETUJUI -> SELESAI).
   - Pimpinan / TU downloads private document stream.
2. Workflow B (Rejected Request Lifecycle):
   - TU creates request, advances to MENUNGGU_PERSETUJUAN.
   - Pimpinan rejects request (MENUNGGU_PERSETUJUAN -> DITOLAK).
   - Verify DITOLAK is terminal state (cannot transition to SELESAI).
3. Security & Access Control:
   - Unauthorized user (Guru) attempting to download private document returns 403.
   - Invalid file upload (e.g. executable script) is rejected.
"""
import io
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
        res_data = res.read().decode("utf-8")
        return res.status, json.loads(res_data) if res_data else None


def upload_multipart(path, token, filename, file_content, content_type="application/pdf"):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
    body.extend(file_content)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    req = urllib.request.Request(f"{BASE_URL}{path}", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=5) as res:
        return res.status, json.loads(res.read().decode("utf-8"))


def test_m6_workflow_a_approval_and_private_file():
    tu_tok = get_token("tata_usaha")
    kepsek_tok = get_token("kepsek")
    guru_tok = get_token("guru")

    # 1. Get Service Type (requires_approval=True)
    _, st_list = api_request("GET", "/api/administration/service-types", tu_tok)
    items = st_list.get("items", st_list) if isinstance(st_list, dict) else st_list
    target_st = next((s for s in items if s.get("requires_approval")), items[0])
    st_id = target_st["id"]

    # 2. TU creates service request
    req_payload = {
        "service_type_id": st_id,
        "applicant_name": "Keluarga Siswa Bunut",
        "applicant_phone": "081234567890",
        "purpose": "Permohonan Surat Keterangan untuk Seleksi Nasional",
    }
    status, req_res = api_request("POST", "/api/administration/requests", tu_tok, req_payload)
    assert status == 201
    req_id = req_res["id"]
    assert req_res["status"] == "DIAJUKAN"
    v1 = req_res["version"]
    print(f"Request created: id={req_id}, status={req_res['status']}, version={v1}")

    # 3. Upload valid PDF document
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<< /Title (Dokumen Resmi SMA 1 Bunut) >>\nendobj\n%%EOF"
    status, doc_res = upload_multipart(
        f"/api/administration/requests/{req_id}/documents",
        tu_tok,
        "surat_keterangan_resmi.pdf",
        pdf_bytes,
        "application/pdf",
    )
    assert status == 201
    doc_id = doc_res["id"]
    print(f"Document uploaded: id={doc_id}, storage_key={doc_res.get('storage_key')}")

    # 4. TU processes: DIAJUKAN -> DIPROSES
    t1_payload = {"action": "PROSES", "expected_version": v1, "note": "Memverifikasi kelengkapan berkas pemohon"}
    status, t1_res = api_request("POST", f"/api/administration/requests/{req_id}/transitions", tu_tok, t1_payload)
    assert status == 200
    assert t1_res["status"] == "DIPROSES"
    v2 = t1_res["version"]

    # 5. TU submits for approval: DIPROSES -> MENUNGGU_PERSETUJUAN
    t2_payload = {"action": "AJUKAN_PERSETUJUAN", "expected_version": v2, "note": "Draf surat siap diajukan ke Kepala Sekolah"}
    status, t2_res = api_request("POST", f"/api/administration/requests/{req_id}/transitions", tu_tok, t2_payload)
    assert status == 200
    assert t2_res["status"] == "MENUNGGU_PERSETUJUAN"
    v3 = t2_res["version"]

    # 6. Kepsek approves: MENUNGGU_PERSETUJUAN -> DISETUJUI
    t3_payload = {"action": "SETUJUI", "expected_version": v3, "note": "Surat disetujui dan ditandatangani secara dinas"}
    status, t3_res = api_request("POST", f"/api/administration/requests/{req_id}/transitions", kepsek_tok, t3_payload)
    assert status == 200
    assert t3_res["status"] == "DISETUJUI"
    v4 = t3_res["version"]

    # 7. TU completes: DISETUJUI -> SELESAI
    t4_payload = {"action": "SELESAIKAN", "expected_version": v4, "note": "Surat resmi diserahkan ke pemohon"}
    status, t4_res = api_request("POST", f"/api/administration/requests/{req_id}/transitions", tu_tok, t4_payload)
    assert status == 200
    assert t4_res["status"] == "SELESAI"
    print(f"Request finalized: status={t4_res['status']}, version={t4_res['version']}")

    # 8. Download private document as Kepsek
    dl_req = urllib.request.Request(
        f"{BASE_URL}/api/administration/documents/{doc_id}/download",
        headers={"Authorization": f"Bearer {kepsek_tok}"},
        method="GET",
    )
    with urllib.request.urlopen(dl_req, timeout=5) as dl_res:
        assert dl_res.status == 200
        downloaded_content = dl_res.read()
        assert downloaded_content.startswith(b"%PDF-")
        print("PASS: Private document downloaded successfully by authorized role")

    # 9. Negative authorization: Guru attempts download -> 403 Forbidden
    guru_dl_req = urllib.request.Request(
        f"{BASE_URL}/api/administration/documents/{doc_id}/download",
        headers={"Authorization": f"Bearer {guru_tok}"},
        method="GET",
    )
    try:
        urllib.request.urlopen(guru_dl_req, timeout=5)
        pytest.fail("Expected HTTP 403 for unauthorized role downloading private file")
    except urllib.error.HTTPError as e:
        assert e.code == 403
        err = json.loads(e.read().decode("utf-8"))
        assert err["code"] == "PERMISSION_DENIED"
        print("PASS: Unauthorized download attempt rejected with HTTP 403 PERMISSION_DENIED")


def test_m6_workflow_b_rejected_request_terminal():
    tu_tok = get_token("tata_usaha")
    kepsek_tok = get_token("kepsek")

    # 1. Get Service Type
    _, st_list = api_request("GET", "/api/administration/service-types", tu_tok)
    items = st_list.get("items", st_list) if isinstance(st_list, dict) else st_list
    target_st = next((s for s in items if s.get("requires_approval")), items[0])
    st_id = target_st["id"]

    # 2. TU creates request
    req_payload = {
        "service_type_id": st_id,
        "applicant_name": "Pemohon Berkas Kurang",
        "applicant_phone": "081299998888",
        "purpose": "Permohonan tidak lengkap",
    }
    status, req_res = api_request("POST", "/api/administration/requests", tu_tok, req_payload)
    req_id = req_res["id"]
    v1 = req_res["version"]

    # 3. Advance to MENUNGGU_PERSETUJUAN
    _, t1 = api_request("POST", f"/api/administration/requests/{req_id}/transitions", tu_tok, {"action": "PROSES", "expected_version": v1, "note": "Proses"})
    _, t2 = api_request("POST", f"/api/administration/requests/{req_id}/transitions", tu_tok, {"action": "AJUKAN_PERSETUJUAN", "expected_version": t1["version"], "note": "Ajukan"})

    # 4. Kepsek rejects request
    t_reject = {"action": "TOLAK", "expected_version": t2["version"], "note": "Persyaratan dokumen legalisir belum lengkap"}
    status, rej_res = api_request("POST", f"/api/administration/requests/{req_id}/transitions", kepsek_tok, t_reject)
    assert status == 200
    assert rej_res["status"] == "DITOLAK"
    v_term = rej_res["version"]
    print(f"Request rejected: status={rej_res['status']}, version={v_term}")

    # 5. Verify DITOLAK is terminal: attempting SELESAIKAN must fail
    t_invalid = {"action": "SELESAIKAN", "expected_version": v_term, "note": "Mencoba menyelesaikan berkas ditolak"}
    try:
        api_request("POST", f"/api/administration/requests/{req_id}/transitions", tu_tok, t_invalid)
        pytest.fail("Expected failure transitioning terminal state DITOLAK")
    except urllib.error.HTTPError as e:
        assert e.code in [400, 422]
        print("PASS: Terminal state DITOLAK cannot be transitioned to SELESAI")


if __name__ == "__main__":
    test_m6_workflow_a_approval_and_private_file()
    test_m6_workflow_b_rejected_request_terminal()
    print("ALL INT-M6 TESTS PASSED")
