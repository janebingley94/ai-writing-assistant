import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "ghost" | "outline";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-full px-4 py-2 text-sm font-semibold transition",
          variant === "default" &&
            "bg-slate-900 text-white hover:bg-slate-800",
          variant === "ghost" && "bg-transparent text-slate-700 hover:bg-slate-100",
          variant === "outline" &&
            "border border-slate-300 text-slate-700 hover:bg-slate-100",
          className,
        )}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";

export { Button };
