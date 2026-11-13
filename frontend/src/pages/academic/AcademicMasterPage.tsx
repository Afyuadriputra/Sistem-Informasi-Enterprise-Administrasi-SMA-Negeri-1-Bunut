import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import {
  Plus,
  Calendar,
  BookOpen,
  Briefcase,
  CheckCircle2,
} from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { StatusBadge } from "@/components/atoms/StatusBadge";
import { FormField } from "@/components/molecules/FormField";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import * as DialogPrimitive from "@radix-ui/react-dialog";

// Models
interface AcademicYearItem {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  is_active: boolean;
}

interface SchoolClassItem {
  id: number;
  academic_year_id: number;
  academic_year_name?: string;
  name: string;
  level: number;
}

interface EmployeeItem {
  id: number;
  user_id: number;
  nip: string;
  name: string;
  phone?: string | null;
  status: string;
  created_at?: string;
}

export const AcademicMasterPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = React.useState<
    "years" | "classes" | "employees"
  >("years");

  // Modals
  const [isYearModalOpen, setIsYearModalOpen] = React.useState(false);
  const [isClassModalOpen, setIsClassModalOpen] = React.useState(false);
  const [isEmployeeModalOpen, setIsEmployeeModalOpen] = React.useState(false);

  // Queries
  const { data: yearsData, isLoading: isYearsLoading } = useQuery<{
    items: AcademicYearItem[];
  }>({
    queryKey: ["academic-years"],
    queryFn: async () => (await apiClient.get("/master/academic-years")).data,
  });

  const { data: classesData, isLoading: isClassesLoading } = useQuery<{
    items: SchoolClassItem[];
  }>({
    queryKey: ["school-classes"],
    queryFn: async () => (await apiClient.get("/master/classes")).data,
  });

  const { data: employeesData, isLoading: isEmployeesLoading } = useQuery<{
    items: EmployeeItem[];
  }>({
    queryKey: ["school-employees"],
    queryFn: async () => (await apiClient.get("/master/employees")).data,
  });

  // Year Mutations
  const createYearMutation = useMutation({
    mutationFn: async (payload: {
      name: string;
      start_date: string;
      end_date: string;
      is_active: boolean;
    }) => (await apiClient.post("/master/academic-years", payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["academic-years"] });
      toast.success("Tahun ajaran berhasil dibuat");
      setIsYearModalOpen(false);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(
        errObj?.normalized?.message || "Gagal menyimpan tahun ajaran",
      );
    },
  });

  const toggleYearActiveMutation = useMutation({
    mutationFn: async ({ id, is_active }: { id: number; is_active: boolean }) =>
      (await apiClient.patch(`/master/academic-years/${id}`, { is_active }))
        .data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["academic-years"] });
      toast.success("Status aktif tahun ajaran diperbarui");
    },
  });

  // Class Mutation
  const createClassMutation = useMutation({
    mutationFn: async (payload: {
      academic_year_id: number;
      name: string;
      level: number;
    }) => (await apiClient.post("/master/classes", payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["school-classes"] });
      toast.success("Rombongan belajar kelas berhasil ditambahkan");
      setIsClassModalOpen(false);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal menambahkan kelas");
    },
  });

  // Employee Mutation
  const createEmployeeMutation = useMutation({
    mutationFn: async (payload: {
      user_id: number;
      nip: string;
      name: string;
      phone?: string;
      status: string;
    }) => (await apiClient.post("/master/employees", payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["school-employees"] });
      toast.success("Data pegawai sekolah berhasil ditambahkan");
      setIsEmployeeModalOpen(false);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal menambahkan pegawai");
    },
  });

  // Forms
  const {
    register: regYear,
    handleSubmit: submitYear,
    reset: resetYear,
  } = useForm<{
    name: string;
    start_date: string;
    end_date: string;
    is_active: boolean;
  }>({
    defaultValues: { name: "", start_date: "", end_date: "", is_active: false },
  });

  const {
    register: regClass,
    handleSubmit: submitClass,
    reset: resetClass,
  } = useForm<{
    academic_year_id: number;
    name: string;
    level: number;
  }>();

  const {
    register: regEmp,
    handleSubmit: submitEmp,
    reset: resetEmp,
  } = useForm<{
    user_id: number;
    nip: string;
    name: string;
    phone: string;
    status: string;
  }>({
    defaultValues: { status: "AKTIF" },
  });

  // Columns for Years
  const yearColumns: ColumnDef<AcademicYearItem>[] = [
    { header: "Tahun Ajaran", accessorKey: "name", className: "font-semibold" },
    { header: "Tanggal Mulai", accessorKey: "start_date" },
    { header: "Tanggal Berakhir", accessorKey: "end_date" },
    {
      header: "Status Aktif",
      cell: (item) =>
        item.is_active ? (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-sm bg-semantic-success-bg text-semantic-success-fg text-xs font-semibold">
            <CheckCircle2 className="h-3.5 w-3.5" /> Aktif
          </span>
        ) : (
          <span className="text-xs text-text-muted">Tidak Aktif</span>
        ),
    },
    {
      header: "Aksi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (item) =>
        !item.is_active && (
          <Button
            variant="secondary"
            size="sm"
            onClick={() =>
              toggleYearActiveMutation.mutate({ id: item.id, is_active: true })
            }
            isLoading={toggleYearActiveMutation.isPending}
          >
            Jadikan Aktif
          </Button>
        ),
    },
  ];

  // Columns for Classes
  const classColumns: ColumnDef<SchoolClassItem>[] = [
    { header: "Nama Rombel", accessorKey: "name", className: "font-semibold" },
    { header: "Tingkat", cell: (item) => `Tingkat ${item.level}` },
    { header: "Tahun Ajaran", cell: (item) => item.academic_year_name || "-" },
  ];

  // Columns for Employees
  const employeeColumns: ColumnDef<EmployeeItem>[] = [
    { header: "NIP", accessorKey: "nip", className: "font-mono text-xs" },
    { header: "Nama Pegawai", accessorKey: "name", className: "font-semibold" },
    { header: "Telepon / Kontak", cell: (item) => item.phone || "-" },
    { header: "Status", cell: (item) => <StatusBadge status={item.status} /> },
  ];

  return (
    <div className="space-y-6">
      {/* Tab Switcher */}
      <div className="flex border-b border-border bg-surface rounded-t-card px-4 pt-3 gap-2">
        <button
          type="button"
          onClick={() => setActiveTab("years")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === "years"
              ? "border-brand-primary text-brand-primary"
              : "border-transparent text-text-muted hover:text-text-foreground"
          }`}
        >
          <Calendar className="h-4 w-4" />
          <span>Tahun Ajaran</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("classes")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === "classes"
              ? "border-brand-primary text-brand-primary"
              : "border-transparent text-text-muted hover:text-text-foreground"
          }`}
        >
          <BookOpen className="h-4 w-4" />
          <span>Rombongan Belajar (Kelas)</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("employees")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === "employees"
              ? "border-brand-primary text-brand-primary"
              : "border-transparent text-text-muted hover:text-text-foreground"
          }`}
        >
          <Briefcase className="h-4 w-4" />
          <span>Data Pegawai Sekolah</span>
        </button>
      </div>

      {/* Tab 1: Tahun Ajaran */}
      {activeTab === "years" && (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-surface p-4 rounded-card border border-border shadow-sm">
            <div>
              <h3 className="font-semibold text-text-foreground">
                Siklus Tahun Ajaran
              </h3>
              <p className="text-xs text-text-muted">
                Hanya boleh ada 1 tahun ajaran yang aktif dalam satu waktu.
              </p>
            </div>
            <Button
              variant="primary"
              onClick={() => {
                resetYear();
                setIsYearModalOpen(true);
              }}
            >
              <Plus className="h-4 w-4 mr-1.5" /> Tambah Tahun Ajaran
            </Button>
          </div>

          <DataTable<AcademicYearItem>
            columns={yearColumns}
            data={yearsData?.items || []}
            isLoading={isYearsLoading}
            keyExtractor={(i) => i.id}
          />
        </div>
      )}

      {/* Tab 2: Kelas Rombel */}
      {activeTab === "classes" && (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-surface p-4 rounded-card border border-border shadow-sm">
            <div>
              <h3 className="font-semibold text-text-foreground">
                Daftar Rombongan Belajar
              </h3>
              <p className="text-xs text-text-muted">
                Kelas terdaftar untuk alokasi siswa dan guru pengampu.
              </p>
            </div>
            <Button
              variant="primary"
              onClick={() => {
                resetClass();
                setIsClassModalOpen(true);
              }}
            >
              <Plus className="h-4 w-4 mr-1.5" /> Tambah Rombel
            </Button>
          </div>

          <DataTable<SchoolClassItem>
            columns={classColumns}
            data={classesData?.items || []}
            isLoading={isClassesLoading}
            keyExtractor={(i) => i.id}
          />
        </div>
      )}

      {/* Tab 3: Pegawai Sekolah */}
      {activeTab === "employees" && (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-surface p-4 rounded-card border border-border shadow-sm">
            <div>
              <h3 className="font-semibold text-text-foreground">
                Data Tenaga Pendidik & Kependidikan
              </h3>
              <p className="text-xs text-text-muted">
                Profil NIP dan kontak resmi pegawai SMAN 1 Bunut.
              </p>
            </div>
            <Button
              variant="primary"
              onClick={() => {
                resetEmp();
                setIsEmployeeModalOpen(true);
              }}
            >
              <Plus className="h-4 w-4 mr-1.5" /> Tambah Pegawai
            </Button>
          </div>

          <DataTable<EmployeeItem>
            columns={employeeColumns}
            data={employeesData?.items || []}
            isLoading={isEmployeesLoading}
            keyExtractor={(i) => i.id}
          />
        </div>
      )}

      {/* Modal: Tambah Tahun Ajaran */}
      <DialogPrimitive.Root
        open={isYearModalOpen}
        onOpenChange={setIsYearModalOpen}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground pb-2 border-b border-border">
              Tambah Tahun Ajaran Baru
            </DialogPrimitive.Title>

            <form
              onSubmit={submitYear((d) => createYearMutation.mutate(d))}
              className="space-y-4 pt-4"
            >
              <FormField id="ay_name" label="Nama Tahun Ajaran" isRequired>
                <Input
                  id="ay_name"
                  placeholder="Contoh: 2026/2027 Ganjil"
                  {...regYear("name", { required: true })}
                />
              </FormField>

              <div className="grid grid-cols-2 gap-3">
                <FormField id="ay_start" label="Tanggal Mulai" isRequired>
                  <Input
                    id="ay_start"
                    type="date"
                    {...regYear("start_date", { required: true })}
                  />
                </FormField>
                <FormField id="ay_end" label="Tanggal Selesai" isRequired>
                  <Input
                    id="ay_end"
                    type="date"
                    {...regYear("end_date", { required: true })}
                  />
                </FormField>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsYearModalOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createYearMutation.isPending}
                >
                  Simpan
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      {/* Modal: Tambah Kelas */}
      <DialogPrimitive.Root
        open={isClassModalOpen}
        onOpenChange={setIsClassModalOpen}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground pb-2 border-b border-border">
              Tambah Rombel Kelas Baru
            </DialogPrimitive.Title>

            <form
              onSubmit={submitClass((d) =>
                createClassMutation.mutate({
                  name: d.name,
                  level: Number(d.level),
                  academic_year_id: Number(d.academic_year_id),
                }),
              )}
              className="space-y-4 pt-4"
            >
              <FormField id="cl_year" label="Tahun Ajaran" isRequired>
                <select
                  id="cl_year"
                  className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm"
                  {...regClass("academic_year_id", { required: true })}
                >
                  <option value="">Pilih Tahun Ajaran</option>
                  {yearsData?.items.map((y) => (
                    <option key={y.id} value={y.id}>
                      {y.name} {y.is_active ? "(Aktif)" : ""}
                    </option>
                  ))}
                </select>
              </FormField>

              <FormField id="cl_name" label="Nama Rombel" isRequired>
                <Input
                  id="cl_name"
                  placeholder="Contoh: X MIPA 1"
                  {...regClass("name", { required: true })}
                />
              </FormField>

              <FormField id="cl_level" label="Tingkat Kelas" isRequired>
                <select
                  id="cl_level"
                  className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm"
                  {...regClass("level", { required: true })}
                >
                  <option value={10}>Kelas 10 (Fase E)</option>
                  <option value={11}>Kelas 11 (Fase F)</option>
                  <option value={12}>Kelas 12 (Fase F)</option>
                </select>
              </FormField>

              <div className="flex justify-end gap-2 pt-3 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsClassModalOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createClassMutation.isPending}
                >
                  Simpan Rombel
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      {/* Modal: Tambah Pegawai */}
      <DialogPrimitive.Root
        open={isEmployeeModalOpen}
        onOpenChange={setIsEmployeeModalOpen}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground pb-2 border-b border-border">
              Tambah Pegawai Baru
            </DialogPrimitive.Title>

            <form
              onSubmit={submitEmp((d) =>
                createEmployeeMutation.mutate({
                  user_id: Number(d.user_id),
                  nip: d.nip,
                  name: d.name,
                  phone: d.phone,
                  status: d.status,
                }),
              )}
              className="space-y-4 pt-4"
            >
              <FormField
                id="emp_user"
                label="ID Akun Pengguna (User ID)"
                isRequired
              >
                <Input
                  id="emp_user"
                  type="number"
                  placeholder="Contoh: 12"
                  {...regEmp("user_id", { required: true })}
                />
              </FormField>

              <FormField id="emp_nip" label="NIP / Nomor Pegawai" isRequired>
                <Input
                  id="emp_nip"
                  placeholder="Contoh: 198501012010011005"
                  {...regEmp("nip", { required: true })}
                />
              </FormField>

              <FormField id="emp_name" label="Nama Lengkap Pegawai" isRequired>
                <Input
                  id="emp_name"
                  placeholder="Contoh: Dr. H. Ahmad Dahlan, M.Pd."
                  {...regEmp("name", { required: true })}
                />
              </FormField>

              <FormField id="emp_phone" label="Nomor Telepon / WhatsApp">
                <Input
                  id="emp_phone"
                  placeholder="Contoh: 081234567890"
                  {...regEmp("phone")}
                />
              </FormField>

              <div className="flex justify-end gap-2 pt-3 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsEmployeeModalOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createEmployeeMutation.isPending}
                >
                  Simpan Pegawai
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    </div>
  );
};
