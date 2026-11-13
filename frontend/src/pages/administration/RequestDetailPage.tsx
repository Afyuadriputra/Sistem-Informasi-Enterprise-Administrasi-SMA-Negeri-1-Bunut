import * as React from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import {
  ArrowLeft,
  FileText,
  Download,
  Upload,
  CheckCircle,
  XCircle,
  Send,
  Play,
  ShieldCheck,
  ShieldAlert,
} from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/stores/auth-store";
import { Button } from "@/components/atoms/Button";
import { StatusBadge } from "@/components/atoms/StatusBadge";
import { FormField } from "@/components/molecules/FormField";
import { formatDate, formatDateTime } from "@/lib/formatters";

interface DocumentItem {
  id: number;
  original_filename: string;
  file_size: number;
  mime_type: string;
  document_type?: string;
  created_at: string;
}

interface ServiceEventItem {
  id: number;
  action: string;
  note?: string | null;
  created_at: string;
  created_by_name?: string;
}

interface ServiceRequestDetail {
  id: number;
  request_number: string;
  service_type_name: string;
  student_id: number;
  student_name?: string;
  student_number?: string;
  class_name?: string;
  applicant_name: string;
  purpose: string;
  status:
    | "DIAJUKAN"
    | "DIPROSES"
    | "MENUNGGU_PERSETUJUAN"
    | "DISETUJUI"
    | "DITOLAK"
    | "SELESAI";
  version: number;
  created_at: string;
  documents: DocumentItem[];
  events: ServiceEventItem[];
}

export const RequestDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const { hasRole } = useAuthStore();
  const isTU = hasRole("Tata Usaha");
  const isPimpinan = hasRole("Pimpinan");

  const [downloadingId, setDownloadingId] = React.useState<number | null>(null);
  const [concurrencyError, setConcurrencyError] = React.useState<string | null>(
    null,
  );
  const [uploadFile, setUploadFile] = React.useState<File | null>(null);

  // Fetch request detail
  const {
    data: reqData,
    isLoading,
    refetch,
  } = useQuery<ServiceRequestDetail>({
    queryKey: ["service-request-detail", id],
    queryFn: async () => {
      const res = await apiClient.get<ServiceRequestDetail>(
        `/administration/requests/${id}`,
      );
      return res.data;
    },
    enabled: !!id,
  });

  const { register, watch, reset } = useForm<{ note: string }>({
    defaultValues: { note: "" },
  });

  // Transition Mutation
  const transitionMutation = useMutation({
    mutationFn: async (payload: {
      action: string;
      note?: string;
      expected_version: number;
    }) => {
      const res = await apiClient.post(
        `/administration/requests/${id}/transitions`,
        payload,
      );
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["service-request-detail", id],
      });
      queryClient.invalidateQueries({ queryKey: ["service-requests"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard-metrics"] });
      toast.success("Status alur permohonan berhasil diperbarui");
      setConcurrencyError(null);
      reset({ note: "" });
    },
    onError: (err: unknown) => {
      const errObj = err as {
        response?: { status: number };
        normalized?: { message: string };
      };
      if (errObj.response?.status === 409) {
        setConcurrencyError(
          "Konflik Konkurensi (409): Status permohonan ini telah diubah oleh pengguna lain. Silakan perbarui data.",
        );
      } else {
        toast.error(
          errObj?.normalized?.message || "Gagal mengubah status permohonan",
        );
      }
    },
  });

  // Document Upload Mutation
  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("document_type", "LAMPIRAN");
      const res = await apiClient.post(
        `/administration/requests/${id}/documents`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        },
      );
      return res.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["service-request-detail", id],
      });
      toast.success("Lampiran berkas berhasil diunggah");
      setUploadFile(null);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(errObj?.normalized?.message || "Gagal mengunggah berkas");
    },
  });

  // Download Document
  const handleDownload = async (doc: DocumentItem) => {
    setDownloadingId(doc.id);
    try {
      const res = await apiClient.get(
        `/administration/documents/${doc.id}/download`,
        {
          responseType: "blob",
        },
      );
      const blob = new Blob([res.data], {
        type: doc.mime_type || "application/octet-stream",
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", doc.original_filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      toast.success("Berkas berhasil diunduh");
    } catch {
      toast.error("Gagal mengunduh berkas privat");
    } finally {
      setDownloadingId(null);
    }
  };

  if (isLoading) {
    return (
      <div className="bg-surface rounded-card border border-border p-8 text-center text-sm text-text-muted">
        Memuat detail permohonan surat...
      </div>
    );
  }

  if (!reqData) {
    return (
      <div className="bg-surface rounded-card border border-border p-8 text-center space-y-4">
        <p className="text-sm text-text-muted">
          Permohonan surat tidak ditemukan.
        </p>
        <Link to="/requests">
          <Button variant="secondary">Kembali ke Daftar</Button>
        </Link>
      </div>
    );
  }

  const isTerminal =
    reqData.status === "SELESAI" || reqData.status === "DITOLAK";

  const onExecuteTransition = (action: string) => {
    transitionMutation.mutate({
      action,
      note: watch("note") || undefined,
      expected_version: reqData.version,
    });
  };

  return (
    <div className="space-y-6">
      {/* Breadcrumb Header */}
      <div className="flex items-center justify-between">
        <Link
          to="/requests"
          className="inline-flex items-center text-sm font-medium text-text-muted hover:text-text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4 mr-1.5" />
          Kembali ke Daftar Permohonan
        </Link>
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-text-muted">
            Versi #{reqData.version}
          </span>
          <StatusBadge status={reqData.status} />
        </div>
      </div>

      {concurrencyError && (
        <div className="bg-semantic-danger-bg border border-semantic-danger-border p-4 rounded-card flex items-start justify-between gap-3 text-semantic-danger-fg text-sm">
          <div className="flex items-start gap-2">
            <ShieldAlert className="h-5 w-5 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Konflik Konkurensi Data</p>
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
            Perbarui Data
          </Button>
        </div>
      )}

      {/* 62:38 Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (62%): Details & Workflow Actions */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
            <div className="flex items-start justify-between border-b border-border pb-3">
              <div>
                <span className="text-xs font-mono text-text-muted block">
                  Nomor Register Surat:
                </span>
                <h3 className="text-xl font-bold text-text-foreground font-mono">
                  {reqData.request_number}
                </h3>
              </div>
              <span className="px-2.5 py-1 rounded-sm bg-brand-primary-subtle text-brand-primary text-xs font-semibold">
                {reqData.service_type_name}
              </span>
            </div>

            <div className="space-y-3">
              <div>
                <span className="text-xs font-semibold uppercase text-text-muted block">
                  Keperluan / Tujuan:
                </span>
                <p className="text-sm text-text-foreground bg-surface-subtle p-3 rounded-input border border-border mt-1">
                  {reqData.purpose}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-3 text-sm pt-2">
                <div>
                  <span className="text-xs text-text-muted block">
                    Pemohon:
                  </span>
                  <span className="font-semibold">
                    {reqData.applicant_name}
                  </span>
                </div>
                <div>
                  <span className="text-xs text-text-muted block">
                    Tanggal Diajukan:
                  </span>
                  <span>{formatDate(reqData.created_at)}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Workflow Actions Card */}
          {!isTerminal && (
            <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
              <h4 className="text-sm font-bold text-text-foreground border-b border-border pb-2.5">
                Proses & Disposisi Layanan Persuratan
              </h4>

              <FormField
                id="action_note"
                label="Catatan Disposisi / Verifikasi"
              >
                <textarea
                  id="action_note"
                  rows={2}
                  placeholder="Tambahkan catatan verifikasi atau pertimbangan..."
                  className="w-full rounded-input border border-border-input bg-surface p-3 text-sm"
                  {...register("note")}
                />
              </FormField>

              <div className="flex flex-wrap gap-2 pt-2">
                {/* TU Actions */}
                {isTU && reqData.status === "DIAJUKAN" && (
                  <Button
                    type="button"
                    variant="primary"
                    onClick={() => onExecuteTransition("PROSES")}
                    isLoading={transitionMutation.isPending}
                  >
                    <Play className="h-4 w-4 mr-1.5" /> Mulai Verifikasi Berkas
                  </Button>
                )}

                {isTU && reqData.status === "DIPROSES" && (
                  <Button
                    type="button"
                    variant="accent"
                    onClick={() => onExecuteTransition("AJUKAN_PERSETUJUAN")}
                    isLoading={transitionMutation.isPending}
                  >
                    <Send className="h-4 w-4 mr-1.5" /> Ajukan ke Kepala Sekolah
                  </Button>
                )}

                {isTU && reqData.status === "DISETUJUI" && (
                  <Button
                    type="button"
                    variant="primary"
                    onClick={() => onExecuteTransition("SELESAIKAN")}
                    isLoading={transitionMutation.isPending}
                  >
                    <CheckCircle className="h-4 w-4 mr-1.5" /> Terbitkan &
                    Selesaikan Surat
                  </Button>
                )}

                {/* Pimpinan Disposisi Actions */}
                {isPimpinan && reqData.status === "MENUNGGU_PERSETUJUAN" && (
                  <>
                    <Button
                      type="button"
                      variant="accent"
                      onClick={() => onExecuteTransition("SETUJUI")}
                      isLoading={transitionMutation.isPending}
                    >
                      <CheckCircle className="h-4 w-4 mr-1.5" /> Berikan
                      Persetujuan (Disposisi)
                    </Button>
                    <Button
                      type="button"
                      variant="danger"
                      onClick={() => {
                        const note = watch("note");
                        if (!note.trim()) {
                          toast.error(
                            "Alasan penolakan wajib ditulis pada catatan",
                          );
                          return;
                        }
                        onExecuteTransition("TOLAK");
                      }}
                      isLoading={transitionMutation.isPending}
                    >
                      <XCircle className="h-4 w-4 mr-1.5" /> Tolak Permohonan
                    </Button>
                  </>
                )}
              </div>
            </div>
          )}

          {/* Timeline of Events */}
          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
            <h4 className="text-sm font-bold text-text-foreground border-b border-border pb-2.5">
              Jejak Audit & Alur Disposisi
            </h4>

            {reqData.events && reqData.events.length > 0 ? (
              <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-border">
                {reqData.events.map((ev) => (
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
                        Oleh: {ev.created_by_name || "Petugas Tata Usaha"}
                      </p>
                      {ev.note && (
                        <div className="mt-1.5 p-2 rounded-input bg-surface-subtle text-xs text-text-foreground border border-border">
                          {ev.note}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-text-muted italic text-center py-2">
                Belum ada catatan alur.
              </p>
            )}
          </div>
        </div>

        {/* Right Column (38%): Documents & Student */}
        <div className="lg:col-span-5 space-y-6">
          {/* Documents Card */}
          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-border pb-3">
              <div className="flex items-center gap-2">
                <FileText className="h-5 w-5 text-brand-primary" />
                <h4 className="text-sm font-bold text-text-foreground">
                  Lampiran Berkas Privat
                </h4>
              </div>
              <span className="text-xs text-text-muted">
                {reqData.documents.length} berkas
              </span>
            </div>

            {reqData.documents.length > 0 ? (
              <div className="divide-y divide-border border border-border rounded-input overflow-hidden">
                {reqData.documents.map((doc) => (
                  <div
                    key={doc.id}
                    className="p-3 flex items-center justify-between gap-2 text-xs hover:bg-surface-subtle"
                  >
                    <div className="truncate flex-1">
                      <p className="font-semibold text-text-foreground truncate">
                        {doc.original_filename}
                      </p>
                      <p className="text-[11px] text-text-muted">
                        {(doc.file_size / 1024).toFixed(1)} KB •{" "}
                        {doc.document_type || "Lampiran"}
                      </p>
                    </div>
                    <Button
                      type="button"
                      variant="secondary"
                      size="sm"
                      onClick={() => handleDownload(doc)}
                      isLoading={downloadingId === doc.id}
                      aria-label={`Unduh ${doc.original_filename}`}
                    >
                      <Download className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-text-muted italic py-3 text-center">
                Belum ada lampiran berkas yang diunggah.
              </p>
            )}

            {/* Upload More Files (Only TU if not terminal) */}
            {isTU && !isTerminal && (
              <div className="pt-2 border-t border-border space-y-2">
                <span className="text-xs font-semibold text-text-foreground block">
                  Unggah Lampiran Tambahan:
                </span>
                <div className="flex items-center gap-2">
                  <input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    className="text-xs w-full file:mr-2 file:py-1.5 file:px-2.5 file:rounded-input file:border-0 file:text-xs file:font-medium file:bg-brand-primary-subtle file:text-brand-primary"
                  />
                  <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    disabled={!uploadFile}
                    isLoading={uploadMutation.isPending}
                    onClick={() =>
                      uploadFile && uploadMutation.mutate(uploadFile)
                    }
                  >
                    <Upload className="h-3.5 w-3.5 mr-1" /> Unggah
                  </Button>
                </div>
              </div>
            )}
          </div>

          {/* Student Profile Card */}
          <div className="bg-surface border border-border rounded-card p-6 shadow-sm space-y-3">
            <div className="flex items-center gap-2 border-b border-border pb-2.5">
              <ShieldCheck className="h-5 w-5 text-brand-accent" />
              <h4 className="text-sm font-bold text-text-foreground">
                Siswa Pemohon
              </h4>
            </div>

            <div className="space-y-2 text-xs">
              <div>
                <span className="text-text-muted block">Nama Siswa:</span>
                <span className="font-semibold text-text-foreground">
                  {reqData.student_name || `Siswa #${reqData.student_id}`}
                </span>
              </div>
              <div>
                <span className="text-text-muted block">
                  Nomor Induk Siswa (NIS):
                </span>
                <span className="font-mono">
                  {reqData.student_number || "-"}
                </span>
              </div>
              <div>
                <span className="text-text-muted block">Kelas Rombel:</span>
                <span className="font-medium">{reqData.class_name || "-"}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
