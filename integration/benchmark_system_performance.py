"""
System Performance & Latency Benchmark Script
Measures real HTTP round-trip latency (p50, p95, p99) and throughput (RPS)
against the running backend server.
"""
import json
import time
import urllib.request
import statistics


BASE_URL = "http://127.0.0.1:8000"


def get_token(username):
    payload = json.dumps({"username": username, "password": "Password123!"}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as res:
        return json.loads(res.read().decode("utf-8"))["access_token"]


def measure_endpoint(name, method, path, token=None, body=None, iterations=30):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(body).encode("utf-8") if body is not None else None

    latencies_ms = []
    t_start = time.perf_counter()

    for _ in range(iterations):
        req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers=headers, method=method)
        t0 = time.perf_counter()
        with urllib.request.urlopen(req, timeout=10) as res:
            res.read()
        t1 = time.perf_counter()
        latencies_ms.append((t1 - t0) * 1000.0)

    total_time = time.perf_counter() - t_start
    latencies_ms.sort()

    p50 = statistics.median(latencies_ms)
    p95 = latencies_ms[int(len(latencies_ms) * 0.95)]
    p99 = latencies_ms[int(len(latencies_ms) * 0.99)]
    avg = statistics.mean(latencies_ms)
    rps = iterations / total_time

    print(f"| {name:<30} | {avg:>7.2f} ms | {p50:>7.2f} ms | {p95:>7.2f} ms | {p99:>7.2f} ms | {rps:>7.1f} req/s |")
    return {
        "name": name,
        "avg_ms": round(avg, 2),
        "p50_ms": round(p50, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "rps": round(rps, 1),
    }


def run_benchmarks():
    print("=== STARTING PERFORMANCE LATENCY BENCHMARKS ===")
    print(f"| {'Endpoint Operation':<30} | {'Mean':>10} | {'p50':>10} | {'p95':>10} | {'p99':>10} | {'Throughput':>13} |")
    print(f"|{'-'*32}|{'-'*12}|{'-'*12}|{'-'*12}|{'-'*12}|{'-'*15}|")

    results = []
    # 1. Healthcheck
    results.append(measure_endpoint("GET /api/health", "GET", "/api/health", iterations=40))

    # 2. Login
    results.append(measure_endpoint(
        "POST /api/auth/login",
        "POST",
        "/api/auth/login",
        body={"username": "admin", "password": "Password123!"},
        iterations=20,
    ))

    admin_tok = get_token("admin")
    guru_tok = get_token("guru")
    wali_tok = get_token("wali_kelas")
    tu_tok = get_token("tata_usaha")

    # Get XI-MIPA-1 class id
    req = urllib.request.Request(f"{BASE_URL}/api/master/classes", headers={"Authorization": f"Bearer {admin_tok}"})
    with urllib.request.urlopen(req) as res:
        cls_data = json.loads(res.read().decode("utf-8"))
        cls_items = cls_data.get("items", cls_data) if isinstance(cls_data, dict) else cls_data
        target_cls = next((c for c in cls_items if c["name"] == "XI-MIPA-1"), cls_items[0])
        cls_id = target_cls["id"]

    # 3. List Students
    results.append(measure_endpoint("GET /api/master/students", "GET", "/api/master/students?page=1&page_size=20", admin_tok, iterations=30))

    # 4. Attendance Roster
    results.append(measure_endpoint("GET /api/attendance/roster", "GET", f"/api/attendance/roster?class_id={cls_id}&date=2026-11-14", guru_tok, iterations=30))

    # 5. Attendance Recap
    results.append(measure_endpoint("GET /api/attendance (recap)", "GET", f"/api/attendance?class_id={cls_id}&date_from=2026-01-01&date_to=2026-12-31", wali_tok, iterations=30))

    # 6. Dashboard Metrics
    results.append(measure_endpoint("GET /api/reports/dashboard", "GET", "/api/reports/dashboard", guru_tok, iterations=30))

    # 7. List Service Requests
    results.append(measure_endpoint("GET /api/administration/requests", "GET", "/api/administration/requests?page=1&page_size=20", tu_tok, iterations=30))

    # 8. List Audit Logs
    results.append(measure_endpoint("GET /api/audit-logs", "GET", "/api/audit-logs?page=1&page_size=20", admin_tok, iterations=25))

    # 9. PDF Report Generation
    results.append(measure_endpoint("GET /reports/administration.pdf", "GET", "/api/reports/administration.pdf?start_date=2026-01-01&end_date=2026-12-31", tu_tok, iterations=15))

    print("=== BENCHMARK COMPLETED ===")
    return results


if __name__ == "__main__":
    run_benchmarks()
