import * as React from "react";
import { School, ShieldCheck } from "lucide-react";
import { Toaster } from "sonner";

export const AuthLayout: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  return (
    <div className="flex min-h-screen w-full flex-col lg:flex-row bg-background">
      {/* Left panel: School Brand Identity (Desktop 50% / 60%) */}
      <div className="hidden lg:flex lg:w-1/2 flex-col justify-between bg-brand-primary p-12 text-white relative overflow-hidden">
        {/* Subtle decorative motif */}
        <div className="absolute -right-24 -bottom-24 w-96 h-96 rounded-full bg-brand-primary-hover/50 pointer-events-none" />
        <div className="absolute right-12 top-12 w-48 h-48 rounded-full bg-brand-accent/20 pointer-events-none" />

        {/* Top Header */}
        <div className="flex items-center gap-3 z-10">
          <div className="flex h-12 w-12 items-center justify-center rounded-panel bg-white text-brand-primary shadow-md">
            <School className="h-7 w-7" aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              SMA NEGERI 1 BUNUT
            </h1>
            <p className="text-xs text-brand-accent-subtle">
              Kecamatan Bunut, Kabupaten Pelalawan, Riau
            </p>
          </div>
        </div>

        {/* Central Credo */}
        <div className="space-y-4 max-w-md z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-sm bg-brand-accent/30 text-brand-accent-subtle text-xs font-semibold">
            <ShieldCheck className="h-4 w-4" aria-hidden="true" />
            Sistem Informasi Enterprise Terpadu
          </div>
          <h2 className="text-3xl font-bold tracking-tight leading-snug">
            Tata Kelola Administrasi & Presensi Digital Terpercaya.
          </h2>
          <p className="text-sm text-white/80 leading-relaxed">
            Menghubungkan pendidik, staf tata usaha, dan pimpinan sekolah dalam
            satu ekosistem digital yang akuntabel, aman, dan berintegritas
            tinggi.
          </p>
        </div>

        {/* Bottom Disclaimer */}
        <div className="text-xs text-white/60 z-10">
          <p>© 2026 SMA Negeri 1 Bunut. Hak cipta dilindungi undang-undang.</p>
        </div>
      </div>

      {/* Right panel: Login form container */}
      <div className="flex flex-1 flex-col justify-center items-center p-6 sm:p-12 lg:w-1/2">
        <div className="w-full max-w-md space-y-6">
          {/* Mobile Brand Header */}
          <div className="flex items-center gap-3 lg:hidden mb-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-panel bg-brand-primary text-white shadow-sm">
              <School className="h-6 w-6" aria-hidden="true" />
            </div>
            <div>
              <h2 className="text-base font-bold text-text-foreground">
                SMAN 1 BUNUT
              </h2>
              <p className="text-xs text-text-muted">
                Sistem Administrasi Enterprise
              </p>
            </div>
          </div>

          {children}
        </div>
      </div>

      <Toaster position="top-right" richColors closeButton />
    </div>
  );
};
