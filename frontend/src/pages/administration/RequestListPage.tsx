import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { useNavigate, Link } from "react-router-dom";
import { Plus, Eye } from "lucide-react";

import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";
import { StatusBadge } from "@/components/atoms/StatusBadge";
import { SearchBar } from "@/components/molecules/SearchBar";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import { PaginationControl } from "@/components/molecules/PaginationControl";
import { formatDate } from "@/lib/formatters";

interface ServiceRequestItem {
  id: number;
  request_number: string;
  service_type_name?: string;
  student_name?: string;
  student_number?: string;
  applicant_name: string;
  purpose: string;
  status: string;
  version: number;
  created_at: string;
}

interface RequestListResponse {
  items: ServiceRequestItem[];
  total: number;
  page: number;
  page_size: number;
}

export const RequestListPage: React.FC = () => {
  const navigate = useNavigate();
  const { hasRole } = useAuthStore();
  const isTU = hasRole("Tata Usaha");

  const [search, setSearch] = React.useState("");
  const [statusFilter, setStatusFilter] = React.useState("");
  const [page, setPage] = React.useState(1);
  const pageSize = 10;

  const { data, isLoading } = useQuery<RequestListResponse>({
    queryKey: ["service-requests", page, pageSize, search, statusFilter],
    queryFn: async () => {
      const params: Record<string, string | number> = {
        page,
        page_size: pageSize,
      };
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      const res = await apiClient.get<RequestListResponse>(
        "/administration/requests",
        { params },
      );
      return res.data;
    },
  });

  const columns: ColumnDef<ServiceRequestItem>[] = [
    {
      header: "No. Surat",
      accessorKey: "request_number",
      className: "font-mono text-xs font-semibold",
    },
    {
      header: "Jenis Layanan",
      cell: (r) => (
        <div>
          <span className="font-semibold text-text-foreground">
            {r.service_type_name || "Surat Keterangan"}
          </span>
          <span className="text-xs text-text-muted block truncate max-w-xs">
            {r.purpose}
          </span>
        </div>
      ),
    },
    {
      header: "Nama Siswa",
      cell: (r) => r.student_name || `Siswa #${r.student_name || "-"}`,
    },
    {
      header: "Pemohon",
      accessorKey: "applicant_name",
    },
    {
      header: "Status Alur",
      cell: (r) => <StatusBadge status={r.status} />,
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
      header: "Aksi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (r) => (
        <Button
          variant="secondary"
          size="sm"
          onClick={() => navigate(`/requests/${r.id}`)}
        >
          <Eye className="h-4 w-4 mr-1.5" />
          Lihat Detail
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Filter and Action Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-surface p-4 rounded-card border border-border shadow-sm">
        <div className="flex flex-1 flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <SearchBar
            value={search}
            onChange={(val) => {
              setSearch(val);
              setPage(1);
            }}
            placeholder="Cari nomor surat, siswa, atau pemohon..."
          />

          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground"
          >
            <option value="">Semua Status</option>
            <option value="DIAJUKAN">Diajukan</option>
            <option value="DIPROSES">Diproses</option>
            <option value="MENUNGGU_PERSETUJUAN">Menunggu Persetujuan</option>
            <option value="DISETUJUI">Disetujui</option>
            <option value="DITOLAK">Ditolak</option>
            <option value="SELESAI">Selesai</option>
          </select>
        </div>

        {isTU && (
          <Link to="/requests/new">
            <Button variant="primary">
              <Plus className="h-4 w-4 mr-2" />
              Buat Permohonan Baru
            </Button>
          </Link>
        )}
      </div>

      {/* Requests Table */}
      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<ServiceRequestItem>
          columns={columns}
          data={data?.items || []}
          isLoading={isLoading}
          keyExtractor={(item) => item.id}
          onRowClick={(item) => navigate(`/requests/${item.id}`)}
          emptyTitle="Belum Ada Permohonan Persuratan"
          emptyDescription="Tidak ditemukan berkas permohonan surat pada filter yang aktif."
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
