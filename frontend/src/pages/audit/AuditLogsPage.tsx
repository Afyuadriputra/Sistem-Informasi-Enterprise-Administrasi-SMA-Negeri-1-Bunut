import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { ShieldAlert } from "lucide-react";

import { apiClient } from "@/lib/api-client";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import { PaginationControl } from "@/components/molecules/PaginationControl";
import { formatDateTime } from "@/lib/formatters";

interface AuditLogItem {
  id: number;
  user_id?: number | null;
  username?: string | null;
  action: string;
  resource_type: string;
  resource_id?: string | null;
  ip_address?: string | null;
  request_id?: string | null;
  created_at: string;
}

interface AuditLogListResponse {
  items: AuditLogItem[];
  total: number;
  page: number;
  page_size: number;
}

export const AuditLogsPage: React.FC = () => {
  const [page, setPage] = React.useState(1);
  const pageSize = 15;

  const { data, isLoading } = useQuery<AuditLogListResponse>({
    queryKey: ["audit-logs", page, pageSize],
    queryFn: async () => {
      const res = await apiClient.get<AuditLogListResponse>("/audit-logs", {
        params: { page, page_size: pageSize },
      });
      return res.data;
    },
  });

  const columns: ColumnDef<AuditLogItem>[] = [
    {
      header: "Waktu Kejadian",
      cell: (log) => (
        <span className="text-xs font-mono text-text-muted">
          {formatDateTime(log.created_at)}
        </span>
      ),
    },
    {
      header: "Aktor Pengguna",
      cell: (log) => (
        <span className="font-semibold text-text-foreground">
          {log.username || (log.user_id ? `User #${log.user_id}` : "Sistem")}
        </span>
      ),
    },
    {
      header: "Tindakan (Action)",
      cell: (log) => (
        <span className="px-2 py-0.5 rounded-sm bg-brand-primary-subtle text-brand-primary text-xs font-mono font-bold">
          {log.action}
        </span>
      ),
    },
    {
      header: "Objek / Modul",
      cell: (log) => (
        <span className="text-xs font-mono">
          {log.resource_type} {log.resource_id ? `(#${log.resource_id})` : ""}
        </span>
      ),
    },
    {
      header: "IP / Request ID",
      cell: (log) => (
        <div className="text-[11px] font-mono text-text-muted truncate max-w-xs">
          {log.ip_address || "-"} {log.request_id ? `• ${log.request_id}` : ""}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-surface p-5 rounded-card border border-border shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-text-foreground">
            Log Rekaman Jejak Audit Sistem
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Audit trail kronologis seluruh aksi dan mutasi data oleh pengguna
            pada aplikasi enterprise SMAN 1 Bunut.
          </p>
        </div>
        <div className="flex items-center gap-2 p-2 rounded-panel bg-brand-primary-subtle text-brand-primary text-xs font-semibold">
          <ShieldAlert className="h-4 w-4" />
          <span>Akses Terproteksi Administrator</span>
        </div>
      </div>

      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<AuditLogItem>
          columns={columns}
          data={data?.items || []}
          isLoading={isLoading}
          keyExtractor={(item) => item.id}
          emptyTitle="Belum Ada Log Audit"
          emptyDescription="Rekaman aktivitas pengguna belum tersedia."
        />

        <PaginationControl
          currentPage={page}
          pageSize={pageSize}
          totalItems={data?.total || 0}
          onPageChange={setPage}
        />
      </div>
    </div>
  );
};
