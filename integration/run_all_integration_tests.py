"""
Master Integration Test Runner (INT-M1 through INT-M8)
Executes all integration milestones sequentially against live running services.
"""
import subprocess
import sys
from pathlib import Path


SCRIPTS = [
    ("INT-M1: Foundation Gate", "integration/test_int_m1_foundation.py"),
    ("INT-M2: Auth & Session Gate", "integration/test_int_m2_auth.py"),
    ("INT-M3: Master Data Gate", "integration/test_int_m3_master_data.py"),
    ("INT-M4: Attendance Gate", "integration/test_int_m4_attendance.py"),
    ("INT-M5: Affairs & Privacy Gate", "integration/test_int_m5_affairs.py"),
    ("INT-M6: Administration Gate", "integration/test_int_m6_administration.py"),
    ("INT-M7: Reports & Cache Gate", "integration/test_int_m7_reports.py"),
    ("INT-M8: 20 N2N Cross-Module Checks", "integration/test_n2n_cross_module.py"),
]


def main():
    print("=" * 70)
    print("  RUNNING FULL MASTER INTEGRATION TEST SUITE (INT-M1 s/d INT-M8)")
    print("=" * 70)

    all_passed = True
    summary = []

    for name, script in SCRIPTS:
        print(f"\n>>> Running {name} ({script}) ...")
        res = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"PASS: {name}")
            summary.append((name, "PASS", res.stdout.strip().split("\n")[-1]))
        else:
            print(f"FAIL: {name}")
            print(res.stdout)
            print(res.stderr)
            summary.append((name, "FAIL", "Error encountered"))
            all_passed = False

    print("\n" + "=" * 70)
    print("  MASTER INTEGRATION TEST SUMMARY")
    print("=" * 70)
    for name, status, msg in summary:
        print(f"[{status}] {name:<35} : {msg}")

    if all_passed:
        print("\nALL SYSTEM INTEGRATION MILESTONES (INT-M1 s/d INT-M8) PASSED 100%!")
        sys.exit(0)
    else:
        print("\nSOME INTEGRATION TESTS FAILED.")
        sys.exit(1)


if __name__ == "__main__":
    main()
