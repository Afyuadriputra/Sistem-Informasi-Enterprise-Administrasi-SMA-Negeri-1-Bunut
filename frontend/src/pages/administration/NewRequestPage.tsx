import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate, Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { ArrowLeft } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/atoms/Button";
import { Input } from "@/components/atoms/Input";
import { FormField } from "@/components/molecules/FormField";

interface ServiceTypeItem {
  id: number;
  code: string;
  name: string;
  description?: string;
}

const requestSchema = z.object({
  service_type_id: z.coerce.number().min(1, "Pilih jenis layanan persuratan"),
  student_id: z.coerce.number().min(1, "ID Siswa wajib diisi"),
  applicant_name: z.string().min(2, "Nama pemohon wajib diisi"),
  purpose: z.string().min(5, "Tujuan dan keperluan surat minimal 5 karakter"),
});

type RequestFormData = z.infer<typeof requestSchema>;

export const NewRequestPage: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
  const [fileError, setFileError] = React.useState<string | null>(null);

  // Fetch service types
  const { data: serviceTypes, isLoading: isTypesLoading } = useQuery<{
    items: ServiceTypeItem[];
  }>({
    queryKey: ["service-types"],
    queryFn: async () =>
      (await apiClient.get("/administration/service-types")).data,
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RequestFormData>({
    resolver: zodResolver(requestSchema),
    defaultValues: {
      applicant_name: "",
      purpose: "",
    },
  });

  // Handle file selection with validation
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFileError(null);
    const file = e.target.files?.[0];
    if (!file) {
      setSelectedFile(null);
      return;
    }

    // Size limit: 5 MB
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      setFileError("Ukuran berkas melebihi batas maksimal 5 MB.");
      setSelectedFile(null);
      return;
    }

    // Allowed extensions
    const validExtensions = [".pdf", ".jpg", ".jpeg", ".png"];
    const fileName = file.name.toLowerCase();
    const isValidExt = validExtensions.some((ext) => fileName.endsWith(ext));
    if (!isValidExt) {
      setFileError(
        "Format berkas tidak diizinkan. Gunakan berkas PDF atau gambar (JPG/PNG).",
      );
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  // Submit Mutation
  const submitMutation = useMutation({
    mutationFn: async (formData: RequestFormData) => {
      // 1. Create service request
      const res = await apiClient.post<{ id: number }>(
        "/administration/requests",
        formData,
      );
      const requestId = res.data.id;

      // 2. Upload attachment if provided
      if (selectedFile) {
        const fileData = new FormData();
        fileData.append("file", selectedFile);
        fileData.append("document_type", "LAMPIRAN");
        await apiClient.post(
          `/administration/requests/${requestId}/documents`,
          fileData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          },
        );
      }

      return requestId;
    },
    onSuccess: (requestId) => {
      queryClient.invalidateQueries({ queryKey: ["service-requests"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard-metrics"] });
      toast.success("Permohonan surat berhasil dibuat");
      navigate(`/requests/${requestId}`);
    },
    onError: (err: unknown) => {
      const errObj = err as { normalized?: { message: string } };
      toast.error(
        errObj?.normalized?.message || "Gagal membuat permohonan surat",
      );
    },
  });

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center gap-3">
        <Link
          to="/requests"
          className="p-2 rounded-button text-text-muted hover:bg-surface hover:text-text-foreground transition-colors"
          aria-label="Kembali"
        >
          <ArrowLeft className="h-5 w-5" />
        </Link>
        <div>
          <h2 className="text-xl font-bold text-text-foreground">
            Buat Permohonan Surat Baru
          </h2>
          <p className="text-xs text-text-muted">
            Layanan administrasi persuratan Tata Usaha SMAN 1 Bunut.
          </p>
        </div>
      </div>

      <div className="bg-surface border border-border rounded-card p-6 shadow-sm">
        <form
          onSubmit={handleSubmit((d) => submitMutation.mutate(d))}
          className="space-y-4"
        >
          <FormField
            id="service_type_id"
            label="Jenis Surat Administrasi"
            isRequired
            error={errors.service_type_id?.message}
          >
            <select
              id="service_type_id"
              className="w-full h-10 rounded-input border border-border-input bg-surface px-3 text-sm text-text-foreground"
              {...register("service_type_id")}
              disabled={isTypesLoading}
            >
              <option value="">Pilih Jenis Layanan Surat</option>
              {serviceTypes?.items.map((st) => (
                <option key={st.id} value={st.id}>
                  {st.name} ({st.code})
                </option>
              ))}
            </select>
          </FormField>

          <FormField
            id="student_id"
            label="ID Siswa Bersangkutan"
            isRequired
            error={errors.student_id?.message}
            helperText="Masukkan ID database siswa pemohon."
          >
            <Input
              id="student_id"
              type="number"
              placeholder="Contoh: 101"
              {...register("student_id")}
            />
          </FormField>

          <FormField
            id="applicant_name"
            label="Nama Pemohon / Orang Tua / Siswa"
            isRequired
            error={errors.applicant_name?.message}
          >
            <Input
              id="applicant_name"
              placeholder="Contoh: Bapak Hendra Kusuma"
              {...register("applicant_name")}
            />
          </FormField>

          <FormField
            id="purpose"
            label="Keperluan & Tujuan Permohonan Surat"
            isRequired
            error={errors.purpose?.message}
          >
            <textarea
              id="purpose"
              rows={3}
              placeholder="Contoh: Pengajuan beasiswa PIP Kementerian Pendidikan..."
              className="w-full rounded-input border border-border-input bg-surface p-3 text-sm text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
              {...register("purpose")}
            />
          </FormField>

          {/* File Upload Section */}
          <div className="pt-2 border-t border-border space-y-2">
            <label className="text-sm font-medium text-text-foreground block">
              Lampiran Dokumen Persyaratan (Opsional)
            </label>
            <div className="flex items-center gap-3">
              <input
                id="file_upload"
                type="file"
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={handleFileChange}
                className="text-xs file:mr-3 file:py-2 file:px-3 file:rounded-input file:border-0 file:text-xs file:font-semibold file:bg-brand-primary-subtle file:text-brand-primary hover:file:bg-brand-primary-hover hover:file:text-white"
              />
            </div>
            {selectedFile && (
              <p className="text-xs text-semantic-success-fg">
                Berkas dipilih: {selectedFile.name} (
                {(selectedFile.size / 1024).toFixed(1)} KB)
              </p>
            )}
            {fileError && (
              <p className="text-xs text-semantic-danger-fg">{fileError}</p>
            )}
            <p className="text-[11px] text-text-muted">
              Maksimal 5 MB. Format resmi: Dokumen PDF atau Citra Scan
              (JPG/PNG). Berkas disimpan secara privat dan terenkripsi.
            </p>
          </div>

          <div className="flex justify-end gap-2 pt-4 border-t border-border">
            <Link to="/requests">
              <Button type="button" variant="secondary">
                Batal
              </Button>
            </Link>
            <Button
              type="submit"
              variant="primary"
              isLoading={submitMutation.isPending}
            >
              Kirim Permohonan
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
