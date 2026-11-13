import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { Eye } from "lucide-react";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/atoms/Button";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import { formatDate } from "@/lib/formatters";

interface ApprovalItem {
  id: number;
  request_number: string;
  service_type_name?: string;
  student_name?: string;
  applicant_name: string;
  purpose: string;
  status: string;
  version: number;
  created_at: string;
}

export const ApprovalsQueuePage: React.FC = () => {
  const navigate = useNavigate();

  const { data, isLoading } = useQuery<{ items: ApprovalItem[] }>({
    queryKey: ["approvals-queue"],
    queryFn: async () => {
      const res = await apiClient.get("/administration/requests", {
        params: { status: "MENUNGGU_PERSETUJUAN" },
      });
      return res.data;
    },
  });

  const columns: ColumnDef<ApprovalItem>[] = [
    {
      header: "No. Surat",
      accessorKey: "request_number",
      className: "font-mono text-xs font-semibold",
    },
    {
      header: "Layanan & Keperluan",
      cell: (r) => (
        <div>
          <span className="font-semibold text-text-foreground">
            {r.service_type_name}
          </span>
          <span className="text-xs text-text-muted block truncate max-w-sm">
            {r.purpose}
          </span>
        </div>
      ),
    },
    {
      header: "Nama Siswa",
      cell: (r) => r.student_name || "Siswa",
    },
    {
      header: "Pemohon",
      accessorKey: "applicant_name",
    },
    {
      header: "Tanggal Pengajuan",
      cell: (r) => (
        <span className="text-xs text-text-muted">
          {formatDate(r.created_at)}
        </span>
      ),
    },
    {
      header: "Aksi Disposisi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (r) => (
        <Button
          variant="primary"
          size="sm"
          onClick={() => navigate(`/requests/${r.id}`)}
        >
          <Eye className="h-4 w-4 mr-1.5" />
          Tinjau & Disposisi
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-surface p-5 rounded-card border border-border shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-text-foreground">
            Antrean Persetujuan Disposisi Pimpinan
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Daftar permohonan persuratan siswa yang telah diverifikasi oleh staf
            Tata Usaha dan menunggu tanda tangan / persetujuan resmi Kepala
            Sekolah.
          </p>
        </div>
        <span className="px-3 py-1 rounded-panel bg-semantic-warning-bg text-semantic-warning-fg border border-semantic-warning-border text-xs font-bold">
          {data?.items?.length || 0} Permohonan Menunggu
        </span>
      </div>

      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<ApprovalItem>
          columns={columns}
          data={data?.items || []}
          isLoading={isLoading}
          keyExtractor={(i) => i.id}
          onRowClick={(i) => navigate(`/requests/${i.id}`)}
          emptyTitle="Tidak Ada Antrean Disposisi"
          emptyDescription="Seluruh permohonan surat masuk telah ditinjau dan disetujui."
        />
      </div>
    </div>
  );
};
