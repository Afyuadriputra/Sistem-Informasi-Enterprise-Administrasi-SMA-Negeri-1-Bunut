import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { UserPlus, Eye, Edit, X, GraduationCap } from "lucide-react";
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
import * as DialogPrimitive from "@radix-ui/react-dialog";

interface StudentItem {
  id: number;
  student_number: string;
  name: string;
  gender: string;
  status: string;
  current_class_name?: string | null;
}

interface StudentDetailResponse extends StudentItem {
  enrollments?: Array<{
    id: number;
    class_id: number;
    class_name: string;
    academic_year_name: string;
    start_date: string;
    end_date?: string | null;
  }>;
}

interface StudentListResponse {
  items: StudentItem[];
  total: number;
  page: number;
  page_size: number;
}

const studentSchema = z.object({
  student_number: z.string().min(3, "Nomor induk siswa wajib diisi"),
  name: z.string().min(2, "Nama siswa wajib diisi"),
  gender: z.enum(["L", "P"]),
  status: z.enum(["AKTIF", "MUTASI_KELUAR", "LULUS", "NONAKTIF"]),
});

type StudentFormData = z.infer<typeof studentSchema>;

export const StudentListPage: React.FC = () => {
  const queryClient = useQueryClient();
  const { hasRole } = useAuthStore();
  const isAdmin = hasRole("Administrator");

  const [search, setSearch] = React.useState("");
  const [statusFilter, setStatusFilter] = React.useState("");
  const [page, setPage] = React.useState(1);
  const pageSize = 10;

  const [selectedStudentId, setSelectedStudentId] = React.useState<
    number | null
  >(null);
  const [isDetailOpen, setIsDetailOpen] = React.useState(false);
  const [isCreateOpen, setIsCreateOpen] = React.useState(false);
  const [editingStudent, setEditingStudent] =
    React.useState<StudentItem | null>(null);

  // Fetch students
  const { data, isLoading } = useQuery<StudentListResponse>({
    queryKey: ["master-students", page, pageSize, search, statusFilter],
    queryFn: async () => {
      const params: Record<string, string | number> = {
        page,
        page_size: pageSize,
      };
      if (search) params.search = search;
      if (statusFilter) params.status = statusFilter;
      const res = await apiClient.get<StudentListResponse>("/master/students", {
        params,
      });
      return res.data;
    },
  });

  // Fetch student detail
  const { data: studentDetail, isLoading: isDetailLoading } =
    useQuery<StudentDetailResponse>({
      queryKey: ["master-student-detail", selectedStudentId],
      queryFn: async () => {
        const res = await apiClient.get<StudentDetailResponse>(
          `/master/students/${selectedStudentId}`,
        );
        return res.data;
      },
      enabled: selectedStudentId !== null && isDetailOpen,
    });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: async (payload: StudentFormData) => {
      const res = await apiClient.post("/master/students", payload);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["master-students"] });
      toast.success("Data siswa berhasil ditambahkan");
      setIsCreateOpen(false);
      reset();
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(
        errObj?.normalized?.message || "Gagal menambahkan data siswa",
      );
    },
  });

  // Edit mutation
  const editMutation = useMutation({
    mutationFn: async ({
      id,
      payload,
    }: {
      id: number;
      payload: Partial<StudentFormData>;
    }) => {
      const res = await apiClient.patch(`/master/students/${id}`, payload);
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["master-students"] });
      toast.success("Data siswa berhasil diperbarui");
      setEditingStudent(null);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(
        errObj?.normalized?.message || "Gagal memperbarui data siswa",
      );
    },
  });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<StudentFormData>({
    resolver: zodResolver(studentSchema),
    defaultValues: {
      student_number: "",
      name: "",
      gender: "L",
      status: "AKTIF",
    },
  });

  const {
    register: registerEdit,
    handleSubmit: handleSubmitEdit,
    reset: resetEdit,
    formState: { errors: errorsEdit },
  } = useForm<Partial<StudentFormData>>({
    defaultValues: {
      name: "",
      gender: "L",
      status: "AKTIF",
    },
  });

  const openEditModal = (student: StudentItem) => {
    setEditingStudent(student);
    resetEdit({
      name: student.name,
      gender: student.gender as "L" | "P",
      status: student.status as
        "AKTIF" | "MUTASI_KELUAR" | "LULUS" | "NONAKTIF",
    });
  };

  const columns: ColumnDef<StudentItem>[] = [
    {
      header: "NIS / NISN",
      accessorKey: "student_number",
      className: "font-mono text-xs font-semibold",
    },
    {
      header: "Nama Siswa",
      cell: (student) => (
        <span className="font-semibold text-text-foreground">
          {student.name}
        </span>
      ),
    },
    {
      header: "Jenis Kelamin",
      cell: (student) => (student.gender === "L" ? "Laki-laki" : "Perempuan"),
    },
    {
      header: "Kelas Aktif",
      cell: (student) => student.current_class_name || "-",
    },
    {
      header: "Status",
      cell: (student) => <StatusBadge status={student.status} />,
    },
    {
      header: "Aksi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (student) => (
        <div className="flex items-center justify-end gap-1.5">
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              setSelectedStudentId(student.id);
              setIsDetailOpen(true);
            }}
            aria-label={`Lihat detail ${student.name}`}
          >
            <Eye className="h-4 w-4" aria-hidden="true" />
          </Button>

          {isAdmin && (
            <Button
              variant="secondary"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                openEditModal(student);
              }}
              aria-label={`Ubah data ${student.name}`}
            >
              <Edit className="h-3.5 w-3.5 mr-1" aria-hidden="true" />
              Ubah
            </Button>
          )}
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Search and Action Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-surface p-4 rounded-card border border-border shadow-sm">
        <div className="flex flex-1 flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <SearchBar
            value={search}
            onChange={(val) => {
              setSearch(val);
              setPage(1);
            }}
            placeholder="Cari nama atau NIS siswa..."
          />
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
            aria-label="Filter status siswa"
          >
            <option value="">Semua Status</option>
            <option value="AKTIF">Aktif</option>
            <option value="MUTASI_KELUAR">Mutasi Keluar</option>
            <option value="LULUS">Lulus</option>
            <option value="NONAKTIF">Nonaktif</option>
          </select>
        </div>

        {isAdmin && (
          <Button
            variant="primary"
            onClick={() => {
              reset();
              setIsCreateOpen(true);
            }}
          >
            <UserPlus className="h-4 w-4 mr-2" aria-hidden="true" />
            Tambah Siswa
          </Button>
        )}
      </div>

      {/* Student Data Table */}
      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<StudentItem>
          columns={columns}
          data={data?.items || []}
          isLoading={isLoading}
          keyExtractor={(item) => item.id}
          emptyTitle="Belum Ada Data Siswa"
          emptyDescription="Data siswa tidak ditemukan untuk kata kunci atau status yang dipilih."
        />

        <PaginationControl
          currentPage={page}
          pageSize={pageSize}
          totalItems={data?.total || 0}
          onPageChange={setPage}
        />
      </div>

      {/* Student Detail Modal */}
      <DialogPrimitive.Root open={isDetailOpen} onOpenChange={setIsDetailOpen}>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-lg translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <div className="flex items-center gap-2">
                <GraduationCap
                  className="h-5 w-5 text-brand-primary"
                  aria-hidden="true"
                />
                <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                  Detail Induk Siswa
                </DialogPrimitive.Title>
              </div>
              <DialogPrimitive.Close asChild>
                <button
                  type="button"
                  className="p-1 rounded-sm text-text-muted hover:text-text-foreground"
                  aria-label="Tutup"
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                </button>
              </DialogPrimitive.Close>
            </div>

            {isDetailLoading ? (
              <div className="py-8 text-center text-sm text-text-muted">
                Memuat detail siswa...
              </div>
            ) : studentDetail ? (
              <div className="space-y-4 pt-4">
                <div className="grid grid-cols-2 gap-4 text-sm bg-surface-subtle p-3.5 rounded-input border border-border">
                  <div>
                    <span className="text-xs text-text-muted block">
                      NIS / NISN
                    </span>
                    <span className="font-mono font-semibold">
                      {studentDetail.student_number}
                    </span>
                  </div>
                  <div>
                    <span className="text-xs text-text-muted block">
                      Nama Siswa
                    </span>
                    <span className="font-semibold">{studentDetail.name}</span>
                  </div>
                  <div>
                    <span className="text-xs text-text-muted block">
                      Jenis Kelamin
                    </span>
                    <span>
                      {studentDetail.gender === "L" ? "Laki-laki" : "Perempuan"}
                    </span>
                  </div>
                  <div>
                    <span className="text-xs text-text-muted block">
                      Status Siswa
                    </span>
                    <StatusBadge status={studentDetail.status} />
                  </div>
                </div>

                <div>
                  <h4 className="text-xs font-semibold uppercase text-text-muted mb-2">
                    Riwayat Penempatan Kelas (Enrollments):
                  </h4>
                  {studentDetail.enrollments &&
                  studentDetail.enrollments.length > 0 ? (
                    <div className="divide-y divide-border border border-border rounded-input overflow-hidden text-xs">
                      {studentDetail.enrollments.map((en) => (
                        <div
                          key={en.id}
                          className="p-2.5 flex items-center justify-between"
                        >
                          <span className="font-semibold text-text-foreground">
                            {en.class_name} ({en.academic_year_name})
                          </span>
                          <span className="text-text-muted">
                            {en.start_date}{" "}
                            {en.end_date ? `s/d ${en.end_date}` : "(Aktif)"}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-text-muted italic">
                      Belum ada riwayat penempatan kelas.
                    </p>
                  )}
                </div>

                <div className="flex justify-end pt-3 border-t border-border">
                  <Button
                    variant="secondary"
                    onClick={() => setIsDetailOpen(false)}
                  >
                    Tutup
                  </Button>
                </div>
              </div>
            ) : null}
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      {/* Create Student Modal */}
      <DialogPrimitive.Root open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-lg translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                Tambah Siswa Baru
              </DialogPrimitive.Title>
              <DialogPrimitive.Close asChild>
                <button
                  type="button"
                  className="p-1 rounded-sm text-text-muted hover:text-text-foreground"
                  aria-label="Tutup"
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                </button>
              </DialogPrimitive.Close>
            </div>

            <form
              onSubmit={handleSubmit((d) => createMutation.mutate(d))}
              className="space-y-4 pt-4"
            >
              <FormField
                id="student_number"
                label="Nomor Induk Siswa (NIS/NISN)"
                isRequired
                error={errors.student_number?.message}
              >
                <Input
                  id="student_number"
                  placeholder="Contoh: 10091"
                  {...register("student_number")}
                />
              </FormField>

              <FormField
                id="name"
                label="Nama Lengkap Siswa"
                isRequired
                error={errors.name?.message}
              >
                <Input
                  id="name"
                  placeholder="Contoh: Muhammad Raditya"
                  {...register("name")}
                />
              </FormField>

              <div className="grid grid-cols-2 gap-4">
                <FormField id="gender" label="Jenis Kelamin" isRequired>
                  <select
                    id="gender"
                    className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground"
                    {...register("gender")}
                  >
                    <option value="L">Laki-laki</option>
                    <option value="P">Perempuan</option>
                  </select>
                </FormField>

                <FormField id="status" label="Status Siswa" isRequired>
                  <select
                    id="status"
                    className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground"
                    {...register("status")}
                  >
                    <option value="AKTIF">Aktif</option>
                    <option value="MUTASI_KELUAR">Mutasi Keluar</option>
                    <option value="LULUS">Lulus</option>
                    <option value="NONAKTIF">Nonaktif</option>
                  </select>
                </FormField>
              </div>

              <div className="flex justify-end gap-2 pt-4 border-t border-border">
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
                  Simpan Siswa
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      {/* Edit Student Modal */}
      <DialogPrimitive.Root
        open={editingStudent !== null}
        onOpenChange={(open) => !open && setEditingStudent(null)}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-lg translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                Ubah Data Siswa ({editingStudent?.student_number})
              </DialogPrimitive.Title>
              <DialogPrimitive.Close asChild>
                <button
                  type="button"
                  className="p-1 rounded-sm text-text-muted hover:text-text-foreground"
                  aria-label="Tutup"
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                </button>
              </DialogPrimitive.Close>
            </div>

            <form
              onSubmit={handleSubmitEdit((d) => {
                if (editingStudent) {
                  editMutation.mutate({ id: editingStudent.id, payload: d });
                }
              })}
              className="space-y-4 pt-4"
            >
              <FormField
                id="edit_name"
                label="Nama Lengkap Siswa"
                isRequired
                error={errorsEdit.name?.message}
              >
                <Input id="edit_name" {...registerEdit("name")} />
              </FormField>

              <div className="grid grid-cols-2 gap-4">
                <FormField id="edit_gender" label="Jenis Kelamin" isRequired>
                  <select
                    id="edit_gender"
                    className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground"
                    {...registerEdit("gender")}
                  >
                    <option value="L">Laki-laki</option>
                    <option value="P">Perempuan</option>
                  </select>
                </FormField>

                <FormField id="edit_status" label="Status Siswa" isRequired>
                  <select
                    id="edit_status"
                    className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground"
                    {...registerEdit("status")}
                  >
                    <option value="AKTIF">Aktif</option>
                    <option value="MUTASI_KELUAR">Mutasi Keluar</option>
                    <option value="LULUS">Lulus</option>
                    <option value="NONAKTIF">Nonaktif</option>
                  </select>
                </FormField>
              </div>

              <div className="flex justify-end gap-2 pt-4 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setEditingStudent(null)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={editMutation.isPending}
                >
                  Simpan Perubahan
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    </div>
  );
};
