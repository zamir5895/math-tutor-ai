import { BookOpen, GraduationCap, School } from 'lucide-react'
import React, { useState } from 'react'
import { Button } from '../UI/Buttom'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../UI/Card'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@radix-ui/react-tabs'
import { Input } from '../UI/Input'
import { Label } from '../UI/label'
import {  Link } from 'react-router-dom'
import { login } from '../../Service/Auth/AuthService'


const LoginComponent = () => {
    const [loginData, setLoginData] = useState({email:"", password:""});
    const [showPassword, setShowPassword] = useState(false);
    
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
    <div className="w-full min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-50 to-blue-100 p-4">
      <div className="w-full max-w-md">
        <div className="flex justify-center mb-6">
          <div className="bg-white p-3 rounded-full shadow-sm">
            <School className="h-10 w-10 text-blue-600" />
          </div>
        </div>
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-2">Matemix</h1>
        <p className="text-center text-gray-600 mb-6">Accede a tu cuenta para continuar</p>
        <Card>
          <CardHeader>
            <CardTitle>Iniciar Sesión</CardTitle>
            <CardDescription>Selecciona tu tipo de usuario e ingresa tus credenciales</CardDescription>
          </CardHeader>
          <CardContent className="flex items-center">
            <Tabs defaultValue="estudiante" className="w-full">
                <TabsList className="flex justify-center mb-4 bg-gray-50">
                    <TabsTrigger 
                      value="estudiante" 
                      className="flex items-center gap-2 w-40 data-[state=active]:text-black data-[state=active]:bg-white rounded-md px-3 py-1">
                      <GraduationCap className="h-4 w-4" />
                      <span>Estudiante</span>
                    </TabsTrigger>
                    <TabsTrigger 
                      value="profesor" 
                      className="flex items-center gap-2 w-40 data-[state=active]:text-black data-[state=active]:bg-white rounded-md px-3 py-1">
                      <BookOpen className="h-4 w-4" />
                      <span>Profesor</span>
                    </TabsTrigger>
                </TabsList>

              <TabsContent value="estudiante">
                <form onSubmit={HandleLoginSubmit}>
                  <div className="grid gap-4">
                    <div className="grid gap-2">
                      <Label htmlFor="email-estudiante">Correo electrónico</Label>
                      <Input id="email" type="email" name="email" placeholder="estudiante@ejemplo.com" onChange={handleLoginChange}/>
                    </div>
                    <div className="grid gap-2 relative">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="password-estudiante">Contraseña</Label>
                        <Link to="#" className="text-sm text-blue-600 hover:underline">
                          ¿Olvidaste tu contraseña?
                        </Link>
                      </div>
                      <Input id="password" 
                      type={showPassword ? "text" : "password"}
                      name="password" 
                      onChange={handleLoginChange}/>
                        <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute inset-y-0 right-0 pr-3  items-center text-sm "
                    >
                        {showPassword ? "Ocultar" : "Mostrar"}
                    </button>
                    </div>
                    <Button variant="submit" className="w-full">
                      Iniciar sesión
                    </Button>
                  </div>
                </form>
              </TabsContent>

              <TabsContent value="profesor">
                <form onSubmit={HandleLoginSubmit}>
                  <div className="grid gap-4">
                    <div className="grid gap-2">
                      <Label htmlFor="email-profesor">Correo electrónico</Label>
                      <Input id="email" 
                      type="email" 
                      name="email"
                      placeholder="profesor@ejemplo.com" onChange={handleLoginChange}/>
                    </div>
                    <div className="grid gap-2 relative" >
                      <div className="flex items-center justify-between">
                        <Label htmlFor="password-profesor">Contraseña</Label>
                        <Link to="#" className="text-sm text-blue-600 hover:underline">
                          ¿Olvidaste tu contraseña?
                        </Link>
                      </div>
                      <Input id="contraseña" name="password" type={showPassword ? "text" : "password"} onChange={handleLoginChange}/>
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute inset-y-0 right-0 pr-3  items-center text-sm "
                    >
                        {showPassword ? "Ocultar" : "Mostrar"}
                    </button>
                    </div>
                    <Button variant="submit" className="w-full">
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
              <Link to="#" className="text-blue-600 hover:underline">
                Regístrate aquí
              </Link>
            </div>
            <div className="text-center text-xs text-gray-500">
              Al iniciar sesión, aceptas nuestros{" "}
              <Link to="#" className="text-blue-600 hover:underline">
                Términos de servicio
              </Link>{" "}
              y{" "}
              <Link to="#" className="text-blue-600 hover:underline">
                Política de privacidad
              </Link>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  )
}


export default LoginComponent