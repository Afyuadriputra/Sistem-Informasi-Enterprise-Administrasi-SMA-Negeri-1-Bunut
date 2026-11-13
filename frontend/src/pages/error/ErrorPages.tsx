import * as React from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ShieldAlert,
  FileQuestion,
  ServerCrash,
  RefreshCw,
} from "lucide-react";
import { Button } from "@/components/atoms/Button";

export const NotFoundPage: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6 bg-surface border border-border rounded-card shadow-sm">
      <div className="flex h-16 w-16 items-center justify-center rounded-panel bg-brand-primary-subtle text-brand-primary mb-4">
        <FileQuestion className="h-8 w-8" aria-hidden="true" />
      </div>
      <h2 className="text-2xl font-bold text-text-foreground mb-2">
        Halaman Tidak Ditemukan (404)
      </h2>
      <p className="text-sm text-text-muted max-w-md mb-6 leading-relaxed">
        Tautan atau rute yang Anda tuju tidak terdaftar dalam sistem informasi
        SMA Negeri 1 Bunut.
      </p>
      <Link to="/dashboard">
        <Button variant="primary">Kembali ke Dashboard</Button>
      </Link>
    </div>
  );
};

export const ForbiddenPage: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6 bg-surface border border-border rounded-card shadow-sm">
      <div className="flex h-16 w-16 items-center justify-center rounded-panel bg-semantic-danger-bg text-semantic-danger-fg mb-4">
        <ShieldAlert className="h-8 w-8" aria-hidden="true" />
      </div>
      <h2 className="text-2xl font-bold text-text-foreground mb-2">
        Akses Terbatas (403)
      </h2>
      <p className="text-sm text-text-muted max-w-md mb-6 leading-relaxed">
        Anda tidak memiliki wewenang peran yang sah untuk mengakses halaman atau
        fitur ini.
      </p>
      <div className="flex gap-3">
        <Link to="/dashboard">
          <Button variant="primary">Kembali ke Dashboard</Button>
        </Link>
        <Link to="/profile">
          <Button variant="secondary">Cek Profil Akun</Button>
        </Link>
      </div>
    </div>
  );
};

export const ServerErrorPage: React.FC<{ onRetry?: () => void }> = ({
  onRetry,
}) => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6 bg-surface border border-border rounded-card shadow-sm">
      <div className="flex h-16 w-16 items-center justify-center rounded-panel bg-semantic-danger-bg text-semantic-danger-fg mb-4">
        <ServerCrash className="h-8 w-8" aria-hidden="true" />
      </div>
      <h2 className="text-2xl font-bold text-text-foreground mb-2">
        Kendala Sistem (500)
      </h2>
      <p className="text-sm text-text-muted max-w-md mb-6 leading-relaxed">
        Terjadi kendala saat menghubungkan ke server aplikasi. Silakan muat
        ulang halaman atau coba beberapa saat lagi.
      </p>
      <div className="flex gap-3">
        <Button
          variant="primary"
          onClick={() => (onRetry ? onRetry() : window.location.reload())}
        >
          <RefreshCw className="h-4 w-4 mr-2" /> Muat Ulang Halaman
        </Button>
        <Button variant="secondary" onClick={() => navigate("/dashboard")}>
          Dashboard
        </Button>
      </div>
    </div>
  );
};
