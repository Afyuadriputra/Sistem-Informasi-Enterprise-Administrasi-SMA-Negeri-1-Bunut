import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Save, CheckCheck } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { ConfirmDialog } from "@/components/organisms/ConfirmDialog";
import { EmptyState } from "@/components/molecules/EmptyState";

export type AttendanceStatus = "HADIR" | "SAKIT" | "IZIN" | "ALPA";

interface StudentRosterItem {
  student_id: number;
  student_number: string;
  name: string;
  gender: string;
  status: AttendanceStatus | null;
  notes?: string | null;
}

interface RosterResponse {
  class_id: number;
  class_name: string;
  date: string;
  students: StudentRosterItem[];
}

export const RecordAttendancePage: React.FC = () => {
  const queryClient = useQueryClient();
  const { user } = useAuthStore();

  const todayStr = new Date().toISOString().split("T")[0];
  const [selectedClassId, setSelectedClassId] = React.useState<number | "">("");
  const [selectedDate, setSelectedDate] = React.useState<string>(todayStr);

  const [rosterDraft, setRosterDraft] = React.useState<
    Record<number, { status: AttendanceStatus; notes: string }>
  >({});
  const [isDirty, setIsDirty] = React.useState(false);
  const [showConfirmDialog, setShowConfirmDialog] = React.useState(false);

  // Available classes: from user.assigned_classes or query
  const assignedClasses = user?.assigned_classes || [];

  // Fallback to fetch classes if user has none explicitly listed
  const { data: fallbackClasses } = useQuery<{
    items: Array<{ id: number; name: string }>;
  }>({
    queryKey: ["available-classes-attendance"],
    queryFn: async () => (await apiClient.get("/master/classes")).data,
    enabled: assignedClasses.length === 0,
  });

  const classList =
    assignedClasses.length > 0 ? assignedClasses : fallbackClasses?.items || [];

  // Set default selected class once loaded
  React.useEffect(() => {
    if (!selectedClassId && classList.length > 0) {
      setSelectedClassId(classList[0].id);
    }
  }, [classList, selectedClassId]);

  // Fetch roster
  const { data: rosterData, isLoading } = useQuery<RosterResponse>({
    queryKey: ["attendance-roster", selectedClassId, selectedDate],
    queryFn: async () => {
      const res = await apiClient.get<RosterResponse>("/attendance/roster", {
        params: {
          class_id: selectedClassId,
          date: selectedDate,
        },
      });
      return res.data;
    },
    enabled: !!selectedClassId && !!selectedDate,
  });

  // Sync draft whenever server roster data is fetched
  React.useEffect(() => {
    if (rosterData?.students) {
      const initial: Record<
        number,
        { status: AttendanceStatus; notes: string }
      > = {};
      rosterData.students.forEach((s) => {
        initial[s.student_id] = {
          status: s.status || "HADIR", // Default HADIR per school policy
          notes: s.notes || "",
        };
      });
      setRosterDraft(initial);
      setIsDirty(false);
    }
  }, [rosterData]);

  // Bulk Save Mutation
  const saveMutation = useMutation({
    mutationFn: async () => {
      const items = Object.entries(rosterDraft).map(([studentId, val]) => ({
        student_id: Number(studentId),
        status: val.status,
        notes: val.notes || undefined,
      }));

      const res = await apiClient.post("/attendance/bulk", {
        class_id: Number(selectedClassId),
        date: selectedDate,
        items,
      });
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["attendance-roster"] });
      queryClient.invalidateQueries({ queryKey: ["attendance-recap"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard-metrics"] });
      toast.success("Kehadiran kelas berhasil disimpan secara atomik");
      setIsDirty(false);
      setShowConfirmDialog(false);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(
        errObj?.normalized?.message || "Gagal menyimpan absensi kelas",
      );
    },
  });

  const handleStatusChange = (studentId: number, status: AttendanceStatus) => {
    setRosterDraft((prev) => ({
      ...prev,
      [studentId]: {
        ...(prev[studentId] || { notes: "" }),
        status,
      },
    }));
    setIsDirty(true);
  };

  const handleNotesChange = (studentId: number, notes: string) => {
    setRosterDraft((prev) => ({
      ...prev,
      [studentId]: {
        ...(prev[studentId] || { status: "HADIR" }),
        notes,
      },
    }));
    setIsDirty(true);
  };

  const handleMarkAllHadir = () => {
    if (!rosterData?.students) return;
    const updated = { ...rosterDraft };
    rosterData.students.forEach((s) => {
      updated[s.student_id] = {
        ...(updated[s.student_id] || { notes: "" }),
        status: "HADIR",
      };
    });
    setRosterDraft(updated);
    setIsDirty(true);
    toast.info("Semua siswa ditandai Hadir");
  };

  // Live Summary Calculation
  const totalStudents = rosterData?.students.length || 0;
  let hadirCount = 0;
  let sakitCount = 0;
  let izinCount = 0;
  let alpaCount = 0;

  Object.values(rosterDraft).forEach((item) => {
    if (item.status === "HADIR") hadirCount++;
    else if (item.status === "SAKIT") sakitCount++;
    else if (item.status === "IZIN") izinCount++;
    else if (item.status === "ALPA") alpaCount++;
  });

  const hadirPercentage =
    totalStudents > 0 ? ((hadirCount / totalStudents) * 100).toFixed(1) : "0";

  return (
    <div className="space-y-6">
      {/* Filter and Control Bar */}
      <div className="bg-surface p-5 rounded-card border border-border shadow-sm flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 flex-1">
          <div>
            <label
              htmlFor="class-select"
              className="text-xs font-semibold uppercase text-text-muted mb-1 block"
            >
              Pilih Rombongan Belajar:
            </label>
            <select
              id="class-select"
              value={selectedClassId}
              onChange={(e) => setSelectedClassId(Number(e.target.value))}
              className="h-10 rounded-input border border-border-input bg-surface px-3 text-sm font-semibold text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
            >
              {classList.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label
              htmlFor="date-select"
              className="text-xs font-semibold uppercase text-text-muted mb-1 block"
            >
              Tanggal Presensi:
            </label>
            <Input
              id="date-select"
              type="date"
              max={todayStr}
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="h-10 font-semibold"
            />
          </div>
        </div>

        <div className="flex items-center gap-2 pt-2 md:pt-0">
          <Button
            type="button"
            variant="secondary"
            size="md"
            onClick={handleMarkAllHadir}
            disabled={totalStudents === 0}
          >
            <CheckCheck className="h-4 w-4 mr-1.5" />
            Tandai Semua Hadir
          </Button>

          <Button
            type="button"
            variant="primary"
            size="md"
            onClick={() => setShowConfirmDialog(true)}
            disabled={totalStudents === 0 || !isDirty}
            isLoading={saveMutation.isPending}
          >
            <Save className="h-4 w-4 mr-1.5" />
            Simpan Kehadiran
          </Button>
        </div>
      </div>

      {/* Live Metrics Summary Bar */}
      {totalStudents > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div className="bg-surface border border-border rounded-card p-3 shadow-sm text-center">
            <span className="text-xs text-text-muted block">Total Siswa</span>
            <span className="text-xl font-bold text-text-foreground tabular-nums">
              {totalStudents}
            </span>
          </div>
          <div className="bg-semantic-success-bg border border-semantic-success-border rounded-card p-3 shadow-sm text-center">
            <span className="text-xs text-semantic-success-fg font-medium block">
              Hadir
            </span>
            <span className="text-xl font-bold text-semantic-success-fg tabular-nums">
              {hadirCount}{" "}
              <span className="text-xs font-normal">({hadirPercentage}%)</span>
            </span>
          </div>
          <div className="bg-semantic-info-bg border border-semantic-info-border rounded-card p-3 shadow-sm text-center">
            <span className="text-xs text-semantic-info-fg font-medium block">
              Sakit
            </span>
            <span className="text-xl font-bold text-semantic-info-fg tabular-nums">
              {sakitCount}
            </span>
          </div>
          <div className="bg-semantic-warning-bg border border-semantic-warning-border rounded-card p-3 shadow-sm text-center">
            <span className="text-xs text-semantic-warning-fg font-medium block">
              Izin
            </span>
            <span className="text-xl font-bold text-semantic-warning-fg tabular-nums">
              {izinCount}
            </span>
          </div>
          <div className="bg-semantic-danger-bg border border-semantic-danger-border rounded-card p-3 shadow-sm text-center col-span-2 sm:col-span-1">
            <span className="text-xs text-semantic-danger-fg font-medium block">
              Alpa
            </span>
            <span className="text-xl font-bold text-semantic-danger-fg tabular-nums">
              {alpaCount}
            </span>
          </div>
        </div>
      )}

      {/* Roster Table (Desktop) & Cards (Mobile) */}
      {isLoading ? (
        <div className="bg-surface rounded-card border border-border p-8 text-center text-sm text-text-muted">
          Memuat roster kehadiran kelas...
        </div>
      ) : totalStudents === 0 ? (
        <EmptyState
          title="Tidak Ada Siswa di Kelas Ini"
          description="Rombongan belajar yang dipilih belum memiliki siswa yang ditempatkan."
        />
      ) : (
        <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
          {/* Desktop Table View */}
          <div className="hidden sm:block overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-surface-subtle border-b border-border text-xs uppercase text-text-muted font-semibold">
                <tr>
                  <th className="px-4 py-3.5 w-16">No</th>
                  <th className="px-4 py-3.5 w-28">NIS</th>
                  <th className="px-4 py-3.5">Nama Siswa</th>
                  <th className="px-4 py-3.5 text-center w-72">
                    Status Presensi
                  </th>
                  <th className="px-4 py-3.5">Catatan Khusus</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {rosterData?.students.map((student, idx) => {
                  const currentStatus =
                    rosterDraft[student.student_id]?.status || "HADIR";
                  const currentNotes =
                    rosterDraft[student.student_id]?.notes || "";

                  return (
                    <tr
                      key={student.student_id}
                      className="hover:bg-surface-subtle transition-colors"
                    >
                      <td className="px-4 py-3 text-text-muted font-mono text-xs">
                        {idx + 1}
                      </td>
                      <td className="px-4 py-3 text-text-muted font-mono text-xs">
                        {student.student_number}
                      </td>
                      <td className="px-4 py-3 font-semibold text-text-foreground">
                        {student.name}
                        <span className="text-xs font-normal text-text-muted ml-2">
                          ({student.gender})
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div
                          className="flex items-center justify-center gap-1.5"
                          role="radiogroup"
                        >
                          {(
                            [
                              "HADIR",
                              "SAKIT",
                              "IZIN",
                              "ALPA",
                            ] as AttendanceStatus[]
                          ).map((st) => {
                            const isSelected = currentStatus === st;
                            const colors = {
                              HADIR: isSelected
                                ? "bg-semantic-success-fg text-white"
                                : "bg-surface text-semantic-success-fg border-semantic-success-border hover:bg-semantic-success-bg",
                              SAKIT: isSelected
                                ? "bg-semantic-info-fg text-white"
                                : "bg-surface text-semantic-info-fg border-semantic-info-border hover:bg-semantic-info-bg",
                              IZIN: isSelected
                                ? "bg-semantic-warning-fg text-white"
                                : "bg-surface text-semantic-warning-fg border-semantic-warning-border hover:bg-semantic-warning-bg",
                              ALPA: isSelected
                                ? "bg-semantic-danger-fg text-white"
                                : "bg-surface text-semantic-danger-fg border-semantic-danger-border hover:bg-semantic-danger-bg",
                            }[st];

                            return (
                              <button
                                type="button"
                                key={st}
                                onClick={() =>
                                  handleStatusChange(student.student_id, st)
                                }
                                className={`px-3 py-1.5 rounded-button text-xs font-bold border transition-all ${colors}`}
                                aria-label={`${st} untuk ${student.name}`}
                              >
                                {st}
                              </button>
                            );
                          })}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <Input
                          placeholder="Catatan..."
                          value={currentNotes}
                          onChange={(e) =>
                            handleNotesChange(
                              student.student_id,
                              e.target.value,
                            )
                          }
                          className="h-8 text-xs"
                        />
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Mobile Card View (Touch Friendly) */}
          <div className="sm:hidden divide-y divide-border">
            {rosterData?.students.map((student, idx) => {
              const currentStatus =
                rosterDraft[student.student_id]?.status || "HADIR";
              const currentNotes = rosterDraft[student.student_id]?.notes || "";

              return (
                <div key={student.student_id} className="p-4 space-y-3">
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="font-semibold text-text-foreground">
                        {student.name}
                      </div>
                      <div className="text-xs text-text-muted font-mono">
                        {student.student_number} • {student.gender}
                      </div>
                    </div>
                    <span className="text-xs font-mono text-text-muted">
                      #{idx + 1}
                    </span>
                  </div>

                  <div className="grid grid-cols-4 gap-2">
                    {(
                      ["HADIR", "SAKIT", "IZIN", "ALPA"] as AttendanceStatus[]
                    ).map((st) => {
                      const isSelected = currentStatus === st;
                      const colors = {
                        HADIR: isSelected
                          ? "bg-semantic-success-fg text-white"
                          : "bg-surface text-semantic-success-fg border-semantic-success-border",
                        SAKIT: isSelected
                          ? "bg-semantic-info-fg text-white"
                          : "bg-surface text-semantic-info-fg border-semantic-info-border",
                        IZIN: isSelected
                          ? "bg-semantic-warning-fg text-white"
                          : "bg-surface text-semantic-warning-fg border-semantic-warning-border",
                        ALPA: isSelected
                          ? "bg-semantic-danger-fg text-white"
                          : "bg-surface text-semantic-danger-fg border-semantic-danger-border",
                      }[st];

                      return (
                        <button
                          type="button"
                          key={st}
                          onClick={() =>
                            handleStatusChange(student.student_id, st)
                          }
                          className={`h-11 rounded-button text-xs font-bold border flex items-center justify-center transition-all ${colors}`}
                        >
                          {st}
                        </button>
                      );
                    })}
                  </div>

                  <Input
                    placeholder="Catatan..."
                    value={currentNotes}
                    onChange={(e) =>
                      handleNotesChange(student.student_id, e.target.value)
                    }
                    className="h-9 text-xs"
                  />
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Confirmation Dialog */}
      <ConfirmDialog
        isOpen={showConfirmDialog}
        onOpenChange={setShowConfirmDialog}
        title="Konfirmasi Simpan Presensi"
        description={`Anda akan menyimpan presensi rombel untuk ${totalStudents} siswa pada tanggal ${selectedDate}. Data tersimpan secara atomik dan audit trail riwayat akan tercatat.`}
        confirmLabel="Ya, Simpan Kehadiran"
        variant="primary"
        isLoading={saveMutation.isPending}
        onConfirm={() => saveMutation.mutate()}
      />
    </div>
  );
};
