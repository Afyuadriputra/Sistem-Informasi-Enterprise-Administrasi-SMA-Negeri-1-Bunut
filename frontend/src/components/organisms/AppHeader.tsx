import * as React from "react";
import { Menu, LogOut, User, ChevronDown } from "lucide-react";
import { useAuthStore } from "@/stores/auth-store";
import { Link, useNavigate } from "react-router-dom";

export interface AppHeaderProps {
  onToggleSidebar: () => void;
  title?: string;
}

export const AppHeader: React.FC<AppHeaderProps> = ({
  onToggleSidebar,
  title,
}) => {
  const { user, activeRole, setActiveRole, logout } = useAuthStore();
  const navigate = useNavigate();
  const [isDropdownOpen, setIsDropdownOpen] = React.useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const userRoles = user?.roles || [];
  const hasMultipleRoles = userRoles.length > 1;

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-border bg-surface px-4 shadow-sm sm:px-6">
      {/* Left side: Hamburger button + Page Title */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onToggleSidebar}
          className="p-2 rounded-button text-text-muted hover:bg-surface-subtle hover:text-text-foreground lg:hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
          aria-label="Buka menu navigasi"
        >
          <Menu className="h-5 w-5" aria-hidden="true" />
        </button>
        {title && (
          <h2 className="text-lg font-bold text-text-foreground tracking-tight line-clamp-1">
            {title}
          </h2>
        )}
      </div>

      {/* Right side: Role context selector + User menu */}
      <div className="flex items-center gap-3">
        {/* Multi-role Context Selector */}
        {hasMultipleRoles && (
          <div className="hidden sm:flex items-center gap-2">
            <span className="text-xs text-text-muted">Konteks Peran:</span>
            <select
              value={activeRole || ""}
              onChange={(e) => setActiveRole(e.target.value)}
              className="h-8 rounded-input border border-border-input bg-surface px-2.5 text-xs font-medium text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
              aria-label="Pilih konteks peran"
            >
              {userRoles.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Profile Dropdown */}
        <div className="relative" ref={dropdownRef}>
          <button
            type="button"
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="flex items-center gap-2 p-1.5 rounded-button text-left hover:bg-surface-subtle focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
            aria-expanded={isDropdownOpen}
            aria-haspopup="true"
            aria-label="Menu pengguna"
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-primary text-white text-xs font-bold uppercase">
              {user?.name ? user.name.charAt(0) : "U"}
            </div>
            <div className="hidden md:block text-left">
              <div className="text-xs font-semibold text-text-foreground leading-tight">
                {user?.name || user?.username || "Pengguna"}
              </div>
              <div className="text-[11px] text-text-muted leading-tight">
                {activeRole || userRoles[0] || "Staf"}
              </div>
            </div>
            <ChevronDown
              className="h-3.5 w-3.5 text-text-muted hidden md:block"
              aria-hidden="true"
            />
          </button>

          {/* Dropdown Menu */}
          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-56 rounded-card border border-border bg-surface py-1 shadow-lg ring-1 ring-black/5 z-50 animate-in fade-in-0 zoom-in-95">
              <div className="px-4 py-2 border-b border-border">
                <p className="text-xs font-semibold text-text-foreground truncate">
                  {user?.name}
                </p>
                <p className="text-[11px] text-text-muted truncate">
                  @{user?.username}
                </p>
                <div className="mt-1 flex flex-wrap gap-1">
                  {userRoles.map((r) => (
                    <span
                      key={r}
                      className="px-1.5 py-0.5 rounded-sm bg-brand-primary-subtle text-brand-primary text-[10px] font-medium"
                    >
                      {r}
                    </span>
                  ))}
                </div>
              </div>

              <Link
                to="/profile"
                onClick={() => setIsDropdownOpen(false)}
                className="flex items-center gap-2 px-4 py-2 text-xs text-text-foreground hover:bg-surface-subtle"
              >
                <User className="h-4 w-4 text-text-muted" aria-hidden="true" />
                <span>Profil & Konteks Sesi</span>
              </Link>

              <div className="border-t border-border my-1" />

              <button
                type="button"
                onClick={handleLogout}
                className="flex w-full items-center gap-2 px-4 py-2 text-xs text-semantic-danger-fg hover:bg-red-50"
              >
                <LogOut className="h-4 w-4" aria-hidden="true" />
                <span>Keluar dari Sistem</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
