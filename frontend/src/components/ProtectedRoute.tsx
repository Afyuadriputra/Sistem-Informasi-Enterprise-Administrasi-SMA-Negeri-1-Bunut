import * as React from "react";
import { Navigate, useLocation, Link } from "react-router-dom";
import { ShieldX } from "lucide-react";
import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";

export interface ProtectedRouteProps {
  allowedRoles?: string[];
  children?: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  allowedRoles,
  children,
}) => {
  const { isAuthenticated, user, hasAnyRole } = useAuthStore();
  const location = useLocation();

  if (!isAuthenticated || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedRoles && allowedRoles.length > 0 && !hasAnyRole(allowedRoles)) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-6 bg-surface border border-border rounded-card">
        <div className="flex h-14 w-14 items-center justify-center rounded-panel bg-semantic-danger-bg text-semantic-danger-fg mb-4">
          <ShieldX className="h-8 w-8" aria-hidden="true" />
        </div>
        <h2 className="text-xl font-bold text-text-foreground mb-2">
          Akses Ditolak (403)
        </h2>
        <p className="text-sm text-text-muted max-w-md mb-6">
          Anda tidak memiliki wewenang peran yang sah untuk mengakses modul ini.
          Halaman ini hanya dapat diakses oleh peran:{" "}
          <span className="font-semibold">{allowedRoles.join(", ")}</span>.
        </p>
        <div className="flex gap-3">
          <Link to="/dashboard">
            <Button variant="primary">Kembali ke Dashboard</Button>
          </Link>
          <Link to="/profile">
            <Button variant="secondary">Periksa Profil & Peran</Button>
          </Link>
        </div>
      </div>
    );
  }

  return children ? <>{children}</> : null;
};
