import * as React from "react";
import { AlertCircle, RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/atoms/Button";

export interface ErrorStateProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  message?: string;
  requestId?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = "Gagal Memuat Data",
  message = "Terjadi kendala saat menghubungkan ke sistem sekolah. Silakan coba kembali.",
  requestId,
  onRetry,
  className,
  ...props
}) => {
  return (
    <div
      role="alert"
      className={cn(
        "flex flex-col items-center justify-center p-8 text-center bg-semantic-danger-bg border border-semantic-danger-border rounded-card my-4",
        className,
      )}
      {...props}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-panel bg-red-100 text-semantic-danger-fg mb-3">
        <AlertCircle className="h-6 w-6" aria-hidden="true" />
      </div>
      <h3 className="text-base font-semibold text-semantic-danger-fg mb-1">
        {title}
      </h3>
      <p className="text-sm text-text-foreground max-w-md mb-2">{message}</p>
      {requestId && (
        <p className="text-xs text-text-muted font-mono mb-4">
          ID Permintaan: <span className="select-all">{requestId}</span>
        </p>
      )}
      {onRetry && (
        <Button variant="danger" size="sm" onClick={onRetry}>
          <RefreshCw className="mr-2 h-4 w-4" aria-hidden="true" />
          Coba Lagi
        </Button>
      )}
    </div>
  );
};
