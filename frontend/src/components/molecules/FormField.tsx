import * as React from "react";
import { Label } from "@/components/atoms/Label";
import { cn } from "@/lib/utils";

export interface FormFieldProps extends React.HTMLAttributes<HTMLDivElement> {
  id: string;
  label: string;
  isRequired?: boolean;
  error?: string;
  helperText?: string;
}

export const FormField: React.FC<FormFieldProps> = ({
  id,
  label,
  isRequired,
  error,
  helperText,
  children,
  className,
  ...props
}) => {
  return (
    <div className={cn("space-y-1.5", className)} {...props}>
      <Label htmlFor={id} isRequired={isRequired}>
        {label}
      </Label>
      {children}
      {error ? (
        <p
          id={`${id}-error`}
          className="text-xs text-semantic-danger-fg font-medium"
          role="alert"
        >
          {error}
        </p>
      ) : helperText ? (
        <p id={`${id}-helper`} className="text-xs text-text-muted">
          {helperText}
        </p>
      ) : null}
    </div>
  );
};
