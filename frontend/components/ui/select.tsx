import * as React from "react";
import { cn } from "@/lib/utils";

export interface SelectProps
  extends React.SelectHTMLAttributes<HTMLSelectElement> {}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, ...props }, ref) => {
    return (
      <select
        ref={ref}
        className={cn(
          "w-full rounded-2xl border border-slate-200 bg-white/90 px-4 py-2 text-sm text-slate-800 shadow-sm outline-none transition focus:border-slate-400",
          className,
        )}
        {...props}
      />
    );
  },
);
Select.displayName = "Select";

export { Select };
