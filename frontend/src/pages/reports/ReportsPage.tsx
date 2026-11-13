import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { FileSpreadsheet, FileText, Download } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { FormField } from "@/components/molecules/FormField";

export const ReportsPage: React.FC = () => {
  const now = new Date();
  const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1)
    .toISOString()
    .split("T")[0];
  const todayStr = now.toISOString().split("T")[0];

  const [classId, setClassId] = React.useState<number | "">("");
  const [attStartDate, setAttStartDate] = React.useState(startOfMonth);
  const [attEndDate, setAttEndDate] = React.useState(todayStr);
  const [isExportingAtt, setIsExportingAtt] = React.useState(false);

  const [admStartDate, setAdmStartDate] = React.useState(startOfMonth);
  const [admEndDate, setAdmEndDate] = React.useState(todayStr);
  const [isExportingAdm, setIsExportingAdm] = React.useState(false);

  // Fetch classes for dropdown
  const { data: classesData } = useQuery<{
    items: Array<{ id: number; name: string }>;
  }>({
    queryKey: ["report-classes"],
    queryFn: async () => (await apiClient.get("/master/classes")).data,
  });

  // Export Attendance Excel
  const handleExportAttendance = async () => {
    setIsExportingAtt(true);
    try {
      const params: Record<string, string | number> = {
        start_date: attStartDate,
        end_date: attEndDate,
      };
      if (classId) params.class_id = classId;

      const res = await apiClient.get("/reports/attendance.xlsx", {
        params,
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
        `laporan_presensi_sman1bunut_${attStartDate}_${attEndDate}.xlsx`,
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success("Laporan Excel presensi berhasil diunduh");
    } catch {
      toast.error("Gagal mengunduh laporan presensi");
    } finally {
      setIsExportingAtt(false);
    }
  };

  // Export Administration PDF
  const handleExportAdministration = async () => {
    setIsExportingAdm(true);
    try {
      const res = await apiClient.get("/reports/administration.pdf", {
        params: {
          start_date: admStartDate,
          end_date: admEndDate,
        },
        responseType: "blob",
      });

      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `laporan_administrasi_sman1bunut_${admStartDate}_${admEndDate}.pdf`,
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success("Laporan resmi PDF administrasi berhasil diunduh");
    } catch {
      toast.error("Gagal mengunduh laporan administrasi");
    } finally {
      setIsExportingAdm(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-surface p-5 rounded-card border border-border shadow-sm">
        <h2 className="text-xl font-bold text-text-foreground">
          Laporan Terpadu & Ekspor Data Resmi
        </h2>
        <p className="text-xs text-text-muted mt-0.5">
          Penerbitan berkas spreadsheet (.xlsx) dan dokumen cetak (.pdf) resmi
          SMAN 1 Bunut untuk arsip dan monitoring pimpinan.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Report 1: Attendance Excel */}
        <div className="bg-surface border border-border rounded-card p-6 shadow-sm flex flex-col justify-between space-y-4">
          <div className="space-y-4">
            <div className="flex items-center gap-3 border-b border-border pb-3">
              <div className="p-2.5 rounded-panel bg-semantic-success-bg text-semantic-success-fg">
                <FileSpreadsheet className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-text-foreground">
                  Laporan Rekapitulasi Presensi (.xlsx)
                </h3>
                <p className="text-xs text-text-muted">
                  Data kehadiran siswa terformat tema Institusional Navy.
                </p>
              </div>
            </div>

            <FormField
              id="class_select"
              label="Filter Rombongan Belajar (Opsional)"
            >
              <select
                id="class_select"
                value={classId}
                onChange={(e) =>
                  setClassId(e.target.value ? Number(e.target.value) : "")
                }
                className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm"
              >
                <option value="">Semua Rombongan Belajar</option>
                {classesData?.items.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </FormField>

            <div className="grid grid-cols-2 gap-3">
              <FormField id="att_start" label="Mulai Tanggal" isRequired>
                <Input
                  id="att_start"
                  type="date"
                  value={attStartDate}
                  onChange={(e) => setAttStartDate(e.target.value)}
                />
              </FormField>
              <FormField id="att_end" label="Sampai Tanggal" isRequired>
                <Input
                  id="att_end"
                  type="date"
                  max={todayStr}
                  value={attEndDate}
                  onChange={(e) => setAttEndDate(e.target.value)}
                />
              </FormField>
            </div>
          </div>

          <Button
            type="button"
            variant="accent"
            size="lg"
            className="w-full mt-4"
            onClick={handleExportAttendance}
            isLoading={isExportingAtt}
          >
            <Download className="h-4 w-4 mr-2" />
            Unduh Berkas Excel (.xlsx)
          </Button>
        </div>

        {/* Report 2: Administration PDF */}
        <div className="bg-surface border border-border rounded-card p-6 shadow-sm flex flex-col justify-between space-y-4">
          <div className="space-y-4">
            <div className="flex items-center gap-3 border-b border-border pb-3">
              <div className="p-2.5 rounded-panel bg-semantic-danger-bg text-semantic-danger-fg">
                <FileText className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-base font-bold text-text-foreground">
                  Laporan Layanan Administrasi (.pdf)
                </h3>
                <p className="text-xs text-text-muted">
                  Dokumen cetak resmi rekap surat disposisi dan arsip
                  persuratan.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <FormField id="adm_start" label="Mulai Tanggal" isRequired>
                <Input
                  id="adm_start"
                  type="date"
                  value={admStartDate}
                  onChange={(e) => setAdmStartDate(e.target.value)}
                />
              </FormField>
              <FormField id="adm_end" label="Sampai Tanggal" isRequired>
                <Input
                  id="adm_end"
                  type="date"
                  max={todayStr}
                  value={admEndDate}
                  onChange={(e) => setAdmEndDate(e.target.value)}
                />
              </FormField>
            </div>

            <p className="text-xs text-text-muted bg-surface-subtle p-3 rounded-input border border-border">
              Laporan PDF menyertakan kop surat resmi SMA Negeri 1 Bunut,
              rekapitulasi status pengajuan, disposisi persetujuan pimpinan,
              serta nomor register surat yang diterbitkan.
            </p>
          </div>

          <Button
            type="button"
            variant="primary"
            size="lg"
            className="w-full mt-4"
            onClick={handleExportAdministration}
            isLoading={isExportingAdm}
          >
            <Download className="h-4 w-4 mr-2" />
            Unduh Dokumen PDF Resmi
          </Button>
        </div>
      </div>
    </div>
  );
};
