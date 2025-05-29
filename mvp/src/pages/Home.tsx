"use client"

import { useState } from "react"
import { Button } from "../components/ui/Button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { Input } from "../components/ui/Input"
import { Label } from "../components/ui/Label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/Tabs"
import { BookOpen, Calculator, TrendingUp, Users } from "lucide-react"
import { useNavigate } from "react-router-dom"

export default function HomePage() {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async () => {
    setIsLoading(true)
    // Simular llamada a API
    setTimeout(() => {
      setIsLoading(false)
      navigate("/dashboard")
    }, 1000)
  }

  const handleRegister = async () => {
    setIsLoading(true)
    // Simular llamada a API
    setTimeout(() => {
      setIsLoading(false)
      navigate("/dashboard")
    }, 1000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Calculator className="h-12 w-12 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">MathLearn</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Plataforma inteligente para aprender y reforzar matemáticas de forma personalizada
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <Card>
            <CardHeader className="text-center">
              <BookOpen className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <CardTitle>Ejercicios Personalizados</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">Ejercicios adaptados a tu nivel y dificultades específicas</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <TrendingUp className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <CardTitle>Seguimiento de Progreso</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">Monitorea tu avance y identifica áreas de mejora</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <Users className="h-8 w-8 text-purple-600 mx-auto mb-2" />
              <CardTitle>Análisis Inteligente</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">IA que analiza patrones y sugiere mejoras</p>
            </CardContent>
          </Card>
        </div>

        {/* Auth Forms */}
        <div className="max-w-md mx-auto">
          <Tabs defaultValue="login" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
                         <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger
                value="login"
                className="
                  w-full
                  data-[state=active]:bg-white
                  data-[state=active]:text-black
                  data-[state=active]:shadow-2xl
                  data-[state=active]:text-base
                  py-3
                  rounded-md text-sm font-medium
                  transition-colors duration-300
                  bg-gray-200 text-gray-700 hover:bg-gray-300
                "
              >
                Iniciar Sesión
              </TabsTrigger>
              <TabsTrigger
                value="register"
                className="
                  w-full
                  data-[state=active]:bg-white
                  data-[state=active]:text-black
                  data-[state=active]:shadow-2xl
                  data-[state=active]:text-base
                  py-3
                  rounded-md text-sm font-medium
                  transition-colors duration-300
                  bg-gray-200 text-gray-700 hover:bg-gray-300
                "
              >
                Registrarse
              </TabsTrigger>
            </TabsList>
            </TabsList>

            <TabsContent value="login">
              <Card>
                <CardHeader>
                  <CardTitle>Iniciar Sesión</CardTitle>
                  <CardDescription>Ingresa tus credenciales para acceder</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" placeholder="tu@email.com" />
                  </div>
                  <div>
                    <Label htmlFor="password">Contraseña</Label>
                    <Input id="password" type="password" />
                  </div>
                  <Button className="w-full" onClick={handleLogin} disabled={isLoading}>
                    {isLoading ? "Iniciando sesión..." : "Iniciar Sesión"}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="register">
              <Card>
                <CardHeader>
                  <CardTitle>Crear Cuenta</CardTitle>
                  <CardDescription>Regístrate para comenzar a aprender</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="nombre">Nombre Completo</Label>
                    <Input id="nombre" placeholder="Juan Pérez" />
                  </div>
                  <div>
                    <Label htmlFor="email-reg">Email</Label>
                    <Input id="email-reg" type="email" placeholder="juan.perez@email.com" />
                  </div>
                  <div>
                    <Label htmlFor="password-reg">Contraseña</Label>
                    <Input id="password-reg" type="password" />
                  </div>
                  <Button className="w-full" onClick={handleRegister} disabled={isLoading}>
                    {isLoading ? "Creando cuenta..." : "Crear Cuenta"}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Footer */}
        <div className="text-center mt-16 text-gray-500">
          <p>&copy; 2024 MathLearn. Todos los derechos reservados.</p>
        </div>
      </div>
    </div>
  )
}
