import { BookOpen, GraduationCap, School } from 'lucide-react'
import React from 'react'
import { Button } from '../UI/Buttom'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../UI/Card'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@radix-ui/react-tabs'
import { Input } from '../UI/Input'
import { Label } from '../UI/label'
import {  Link } from 'react-router-dom'


const LoginComponent = () => {
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
                <form>
                  <div className="grid gap-4">
                    <div className="grid gap-2">
                      <Label htmlFor="email-estudiante">Correo electrónico</Label>
                      <Input id="email-estudiante" type="email" placeholder="estudiante@ejemplo.com" />
                    </div>
                    <div className="grid gap-2">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="password-estudiante">Contraseña</Label>
                        <Link to="#" className="text-sm text-blue-600 hover:underline">
                          ¿Olvidaste tu contraseña?
                        </Link>
                      </div>
                      <Input id="password-estudiante" type="password" />
                    </div>
                    <Button variant="submit" className="w-full">
                      Iniciar sesión
                    </Button>
                  </div>
                </form>
              </TabsContent>

              <TabsContent value="profesor">
                <form>
                  <div className="grid gap-4">
                    <div className="grid gap-2">
                      <Label htmlFor="email-profesor">Correo electrónico</Label>
                      <Input id="email-profesor" type="email" placeholder="profesor@ejemplo.com" />
                    </div>
                    <div className="grid gap-2">
                      <div className="flex items-center justify-between">
                        <Label htmlFor="password-profesor">Contraseña</Label>
                        <Link to="#" className="text-sm text-blue-600 hover:underline">
                          ¿Olvidaste tu contraseña?
                        </Link>
                      </div>
                      <Input id="password-profesor" type="password" />
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