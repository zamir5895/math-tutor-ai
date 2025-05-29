import React from "react"
import clsx from "clsx"

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number
  color?: "green" | "orange" | "red" | "blue" | "gray"
  className?: string
}

export function Progress({ value, color = "blue", className, ...props }: ProgressProps) {
  const bgMap: Record<string, string> = {
    green: "bg-emerald-500",
    orange: "bg-orange-600",
    red: "bg-pink-600",
    blue: "bg-blue-500",
    gray: "bg-gray-600",
  }

  return (
    <div className={clsx("w-full bg-gray-200 rounded h-2", className)} {...props}>
      <div
        className={clsx("h-2 rounded transition-all duration-300", bgMap[color])}
        style={{ width: `${value}%` }}
      />
    </div>
  )
}