import * as React from "react";
import { cn } from "@/lib/utils";

export interface MetricCardProps extends React.HTMLAttributes<HTMLDivElement> {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  badge?: React.ReactNode;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  badge,
  className,
  ...props
}) => {
  return (
    <div
      className={cn(
        "bg-surface border border-border rounded-card p-5 shadow-sm transition-shadow hover:shadow-md flex flex-col justify-between",
        className,
      )}
      {...props}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <span className="text-sm font-medium text-text-muted">{title}</span>
        {icon && (
          <div className="p-2 rounded-panel bg-brand-primary-subtle text-brand-primary">
            {icon}
          </div>
        )}
      </div>
      <div>
        <div className="text-2xl font-bold tracking-tight text-text-foreground tabular-nums">
          {value}
        </div>
        <div className="flex items-center justify-between mt-1 text-xs text-text-muted">
          {subtitle && <span>{subtitle}</span>}
          {badge && <span>{badge}</span>}
        </div>
      </div>
    </div>
  );
};
