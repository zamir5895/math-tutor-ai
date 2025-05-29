import React from "react"
import clsx from "clsx"

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  color?: "green" | "orange" | "red" | "blue" | "gray"
  variant?: "solid" | "outline" | "secondary"
  children: React.ReactNode
}

export function Badge({
  color = "gray",
  variant = "solid",
  className,
  children,
  ...props
}: BadgeProps) {
  const base =
    "inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold transition-colors";
  const colorMap: Record<
    NonNullable<BadgeProps["variant"]>,
    Record<NonNullable<BadgeProps["color"]>, string>
  > = {
    solid: {
      green: "bg-emerald-500 text-white",
      orange: "bg-amber-500 text-white",
      red: "bg-pink-600 text-white",
      blue: "bg-blue-500 text-white",
      gray: "bg-gray-600 text-white",
    },
    outline: {
      green: "border border-emerald-500 text-emerald-500 bg-transparent",
      orange: "border border-amber-500 text-amber-500 bg-transparent",
      red: "border border-pink-600 text-pink-600 bg-transparent",
      blue: "border border-blue-500 text-blue-500 bg-transparent",
      gray: "border border-gray-600 text-gray-600 bg-transparent",
    },
    secondary: {
      green: "bg-green-100 text-green-800",
      orange: "bg-orange-100 text-orange-800",
      red: "bg-red-100 text-red-800",
      blue: "bg-blue-100 text-blue-800",
      gray: "bg-gray-200 text-gray-800",
    },
  };

  return (
    <span
      className={clsx(
        base,
        colorMap[variant][color],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}