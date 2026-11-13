import * as React from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  GraduationCap,
  BookOpen,
  UserCheck,
  ClipboardCheck,
  BarChart3,
  AlertCircle,
  FileText,
  Archive,
  FileSpreadsheet,
  ShieldAlert,
  School,
  X,
} from "lucide-react";
import { useAuthStore } from "@/stores/auth-store";
import { cn } from "@/lib/utils";

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  roles: string[];
}

const ALL_NAV_ITEMS: NavItem[] = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
    roles: [
      "Administrator",
      "Guru",
      "Wali Kelas",
      "Kesiswaan",
      "Tata Usaha",
      "Pimpinan",
    ],
  },
  {
    name: "Manajemen Akun",
    href: "/accounts",
    icon: Users,
    roles: ["Administrator"],
  },
  {
    name: "Data Siswa",
    href: "/students",
    icon: GraduationCap,
    roles: ["Administrator", "Kesiswaan"],
  },
  {
    name: "Data Akademik",
    href: "/academic",
    icon: BookOpen,
    roles: ["Administrator"],
  },
  {
    name: "Penempatan & Penugasan",
    href: "/assignments",
    icon: UserCheck,
    roles: ["Administrator"],
  },
  {
    name: "Catat Kehadiran",
    href: "/attendance/record",
    icon: ClipboardCheck,
    roles: ["Guru", "Wali Kelas"],
  },
  {
    name: "Rekap Kehadiran",
    href: "/attendance/recap",
    icon: BarChart3,
    roles: ["Guru", "Wali Kelas"],
  },
  {
    name: "Kasus Kesiswaan & BK",
    href: "/cases",
    icon: AlertCircle,
    roles: ["Kesiswaan", "Wali Kelas", "Guru"],
  },
  {
    name: "Layanan Persuratan",
    href: "/requests",
    icon: FileText,
    roles: ["Tata Usaha"],
  },
  {
    name: "Persetujuan Disposisi",
    href: "/approvals",
    icon: FileText,
    roles: ["Pimpinan"],
  },
  {
    name: "Arsip Dokumen Digital",
    href: "/documents",
    icon: Archive,
    roles: ["Tata Usaha", "Pimpinan"],
  },
  {
    name: "Laporan & Ekspor",
    href: "/reports",
    icon: FileSpreadsheet,
    roles: ["Pimpinan", "Tata Usaha"],
  },
  {
    name: "Log Audit Sistem",
    href: "/audit-logs",
    icon: ShieldAlert,
    roles: ["Administrator"],
  },
];

export interface AppSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AppSidebar: React.FC<AppSidebarProps> = ({ isOpen, onClose }) => {
  const { user, activeRole } = useAuthStore();
  const userRoles = user?.roles || [];

  // Filter items: if activeRole is selected, check that role; otherwise check union of userRoles
  const visibleNavItems = ALL_NAV_ITEMS.filter((item) => {
    if (activeRole) {
      return item.roles.includes(activeRole);
    }
    return item.roles.some((r) => userRoles.includes(r));
  });

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex flex-col w-64 bg-brand-primary text-white transition-transform duration-200 ease-in-out lg:static lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        {/* Brand Header */}
        <div className="flex items-center justify-between h-16 px-4 bg-brand-primary-hover border-b border-brand-primary/50">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-panel bg-white text-brand-primary shadow-sm">
              <School className="h-6 w-6" aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-sm font-bold tracking-tight text-white leading-tight">
                SMAN 1 BUNUT
              </h1>
              <p className="text-xs text-brand-accent-subtle">
                Sistem Informasi Enterprise
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1 rounded-sm text-white/80 hover:text-white lg:hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"
            aria-label="Tutup menu navigasi"
          >
            <X className="h-5 w-5" aria-hidden="true" />
          </button>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          {visibleNavItems.map((item) => (
            <NavLink
              key={item.href}
              to={item.href}
              onClick={() => onClose()}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-button text-sm font-medium transition-colors select-none",
                  isActive
                    ? "bg-brand-accent text-white shadow-sm font-semibold"
                    : "text-white/80 hover:bg-brand-primary-hover hover:text-white",
                )
              }
            >
              <item.icon className="h-5 w-5 shrink-0" aria-hidden="true" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </nav>

        {/* School Footer Metadata */}
        <div className="p-4 bg-brand-primary-hover/50 border-t border-brand-primary/40 text-xs text-white/70">
          <p className="font-medium text-white">SMA Negeri 1 Bunut</p>
          <p className="text-[11px] text-white/60">
            T.A. 2026/2027 • Pelalawan, Riau
          </p>
        </div>
      </aside>
    </>
  );
};
