import * as React from "react"
import { cn } from "../../utils"

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  children: React.ReactNode
}

export function Select({ children, className, ...props }: SelectProps) {
  return (
    <select
      className={cn(
        "block w-full rounded border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-blue-500 focus:outline-none",
        className
      )}
      {...props}
    >
      {children}
    </select>
  )
}

interface SelectTriggerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode
}

export function SelectTrigger({ children, className, ...props }: SelectTriggerProps) {
  return (
    <div
      className={cn(
        "flex items-center justify-between rounded border border-gray-300 bg-white px-3 py-2 text-sm cursor-pointer",
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

interface SelectValueProps {
  placeholder?: string
  value?: string
  children?: React.ReactNode
}

export function SelectValue({ placeholder, value, children }: SelectValueProps) {
  return (
    <span className="text-gray-700">
      {value ? value : placeholder}
      {children}
    </span>
  )
}

interface SelectContentProps {
  children: React.ReactNode
  className?: string
}

export function SelectContent({ children, className }: SelectContentProps) {
  return (
    <div className={cn("mt-1 rounded border border-gray-300 bg-white shadow-lg z-10", className)}>
      {children}
    </div>
  )
}

interface SelectItemProps extends React.OptionHTMLAttributes<HTMLOptionElement> {
  children: React.ReactNode
}

export function SelectItem({ children, className, ...props }: SelectItemProps) {
  return (
    <option className={cn(className)} {...props}>
      {children}
    </option>
  )
}