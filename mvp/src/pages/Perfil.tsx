"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { Button } from "../components/ui/Button"
import { Input } from "../components/ui/Input"
import { Label } from "../components/ui/Label"
import { Textarea } from "../components/ui/Textarea"
import { Badge } from "../components/ui/Badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/Tabs"
import { User, Settings, Shield, Bell, Award } from "lucide-react"

export default function PerfilPage() {
  const userData = {
    nombre: "Juan Pérez",
    email: "juan.perez@email.com",
    fechaRegistro: "15 de Enero, 2024",
    nivelActual: "Intermedio",
    temasCompletados: 3,
    ejerciciosResueltos: 127,
    horasEstudio: 45,
    rachaMaxima: 12,
    logros: [
      { nombre: "Primera Semana", fecha: "22 Ene 2024", icono: "🎯" },
      { nombre: "Maestro de Fracciones", fecha: "28 Ene 2024", icono: "🏆" },
      { nombre: "Maratonista", fecha: "05 Feb 2024", icono: "🏃" },
    ],
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto max-w-4xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Mi Perfil</h1>
          <p className="text-gray-600">Gestiona tu información personal y configuraciones</p>
        </div>

        <Tabs defaultValue="perfil" className="space-y-6">
          <TabsList>
            <TabsTrigger value="perfil">Información Personal</TabsTrigger>
            <TabsTrigger value="estadisticas">Estadísticas</TabsTrigger>
            <TabsTrigger value="logros">Logros</TabsTrigger>
            <TabsTrigger value="configuracion">Configuración</TabsTrigger>
          </TabsList>

          <TabsContent value="perfil" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <User className="h-5 w-5 mr-2" />
                  Información Personal
                </CardTitle>
                <CardDescription>Actualiza tu información básica</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <Label htmlFor="nombre">Nombre Completo</Label>
                    <Input id="nombre" defaultValue={userData.nombre} />
                  </div>
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input id="email" type="email" defaultValue={userData.email} />
                  </div>
                </div>

                <div>
                  <Label htmlFor="bio">Biografía (Opcional)</Label>
                  <Textarea
                    id="bio"
                    placeholder="Cuéntanos un poco sobre ti y tus objetivos de aprendizaje..."
                    className="min-h-[100px]"
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <Label>Fecha de Registro</Label>
                    <Input value={userData.fechaRegistro} disabled />
                  </div>
                  <div>
                    <Label>Nivel Actual</Label>
                    <div className="flex items-center space-x-2 mt-2">
                      <Badge className="bg-blue-600">{userData.nivelActual}</Badge>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end space-x-3">
                  <Button variant="outline">Cancelar</Button>
                  <Button>Guardar Cambios</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="estadisticas" className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Ejercicios Resueltos</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-blue-600">{userData.ejerciciosResueltos}</div>
                  <p className="text-sm text-gray-500">Total acumulado</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Horas de Estudio</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-green-600">{userData.horasEstudio}h</div>
                  <p className="text-sm text-gray-500">Tiempo invertido</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Temas Completados</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-purple-600">{userData.temasCompletados}</div>
                  <p className="text-sm text-gray-500">de 8 disponibles</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Racha Máxima</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-orange-600">{userData.rachaMaxima}</div>
                  <p className="text-sm text-gray-500">días consecutivos</p>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Progreso Detallado</CardTitle>
                <CardDescription>Tu evolución en cada tema</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="font-medium">Fracciones</span>
                    <span>85% - Dominado</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-green-600 h-3 rounded-full" style={{ width: "85%" }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="font-medium">Álgebra Básica</span>
                    <span>72% - En progreso</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-blue-600 h-3 rounded-full" style={{ width: "72%" }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="font-medium">Geometría</span>
                    <span>45% - Iniciando</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-yellow-600 h-3 rounded-full" style={{ width: "45%" }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="font-medium">Estadística</span>
                    <span>30% - Iniciando</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-red-600 h-3 rounded-full" style={{ width: "30%" }}></div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="logros" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Award className="h-5 w-5 mr-2" />
                  Mis Logros
                </CardTitle>
                <CardDescription>Reconocimientos obtenidos por tu dedicación</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {userData.logros.map((logro, index) => (
                    <div
                      key={index}
                      className="flex items-center p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border border-yellow-200"
                    >
                      <div className="text-3xl mr-4">{logro.icono}</div>
                      <div>
                        <p className="font-semibold text-gray-800">{logro.nombre}</p>
                        <p className="text-sm text-gray-600">{logro.fecha}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Próximos Logros</CardTitle>
                <CardDescription>Objetivos que puedes alcanzar pronto</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="text-2xl mr-4">🎯</div>
                      <div>
                        <p className="font-medium">Precisión Experta</p>
                        <p className="text-sm text-gray-600">Mantén 90% de precisión por una semana</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">85% / 90%</p>
                      <div className="w-20 bg-gray-200 rounded-full h-2 mt-1">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: "94%" }}></div>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <div className="text-2xl mr-4">📚</div>
                      <div>
                        <p className="font-medium">Estudiante Constante</p>
                        <p className="text-sm text-gray-600">Estudia 30 días consecutivos</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">7 / 30 días</p>
                      <div className="w-20 bg-gray-200 rounded-full h-2 mt-1">
                        <div className="bg-green-600 h-2 rounded-full" style={{ width: "23%" }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="configuracion" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Settings className="h-5 w-5 mr-2" />
                  Preferencias de Aprendizaje
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <Label>Nivel de Dificultad Preferido</Label>
                  <select className="w-full mt-1 p-2 border rounded-md">
                    <option>Fácil</option>
                    <option selected>Intermedio</option>
                    <option>Difícil</option>
                    <option>Adaptativo</option>
                  </select>
                </div>

                <div>
                  <Label>Tiempo de Sesión Ideal</Label>
                  <select className="w-full mt-1 p-2 border rounded-md">
                    <option>15 minutos</option>
                    <option selected>30 minutos</option>
                    <option>45 minutos</option>
                    <option>60 minutos</option>
                  </select>
                </div>

                <div>
                  <Label>Temas de Interés</Label>
                  <div className="flex flex-wrap gap-2 mt-2">
                    <Badge variant="outline">Fracciones</Badge>
                    <Badge className="bg-blue-600">Álgebra</Badge>
                    <Badge variant="outline">Geometría</Badge>
                    <Badge variant="outline">Estadística</Badge>
                    <Badge variant="outline">Trigonometría</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Bell className="h-5 w-5 mr-2" />
                  Notificaciones
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Recordatorios de estudio</p>
                    <p className="text-sm text-gray-600">Recibe recordatorios para mantener tu racha</p>
                  </div>
                  <input type="checkbox" className="toggle" defaultChecked />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Reportes semanales</p>
                    <p className="text-sm text-gray-600">Resumen de tu progreso cada semana</p>
                  </div>
                  <input type="checkbox" className="toggle" defaultChecked />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Nuevos logros</p>
                    <p className="text-sm text-gray-600">Notificaciones cuando obtengas logros</p>
                  </div>
                  <input type="checkbox" className="toggle" defaultChecked />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Shield className="h-5 w-5 mr-2" />
                  Seguridad
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button variant="outline" className="w-full">
                  Cambiar Contraseña
                </Button>
                <Button variant="outline" className="w-full">
                  Configurar Autenticación de Dos Factores
                </Button>
                <Button variant="ghost" className="w-full">
                  Eliminar Cuenta
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
