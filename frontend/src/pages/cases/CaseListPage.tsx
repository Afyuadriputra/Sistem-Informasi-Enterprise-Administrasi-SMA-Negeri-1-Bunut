import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { AlertCircle, Plus, Eye } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { StatusBadge } from "@/components/atoms/StatusBadge";
import { SearchBar } from "@/components/molecules/SearchBar";
import { FormField } from "@/components/molecules/FormField";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import { PaginationControl } from "@/components/molecules/PaginationControl";
import { formatDate } from "@/lib/formatters";
import * as DialogPrimitive from "@radix-ui/react-dialog";

interface CaseItem {
  id: number;
  case_number: string;
  student_id: number;
  student_name?: string;
  student_number?: string;
  class_name?: string;
  category: string;
  status: "BARU" | "DIPROSES" | "SELESAI" | "DIBATALKAN";
  version: number;
  created_at: string;
  reported_by_name?: string;
}

interface CaseListResponse {
  items: CaseItem[];
  total: number;
  page: number;
  page_size: number;
}

const createCaseSchema = z.object({
  student_id: z.coerce.number().min(1, "Pilih siswa yang bersangkutan"),
  category: z.string().min(2, "Kategori kasus wajib diisi"),
  description: z.string().min(5, "Uraian pengaduan/kasus minimal 5 karakter"),
});

type CreateCaseFormData = z.infer<typeof createCaseSchema>;

export const CaseListPage: React.FC = () => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { hasAnyRole } = useAuthStore();
  const canCreate = hasAnyRole(["Kesiswaan", "Wali Kelas", "Guru"]);

  const [search, setSearch] = React.useState("");
  const [statusFilter, setStatusFilter] = React.useState("");
  const [page, setPage] = React.useState(1);
  const pageSize = 10;
  const [isCreateOpen, setIsCreateOpen] = React.useState(false);

  // Fetch Cases
  const { data, isLoading } = useQuery<CaseListResponse>({
    queryKey: ["student-cases", page, pageSize, search, statusFilter],
    queryFn: async () => {
      const params: Record<string, string | number> = {
        page,
        page_size: pageSize,
      };
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      const res = await apiClient.get<CaseListResponse>(
        "/student-affairs/cases",
        { params },
      );
      return res.data;
    },
  });

  // Create Case Mutation
  const createMutation = useMutation({
    mutationFn: async (payload: CreateCaseFormData) => {
      const res = await apiClient.post("/student-affairs/cases", payload);
      return res.data;
    },
    onSuccess: (newCase: { id: number }) => {
      queryClient.invalidateQueries({ queryKey: ["student-cases"] });
      toast.success("Laporan rujukan kasus berhasil dicatat");
      setIsCreateOpen(false);
      reset();
      navigate(`/cases/${newCase.id}`);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal membuat laporan kasus");
    },
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateCaseFormData>({
    resolver: zodResolver(createCaseSchema),
    defaultValues: {
      category: "KEDISIPLINAN",
      description: "",
    },
  });

  const columns: ColumnDef<CaseItem>[] = [
    {
      header: "No. Kasus",
      accessorKey: "case_number",
      className: "font-mono text-xs font-semibold",
    },
    {
      header: "Nama Siswa",
      cell: (item) => (
        <div>
          <span className="font-semibold text-text-foreground">
            {item.student_name || `Siswa #${item.student_id}`}
          </span>
          <span className="text-xs text-text-muted block">
            {item.class_name || "-"}
          </span>
        </div>
      ),
    },
    {
      header: "Kategori",
      accessorKey: "category",
      className: "text-xs font-medium",
    },
    {
      header: "Status",
      cell: (item) => <StatusBadge status={item.status} />,
    },
    {
      header: "Tanggal Lapor",
      cell: (item) => (
        <span className="text-xs text-text-muted">
          {formatDate(item.created_at)}
        </span>
      ),
    },
    {
      header: "Aksi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (item) => (
        <Button
          variant="secondary"
          size="sm"
          onClick={() => navigate(`/cases/${item.id}`)}
        >
          <Eye className="h-4 w-4 mr-1.5" />
          Detail Kasus
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Filter and Create Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-surface p-4 rounded-card border border-border shadow-sm">
        <div className="flex flex-1 flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <SearchBar
            value={search}
            onChange={(val) => {
              setSearch(val);
              setPage(1);
            }}
            placeholder="Cari nomor kasus atau nama siswa..."
          />
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
          >
            <option value="">Semua Status</option>
            <option value="BARU">Baru</option>
            <option value="DIPROSES">Diproses</option>
            <option value="SELESAI">Selesai</option>
            <option value="DIBATALKAN">Dibatalkan</option>
          </select>
        </div>

        {canCreate && (
          <Button
            variant="primary"
            onClick={() => {
              reset();
              setIsCreateOpen(true);
            }}
          >
            <Plus className="h-4 w-4 mr-2" />
            Rujuk Kasus Baru
          </Button>
        )}
      </div>

      {/* Cases Table */}
      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<CaseItem>
          columns={columns}
          data={data?.items || []}
          isLoading={isLoading}
          keyExtractor={(item) => item.id}
          onRowClick={(item) => navigate(`/cases/${item.id}`)}
          emptyTitle="Belum Ada Kasus Kesiswaan"
          emptyDescription="Tidak ditemukan rekam kasus kesiswaan pada filter yang dipilih."
        />

        <PaginationControl
          currentPage={page}
          pageSize={pageSize}
          totalItems={data?.total || 0}
          onPageChange={setPage}
        />
      </div>

      {/* Modal: Rujuk Kasus Baru */}
      <DialogPrimitive.Root open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-lg translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <div className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-brand-primary" />
                <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                  Laporan Rujukan Kasus Siswa
                </DialogPrimitive.Title>
              </div>
            </div>

            <form
              onSubmit={handleSubmit((d) => createMutation.mutate(d))}
              className="space-y-4 pt-4"
            >
              <FormField
                id="student_id"
                label="ID Siswa Terlapor"
                isRequired
                error={errors.student_id?.message}
              >
                <Input
                  id="student_id"
                  type="number"
                  placeholder="Masukkan ID siswa..."
                  {...register("student_id")}
                />
              </FormField>

              <FormField
                id="category"
                label="Kategori Kasus"
                isRequired
                error={errors.category?.message}
              >
                <select
                  id="category"
                  className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground"
                  {...register("category")}
                >
                  <option value="KEDISIPLINAN">
                    Kedisiplinan & Tata Tertib
                  </option>
                  <option value="KEHADIRAN">Presensi & Kerapihan</option>
                  <option value="AKADEMIK">Kendala Akademik Belajar</option>
                  <option value="KONSELING_BK">
                    Bimbingan Konseling Pribadi
                  </option>
                  <option value="MEDIASI">Mediasi Antar-Siswa</option>
                </select>
              </FormField>

              <FormField
                id="description"
                label="Uraian Rujukan Kasus"
                isRequired
                error={errors.description?.message}
              >
                <textarea
                  id="description"
                  rows={4}
                  className="w-full rounded-input border border-border-input bg-surface p-3 text-sm text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
                  placeholder="Jelaskan latar belakang kasus, tanggal kejadian, atau temuan observasi..."
                  {...register("description")}
                />
              </FormField>

              <div className="flex justify-end gap-2 pt-3 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsCreateOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createMutation.isPending}
                >
                  Simpan Rujukan
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    </div>
  );
};
