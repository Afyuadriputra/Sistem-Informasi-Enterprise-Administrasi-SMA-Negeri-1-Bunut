import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

export const buttonVariants = cva(
  "inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 select-none active:scale-[0.98]",
  {
    variants: {
      variant: {
        primary:
          "bg-brand-primary text-white hover:bg-brand-primary-hover shadow-sm",
        accent:
          "bg-brand-accent text-white hover:bg-brand-accent-hover shadow-sm",
        secondary:
          "bg-white text-text-foreground border border-border hover:bg-surface-subtle shadow-sm",
        outline:
          "border border-brand-primary text-brand-primary hover:bg-brand-primary-subtle",
        danger: "bg-semantic-danger-fg text-white hover:bg-red-800 shadow-sm",
        ghost: "text-text-foreground hover:bg-surface-subtle",
        link: "text-brand-primary underline-offset-4 hover:underline p-0 h-auto",
      },
      size: {
        sm: "h-8 px-3 text-xs rounded-button min-h-[36px]",
        md: "h-10 px-4 text-sm rounded-button min-h-[40px]",
        lg: "h-12 px-6 text-base rounded-button min-h-[44px]",
        icon: "h-10 w-10 min-h-[40px] min-w-[40px] rounded-button",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  },
);

export interface ButtonProps
  extends
    React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { className, variant, size, isLoading, children, disabled, ...props },
    ref,
  ) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size, className }))}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <Loader2 className="mr-2 h-4 w-4 animate-spin" aria-hidden="true" />
        )}
        {children}
      </button>
    );
  },
);

Button.displayName = "Button";
