import * as React from "react";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface SpinnerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg";
  label?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = "md",
  label = "Memuat data...",
  className,
  ...props
}) => {
  const sizeClass = {
    sm: "h-4 w-4",
    md: "h-6 w-6",
    lg: "h-8 w-8",
  }[size];

  return (
    <div
      role="status"
      className={cn(
        "inline-flex items-center justify-center text-brand-primary",
        className,
      )}
      {...props}
    >
      <Loader2 className={cn("animate-spin", sizeClass)} aria-hidden="true" />
      <span className="sr-only">{label}</span>
    </div>
  );
};
