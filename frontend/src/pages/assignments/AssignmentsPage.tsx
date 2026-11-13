import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { Plus, UserCheck, GraduationCap } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { FormField } from "@/components/molecules/FormField";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import * as DialogPrimitive from "@radix-ui/react-dialog";

interface EnrollmentItem {
  id: number;
  student_id: number;
  student_name?: string;
  student_number?: string;
  class_id: number;
  class_name?: string;
  start_date: string;
  end_date?: string | null;
}

interface AssignmentItem {
  id: number;
  employee_id: number;
  employee_name?: string;
  class_id: number;
  class_name?: string;
  role: "GURU_MAPEL" | "WALI_KELAS";
  start_date: string;
  end_date?: string | null;
}

export const AssignmentsPage: React.FC = () => {
  const queryClient = useQueryClient();
  const [activeTab, setActiveTab] = React.useState<
    "enrollments" | "assignments"
  >("enrollments");

  const [isEnrollModalOpen, setIsEnrollModalOpen] = React.useState(false);
  const [isAssignModalOpen, setIsAssignModalOpen] = React.useState(false);

  // Fetch classes for dropdowns
  const { data: classesData } = useQuery<{
    items: Array<{ id: number; name: string }>;
  }>({
    queryKey: ["school-classes-brief"],
    queryFn: async () => (await apiClient.get("/master/classes")).data,
  });

  // Queries
  const { data: enrollData, isLoading: isEnrollLoading } = useQuery<{
    items: EnrollmentItem[];
  }>({
    queryKey: ["master-enrollments"],
    queryFn: async () => (await apiClient.get("/master/enrollments")).data,
  });

  const { data: assignData, isLoading: isAssignLoading } = useQuery<{
    items: AssignmentItem[];
  }>({
    queryKey: ["master-assignments"],
    queryFn: async () => (await apiClient.get("/master/assignments")).data,
  });

  // Mutations
  const createEnrollMutation = useMutation({
    mutationFn: async (payload: {
      student_id: number;
      class_id: number;
      start_date: string;
    }) => (await apiClient.post("/master/enrollments", payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["master-enrollments"] });
      toast.success("Penempatan siswa ke rombel berhasil");
      setIsEnrollModalOpen(false);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal menempatkan siswa");
    },
  });

  const createAssignMutation = useMutation({
    mutationFn: async (payload: {
      employee_id: number;
      class_id: number;
      role: string;
      start_date: string;
    }) => (await apiClient.post("/master/assignments", payload)).data,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["master-assignments"] });
      toast.success("Penugasan guru berhasil disimpan");
      setIsAssignModalOpen(false);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(
        errObj?.normalized?.message || "Gagal menyimpan penugasan guru",
      );
    },
  });

  const {
    register: regEnroll,
    handleSubmit: submitEnroll,
    reset: resetEnroll,
  } = useForm<{
    student_id: number;
    class_id: number;
    start_date: string;
  }>();

  const {
    register: regAssign,
    handleSubmit: submitAssign,
    reset: resetAssign,
  } = useForm<{
    employee_id: number;
    class_id: number;
    role: "GURU_MAPEL" | "WALI_KELAS";
    start_date: string;
  }>({
    defaultValues: { role: "GURU_MAPEL" },
  });

  const enrollColumns: ColumnDef<EnrollmentItem>[] = [
    {
      header: "ID Siswa",
      accessorKey: "student_id",
      className: "font-mono text-xs",
    },
    {
      header: "Siswa",
      cell: (i) =>
        i.student_name
          ? `${i.student_name} (${i.student_number || ""})`
          : `Siswa #${i.student_id}`,
    },
    {
      header: "Rombel Kelas",
      cell: (i) => i.class_name || `Kelas #${i.class_id}`,
    },
    { header: "Tanggal Masuk", accessorKey: "start_date" },
    {
      header: "Status",
      cell: (i) =>
        i.end_date ? (
          <span className="text-xs text-text-muted">
            Selesai ({i.end_date})
          </span>
        ) : (
          <span className="px-2 py-0.5 rounded-sm bg-semantic-success-bg text-semantic-success-fg text-xs font-semibold">
            Aktif di Rombel
          </span>
        ),
    },
  ];

  const assignColumns: ColumnDef<AssignmentItem>[] = [
    {
      header: "ID Pegawai",
      accessorKey: "employee_id",
      className: "font-mono text-xs",
    },
    {
      header: "Pegawai / Guru",
      cell: (i) => i.employee_name || `Pegawai #${i.employee_id}`,
    },
    {
      header: "Rombel Ditugaskan",
      cell: (i) => i.class_name || `Kelas #${i.class_id}`,
    },
    {
      header: "Peran Penugasan",
      cell: (i) => (
        <span
          className={`px-2 py-0.5 rounded-sm text-xs font-semibold ${
            i.role === "WALI_KELAS"
              ? "bg-brand-primary-subtle text-brand-primary"
              : "bg-brand-accent-subtle text-brand-accent"
          }`}
        >
          {i.role === "WALI_KELAS" ? "Wali Kelas" : "Guru Pengampu"}
        </span>
      ),
    },
    { header: "Mulai Penugasan", accessorKey: "start_date" },
  ];

  return (
    <div className="space-y-6">
      {/* Tab Switcher */}
      <div className="flex border-b border-border bg-surface rounded-t-card px-4 pt-3 gap-2">
        <button
          type="button"
          onClick={() => setActiveTab("enrollments")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === "enrollments"
              ? "border-brand-primary text-brand-primary"
              : "border-transparent text-text-muted hover:text-text-foreground"
          }`}
        >
          <GraduationCap className="h-4 w-4" />
          <span>Penempatan Rombel Siswa</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab("assignments")}
          className={`flex items-center gap-2 px-4 py-2.5 text-sm font-semibold border-b-2 transition-colors ${
            activeTab === "assignments"
              ? "border-brand-primary text-brand-primary"
              : "border-transparent text-text-muted hover:text-text-foreground"
          }`}
        >
          <UserCheck className="h-4 w-4" />
          <span>Penugasan Guru & Wali Kelas</span>
        </button>
      </div>

      {activeTab === "enrollments" ? (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-surface p-4 rounded-card border border-border shadow-sm">
            <div>
              <h3 className="font-semibold text-text-foreground">
                Alokasi Siswa ke Kelas Rombel
              </h3>
              <p className="text-xs text-text-muted">
                Menempatkan siswa aktif ke rombongan belajar tahun ajaran
                berjalan.
              </p>
            </div>
            <Button
              variant="primary"
              onClick={() => {
                resetEnroll();
                setIsEnrollModalOpen(true);
              }}
            >
              <Plus className="h-4 w-4 mr-1.5" /> Tempatkan Siswa
            </Button>
          </div>

          <DataTable<EnrollmentItem>
            columns={enrollColumns}
            data={enrollData?.items || []}
            isLoading={isEnrollLoading}
            keyExtractor={(i) => i.id}
          />
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex justify-between items-center bg-surface p-4 rounded-card border border-border shadow-sm">
            <div>
              <h3 className="font-semibold text-text-foreground">
                SK Penugasan Guru & Wali Kelas
              </h3>
              <p className="text-xs text-text-muted">
                Menetapkan guru mata pelajaran dan wali kelas pada rombel aktif.
              </p>
            </div>
            <Button
              variant="primary"
              onClick={() => {
                resetAssign();
                setIsAssignModalOpen(true);
              }}
            >
              <Plus className="h-4 w-4 mr-1.5" /> Tambah Penugasan
            </Button>
          </div>

          <DataTable<AssignmentItem>
            columns={assignColumns}
            data={assignData?.items || []}
            isLoading={isAssignLoading}
            keyExtractor={(i) => i.id}
          />
        </div>
      )}

      {/* Modal: Tempatkan Siswa */}
      <DialogPrimitive.Root
        open={isEnrollModalOpen}
        onOpenChange={setIsEnrollModalOpen}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground pb-2 border-b border-border">
              Tempatkan Siswa ke Rombel
            </DialogPrimitive.Title>

            <form
              onSubmit={submitEnroll((d) =>
                createEnrollMutation.mutate({
                  student_id: Number(d.student_id),
                  class_id: Number(d.class_id),
                  start_date: d.start_date,
                }),
              )}
              className="space-y-4 pt-4"
            >
              <FormField id="en_student" label="ID Siswa" isRequired>
                <Input
                  id="en_student"
                  type="number"
                  placeholder="Contoh: 101"
                  {...regEnroll("student_id", { required: true })}
                />
              </FormField>

              <FormField id="en_class" label="Rombongan Belajar" isRequired>
                <select
                  id="en_class"
                  className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm"
                  {...regEnroll("class_id", { required: true })}
                >
                  <option value="">Pilih Rombel Kelas</option>
                  {classesData?.items.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </FormField>

              <FormField id="en_start" label="Tanggal Masuk Rombel" isRequired>
                <Input
                  id="en_start"
                  type="date"
                  {...regEnroll("start_date", { required: true })}
                />
              </FormField>

              <div className="flex justify-end gap-2 pt-3 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsEnrollModalOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createEnrollMutation.isPending}
                >
                  Simpan Penempatan
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>

      {/* Modal: Tambah Penugasan */}
      <DialogPrimitive.Root
        open={isAssignModalOpen}
        onOpenChange={setIsAssignModalOpen}
      >
        <DialogPrimitive.Portal>
          <DialogPrimitive.Overlay className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm" />
          <DialogPrimitive.Content className="fixed left-[50%] top-[50%] z-50 w-full max-w-md translate-x-[-50%] translate-y-[-50%] rounded-panel border border-border bg-surface p-6 shadow-lg">
            <DialogPrimitive.Title className="text-lg font-semibold text-text-foreground pb-2 border-b border-border">
              Tetapkan Penugasan Guru
            </DialogPrimitive.Title>

            <form
              onSubmit={submitAssign((d) =>
                createAssignMutation.mutate({
                  employee_id: Number(d.employee_id),
                  class_id: Number(d.class_id),
                  role: d.role,
                  start_date: d.start_date,
                }),
              )}
              className="space-y-4 pt-4"
            >
              <FormField id="as_emp" label="ID Pegawai Guru" isRequired>
                <Input
                  id="as_emp"
                  type="number"
                  placeholder="Contoh: 15"
                  {...regAssign("employee_id", { required: true })}
                />
              </FormField>

              <FormField id="as_class" label="Rombongan Belajar" isRequired>
                <select
                  id="as_class"
                  className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm"
                  {...regAssign("class_id", { required: true })}
                >
                  <option value="">Pilih Rombel Kelas</option>
                  {classesData?.items.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </FormField>

              <FormField id="as_role" label="Peran Penugasan" isRequired>
                <select
                  id="as_role"
                  className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm"
                  {...regAssign("role", { required: true })}
                >
                  <option value="GURU_MAPEL">
                    Guru Pengampu Mata Pelajaran
                  </option>
                  <option value="WALI_KELAS">Wali Kelas</option>
                </select>
              </FormField>

              <FormField id="as_start" label="Tanggal SK Mulai" isRequired>
                <Input
                  id="as_start"
                  type="date"
                  {...regAssign("start_date", { required: true })}
                />
              </FormField>

              <div className="flex justify-end gap-2 pt-3 border-t border-border">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setIsAssignModalOpen(false)}
                >
                  Batal
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  isLoading={createAssignMutation.isPending}
                >
                  Simpan Penugasan
                </Button>
              </div>
            </form>
          </DialogPrimitive.Content>
        </DialogPrimitive.Portal>
      </DialogPrimitive.Root>
    </div>
  );
};
