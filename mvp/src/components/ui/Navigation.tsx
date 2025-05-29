"use client"

import { useState } from "react"
import { Button } from "../ui/Button"
import { Calculator, BookOpen, TrendingUp, FileText, Brain, Home, Menu, X } from "lucide-react"
import { cn } from "../../utils"
import { useNavigate, useLocation, Link } from "react-router-dom"

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: Home },
  { name: "Ejercicios", href: "/ejercicios", icon: BookOpen },
  { name: "Mi Progreso", href: "/progreso", icon: TrendingUp },
  { name: "Reportes", href: "/reportes", icon: FileText },
  { name: "Análisis IA", href: "/analisis", icon: Brain },
]

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false)
  const location = useLocation()
  const pathname = location.pathname
  const router = useNavigate()

  // No mostrar navegación en la página principal
  if (pathname === "/") {
    return null
  }

  const handleLogout = () => {
    // Aquí iría la lógica de logout
    router("/")
  }

  return (
    <nav className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center">
            <Calculator className="h-8 w-8 text-blue-600 mr-3" />
            <span className="text-xl font-bold">MathLearn</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => {
              const Icon = item.icon
              const isActive = pathname === item.href

              return (
                <Link key={item.name} to={item.href}>
                  <Button
                    variant={isActive ? "default" : "ghost"}
                    className={cn("flex items-center space-x-2", isActive && "bg-blue-600 text-white")}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.name}</span>
                  </Button>
                </Link>
              )
            })}
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/perfil" className="text-gray-600 hover:text-blue-600">
              ¡Hola, Juan!
            </Link>
            <Button variant="outline" className="text-sm" onClick={handleLogout}>
              Cerrar Sesión
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button variant="ghost" className="text-sm" onClick={() => setIsOpen(!isOpen)}>
              {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4 border-t">
            <div className="space-y-2">
              {navigation.map((item) => {
                const Icon = item.icon
                const isActive = pathname === item.href

                return (
                  <Link key={item.name} to={item.href}>
                    <Button
                      variant={isActive ? "default" : "ghost"}
                      className={cn(
                        "w-full justify-start flex items-center space-x-2",
                        isActive && "bg-blue-600 text-white",
                      )}
                      onClick={() => setIsOpen(false)}
                    >
                      <Icon className="h-4 w-4" />
                      <span>{item.name}</span>
                    </Button>
                  </Link>
                )
              })}
              <div className="pt-4 border-t">
                <Button variant="outline" className="sm-text w-full" onClick={handleLogout}>
                  Cerrar Sesión
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
