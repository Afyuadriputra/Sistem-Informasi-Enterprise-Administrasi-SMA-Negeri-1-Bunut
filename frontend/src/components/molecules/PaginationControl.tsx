import * as React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/atoms/Button";
import { cn } from "@/lib/utils";

export interface PaginationControlProps {
  currentPage: number;
  pageSize: number;
  totalItems: number;
  onPageChange: (page: number) => void;
  className?: string;
}

export const PaginationControl: React.FC<PaginationControlProps> = ({
  currentPage,
  pageSize,
  totalItems,
  onPageChange,
  className,
}) => {
  const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));
  const startItem = totalItems === 0 ? 0 : (currentPage - 1) * pageSize + 1;
  const endItem = Math.min(currentPage * pageSize, totalItems);

  return (
    <div
      className={cn(
        "flex flex-col sm:flex-row items-center justify-between gap-3 px-4 py-3 bg-surface border-t border-border text-sm text-text-muted",
        className,
      )}
    >
      <div>
        Menampilkan{" "}
        <span className="font-medium text-text-foreground">{startItem}</span> -{" "}
        <span className="font-medium text-text-foreground">{endItem}</span> dari{" "}
        <span className="font-medium text-text-foreground">{totalItems}</span>{" "}
        data
      </div>
      <div className="flex items-center gap-2">
        <Button
          variant="secondary"
          size="sm"
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage <= 1}
          aria-label="Halaman sebelumnya"
        >
          <ChevronLeft className="h-4 w-4 mr-1" aria-hidden="true" />
          Sebelumnya
        </Button>
        <span className="text-xs font-medium px-2">
          Halaman {currentPage} dari {totalPages}
        </span>
        <Button
          variant="secondary"
          size="sm"
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage >= totalPages}
          aria-label="Halaman berikutnya"
        >
          Berikutnya
          <ChevronRight className="h-4 w-4 ml-1" aria-hidden="true" />
        </Button>
      </div>
    </div>
  );
};
