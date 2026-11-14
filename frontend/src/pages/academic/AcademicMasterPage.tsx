import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import {
  Plus,
  Calendar,
  BookOpen,
  Briefcase,
  CheckCircle2,
  FileText,
  Edit,
  X,
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

interface ServiceTypeItem {
  id: number;
  code: string;
  name: string;
  description?: string | null;
  requires_approval: boolean;
  is_active: boolean;
}

export const AcademicMasterPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = React.useState<
    "years" | "classes" | "employees" | "services"
  >("years");

  // Modals
  const [isYearModalOpen, setIsYearModalOpen] = React.useState(false);
  const [isClassModalOpen, setIsClassModalOpen] = React.useState(false);
  const [isEmployeeModalOpen, setIsEmployeeModalOpen] = React.useState(false);
  const [isServiceTypeModalOpen, setIsServiceTypeModalOpen] =
    React.useState(false);
  const [editingServiceType, setEditingServiceType] =
    React.useState<ServiceTypeItem | null>(null);

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

  const { data: servicesData, isLoading: isServicesLoading } = useQuery<{
    items: ServiceTypeItem[];
  }>({
    queryKey: ["service-types-master"],
    queryFn: async () =>
      (await apiClient.get("/administration/service-types")).data,
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

  // Service Type Mutations (createServiceType & updateServiceType)
  const createServiceTypeMutation = useMutation({
    mutationFn: async (payload: {
      code: string;
      name: string;
      description?: string;
      requires_approval: boolean;
    }) => (await apiClient.post("/administration/service-types", payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["service-types-master"] });
      queryClient.invalidateQueries({ queryKey: ["service-types"] });
      toast.success("Jenis layanan persuratan berhasil ditambahkan");
      setIsServiceTypeModalOpen(false);
      resetServiceType();
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal membuat jenis layanan");
    },
  });

  const updateServiceTypeMutation = useMutation({
    mutationFn: async ({
      id,
      payload,
    }: {
      id: number;
      payload: {
        name?: string;
        description?: string;
        requires_approval?: boolean;
        is_active?: boolean;
      };
    }) =>
      (await apiClient.patch(`/administration/service-types/${id}`, payload))
        .data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["service-types-master"] });
      queryClient.invalidateQueries({ queryKey: ["service-types"] });
      toast.success("Jenis layanan persuratan berhasil diperbarui");
      setEditingServiceType(null);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(
        errObj?.normalized?.message || "Gagal memperbarui jenis layanan",
      );
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

  const {
    register: regServiceType,
    handleSubmit: submitServiceType,
    reset: resetServiceType,
  } = useForm<{
    code: string;
    name: string;
    description: string;
    requires_approval: boolean;
  }>({
    defaultValues: {
      code: "",
      name: "",
      description: "",
      requires_approval: true,
    },
  });

  const {
    register: regEditServiceType,
    handleSubmit: submitEditServiceType,
    reset: resetEditServiceType,
  } = useForm<{
    name: string;
    description: string;
    requires_approval: boolean;
    is_active: boolean;
  }>();

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

  // Columns for Service Types
  const serviceTypeColumns: ColumnDef<ServiceTypeItem>[] = [
    {
      header: "Kode Layanan",
      accessorKey: "code",
      className: "font-mono text-xs font-semibold",
    },
    {
      header: "Nama Layanan Surat",
      cell: (item) => (
        <div>
          <span className="font-semibold text-text-foreground">
            {item.name}
          </span>
          {item.description && (
            <p className="text-xs text-text-muted mt-0.5">{item.description}</p>
          )}
        </div>
      ),
    },
    {
      header: "Persetujuan Kepsek",
      cell: (item) => (
        <span
          className={`px-2 py-0.5 rounded-sm text-xs font-semibold ${
            item.requires_approval
              ? "bg-brand-primary-subtle text-brand-primary"
              : "bg-surface-subtle text-text-muted"
          }`}
        >
          {item.requires_approval ? "Perlu Persetujuan" : "Tanpa Persetujuan"}
        </span>
      ),
    },
    {
      header: "Status",
      cell: (item) => (
        <StatusBadge status={item.is_active ? "AKTIF" : "NONAKTIF"} />
      ),
    },
    {
      header: "Aksi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (item) => (
        <div className="flex items-center justify-end gap-1.5">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              setEditingServiceType(item);
              resetEditServiceType({
                name: item.name,
                description: item.description || "",
                requires_approval: item.requires_approval,
                is_active: item.is_active,
              });
            }}
          >
            <Edit className="h-3.5 w-3.5 mr-1" />
            Ubah
          </Button>
          <Button
            variant={item.is_active ? "danger" : "accent"}
            size="sm"
            onClick={() =>
              updateServiceTypeMutation.mutate({
                id: item.id,
                payload: { is_active: !item.is_active },
              })
            }
            isLoading={updateServiceTypeMutation.isPending}
          >
            {item.is_active ? "Nonaktifkan" : "Aktifkan"}
          </Button>
        </div>
      ),
    },
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

        <button
          type="button"
          onClick={() => setActiveTab("services")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === "services"
              ? "border-brand-primary text-brand-primary"
              : "border-transparent text-text-muted hover:text-text-foreground"
          }`}
        >
          <FileText className="h-4 w-4" />
          <span>Layanan Persuratan TU</span>
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

      {/* Tab 4: Layanan Persuratan TU (listServiceTypes, createServiceType, updateServiceType) */}
      {activeTab === "services" && (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-surface p-4 rounded-card border border-border shadow-sm">
            <div>
              <h3 className="font-semibold text-text-foreground">
                Katalog Jenis Layanan Persuratan Tata Usaha
              </h3>
              <p className="text-xs text-text-muted">
                Jenis surat dinas dan disposisi persetujuan Kepala Sekolah.
              </p>
            </div>
            <Button
              variant="primary"
              onClick={() => {
                resetServiceType();
                setIsServiceTypeModalOpen(true);
              }}
            >
              <Plus className="h-4 w-4 mr-1.5" /> Tambah Jenis Layanan
            </Button>
          </div>

          <DataTable<ServiceTypeItem>
            columns={serviceTypeColumns}
            data={servicesData?.items || []}
            isLoading={isServicesLoading}
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

      {/* Modal: Tambah Jenis Layanan (createServiceType) */}
      <DialogPrimitive.Root
        open={isServiceTypeModalOpen}
        onOpenChange={setIsServiceTypeModalOpen}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-2 border-b border-border">
              <div className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-brand-primary" />
                <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                  Tambah Jenis Layanan Persuratan
                </DialogPrimitive.Title>
              </div>
              <DialogPrimitive.Close asChild>
                <button
                  type="button"
                  className="p-1 rounded-sm text-text-muted hover:text-text-foreground"
                  aria-label="Tutup"
                >
                  <X className="h-4 w-4" />
                </button>
              </DialogPrimitive.Close>
            </div>

            <form
              onSubmit={submitServiceType((d) =>
                createServiceTypeMutation.mutate(d),
              )}
              className="space-y-4 pt-4"
            >
              <FormField id="st_code" label="Kode Layanan" isRequired>
                <Input
                  id="st_code"
                  placeholder="Contoh: SK-AKTIF"
                  {...regServiceType("code", { required: true })}
                />
              </FormField>

              <FormField id="st_name" label="Nama Layanan Surat" isRequired>
                <Input
                  id="st_name"
                  placeholder="Contoh: Surat Keterangan Siswa Aktif"
                  {...regServiceType("name", { required: true })}
                />
              </FormField>

              <FormField id="st_desc" label="Deskripsi / Catatan Persyaratan">
                <Input
                  id="st_desc"
                  placeholder="Contoh: Diperlukan untuk permohonan beasiswa atau tunjangan dinas"
                  {...regServiceType("description")}
                />
              </FormField>

              <div className="flex items-center gap-2 pt-2">
                <input
                  id="st_approval"
                  type="checkbox"
                  className="h-4 w-4 rounded border-border-input text-brand-primary focus:ring-brand-primary"
                  {...regServiceType("requires_approval")}
                />
                <label
                  htmlFor="st_approval"
                  className="text-sm font-medium text-text-foreground"
                >
                  Wajib Persetujuan Kepala Sekolah (Disposisi)
                </label>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsServiceTypeModalOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createServiceTypeMutation.isPending}
                >
                  Simpan Jenis Layanan
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      {/* Modal: Ubah Jenis Layanan (updateServiceType) */}
      <DialogPrimitive.Root
        open={editingServiceType !== null}
        onOpenChange={(open) => !open && setEditingServiceType(null)}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <div className="flex items-center justify-between pb-2 border-b border-border">
              <div className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-brand-primary" />
                <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground">
                  Ubah Jenis Layanan ({editingServiceType?.code})
                </DialogPrimitive.Title>
              </div>
              <DialogPrimitive.Close asChild>
                <button
                  type="button"
                  className="p-1 rounded-sm text-text-muted hover:text-text-foreground"
                  aria-label="Tutup"
                >
                  <X className="h-4 w-4" />
                </button>
              </DialogPrimitive.Close>
            </div>

            {editingServiceType && (
              <form
                onSubmit={submitEditServiceType((d) =>
                  updateServiceTypeMutation.mutate({
                    id: editingServiceType.id,
                    payload: d,
                  }),
                )}
                className="space-y-4 pt-4"
              >
                <FormField
                  id="edit_st_name"
                  label="Nama Layanan Surat"
                  isRequired
                >
                  <Input
                    id="edit_st_name"
                    {...regEditServiceType("name", { required: true })}
                  />
                </FormField>

                <FormField
                  id="edit_st_desc"
                  label="Deskripsi / Catatan Persyaratan"
                >
                  <Input
                    id="edit_st_desc"
                    {...regEditServiceType("description")}
                  />
                </FormField>

                <div className="flex items-center gap-2 pt-2">
                  <input
                    id="edit_st_approval"
                    type="checkbox"
                    className="h-4 w-4 rounded border-border-input text-brand-primary focus:ring-brand-primary"
                    {...regEditServiceType("requires_approval")}
                  />
                  <label
                    htmlFor="edit_st_approval"
                    className="text-sm font-medium text-text-foreground"
                  >
                    Wajib Persetujuan Kepala Sekolah (Disposisi)
                  </label>
                </div>

                <div className="flex items-center gap-2">
                  <input
                    id="edit_st_active"
                    type="checkbox"
                    className="h-4 w-4 rounded border-border-input text-brand-primary focus:ring-brand-primary"
                    {...regEditServiceType("is_active")}
                  />
                  <label
                    htmlFor="edit_st_active"
                    className="text-sm font-medium text-text-foreground"
                  >
                    Status Layanan Aktif
                  </label>
                </div>

                <div className="flex justify-end gap-2 pt-3 border-t border-border">
                  <Button
                    type="button"
                    variant="secondary"
                    onClick={() => setEditingServiceType(null)}
                  >
                    Batal
                  </Button>
                  <Button
                    type="submit"
                    variant="primary"
                    isLoading={updateServiceTypeMutation.isPending}
                  >
                    Simpan Perubahan
                  </Button>
                </div>
              </form>
            )}
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    </div>
  );
};
