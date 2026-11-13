import * as React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import {
  ArrowLeft,
  GraduationCap,
  CheckCircle2,
  XCircle,
  Play,
  FileEdit,
  ShieldAlert,
} from "lucide-react";
import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";
import { StatusBadge } from "@/components/atoms/StatusBadge";
import { FormField } from "@/components/molecules/FormField";
import { formatDateTime } from "@/lib/formatters";

interface CaseEventItem {
  id: number;
  action: string;
  note?: string | null;
  created_at: string;
  created_by_name?: string;
}

interface CaseDetailResponse {
  id: number;
  case_number: string;
  student_id: number;
  student_name?: string;
  student_number?: string;
  class_name?: string;
  category: string;
  description: string;
  status: "BARU" | "DIPROSES" | "SELESAI" | "DIBATALKAN";
  version: number;
  created_at: string;
  reported_by_name?: string;
  events: CaseEventItem[];
}

export const CaseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const { hasRole } = useAuthStore();
  const isKesiswaan = hasRole("Kesiswaan");

  const [concurrencyError, setConcurrencyError] = React.useState<string | null>(
    null,
  );

  // Fetch case detail
  const {
    data: caseData,
    isLoading,
    refetch,
  } = useQuery<CaseDetailResponse>({
    queryKey: ["student-case-detail", id],
    queryFn: async () => {
      const res = await apiClient.get<CaseDetailResponse>(
        `/student-affairs/cases/${id}`,
      );
      return res.data;
    },
    enabled: !!id,
  });

  const { register, watch, reset } = useForm<{
    action: string;
    note: string;
  }>({
    defaultValues: { action: "", note: "" },
  });

  const selectedAction = watch("action");

  // Transition Mutation
  const transitionMutation = useMutation({
    mutationFn: async (payload: {
      action: string;
      note?: string;
      expected_version: number;
    }) => {
      const res = await apiClient.post(
        `/student-affairs/cases/${id}/transitions`,
        payload,
      );
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["student-case-detail", id] });
      queryClient.invalidateQueries({ queryKey: ["student-cases"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard-metrics"] });
      toast.success("Status kasus berhasil diperbarui");
      setConcurrencyError(null);
      reset({ action: "", note: "" });
    },
    onError: (err: unknown) => {
      const errObj = err as {
        response?: { status: number };
        normalized?: { message: string };
      };
      if (errObj.response?.status === 409) {
        setConcurrencyError(
          "Konflik Konkurensi (409): Kasus ini telah diubah oleh pengguna lain. Silakan perbarui data sebelum melanjutkan.",
        );
      } else {
        toast.error(
          errObj?.normalized?.message || "Gagal mengubah status kasus",
        );
      }
    },
  });

  if (isLoading) {
    return (
      <div className="bg-surface rounded-card border border-border p-8 text-center text-sm text-text-muted">
        Memuat rincian data kasus kesiswaan...
      </div>
    );
  }

  if (!caseData) {
    return (
      <div className="bg-surface rounded-card border border-border p-8 text-center space-y-4">
        <p className="text-sm text-text-muted">
          Kasus kesiswaan tidak ditemukan atau telah dihapus.
        </p>
        <Link to="/cases">
          <Button variant="secondary">Kembali ke Daftar Kasus</Button>
        </Link>
      </div>
    );
  }

  const isTerminal =
    caseData.status === "SELESAI" || caseData.status === "DIBATALKAN";

  const onExecuteTransition = (action: string, note: string) => {
    transitionMutation.mutate({
      action,
      note: note || undefined,
      expected_version: caseData.version,
    });
  };

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb and Navigation */}
      <div className="flex items-center justify-between">
        <Link
          to="/cases"
          className="inline-flex items-center text-sm font-medium text-text-muted hover:text-text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4 mr-1.5" />
          Kembali ke Daftar Kasus
        </Link>
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-text-muted">
            Versi #{caseData.version}
          </span>
          <StatusBadge status={caseData.status} />
        </div>
      </div>

      {concurrencyError && (
        <div className="bg-semantic-danger-bg border border-semantic-danger-border p-4 rounded-card flex items-start justify-between gap-3 text-semantic-danger-fg text-sm">
          <div className="flex items-start gap-2">
            <ShieldAlert className="h-5 w-5 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Terjadi Konflik Versi Data</p>
              <p className="text-xs text-text-foreground mt-0.5">
                {concurrencyError}
              </p>
            </div>
          </div>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => {
              refetch();
              setConcurrencyError(null);
            }}
          >
            Muat Ulang Data Terbaru
          </Button>
        </div>
      )}

      {/* 62:38 Golden Ratio Adaptive Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (62%): Case Details & Timeline */}
        <div className="lg:col-span-7 space-y-6">
          {/* Case Description Card */}
          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
            <div className="flex items-start justify-between border-b border-border pb-3">
              <div>
                <span className="text-xs font-mono text-text-muted block">
                  Nomor Registrasi Kasus:
                </span>
                <h3 className="text-xl font-bold text-text-foreground font-mono">
                  {caseData.case_number}
                </h3>
              </div>
              <span className="px-2.5 py-1 rounded-sm bg-brand-primary-subtle text-brand-primary text-xs font-semibold">
                Kategori: {caseData.category}
              </span>
            </div>

            <div>
              <h4 className="text-xs font-semibold uppercase text-text-muted mb-1.5">
                Uraian Rujukan Awal:
              </h4>
              <p className="text-sm text-text-foreground leading-relaxed bg-surface-subtle p-3.5 rounded-input border border-border">
                {caseData.description}
              </p>
            </div>
          </div>

          {/* Action Transition Card (Only if non-terminal & Kesiswaan) */}
          {!isTerminal && isKesiswaan && (
            <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
              <h4 className="text-sm font-bold text-text-foreground border-b border-border pb-2.5">
                Pencatatan Tindakan & Alur Kasus
              </h4>

              <div className="space-y-4">
                <FormField
                  id="action_note"
                  label="Catatan Penanganan / Tindakan Mediasi"
                  isRequired={
                    selectedAction === "CATAT_TINDAKAN" ||
                    selectedAction === "BATALKAN"
                  }
                >
                  <textarea
                    id="action_note"
                    rows={3}
                    placeholder="Tuliskan catatan konseling, arahan pembinaan, atau alasan penutupan..."
                    className="w-full rounded-input border border-border-input bg-surface p-3 text-sm text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
                    {...register("note")}
                  />
                </FormField>

                <div className="flex flex-wrap gap-2 pt-2">
                  {caseData.status === "BARU" && (
                    <Button
                      type="button"
                      variant="primary"
                      onClick={() =>
                        onExecuteTransition("MULAI_PENANGANAN", watch("note"))
                      }
                      isLoading={transitionMutation.isPending}
                    >
                      <Play className="h-4 w-4 mr-1.5" /> Mulai Penanganan
                    </Button>
                  )}

                  {caseData.status === "DIPROSES" && (
                    <>
                      <Button
                        type="button"
                        variant="secondary"
                        onClick={() => {
                          const note = watch("note");
                          if (!note.trim()) {
                            toast.error(
                              "Catatan tindakan wajib diisi untuk aksi ini",
                            );
                            return;
                          }
                          onExecuteTransition("CATAT_TINDAKAN", note);
                        }}
                        isLoading={transitionMutation.isPending}
                      >
                        <FileEdit className="h-4 w-4 mr-1.5" /> Catat Tindakan
                        Mediasi
                      </Button>

                      <Button
                        type="button"
                        variant="accent"
                        onClick={() =>
                          onExecuteTransition("SELESAIKAN", watch("note"))
                        }
                        isLoading={transitionMutation.isPending}
                      >
                        <CheckCircle2 className="h-4 w-4 mr-1.5" /> Selesaikan
                        Kasus
                      </Button>
                    </>
                  )}

                  <Button
                    type="button"
                    variant="danger"
                    onClick={() => {
                      const note = watch("note");
                      if (!note.trim()) {
                        toast.error(
                          "Alasan pembatalan wajib diisi pada catatan",
                        );
                        return;
                      }
                      onExecuteTransition("BATALKAN", note);
                    }}
                    isLoading={transitionMutation.isPending}
                  >
                    <XCircle className="h-4 w-4 mr-1.5" /> Batalkan Kasus
                  </Button>
                </div>
              </div>
            </div>
          )}

          {/* Timeline of Events */}
          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
            <h4 className="text-sm font-bold text-text-foreground border-b border-border pb-2.5">
              Kronologi Rekam Penanganan (Timeline Events)
            </h4>

            {caseData.events && caseData.events.length > 0 ? (
              <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-border">
                {caseData.events.map((ev) => (
                  <div key={ev.id} className="relative">
                    <div className="absolute -left-6 top-1 h-3.5 w-3.5 rounded-full border-2 border-brand-primary bg-surface" />
                    <div>
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-brand-primary">
                          {ev.action.replace(/_/g, " ")}
                        </span>
                        <span className="text-[11px] text-text-muted">
                          {formatDateTime(ev.created_at)}
                        </span>
                      </div>
                      <p className="text-xs text-text-muted mt-0.5">
                        Oleh: {ev.created_by_name || "Petugas BK"}
                      </p>
                      {ev.note && (
                        <div
                          className={`mt-2 p-2.5 rounded-input text-xs ${
                            ev.note.includes("Dirahasiakan")
                              ? "bg-amber-50 text-amber-900 border border-amber-200 italic"
                              : "bg-surface-subtle text-text-foreground border border-border"
                          }`}
                        >
                          {ev.note}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-text-muted italic py-3 text-center">
                Belum ada peristiwa penanganan yang dicatat.
              </p>
            )}
          </div>
        </div>

        {/* Right Column (38%): Student Info & Metadata */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
            <div className="flex items-center gap-2 border-b border-border pb-3">
              <GraduationCap className="h-5 w-5 text-brand-primary" />
              <h4 className="text-sm font-bold text-text-foreground">
                Profil Siswa Terlapor
              </h4>
            </div>

            <div className="space-y-3 text-sm">
              <div>
                <span className="text-xs text-text-muted block">
                  Nama Siswa
                </span>
                <span className="font-semibold text-text-foreground">
                  {caseData.student_name || `Siswa #${caseData.student_id}`}
                </span>
              </div>

              <div>
                <span className="text-xs text-text-muted block">
                  Nomor Induk Siswa (NIS)
                </span>
                <span className="font-mono text-xs">
                  {caseData.student_number || "-"}
                </span>
              </div>

              <div>
                <span className="text-xs text-text-muted block">
                  Rombongan Belajar (Kelas)
                </span>
                <span className="font-medium text-text-foreground">
                  {caseData.class_name || "-"}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-3">
            <h4 className="text-sm font-bold text-text-foreground border-b border-border pb-2">
              Metadata Laporan
            </h4>
            <div className="space-y-2 text-xs text-text-muted">
              <div>
                <span className="block font-medium">Pelapor Awal:</span>
                <span className="text-text-foreground">
                  {caseData.reported_by_name || "Guru Pelapor"}
                </span>
              </div>
              <div>
                <span className="block font-medium">Waktu Dilaporkan:</span>
                <span className="text-text-foreground">
                  {formatDateTime(caseData.created_at)}
                </span>
              </div>
              <div className="pt-2 border-t border-border">
                <span className="block font-medium text-brand-accent">
                  Kepatuhan Privasi Konseling:
                </span>
                <span className="text-text-muted">
                  Memenuhi standar DEC-TECH-18. Catatan konseling privat
                  dimasking otomatis untuk menjaga etika pembinaan siswa.
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
