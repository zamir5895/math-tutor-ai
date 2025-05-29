"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { Button } from "../components/ui/Button"
import { Badge } from "../components/ui/Badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/Tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/Select"
import { FileText, Download, TrendingUp, AlertTriangle, CheckCircle, Brain } from "lucide-react"

export default function ReportesPage() {
  // Datos ficticios para reportes
  const reporteGeneral = {
    fechaGeneracion: "2024-01-15",
    periodoAnalisis: "Últimos 30 días",
    ejerciciosCompletados: 127,
    precisionPromedio: 85,
    tiempoEstudio: "45 horas",
    temasEstudiados: 4,
    fortalezas: ["Fracciones", "Álgebra básica"],
    debilidades: ["Geometría", "Estadística"],
    recomendaciones: [
      "Dedicar más tiempo a geometría",
      "Practicar problemas de estadística básica",
      "Continuar reforzando fracciones complejas",
    ],
  }

  const analisisPatrones = {
    patronesIdentificados: [
      {
        tipo: "Horario óptimo",
        descripcion: "Mejor rendimiento entre 16:00-18:00",
        impacto: "15% mayor precisión",
        recomendacion: "Programar sesiones de estudio en este horario",
      },
      {
        tipo: "Dificultad recurrente",
        descripcion: "Problemas con fracciones mixtas",
        impacto: "25% menor precisión",
        recomendacion: "Ejercicios adicionales de fracciones mixtas",
      },
      {
        tipo: "Progreso acelerado",
        descripcion: "Rápida mejora en álgebra",
        impacto: "30% mejora en 2 semanas",
        recomendacion: "Avanzar a nivel intermedio",
      },
    ],
    predicciones: [
      "Dominio completo de fracciones en 2 semanas",
      "Necesitará 4 semanas adicionales para geometría",
      "Listo para álgebra intermedia en 1 semana",
    ],
  }

  const reportesPrevios = [
    {
      fecha: "2024-01-15",
      tipo: "Reporte Mensual",
      temas: ["Fracciones", "Álgebra"],
      estado: "Completado",
    },
    {
      fecha: "2024-01-08",
      tipo: "Análisis de Patrones",
      temas: ["Todos"],
      estado: "Completado",
    },
    {
      fecha: "2024-01-01",
      tipo: "Reporte Semanal",
      temas: ["Fracciones"],
      estado: "Completado",
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Reportes y Análisis</h1>
          <p className="text-gray-600">Análisis detallado de tu progreso y patrones de aprendizaje</p>
        </div>

        <Tabs defaultValue="actual" className="space-y-6">
          <TabsList>
            <TabsTrigger value="actual">Reporte Actual</TabsTrigger>
            <TabsTrigger value="patrones">Análisis de Patrones</TabsTrigger>
            <TabsTrigger value="historico">Reportes Anteriores</TabsTrigger>
            <TabsTrigger value="generar">Generar Nuevo</TabsTrigger>
          </TabsList>

          <TabsContent value="actual" className="space-y-6">
            {/* Header del reporte */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center">
                      <FileText className="h-5 w-5 mr-2" />
                      Reporte de Progreso - Enero 2024
                    </CardTitle>
                    <CardDescription>
                      Generado el {reporteGeneral.fechaGeneracion} • {reporteGeneral.periodoAnalisis}
                    </CardDescription>
                  </div>
                  <Button>
                    <Download className="h-4 w-4 mr-2" />
                    Descargar PDF
                  </Button>
                </div>
              </CardHeader>
            </Card>

            {/* Métricas principales */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Ejercicios Completados</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-600">{reporteGeneral.ejerciciosCompletados}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Precisión Promedio</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">{reporteGeneral.precisionPromedio}%</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Tiempo de Estudio</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-purple-600">{reporteGeneral.tiempoEstudio}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-600">Temas Estudiados</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-orange-600">{reporteGeneral.temasEstudiados}</div>
                </CardContent>
              </Card>
            </div>

            {/* Análisis detallado */}
            <div className="grid lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center text-green-600">
                    <CheckCircle className="h-5 w-5 mr-2" />
                    Fortalezas Identificadas
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {reporteGeneral.fortalezas.map((fortaleza, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                        <span className="font-medium text-green-800">{fortaleza}</span>
                        <Badge className="bg-green-600">Dominado</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center text-orange-600">
                    <AlertTriangle className="h-5 w-5 mr-2" />
                    Áreas de Mejora
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {reporteGeneral.debilidades.map((debilidad, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-orange-50 rounded-lg">
                        <span className="font-medium text-orange-800">{debilidad}</span>
                        <Badge variant="outline" className="border-orange-600 text-orange-600">
                          Necesita práctica
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Recomendaciones */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Recomendaciones Personalizadas
                </CardTitle>
                <CardDescription>Sugerencias basadas en tu patrón de aprendizaje</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {reporteGeneral.recomendaciones.map((recomendacion, index) => (
                    <div key={index} className="flex items-start p-4 bg-blue-50 rounded-lg">
                      <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium mr-3 mt-0.5">
                        {index + 1}
                      </div>
                      <p className="text-blue-800">{recomendacion}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="patrones" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="h-5 w-5 mr-2" />
                  Análisis de Patrones de Aprendizaje
                </CardTitle>
                <CardDescription>Patrones identificados mediante inteligencia artificial</CardDescription>
              </CardHeader>
            </Card>

            <div className="space-y-6">
              {analisisPatrones.patronesIdentificados.map((patron, index) => (
                <Card key={index}>
                  <CardHeader>
                    <CardTitle className="text-lg">{patron.tipo}</CardTitle>
                    <CardDescription>{patron.descripcion}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm font-medium text-gray-600 mb-1">Impacto</p>
                        <p className="text-lg font-semibold text-blue-600">{patron.impacto}</p>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-600 mb-1">Recomendación</p>
                        <p className="text-sm">{patron.recomendacion}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Predicciones de Progreso</CardTitle>
                <CardDescription>Estimaciones basadas en tu ritmo actual de aprendizaje</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analisisPatrones.predicciones.map((prediccion, index) => (
                    <div key={index} className="flex items-center p-3 bg-purple-50 rounded-lg">
                      <div className="flex-shrink-0 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-medium mr-3">
                        {index + 1}
                      </div>
                      <p className="text-purple-800">{prediccion}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="historico" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Reportes Anteriores</CardTitle>
                <CardDescription>Historial de reportes generados</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reportesPrevios.map((reporte, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <FileText className="h-5 w-5 text-gray-400" />
                        <div>
                          <p className="font-medium">{reporte.tipo}</p>
                          <p className="text-sm text-gray-600">{reporte.fecha}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="text-sm text-gray-600">{reporte.temas.join(", ")}</div>
                        <Badge variant="outline">{reporte.estado}</Badge>
                        <Button className="text-sm" variant="outline">
                          <Download className="h-4 w-4 mr-1" />
                          Descargar
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="generar" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Generar Nuevo Reporte</CardTitle>
                <CardDescription>Crea un reporte personalizado seleccionando los parámetros</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Tipo de Reporte</label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecciona el tipo" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="general">Reporte General</SelectItem>
                        <SelectItem value="tema">Por Tema Específico</SelectItem>
                        <SelectItem value="patrones">Análisis de Patrones</SelectItem>
                        <SelectItem value="comparativo">Comparativo Temporal</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">Período</label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecciona el período" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="semana">Última semana</SelectItem>
                        <SelectItem value="mes">Último mes</SelectItem>
                        <SelectItem value="trimestre">Último trimestre</SelectItem>
                        <SelectItem value="personalizado">Período personalizado</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">Temas a Incluir</label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecciona los temas" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="todos">Todos los temas</SelectItem>
                        <SelectItem value="fracciones">Solo Fracciones</SelectItem>
                        <SelectItem value="algebra">Solo Álgebra</SelectItem>
                        <SelectItem value="geometria">Solo Geometría</SelectItem>
                        <SelectItem value="estadistica">Solo Estadística</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">Formato</label>
                    <Select>
                      <SelectTrigger>
                        <SelectValue placeholder="Selecciona el formato" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pdf">PDF</SelectItem>
                        <SelectItem value="excel">Excel</SelectItem>
                        <SelectItem value="web">Visualización Web</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="flex justify-end space-x-3">
                  <Button variant="outline">Vista Previa</Button>
                  <Button>
                    <FileText className="h-4 w-4 mr-2" />
                    Generar Reporte
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Reportes Programados</CardTitle>
                <CardDescription>Configura reportes automáticos</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <p className="font-medium">Reporte Semanal</p>
                      <p className="text-sm text-gray-600">Cada lunes a las 9:00 AM</p>
                    </div>
                    <Badge className="bg-green-600">Activo</Badge>
                  </div>

                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <p className="font-medium">Análisis Mensual</p>
                      <p className="text-sm text-gray-600">Primer día de cada mes</p>
                    </div>
                    <Badge variant="outline">Inactivo</Badge>
                  </div>
                </div>

                <Button className="w-full mt-4" variant="outline">
                  Configurar Nuevo Reporte Automático
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
