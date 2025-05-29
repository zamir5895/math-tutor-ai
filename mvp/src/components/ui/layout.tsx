// layout.tsx
import React from "react"
import { ThemeProvider } from "./ThemeProvider"
import { Navigation } from "./Navigation"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
      <div className="min-h-screen flex flex-col bg-white dark:bg-gray-900">
        <Navigation />
        <main className="flex-1">{children}</main>
      </div>
    </ThemeProvider>
  )
}