import { cn } from "../../utils";

import React from "react"

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          "w-full px-3 py-2 border rounded shadow-sm border-transparent focus:outline-none focus:ring-2 focus:ring-gray-500",
          className
        )}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"