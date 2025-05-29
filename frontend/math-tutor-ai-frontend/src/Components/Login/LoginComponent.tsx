import { BookOpen, GraduationCap, School } from 'lucide-react'
import React, { useState, useEffect } from 'react'
import { Button } from '../UI/Buttom'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../UI/Card'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@radix-ui/react-tabs'
import { Input } from '../UI/Input'
import { Label } from '../UI/label'
import {  Link } from 'react-router-dom'
import { login } from '../../Service/Auth/AuthService'
import LogoMatemix from '../../assets/MateMix_Logo.png'

const LoginComponent = () => {
    const [loginData, setLoginData] = useState({email:"", password:""});
    const [showPassword, setShowPassword] = useState(false);
    const colorHex = ["#10B981", "#3B82F6", "#D8315B", "#FFA000"];
    const [colorIndex, setColorIndex] = useState(0);

    useEffect(() => {
      const interval = setInterval(() => {
        setColorIndex((prev) => (prev + 1) % colorHex.length);
      }, 1000);
      return () => clearInterval(interval);
    }, [colorHex.length]);
    
    const handleLoginChange = (e:React.ChangeEvent<HTMLInputElement>)=>{
        const {name, value } = e.target;
        setLoginData((prev)=>({...prev, [name]:value}));
    }
    const HandleLoginSubmit = async(e: React.FormEvent<HTMLFormElement>)=> {
        e.preventDefault();
        console.log("iniciando sesison ", loginData);
        try{
            console.log("Inicianso")
            const response = await login(loginData);
            console.log(response);
            if(response.status === 200){
                console.log("Exito")
            }
        }catch(error){
            console.log("error " , error)
        }
    }
    
  
return (
    <div className="min-h-screen flex flex-col bg-white">
      <header className="flex items-center px-6 py-4 border-b">
        <img src={LogoMatemix} alt="Matemix Logo" className="h-8 w-auto" />
      </header>
      <main className="flex flex-1 items-center justify-center bg-gray-50">
          <div className="w-full max-w-md">          
        
          <Card className="w-full max-w-md mx-auto">
            <CardHeader className="flex flex-col items-center gap-2">
              <div className="bg-white p-3 rounded-full shadow-sm">
                <School className="h-10 w-10" style={{ color: colorHex[colorIndex] }} />
              </div>
              <CardTitle className="mt-4">Iniciar Sesión</CardTitle>
              <CardDescription>Selecciona tu tipo de usuario e ingresa tus credenciales</CardDescription>
            </CardHeader>
            <CardContent className="flex items-center">
              <Tabs defaultValue="estudiante" className="w-full">
                  <TabsList className="flex justify-center gap-4 mb-6">
                      <TabsTrigger 
                        value="estudiante" 
                        className="group flex flex-col items-center w-36 px-4 py-3 border border-gray-300 rounded-xl shadow-sm transition-all duration-300 
                              data-[state=active]:bg-blue-100 data-[state=active]:border-blue-500 data-[state=active]:shadow-md">
                        <div className="bg-blue-200 group-data-[state=active]:bg-blue-500 text-blue-800 group-data-[state=active]:text-white p-2 rounded-full transition">
                          <GraduationCap className="h-5 w-5" />
                        </div>
                        <span>Estudiante</span>
                      </TabsTrigger>
                      <TabsTrigger 
                        value="profesor" 
                        className="group flex flex-col items-center w-36 px-4 py-3 border border-gray-300 rounded-xl shadow-sm transition-all duration-300 
                              data-[state=active]:bg-green-100 data-[state=active]:border-green-500 data-[state=active]:shadow-md">
                        <div className="bg-green-200 group-data-[state=active]:bg-green-500 text-green-800 group-data-[state=active]:text-white p-2 rounded-full transition">
                          <BookOpen className="h-5 w-5" />
                        </div>
                        <span>Profesor</span>
                      </TabsTrigger>
                  </TabsList>

                <TabsContent value="estudiante">
                  <form onSubmit={HandleLoginSubmit}>
                    <div className="grid gap-4">
                      <div className="grid gap-2 relative">
                        <Label htmlFor="email-estudiante">Correo electrónico</Label>
                        <Input id="email" type="email" name="email" placeholder="estudiante@ejemplo.com" onChange={handleLoginChange} className="rounded-[80px]"/>
                      </div>
                      <div className="grid gap-2 relative">
                        <div className="flex items-center justify-between">
                          <Label htmlFor="password-estudiante">Contraseña</Label>
                          <Link to="#" className="text-sm text-blue-500 hover:underline">
                            ¿Olvidaste tu contraseña?
                          </Link>
                        </div>
                        <Input id="password" 
                        type={showPassword ? "text" : "password"}
                        name="password" 
                        onChange={handleLoginChange}
                        className='rounded-[80px]'/>
                          <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute top-2/3 right-3 w-16 -translate-y-1/2 flex items-center justify-center text-sm text-blue-500 hover:underline"
                      >
                          {showPassword ? "Ocultar" : "Mostrar"}
                      </button>
                      </div>
                      <Button variant="submit" className="w-full bg-blue-500 text-white hover:bg-blue-500 rounded-[80px]">
                        Iniciar sesión
                      </Button>
                    </div>
                  </form>
                </TabsContent>

                <TabsContent value="profesor">
                  <form onSubmit={HandleLoginSubmit}>
                    <div className="grid gap-4 relative">
                      <div className="grid gap-2 relative">
                        <Label htmlFor="email-profesor">Correo electrónico</Label>
                        <Input id="email" 
                        type="email" 
                        name="email"
                        placeholder="profesor@ejemplo.com" onChange={handleLoginChange} className="rounded-[80px]"/>
                      </div>
                      <div className="grid gap-2 relative" >
                        <div className="flex items-center justify-between">
                          <Label htmlFor="password-profesor">Contraseña</Label>
                          <Link to="#" className="text-sm text-blue-500 hover:underline">
                            ¿Olvidaste tu contraseña?
                          </Link>
                        </div>
                        <Input id="contraseña" name="password" type={showPassword ? "text" : "password"} onChange={handleLoginChange} className="rounded-[80px]"/>
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute top-2/3 right-3 w-16 -translate-y-1/2 flex items-center justify-center text-sm text-blue-500 hover:underline"
                      >
                          {showPassword ? "Ocultar" : "Mostrar"}
                        </button>
                      </div>
                      <Button variant="submit" className="w-full bg-blue-500 text-white hover:bg-blue-500 rounded-[80px]">
                        Iniciar sesión
                      </Button>
                    </div>
                  </form>
                </TabsContent>
              </Tabs>
            </CardContent>
            <CardFooter className="flex flex-col gap-4">
              <div className="text-center text-sm text-gray-600">
                ¿No tienes una cuenta?{" "}
                <Link to="#" className="text-blue-500 hover:underline">
                  Regístrate aquí
                </Link>
              </div>
              <div className="text-center text-xs text-gray-500">
                Al iniciar sesión, aceptas nuestros{" "}
                <Link to="#" className="text-blue-500 hover:underline">
                  Términos de servicio
                </Link>{" "}
                y{" "}
                <Link to="#" className="text-blue-500 hover:underline">
                  Política de privacidad
                </Link>
              </div>
            </CardFooter>
          </Card>
        </div>
      </main>
    </div>
  )
}


export default LoginComponent