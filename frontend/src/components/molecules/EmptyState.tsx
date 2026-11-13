import * as React from "react";
import { Inbox } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/atoms/Button";

export interface EmptyStateProps extends React.HTMLAttributes<HTMLDivElement> {
  icon?: React.ReactNode;
  title?: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title = "Belum Ada Data",
  description = "Data yang dicari belum tersedia atau belum dimasukkan ke dalam sistem.",
  actionLabel,
  onAction,
  className,
  ...props
}) => {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center p-8 text-center bg-surface border border-dashed border-border rounded-card my-4",
        className,
      )}
      {...props}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-panel bg-brand-primary-subtle text-brand-primary mb-3">
        {icon || <Inbox className="h-6 w-6" aria-hidden="true" />}
      </div>
      <h3 className="text-base font-semibold text-text-foreground mb-1">
        {title}
      </h3>
      <p className="text-sm text-text-muted max-w-sm mb-4">{description}</p>
      {actionLabel && onAction && (
        <Button variant="primary" size="sm" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};
