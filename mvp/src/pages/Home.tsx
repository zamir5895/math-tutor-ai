"use client"

import { useState } from "react"
import { Button } from "../components/ui/Button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { Input } from "../components/ui/Input"
import { Label } from "../components/ui/Label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/Tabs"
import { BookOpen, TrendingUp, Users } from "lucide-react"
import { useNavigate } from "react-router-dom"
<<<<<<< HEAD
import { authService } from "../Service/api"
=======
import logotipo from "../assets/Group 11 (1).svg"
>>>>>>> e5d365901ae3b5466c3d3bae4eb6b21afabfcaef

export default function HomePage() {
  const navigate = useNavigate()
  const [isLoading, setIsLoading] = useState(false)
  const [loginData, setLoginData] = useState({
    username: "",
    password: "",})
    const [registerData, setRegisterData] = useState({
    nombre: "",
    username: "",
    password: "",
    })

  const handleLoginData = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLoginData({ ...loginData, [e.target.id]: e.target.value })
  }

  const handleRegisterData = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.id === "nombre") {
      setRegisterData({ ...registerData, nombre: e.target.value })
    } else if (e.target.id === "username-reg") {
        setRegisterData({ ...registerData, username: e.target.value })
        }
    else if (e.target.id === "password-reg") {
      setRegisterData({ ...registerData, password: e.target.value })
    }
  }

  const handleLogin = async () => {
    setIsLoading(true)
    try{
        const response = await authService.login({
            username: loginData.username,
            password: loginData.password
        })
        if (response){
            navigate("/dashboard")
        }else{
            alert("Credenciales incorrectas")
        }
    }catch {
        alert("Error en la autenticación")
    }finally {
        setIsLoading(false)
    }
  }

  const handleRegister = async () => {
    setIsLoading(true)
    try{
        const response = await authService.signup({
            nombre: registerData.nombre,
            username: registerData.username,
            password: registerData.password
        })
        if (response){
            navigate("/dashboard")
        }else{
            alert("Error en el registro")
        }
    }catch {
        alert("Error en el registro")
    }finally {
        setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <img src={logotipo} alt="MathLearn Logo" className="h-8 w-8 mr-2" />
            <h1 className="text-4xl font-bold text-black">Matemix</h1>
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
                    <Label htmlFor="username">Username</Label>
                    <Input id="username" type="text" placeholder="MYUSER" onChange={handleLoginData} />
                  </div>
                  <div>
                    <Label htmlFor="password">Contraseña</Label>
                    <Input id="password" type="password" onChange={handleLoginData} />
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
                    <Input id="nombre" placeholder="Juan Pérez" onChange={handleRegisterData} />
                  </div>
                  <div>
                    <Label htmlFor="text-reg">Username</Label>
                    <Input id="username-reg" type="text" placeholder="MYUSERNAME" onChange={handleRegisterData}/>
                  </div>
                  <div>
                    <Label htmlFor="password-reg">Contraseña</Label>
                    <Input id="password-reg" type="password" onChange={handleRegisterData} />
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
