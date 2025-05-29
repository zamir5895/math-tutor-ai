"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { Badge } from "../components/ui/Badge"
import { Button } from "../components/ui/Button"
import { Progress } from "../components/ui/Progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/Tabs"
import { TrendingUp, Target, Award, BarChart3, Clock } from "lucide-react"

export default function ProgresoPage() {
  // Datos ficticios de progreso
  const progresoGeneral = {
    ejerciciosCompletados: 127,
    horasEstudio: 45,
    rachaActual: 7,
    precisionPromedio: 85,
    temasCompletados: 3,
    totalTemas: 8,
  }

  const progresoTemas = [
    {
      tema: "Fracciones",
      progreso: 85,
      ejerciciosCompletados: 38,
      totalEjercicios: 45,
      ultimaActividad: "Hace 2 horas",
      nivel: "Intermedio",
      precision: 88,
    },
    {
      tema: "Álgebra Básica",
      progreso: 72,
      ejerciciosCompletados: 23,
      totalEjercicios: 32,
      ultimaActividad: "Ayer",
      nivel: "Fácil",
      precision: 82,
    },
    {
      tema: "Geometría",
      progreso: 43,
      ejerciciosCompletados: 12,
      totalEjercicios: 28,
      ultimaActividad: "Hace 3 días",
      nivel: "Intermedio",
      precision: 75,
    },
    {
      tema: "Estadística",
      progreso: 30,
      ejerciciosCompletados: 6,
      totalEjercicios: 20,
      ultimaActividad: "Hace 1 semana",
      nivel: "Fácil",
      precision: 90,
    },
  ]

  const actividadSemanal = [
    { dia: "Lun", ejercicios: 8, tiempo: 45 },
    { dia: "Mar", ejercicios: 12, tiempo: 60 },
    { dia: "Mié", ejercicios: 6, tiempo: 30 },
    { dia: "Jue", ejercicios: 15, tiempo: 75 },
    { dia: "Vie", ejercicios: 10, tiempo: 50 },
    { dia: "Sáb", ejercicios: 5, tiempo: 25 },
    { dia: "Dom", ejercicios: 8, tiempo: 40 },
  ]

  const logros = [
    { nombre: "Primera Semana", descripcion: "Completa 7 días consecutivos", obtenido: true },
    { nombre: "Maestro de Fracciones", descripcion: "Domina el tema de fracciones", obtenido: true },
    { nombre: "Precisión Experta", descripcion: "Mantén 90% de precisión por una semana", obtenido: false },
    { nombre: "Maratonista", descripcion: "Completa 100 ejercicios", obtenido: true },
    { nombre: "Estudiante Constante", descripcion: "Estudia 30 días consecutivos", obtenido: false },
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Mi Progreso</h1>
          <p className="text-gray-600">Seguimiento detallado de tu aprendizaje</p>
        </div>

        <Tabs defaultValue="general" className="space-y-6">
          <TabsList>
            <TabsTrigger value="general">Resumen General</TabsTrigger>
            <TabsTrigger value="temas">Por Temas</TabsTrigger>
            <TabsTrigger value="actividad">Actividad</TabsTrigger>
            <TabsTrigger value="logros">Logros</TabsTrigger>
          </TabsList>

          <TabsContent value="general" className="space-y-6">
            {/* Métricas principales */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                    <Target className="h-4 w-4 mr-2" />
                    Ejercicios Completados
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-blue-600 mb-2">{progresoGeneral.ejerciciosCompletados}</div>
                  <p className="text-sm text-gray-500">+12 esta semana</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                    <Clock className="h-4 w-4 mr-2" />
                    Horas de Estudio
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-green-600 mb-2">{progresoGeneral.horasEstudio}h</div>
                  <p className="text-sm text-gray-500">+8h esta semana</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                    <TrendingUp className="h-4 w-4 mr-2" />
                    Precisión Promedio
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-purple-600 mb-2">{progresoGeneral.precisionPromedio}%</div>
                  <p className="text-sm text-gray-500">+5% vs mes anterior</p>
                </CardContent>
              </Card>
            </div>

            {/* Progreso general */}
            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Progreso General</CardTitle>
                  <CardDescription>Tu avance en todos los temas</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span>Temas Completados</span>
                      <span>
                        {progresoGeneral.temasCompletados}/{progresoGeneral.totalTemas}
                      </span>
                    </div>
                    <Progress value={(progresoGeneral.temasCompletados / progresoGeneral.totalTemas) * 100} />
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-orange-600">{progresoGeneral.rachaActual}</div>
                      <p className="text-sm text-gray-600">Días consecutivos</p>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">{progresoGeneral.temasCompletados}</div>
                      <p className="text-sm text-gray-600">Temas dominados</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Actividad Reciente</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                      <div>
                        <p className="font-medium">Fracciones completadas</p>
                        <p className="text-sm text-gray-600">Hace 2 horas</p>
                      </div>
                      <Badge variant="secondary">+5 ejercicios</Badge>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                      <div>
                        <p className="font-medium">Nuevo nivel desbloqueado</p>
                        <p className="text-sm text-gray-600">Ayer</p>
                      </div>
                      <Badge>Álgebra Intermedio</Badge>
                    </div>

                    <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                      <div>
                        <p className="font-medium">Logro obtenido</p>
                        <p className="text-sm text-gray-600">Hace 3 días</p>
                      </div>
                      <Badge variant="outline">Maratonista</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="temas" className="space-y-6">
            <div className="grid gap-6">
              {progresoTemas.map((tema, index) => (
                <Card key={index}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{tema.tema}</CardTitle>
                      <div className="flex items-center gap-2">
                        <Badge variant="outline">{tema.nivel}</Badge>
                        <Badge variant="secondary">{tema.precision}% precisión</Badge>
                      </div>
                    </div>
                    <CardDescription>Última actividad: {tema.ultimaActividad}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <div className="flex justify-between text-sm mb-2">
                          <span>Progreso</span>
                          <span>
                            {tema.ejerciciosCompletados}/{tema.totalEjercicios} ejercicios
                          </span>
                        </div>
                        <Progress value={tema.progreso} />
                      </div>

                      <div className="flex justify-between items-center">
                        <span className="text-2xl font-bold text-blue-600">{tema.progreso}%</span>
                        <Button className="text-sm">Continuar Practicando</Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="actividad" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="h-5 w-5 mr-2" />
                  Actividad Semanal
                </CardTitle>
                <CardDescription>Tu actividad de los últimos 7 días</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-7 gap-4">
                  {actividadSemanal.map((dia, index) => (
                    <div key={index} className="text-center">
                      <div className="text-sm font-medium text-gray-600 mb-2">{dia.dia}</div>
                      <div className="bg-blue-100 rounded-lg p-3 mb-2">
                        <div className="text-lg font-bold text-blue-600">{dia.ejercicios}</div>
                        <div className="text-xs text-gray-600">ejercicios</div>
                      </div>
                      <div className="text-xs text-gray-500">{dia.tiempo}min</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Estadísticas del Mes</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Días activos:</span>
                    <span className="font-medium">22/30</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Promedio diario:</span>
                    <span className="font-medium">8.5 ejercicios</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Mejor día:</span>
                    <span className="font-medium">15 ejercicios</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tiempo total:</span>
                    <span className="font-medium">12.5 horas</span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Tendencias</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <span className="text-green-800">Precisión</span>
                    <span className="text-green-600 font-medium">↗ +5%</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <span className="text-blue-800">Velocidad</span>
                    <span className="text-blue-600 font-medium">↗ +12%</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                    <span className="text-purple-800">Constancia</span>
                    <span className="text-purple-600 font-medium">↗ +8%</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="logros" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              {logros.map((logro, index) => (
                <Card key={index} className={logro.obtenido ? "border-green-200 bg-green-50" : ""}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center">
                        <Award className={`h-5 w-5 mr-2 ${logro.obtenido ? "text-green-600" : "text-gray-400"}`} />
                        {logro.nombre}
                      </CardTitle>
                      {logro.obtenido && <Badge className="bg-green-600">Obtenido</Badge>}
                    </div>
                    <CardDescription>{logro.descripcion}</CardDescription>
                  </CardHeader>
                  {!logro.obtenido && (
                    <CardContent>
                      <Button variant="outline" className="text-sm">
                        Ver Requisitos
                      </Button>
                    </CardContent>
                  )}
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
