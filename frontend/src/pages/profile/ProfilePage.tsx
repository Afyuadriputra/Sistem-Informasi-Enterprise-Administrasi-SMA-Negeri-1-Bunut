import * as React from "react";
import { useNavigate } from "react-router-dom";
import { Shield, BookOpen, KeyRound, LogOut } from "lucide-react";

import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";
import { ConfirmDialog } from "@/components/organisms/ConfirmDialog";
import { toast } from "sonner";

export const ProfilePage: React.FC = () => {
  const { user, activeRole, setActiveRole, logout } = useAuthStore();
  const navigate = useNavigate();
  const [showLogoutConfirm, setShowLogoutConfirm] = React.useState(false);
  const [isLoggingOut, setIsLoggingOut] = React.useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await logout();
      toast.success("Berhasil keluar dari sistem");
      navigate("/login");
    } catch {
      toast.error("Gagal keluar dari sesi");
    } finally {
      setIsLoggingOut(false);
      setShowLogoutConfirm(false);
    }
  };

  const userRoles = user?.roles || [];
  const assignedClasses = user?.assigned_classes || [];

  return (
    <div className="space-y-6">
      {/* Header Info Card */}
      <div className="bg-surface border border-border rounded-card p-6 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-brand-primary text-white text-2xl font-bold uppercase shadow-sm">
            {user?.name ? user.name.charAt(0) : "U"}
          </div>
          <div>
            <h2 className="text-xl font-bold text-text-foreground">
              {user?.name}
            </h2>
            <p className="text-sm text-text-muted">@{user?.username}</p>
            {user?.employee_id && (
              <p className="text-xs text-brand-primary font-medium mt-0.5">
                ID Pegawai: {user.employee_id}
              </p>
            )}
          </div>
        </div>

        <Button
          variant="danger"
          size="sm"
          onClick={() => setShowLogoutConfirm(true)}
        >
          <LogOut className="h-4 w-4 mr-2" aria-hidden="true" />
          Keluar dari Sesi
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Roles & Context Switcher Panel */}
        <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-border">
            <Shield className="h-5 w-5 text-brand-primary" aria-hidden="true" />
            <h3 className="text-base font-semibold text-text-foreground">
              Hak Akses & Konteks Peran
            </h3>
          </div>

          <div>
            <label className="text-xs font-semibold uppercase text-text-muted mb-2 block">
              Daftar Peran Sah Terdaftar:
            </label>
            <div className="flex flex-wrap gap-2">
              {userRoles.map((role) => (
                <span
                  key={role}
                  className="px-3 py-1 rounded-sm bg-brand-primary-subtle text-brand-primary text-xs font-semibold border border-brand-primary/20"
                >
                  {role}
                </span>
              ))}
            </div>
          </div>

          {userRoles.length > 1 && (
            <div className="pt-3 border-t border-border">
              <label
                htmlFor="context-role-select"
                className="text-xs font-semibold uppercase text-text-muted mb-2 block"
              >
                Pilih Konteks Navigasi Aktif:
              </label>
              <select
                id="context-role-select"
                value={activeRole || ""}
                onChange={(e) => {
                  setActiveRole(e.target.value);
                  toast.info(`Konteks navigasi diubah ke: ${e.target.value}`);
                }}
                className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
              >
                {userRoles.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
              <p className="text-xs text-text-muted mt-1.5">
                Mengubah konteks peran menyaring navigasi menu sesuai peran
                terkait tanpa mengurangi wewenang otorisasi gabungan (*additive
                union*) di server.
              </p>
            </div>
          )}
        </div>

        {/* Assigned Classes Panel (if any) */}
        <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-border">
            <BookOpen
              className="h-5 w-5 text-brand-accent"
              aria-hidden="true"
            />
            <h3 className="text-base font-semibold text-text-foreground">
              Penugasan Rombongan Belajar
            </h3>
          </div>

          {assignedClasses.length > 0 ? (
            <div className="divide-y divide-border">
              {assignedClasses.map((ac) => (
                <div
                  key={ac.id}
                  className="py-2.5 flex items-center justify-between text-sm"
                >
                  <div>
                    <span className="font-semibold text-text-foreground">
                      {ac.name}
                    </span>
                    <span className="text-xs text-text-muted ml-2">
                      Tingkat {ac.level}
                    </span>
                  </div>
                  <span className="px-2 py-0.5 rounded-sm bg-brand-accent-subtle text-brand-accent text-xs font-medium">
                    {ac.role || "Guru Pengampu"}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-text-muted py-4 text-center">
              Tidak ada rombel kelas yang ditugaskan secara langsung pada akun
              Anda.
            </p>
          )}
        </div>
      </div>

      {/* Security & Architecture Compliance Card */}
      <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-3">
        <div className="flex items-center gap-2 pb-2 border-b border-border">
          <KeyRound className="h-5 w-5 text-text-muted" aria-hidden="true" />
          <h3 className="text-base font-semibold text-text-foreground">
            Keamanan Sesi Enterprise
          </h3>
        </div>
        <p className="text-xs text-text-muted leading-relaxed">
          Sistem Informasi Enterprise SMAN 1 Bunut menerapkan standar keamanan
          Zero-Trust. Token otentikasi disimpan secara eksklusif dalam memori
          volatil aplikasi untuk mencegah eksfiltrasi token melalui serangan
          Cross-Site Scripting (XSS). Sesi otomatis diperbarui secara berkala
          melalui rotasi token atomik (*single-flight refresh*).
        </p>
      </div>

      <ConfirmDialog
        isOpen={showLogoutConfirm}
        onOpenChange={setShowLogoutConfirm}
        title="Konfirmasi Keluar Sesi"
        description="Apakah Anda yakin ingin keluar dari sistem? Seluruh token akses memori akan dicabut secara permanen."
        confirmLabel="Keluar Sekarang"
        variant="danger"
        isLoading={isLoggingOut}
        onConfirm={handleLogout}
      />
    </div>
  );
};
