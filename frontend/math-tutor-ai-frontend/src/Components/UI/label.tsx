import { cn } from "../../Lib/Util";
import React from "react"

export const Label = ({ className, ...props }: React.LabelHTMLAttributes<HTMLLabelElement>) => {
  return (
    <label className={cn("text-sm font-medium text-gray-700", className)} {...props} />
  )
}