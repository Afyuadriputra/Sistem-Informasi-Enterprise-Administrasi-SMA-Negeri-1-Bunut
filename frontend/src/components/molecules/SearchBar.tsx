import * as React from "react";
import { Search, X } from "lucide-react";
import { Input } from "@/components/atoms/Input";
import { cn } from "@/lib/utils";

export interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  placeholder = "Cari data...",
  className,
}) => {
  return (
    <div
      className={cn("relative flex items-center w-full max-w-sm", className)}
    >
      <Search
        className="absolute left-3 h-4 w-4 text-text-muted pointer-events-none"
        aria-hidden="true"
      />
      <Input
        type="search"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="pl-9 pr-9"
      />
      {value && (
        <button
          type="button"
          onClick={() => onChange("")}
          className="absolute right-3 p-1 rounded-sm text-text-muted hover:text-text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-border-focus"
          aria-label="Bersihkan pencarian"
        >
          <X className="h-4 w-4" aria-hidden="true" />
        </button>
      )}
    </div>
  );
};
