import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { Download, FileText } from "lucide-react";

import { toast } from "sonner";
import { apiClient } from "@/lib/api-client";
import { Button } from "@/components/atoms/Button";
import { SearchBar } from "@/components/molecules/SearchBar";
import { DataTable, ColumnDef } from "@/components/organisms/DataTable";
import { formatDate } from "@/lib/formatters";

interface ArchiveDocumentItem {
  id: number;
  original_filename: string;
  file_size: number;
  mime_type: string;
  document_type?: string;
  request_id: number;
  request_number?: string;
  uploaded_by_name?: string;
  created_at: string;
}

export const DocumentArchivePage: React.FC = () => {
  const [search, setSearch] = React.useState("");
  const [downloadingId, setDownloadingId] = React.useState<number | null>(null);

  const { data, isLoading } = useQuery<{ items: ArchiveDocumentItem[] }>({
    queryKey: ["administration-documents"],
    queryFn: async () =>
      (await apiClient.get("/administration/documents")).data,
  });

  const handleDownload = async (doc: ArchiveDocumentItem) => {
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
      toast.success("Berkas arsip digital berhasil diunduh");
    } catch {
      toast.error("Gagal mengunduh berkas");
    } finally {
      setDownloadingId(null);
    }
  };

  const filteredItems = (data?.items || []).filter((item) => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      item.original_filename.toLowerCase().includes(q) ||
      (item.request_number && item.request_number.toLowerCase().includes(q)) ||
      (item.document_type && item.document_type.toLowerCase().includes(q))
    );
  });

  const columns: ColumnDef<ArchiveDocumentItem>[] = [
    {
      header: "Nama Dokumen Digital",
      cell: (d) => (
        <div className="flex items-center gap-2.5">
          <FileText className="h-4 w-4 text-brand-primary shrink-0" />
          <div>
            <span className="font-semibold text-text-foreground block">
              {d.original_filename}
            </span>
            <span className="text-[11px] text-text-muted">{d.mime_type}</span>
          </div>
        </div>
      ),
    },
    {
      header: "Tipe Dokumen",
      cell: (d) => (
        <span className="px-2 py-0.5 rounded-sm bg-surface-subtle border border-border text-xs font-medium">
          {d.document_type || "Lampiran"}
        </span>
      ),
    },
    {
      header: "No. Surat Terkait",
      cell: (d) => d.request_number || `#${d.request_id}`,
      className: "font-mono text-xs",
    },
    {
      header: "Ukuran",
      cell: (d) => `${(d.file_size / 1024).toFixed(1)} KB`,
      className: "tabular-nums text-xs",
    },
    {
      header: "Waktu Unggah",
      cell: (d) => (
        <span className="text-xs text-text-muted">
          {formatDate(d.created_at)}
        </span>
      ),
    },
    {
      header: "Aksi",
      className: "text-right",
      headerClassName: "text-right",
      cell: (d) => (
        <Button
          variant="secondary"
          size="sm"
          onClick={() => handleDownload(d)}
          isLoading={downloadingId === d.id}
          aria-label={`Unduh berkas ${d.original_filename}`}
        >
          <Download className="h-3.5 w-3.5 mr-1" />
          Unduh
        </Button>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-surface p-5 rounded-card border border-border shadow-sm flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-text-foreground">
            Katalog Arsip Dokumen Digital
          </h2>
          <p className="text-xs text-text-muted mt-0.5">
            Kumpulan seluruh berkas permohonan persuratan yang tersimpan secara
            terisolasi pada media penyimpanan privat.
          </p>
        </div>
        <SearchBar
          value={search}
          onChange={setSearch}
          placeholder="Cari nama dokumen atau no. surat..."
        />
      </div>

      <div className="bg-surface rounded-card border border-border shadow-sm overflow-hidden">
        <DataTable<ArchiveDocumentItem>
          columns={columns}
          data={filteredItems}
          isLoading={isLoading}
          keyExtractor={(item) => item.id}
          emptyTitle="Belum Ada Dokumen Terarsip"
          emptyDescription="Tidak ditemukan berkas dokumen pada sistem."
        />
      </div>
    </div>
  );
};
