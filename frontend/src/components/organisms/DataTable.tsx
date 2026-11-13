import * as React from "react";
import { Skeleton } from "@/components/atoms/Skeleton";
import { EmptyState } from "@/components/molecules/EmptyState";
import { cn } from "@/lib/utils";

export interface ColumnDef<T> {
  header: string;
  accessorKey?: keyof T;
  cell?: (item: T, index: number) => React.ReactNode;
  className?: string;
  headerClassName?: string;
}

export interface DataTableProps<T> {
  columns: ColumnDef<T>[];
  data: T[];
  isLoading?: boolean;
  emptyTitle?: string;
  emptyDescription?: string;
  keyExtractor: (item: T, index: number) => string | number;
  onRowClick?: (item: T) => void;
  className?: string;
}

export function DataTable<T>({
  columns,
  data,
  isLoading = false,
  emptyTitle,
  emptyDescription,
  keyExtractor,
  onRowClick,
  className,
}: DataTableProps<T>) {
  if (isLoading) {
    return (
      <div
        className={cn(
          "w-full overflow-x-auto rounded-card border border-border bg-surface",
          className,
        )}
      >
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-subtle border-b border-border text-xs uppercase text-text-muted">
            <tr>
              {columns.map((col, idx) => (
                <th
                  key={idx}
                  className={cn("px-4 py-3 font-semibold", col.headerClassName)}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {Array.from({ length: 5 }).map((_, rIdx) => (
              <tr key={rIdx}>
                {columns.map((_, cIdx) => (
                  <td key={cIdx} className="px-4 py-3">
                    <Skeleton className="h-4 w-full max-w-[120px]" />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div
        className={cn(
          "w-full rounded-card border border-border bg-surface",
          className,
        )}
      >
        <EmptyState title={emptyTitle} description={emptyDescription} />
      </div>
    );
  }

  return (
    <div
      className={cn(
        "w-full overflow-x-auto rounded-card border border-border bg-surface shadow-sm",
        className,
      )}
    >
      <table className="w-full text-left text-sm">
        <thead className="bg-surface-subtle border-b border-border text-xs uppercase text-text-muted font-semibold tracking-wider">
          <tr>
            {columns.map((col, idx) => (
              <th key={idx} className={cn("px-4 py-3.5", col.headerClassName)}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-border">
          {data.map((item, rowIdx) => (
            <tr
              key={keyExtractor(item, rowIdx)}
              onClick={() => onRowClick && onRowClick(item)}
              className={cn(
                "transition-colors hover:bg-surface-subtle",
                onRowClick && "cursor-pointer",
                rowIdx % 2 === 1 && "bg-surface-subtle/50",
              )}
            >
              {columns.map((col, colIdx) => (
                <td
                  key={colIdx}
                  className={cn(
                    "px-4 py-3 text-text-foreground",
                    col.className,
                  )}
                >
                  {col.cell
                    ? col.cell(item, rowIdx)
                    : col.accessorKey
                      ? String(item[col.accessorKey] ?? "-")
                      : "-"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
