import * as React from "react";
import { cn } from "@/lib/utils";

export type StatusType =
  // Attendance
  | "HADIR"
  | "SAKIT"
  | "IZIN"
  | "ALPA"
  // Student Case
  | "BARU"
  | "DIPROSES"
  | "SELESAI"
  | "DIBATALKAN"
  // Service Request
  | "DIAJUKAN"
  | "MENUNGGU_PERSETUJUAN"
  | "DISETUJUI"
  | "DITOLAK"
  // Master / General
  | "AKTIF"
  | "NONAKTIF"
  | "LULUS"
  | "MUTASI"
  | "KELUAR"
  | "DO"
  | string;

interface StatusBadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  status: StatusType;
  label?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  label,
  className,
  ...props
}) => {
  const normalized = (status || "").toUpperCase();

  let colorClasses = "bg-surface-subtle text-text-muted border-border";
  let displayLabel = label || status;

  switch (normalized) {
    // Green Success
    case "HADIR":
    case "DISETUJUI":
    case "SELESAI":
    case "AKTIF":
      colorClasses =
        "bg-semantic-success-bg text-semantic-success-fg border-semantic-success-border";
      if (!label) {
        if (normalized === "HADIR") displayLabel = "Hadir";
        if (normalized === "DISETUJUI") displayLabel = "Disetujui";
        if (normalized === "SELESAI") displayLabel = "Selesai";
        if (normalized === "AKTIF") displayLabel = "Aktif";
      }
      break;

    // Amber Warning
    case "IZIN":
    case "MENUNGGU_PERSETUJUAN":
    case "MUTASI":
    case "MUTASI_KELUAR":
      colorClasses =
        "bg-semantic-warning-bg text-semantic-warning-fg border-semantic-warning-border";
      if (!label) {
        if (normalized === "IZIN") displayLabel = "Izin";
        if (normalized === "MENUNGGU_PERSETUJUAN")
          displayLabel = "Menunggu Persetujuan";
        if (normalized === "MUTASI" || normalized === "MUTASI_KELUAR")
          displayLabel = "Mutasi Keluar";
      }
      break;

    // Red Danger
    case "ALPA":
    case "DITOLAK":
    case "DIBATALKAN":
    case "NONAKTIF":
    case "KELUAR":
    case "DO":
      colorClasses =
        "bg-semantic-danger-bg text-semantic-danger-fg border-semantic-danger-border";
      if (!label) {
        if (normalized === "ALPA") displayLabel = "Alpa";
        if (normalized === "DITOLAK") displayLabel = "Ditolak";
        if (normalized === "DIBATALKAN") displayLabel = "Dibatalkan";
        if (normalized === "NONAKTIF") displayLabel = "Nonaktif";
        if (normalized === "KELUAR") displayLabel = "Keluar";
        if (normalized === "DO") displayLabel = "Drop Out";
      }
      break;

    // Blue / Info
    case "SAKIT":
    case "DIPROSES":
    case "DIAJUKAN":
    case "BARU":
    case "LULUS":
      colorClasses =
        "bg-semantic-info-bg text-semantic-info-fg border-semantic-info-border";
      if (!label) {
        if (normalized === "SAKIT") displayLabel = "Sakit";
        if (normalized === "DIPROSES") displayLabel = "Diproses";
        if (normalized === "DIAJUKAN") displayLabel = "Diajukan";
        if (normalized === "BARU") displayLabel = "Baru";
        if (normalized === "LULUS") displayLabel = "Lulus";
      }
      break;

    default:
      colorClasses = "bg-surface-subtle text-text-muted border-border";
  }

  return (
    <span
      className={cn(
        "inline-flex items-center px-2.5 py-0.5 rounded-sm text-xs font-medium border select-none",
        colorClasses,
        className,
      )}
      {...props}
    >
      {displayLabel}
    </span>
  );
};
