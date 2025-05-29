"use client"
import React, { createContext, useContext, useEffect, useState } from "react"

type Theme = "light" | "dark" | "system"

interface ThemeProviderProps {
  children: React.ReactNode
  attribute?: string
  defaultTheme?: Theme
  enableSystem?: boolean
  disableTransitionOnChange?: boolean
}

const ThemeContext = createContext<{ theme: Theme; setTheme: (t: Theme) => void }>({
  theme: "light",
  setTheme: () => {},
})

export function useTheme() {
  return useContext(ThemeContext)
}

export function ThemeProvider({
  children,
  attribute = "class",
  defaultTheme = "light",
  enableSystem = true,
  disableTransitionOnChange = false,
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(defaultTheme)

  useEffect(() => {
    let appliedTheme = theme
    if (enableSystem && theme === "system") {
      const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches
      appliedTheme = isDark ? "dark" : "light"
    }
    if (attribute === "class") {
      document.documentElement.classList.remove("light", "dark")
      document.documentElement.classList.add(appliedTheme)
    } else {
      document.documentElement.setAttribute(attribute, appliedTheme)
    }
    // Optional: disable transition on theme change
    if (disableTransitionOnChange) {
      document.documentElement.classList.add("notransition")
      setTimeout(() => {
        document.documentElement.classList.remove("notransition")
      }, 0)
    }
  }, [theme, attribute, enableSystem, disableTransitionOnChange])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}