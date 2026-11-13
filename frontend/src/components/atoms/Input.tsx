import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  hasError?: boolean;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, hasError, disabled, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-input border bg-surface px-3 py-2 text-sm text-text-foreground transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus disabled:cursor-not-allowed disabled:bg-surface-muted disabled:text-text-disabled",
          hasError
            ? "border-semantic-danger-fg focus-visible:ring-semantic-danger-fg"
            : "border-border-input hover:border-text-muted focus-visible:border-brand-primary",
          className,
        )}
        ref={ref}
        disabled={disabled}
        aria-invalid={hasError ? "true" : "false"}
        {...props}
      />
    );
  },
);

Input.displayName = "Input";
