import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import {
  Users,
  GraduationCap,
  ClipboardCheck,
  AlertCircle,
  FileText,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";

import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth-store";
import { MetricCard } from "@/components/molecules/MetricCard";
import { Button } from "@/components/atoms/Button";

interface DashboardMetricsResponse {
  role: string;
  academic_year_name?: string;
  active_students_count?: number;
  total_classes_count?: number;
  attendance_today?: {
    hadir: number;
    sakit: number;
    izin: number;
    alpa: number;
    percentage: number;
  };
  pending_requests_count?: number;
  active_cases_count?: number;
  assigned_classes_count?: number;
}

export const DashboardPage: React.FC = () => {
  const { user, activeRole } = useAuthStore();
  const currentRole = activeRole || user?.roles[0] || "Guru";

  // Query dashboard metrics
  const { data: metrics, isLoading } = useQuery<DashboardMetricsResponse>({
    queryKey: ["dashboard-metrics", currentRole],
    queryFn: async () => {
      const res =
        await apiClient.get<DashboardMetricsResponse>("/reports/dashboard");
      return res.data;
    },
  });

  const att = metrics?.attendance_today;

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="bg-surface p-6 rounded-card border border-border shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-sm bg-brand-primary-subtle text-brand-primary text-xs font-semibold mb-2">
            <ShieldCheck className="h-3.5 w-3.5" />
            Peran Aktif: {currentRole}
          </div>
          <h2 className="text-2xl font-bold tracking-tight text-text-foreground">
            Selamat Datang, {user?.name || user?.username}
          </h2>
          <p className="text-sm text-text-muted mt-0.5">
            Tahun Ajaran Aktif:{" "}
            <span className="font-semibold text-text-foreground">
              {metrics?.academic_year_name || "2026/2027"}
            </span>
          </p>
        </div>

        <div className="flex items-center gap-2">
          {currentRole === "Guru" || currentRole === "Wali Kelas" ? (
            <Link to="/attendance/record">
              <Button variant="primary">
                <ClipboardCheck className="h-4 w-4 mr-2" />
                Catat Kehadiran Hari Ini
              </Button>
            </Link>
          ) : currentRole === "Tata Usaha" ? (
            <Link to="/requests/new">
              <Button variant="primary">
                <FileText className="h-4 w-4 mr-2" />
                Buat Surat Permohonan
              </Button>
            </Link>
          ) : currentRole === "Pimpinan" ? (
            <Link to="/approvals">
              <Button variant="primary">
                <CheckCircle2 className="h-4 w-4 mr-2" />
                Tinjau Antrean Disposisi
              </Button>
            </Link>
          ) : currentRole === "Kesiswaan" ? (
            <Link to="/cases">
              <Button variant="primary">
                <AlertCircle className="h-4 w-4 mr-2" />
                Daftar Kasus Kesiswaan
              </Button>
            </Link>
          ) : (
            <Link to="/accounts">
              <Button variant="primary">
                <Users className="h-4 w-4 mr-2" />
                Kelola Akun Sistem
              </Button>
            </Link>
          )}
        </div>
      </div>

      {/* Role-Specific Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Metric 1 */}
        <MetricCard
          title="Siswa Terdaftar Aktif"
          value={isLoading ? "..." : (metrics?.active_students_count ?? 0)}
          subtitle="T.A. 2026/2027"
          icon={<GraduationCap className="h-5 w-5" />}
        />

        {/* Metric 2 */}
        <MetricCard
          title="Rombongan Belajar"
          value={isLoading ? "..." : (metrics?.total_classes_count ?? 0)}
          subtitle="Kelas 10, 11, dan 12"
          icon={<Users className="h-5 w-5" />}
        />

        {/* Metric 3: Presensi Hari Ini */}
        <MetricCard
          title="Tingkat Kehadiran Hari Ini"
          value={isLoading ? "..." : `${att?.percentage ?? 100}%`}
          subtitle={`${att?.hadir ?? 0} Hadir • ${att?.alpa ?? 0} Alpa`}
          icon={<ClipboardCheck className="h-5 w-5" />}
        />

        {/* Metric 4: Role Dependent */}
        {currentRole === "Pimpinan" || currentRole === "Tata Usaha" ? (
          <MetricCard
            title="Antrean Surat Masuk"
            value={isLoading ? "..." : (metrics?.pending_requests_count ?? 0)}
            subtitle="Menunggu proses / disposisi"
            icon={<FileText className="h-5 w-5" />}
          />
        ) : (
          <MetricCard
            title="Kasus Binaan Aktif"
            value={isLoading ? "..." : (metrics?.active_cases_count ?? 0)}
            subtitle="Dalam pemantauan BK"
            icon={<AlertCircle className="h-5 w-5" />}
          />
        )}
      </div>

      {/* Quick Navigation and Functional Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quick Actions Panel */}
        <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-text-foreground border-b border-border pb-3">
            Aksi Cepat Menu Utama
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Link
              to="/attendance/record"
              className="p-4 rounded-card border border-border bg-surface hover:bg-surface-subtle transition-all flex items-center justify-between group"
            >
              <div>
                <span className="font-semibold text-text-foreground block text-sm">
                  Pencatatan Presensi
                </span>
                <span className="text-xs text-text-muted">
                  Isi absensi kelas rombel
                </span>
              </div>
              <ArrowRight className="h-4 w-4 text-text-muted group-hover:text-brand-primary group-hover:translate-x-1 transition-all" />
            </Link>

            <Link
              to="/attendance/recap"
              className="p-4 rounded-card border border-border bg-surface hover:bg-surface-subtle transition-all flex items-center justify-between group"
            >
              <div>
                <span className="font-semibold text-text-foreground block text-sm">
                  Rekapitulasi Kehadiran
                </span>
                <span className="text-xs text-text-muted">
                  Pantau kehadiran berkala
                </span>
              </div>
              <ArrowRight className="h-4 w-4 text-text-muted group-hover:text-brand-primary group-hover:translate-x-1 transition-all" />
            </Link>

            <Link
              to="/cases"
              className="p-4 rounded-card border border-border bg-surface hover:bg-surface-subtle transition-all flex items-center justify-between group"
            >
              <div>
                <span className="font-semibold text-text-foreground block text-sm">
                  Bimbingan Konseling
                </span>
                <span className="text-xs text-text-muted">
                  Rekam catatan kasus siswa
                </span>
              </div>
              <ArrowRight className="h-4 w-4 text-text-muted group-hover:text-brand-primary group-hover:translate-x-1 transition-all" />
            </Link>

            <Link
              to="/reports"
              className="p-4 rounded-card border border-border bg-surface hover:bg-surface-subtle transition-all flex items-center justify-between group"
            >
              <div>
                <span className="font-semibold text-text-foreground block text-sm">
                  Laporan Resmi
                </span>
                <span className="text-xs text-text-muted">
                  Ekspor format Excel & PDF
                </span>
              </div>
              <ArrowRight className="h-4 w-4 text-text-muted group-hover:text-brand-primary group-hover:translate-x-1 transition-all" />
            </Link>
          </div>
        </div>

        {/* Operational Notice / Summary */}
        <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-3">
          <h3 className="text-base font-bold text-text-foreground border-b border-border pb-3">
            Informasi Operasional SMAN 1 Bunut
          </h3>
          <p className="text-xs text-text-muted leading-relaxed">
            Sistem Informasi Enterprise SMAN 1 Bunut beroperasi dengan
            pengamanan tingkat enterprise. Seluruh mutasi status persuratan dan
            kasus siswa dilindungi dengan kontrol konkurensi optimistik
            (*optimistic locking*) dan pencatatan jejak audit riil.
          </p>
          <div className="p-3.5 rounded-input bg-brand-primary-subtle border border-brand-primary/20 text-xs text-brand-primary space-y-1">
            <span className="font-bold block">Pemberitahuan Sistem:</span>
            <span>
              Pencatatan kehadiran harian disimpan secara permanen pada basis
              data sekolah. Pastikan memeriksa kembali rekap sebelum jam
              kepulangan siswa.
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
