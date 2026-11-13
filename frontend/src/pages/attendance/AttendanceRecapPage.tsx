import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { FileSpreadsheet } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { StatusBadge } from "@/components/atoms/StatusBadge";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import { formatDate } from "@/lib/formatters";

interface AttendanceRecordItem {
  id: number;
  student_id: number;
  student_name?: string;
  student_number?: string;
  class_id: number;
  class_name?: string;
  date: string;
  status: "HADIR" | "SAKIT" | "IZIN" | "ALPA";
  notes?: string | null;
  recorded_by_name?: string;
}

export const AttendanceRecapPage: React.FC = () => {
  const { user } = useAuthStore();
  const assignedClasses = user?.assigned_classes || [];

  const now = new Date();
  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
    .toISOString()
    .split("T")[0];
  const todayStr = now.toISOString().split("T")[0];

  const [selectedClassId, setSelectedClassId] = React.useState<number | "">("");
  const [startDate, setStartDate] = React.useState<string>(startOfMonth);
  const [endDate, setEndDate] = React.useState<string>(todayStr);
  const [isDownloading, setIsDownloading] = React.useState(false);

  // Fetch classes if none assigned explicitly
  const { data: fallbackClasses } = useQuery<{
    items: Array<{ id: number; name: string }>;
  }>({
    queryKey: ["available-classes-recap"],
    queryFn: async () => (await apiClient.get("/master/classes")).data,
    enabled: assignedClasses.length === 0,
  });

  const classList =
    assignedClasses.length > 0 ? assignedClasses : fallbackClasses?.items || [];

  React.useEffect(() => {
    if (!selectedClassId && classList.length > 0) {
      setSelectedClassId(classList[0].id);
    }
  }, [classList, selectedClassId]);

  // Query attendance records
  const { data: recapData, isLoading } = useQuery<{
    items: AttendanceRecordItem[];
  }>({
    queryKey: ["attendance-recap", selectedClassId, startDate, endDate],
    queryFn: async () => {
      const res = await apiClient.get("/attendance", {
        params: {
          class_id: selectedClassId,
          start_date: startDate,
          end_date: endDate,
        },
      });
      return res.data;
    },
    enabled: !!selectedClassId,
  });

  // Handle Excel download
  const handleExportExcel = async () => {
    if (!selectedClassId) return;
    setIsDownloading(true);
    try {
      const res = await apiClient.get("/reports/attendance.xlsx", {
        params: {
          class_id: selectedClassId,
          start_date: startDate,
          end_date: endDate,
        },
        responseType: "blob",
      });

      const blob = new Blob([res.data], {
        type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `rekap_presensi_${selectedClassId}_${startDate}_${endDate}.xlsx`,
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success("Berkas Excel rekap kehadiran berhasil diunduh");
    } catch {
      toast.error("Gagal mengunduh laporan rekap kehadiran");
    } finally {
      setIsDownloading(false);
    }
  };

  const records = recapData?.items || [];

  // Metric aggregates
  const totalRecords = records.length;
  let hadirCount = 0;
  let sakitCount = 0;
  let izinCount = 0;
  let alpaCount = 0;

  records.forEach((r) => {
    if (r.status === "HADIR") hadirCount++;
    else if (r.status === "SAKIT") sakitCount++;
    else if (r.status === "IZIN") izinCount++;
    else if (r.status === "ALPA") alpaCount++;
  });

  const columns: ColumnDef<AttendanceRecordItem>[] = [
    {
      header: "Tanggal",
      cell: (r) => (
        <span className="font-semibold text-text-foreground">
          {formatDate(r.date)}
        </span>
      ),
    },
    {
      header: "NIS",
      accessorKey: "student_number",
      className: "font-mono text-xs",
    },
    {
      header: "Nama Siswa",
      accessorKey: "student_name",
      className: "font-semibold",
    },
    {
      header: "Status Presensi",
      cell: (r) => <StatusBadge status={r.status} />,
    },
    {
      header: "Catatan",
      cell: (r) => r.notes || "-",
    },
    {
      header: "Pencatat",
      cell: (r) => r.recorded_by_name || "Guru Pengampu",
      className: "text-xs text-text-muted",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Filter and Export Bar */}
      <div className="bg-surface p-5 rounded-card border border-border shadow-sm flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-3 flex-1">
          <div>
            <label
              htmlFor="recap-class-select"
              className="text-xs font-semibold uppercase text-text-muted mb-1 block"
            >
              Rombongan Belajar:
            </label>
            <select
              id="recap-class-select"
              value={selectedClassId}
              onChange={(e) => setSelectedClassId(Number(e.target.value))}
              className="h-10 rounded-input border border-border-input bg-surface px-3 text-sm font-semibold text-text-foreground"
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
              htmlFor="start-date-input"
              className="text-xs font-semibold uppercase text-text-muted mb-1 block"
            >
              Mulai Tanggal:
            </label>
            <Input
              id="start-date-input"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="h-10 text-xs"
            />
          </div>

          <div>
            <label
              htmlFor="end-date-input"
              className="text-xs font-semibold uppercase text-text-muted mb-1 block"
            >
              Sampai Tanggal:
            </label>
            <Input
              id="end-date-input"
              type="date"
              max={todayStr}
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="h-10 text-xs"
            />
          </div>
        </div>

        <Button
          type="button"
          variant="accent"
          size="md"
          onClick={handleExportExcel}
          disabled={totalRecords === 0}
          isLoading={isDownloading}
        >
          <FileSpreadsheet className="h-4 w-4 mr-2" />
          Ekspor Excel Resmi
        </Button>
      </div>

      {/* Aggregate Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-surface border border-border rounded-card p-4 shadow-sm text-center">
          <span className="text-xs text-text-muted block">
            Total Rekaman Kehadiran
          </span>
          <span className="text-2xl font-bold text-text-foreground tabular-nums">
            {totalRecords}
          </span>
        </div>
        <div className="bg-semantic-success-bg border border-semantic-success-border rounded-card p-4 shadow-sm text-center">
          <span className="text-xs text-semantic-success-fg font-medium block">
            Total Hadir
          </span>
          <span className="text-2xl font-bold text-semantic-success-fg tabular-nums">
            {hadirCount}
          </span>
        </div>
        <div className="bg-semantic-info-bg border border-semantic-info-border rounded-card p-4 shadow-sm text-center">
          <span className="text-xs text-semantic-info-fg font-medium block">
            Sakit / Izin
          </span>
          <span className="text-2xl font-bold text-semantic-info-fg tabular-nums">
            {sakitCount + izinCount}
          </span>
        </div>
        <div className="bg-semantic-danger-bg border border-semantic-danger-border rounded-card p-4 shadow-sm text-center">
          <span className="text-xs text-semantic-danger-fg font-medium block">
            Total Alpa
          </span>
          <span className="text-2xl font-bold text-semantic-danger-fg tabular-nums">
            {alpaCount}
          </span>
        </div>
      </div>

      {/* Recap Table */}
      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<AttendanceRecordItem>
          columns={columns}
          data={records}
          isLoading={isLoading}
          keyExtractor={(item) => item.id}
          emptyTitle="Belum Ada Rekap Presensi"
          emptyDescription="Tidak ditemukan rekam presensi pada rombel dan rentang tanggal yang dipilih."
        />
      </div>
    </div>
  );
};
