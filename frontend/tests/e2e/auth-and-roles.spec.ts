import { test, expect } from "@playwright/test";
import * as path from "path";
import * as fs from "fs";

test.describe("E2E Role-Based Navigation & Workflow Verification", () => {
  const evidenceDir = path.resolve(process.cwd(), "evidence");

  test.beforeAll(() => {
    if (!fs.existsSync(evidenceDir)) {
      fs.mkdirSync(evidenceDir, { recursive: true });
    }
  });

  test("1. Administrator Login, Dashboard & Master Data", async ({ page }) => {
    await page.goto("/login");
    await expect(page.getByText("Sistem Informasi Enterprise")).toBeVisible();

    await page.fill("#username", "admin");
    await page.fill("#password", "Password123!");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.getByText("Peran Aktif: Administrator")).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-01-admin-dashboard.png"),
      fullPage: true,
    });

    // Client-side navigate to accounts via sidebar link
    await page.click('a[href="/accounts"]');
    await expect(page).toHaveURL(/.*\/accounts/);
    await expect(page.getByText("Tambah Akun")).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-02-admin-accounts.png"),
      fullPage: true,
    });

    // Client-side navigate to master academic
    await page.click('a[href="/academic"]');
    await expect(page).toHaveURL(/.*\/academic/);
    await expect(page.getByText("Layanan Persuratan TU")).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-03-admin-academic.png"),
      fullPage: true,
    });
  });

  test("2. Guru Login & Daily Attendance Roster", async ({ page }) => {
    await page.goto("/login");
    await page.fill("#username", "guru");
    await page.fill("#password", "Password123!");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.getByText("Peran Aktif: Guru")).toBeVisible();

    // Client-side navigate to record attendance via sidebar
    await page.click('a[href="/attendance/record"]');
    await expect(page).toHaveURL(/.*\/attendance\/record/);
    await expect(page.getByText("Tandai Semua Hadir")).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-04-guru-attendance.png"),
      fullPage: true,
    });
  });

  test("3. Wali Kelas Login & Class Attendance Recap", async ({ page }) => {
    await page.goto("/login");
    await page.fill("#username", "wali_kelas");
    await page.fill("#password", "Password123!");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.getByText("Peran Aktif: Wali Kelas")).toBeVisible();

    // Client-side navigate to attendance recap
    await page.click('a[href="/attendance/recap"]');
    await expect(page).toHaveURL(/.*\/attendance\/recap/);
    await expect(page.getByText("Rekapitulasi Kehadiran Siswa")).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-05-walikelas-recap.png"),
      fullPage: true,
    });
  });

  test("4. Kesiswaan Login & Case Management", async ({ page }) => {
    await page.goto("/login");
    await page.fill("#username", "kesiswaan");
    await page.fill("#password", "Password123!");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.getByText("Peran Aktif: Kesiswaan")).toBeVisible();

    // Client-side navigate to cases
    await page.click('a[href="/cases"]');
    await expect(page).toHaveURL(/.*\/cases/);
    await expect(page.getByText("Penanganan Kasus Kesiswaan")).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-06-kesiswaan-cases.png"),
      fullPage: true,
    });
  });

  test("5. Tata Usaha Login & Service Request Management", async ({ page }) => {
    await page.goto("/login");
    await page.fill("#username", "tata_usaha");
    await page.fill("#password", "Password123!");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.getByText("Peran Aktif: Tata Usaha")).toBeVisible();

    // Client-side navigate to requests
    await page.click('a[href="/requests"]');
    await expect(page).toHaveURL(/.*\/requests/);
    await expect(page.getByText("Buat Permohonan")).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-07-tu-requests.png"),
      fullPage: true,
    });
  });

  test("6. Pimpinan (Kepsek) Login & Approval Queue", async ({ page }) => {
    await page.goto("/login");
    await page.fill("#username", "kepsek");
    await page.fill("#password", "Password123!");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.getByText("Peran Aktif: Pimpinan")).toBeVisible();

    // Client-side navigate to approvals queue
    await page.click('a[href="/approvals"]');
    await expect(page).toHaveURL(/.*\/approvals/);
    await expect(
      page.getByText("Antrean Persetujuan Disposisi Pimpinan"),
    ).toBeVisible();
    await page.screenshot({
      path: path.join(evidenceDir, "e2e-08-kepsek-approvals.png"),
      fullPage: true,
    });
  });

  test("7. Multi-Role (Guru & Wali Kelas) Login & Role Union", async ({ page }) => {
    await page.goto("/login");
    await page.fill("#username", "guru_walikelas");
    await page.fill("#password", "Password123!");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.getByText(/Peran Aktif: (Guru|Wali Kelas)/)).toBeVisible();

    // Navigate to attendance record
    await page.click('a[href="/attendance/record"]');
    await expect(page).toHaveURL(/.*\/attendance\/record/);

    // Navigate to attendance recap
    await page.click('a[href="/attendance/recap"]');
    await expect(page).toHaveURL(/.*\/attendance\/recap/);
  });
});
