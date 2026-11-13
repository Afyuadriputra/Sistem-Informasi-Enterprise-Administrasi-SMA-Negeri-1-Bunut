import * as React from "react";
import { cn } from "@/lib/utils";

export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  isRequired?: boolean;
}

export const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, isRequired, children, ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={cn(
          "text-sm font-medium leading-none text-text-foreground select-none flex items-center gap-1",
          className,
        )}
        {...props}
      >
        {children}
        {isRequired && (
          <span
            className="text-semantic-danger-fg text-xs font-bold"
            aria-hidden="true"
          >
            *
          </span>
        )}
      </label>
    );
  },
);

Label.displayName = "Label";
