import * as React from "react";
import { Outlet, useLocation } from "react-router-dom";
import { Toaster } from "sonner";
import { AppSidebar } from "@/components/organisms/AppSidebar";
import { AppHeader } from "@/components/organisms/AppHeader";

const ROUTE_TITLES: Record<string, string> = {
  "/dashboard": "Dashboard Terpadu",
  "/accounts": "Manajemen Akun Pengguna",
  "/students": "Data Induk Siswa",
  "/academic": "Data Akademik Sekolah",
  "/assignments": "Penempatan Rombel & Penugasan Guru",
  "/attendance/record": "Pencatatan Kehadiran Kelas",
  "/attendance/recap": "Rekapitulasi Kehadiran Siswa",
  "/cases": "Penanganan Kasus Kesiswaan & Bimbingan Konseling",
  "/requests": "Layanan Administrasi Persuratan",
  "/approvals": "Antrean Persetujuan Disposisi Surat",
  "/documents": "Arsip Dokumen Digital Terbit",
  "/reports": "Laporan Terpadu & Ekspor Data",
  "/audit-logs": "Log Rekaman Jejak Audit Sistem",
  "/profile": "Profil Pengguna & Konteks Sesi",
};

export const AppLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);
  const location = useLocation();

  // Determine current page title
  const currentTitle =
    ROUTE_TITLES[location.pathname] || "Sistem Informasi Enterprise";

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* Skip to main content for accessibility */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-brand-primary focus:text-white focus:rounded-button focus:shadow-lg focus:outline-none"
      >
        Lewati ke konten utama
      </a>

      {/* App Sidebar */}
      <AppSidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content Area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <AppHeader
          title={currentTitle}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        />

        <main
          id="main-content"
          tabIndex={-1}
          className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 outline-none"
        >
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Toast notifications */}
      <Toaster position="top-right" richColors closeButton />
    </div>
  );
};
