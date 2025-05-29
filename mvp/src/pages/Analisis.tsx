"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { Button } from "../components/ui/Button"
import { Badge } from "../components/ui/Badge"
import { Progress } from "../components/ui/Progress"
import { Brain, TrendingUp, AlertCircle, Lightbulb, Target, Clock } from "lucide-react"

export default function AnalisisPage() {
  const analisisIA = {
    nivelAprendizaje: "Intermedio",
    estiloAprendizaje: "Visual-Kinestésico",
    velocidadProgreso: "Por encima del promedio",
    patronesIdentificados: 5,
    recomendacionesActivas: 8,
    prediccionDominio: "3-4 semanas",
  }

  const fortalezasDebilidades = {
    fortalezas: [
      {
        area: "Operaciones básicas",
        nivel: 95,
        descripcion: "Excelente manejo de suma, resta, multiplicación y división",
      },
      { area: "Fracciones simples", nivel: 88, descripcion: "Buen entendimiento de conceptos fundamentales" },
      { area: "Resolución de problemas", nivel: 82, descripcion: "Capacidad analítica desarrollada" },
    ],
    debilidades: [
      { area: "Fracciones complejas", nivel: 45, descripcion: "Dificultad con operaciones mixtas" },
      { area: "Geometría espacial", nivel: 38, descripcion: "Problemas de visualización 3D" },
      { area: "Estadística descriptiva", nivel: 52, descripcion: "Conceptos de media y mediana confusos" },
    ],
  }

  const recomendacionesIA = [
    {
      tipo: "Inmediata",
      titulo: "Reforzar fracciones mixtas",
      descripcion: "Practicar conversión entre fracciones impropias y mixtas",
      prioridad: "Alta",
      tiempoEstimado: "15-20 min/día",
    },
    {
      tipo: "Corto plazo",
      titulo: "Introducir geometría básica",
      descripcion: "Comenzar con figuras 2D antes de avanzar a 3D",
      prioridad: "Media",
      tiempoEstimado: "30 min, 3x/semana",
    },
    {
      tipo: "Largo plazo",
      titulo: "Preparación para álgebra",
      descripcion: "Fortalecer bases numéricas para transición suave",
      prioridad: "Baja",
      tiempoEstimado: "Progresivo",
    },
  ]

  const predicciones = [
    {
      tema: "Fracciones",
      dominioActual: 75,
      dominioProyectado: 95,
      tiempoEstimado: "2 semanas",
      confianza: 92,
    },
    {
      tema: "Álgebra básica",
      dominioActual: 60,
      dominioProyectado: 85,
      tiempoEstimado: "4 semanas",
      confianza: 87,
    },
    {
      tema: "Geometría",
      dominioActual: 40,
      dominioProyectado: 70,
      tiempoEstimado: "6 semanas",
      confianza: 78,
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2 flex items-center">
            <Brain className="h-8 w-8 mr-3 text-purple-600" />
            Análisis con Inteligencia Artificial
          </h1>
          <p className="text-gray-600">Insights personalizados sobre tu aprendizaje</p>
        </div>

        {/* Resumen del análisis */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Nivel de Aprendizaje</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600 mb-1">{analisisIA.nivelAprendizaje}</div>
              <p className="text-sm text-gray-500">Basado en rendimiento general</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Estilo de Aprendizaje</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600 mb-1">{analisisIA.estiloAprendizaje}</div>
              <p className="text-sm text-gray-500">Detectado por IA</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Velocidad de Progreso</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-lg font-bold text-green-600 mb-1">{analisisIA.velocidadProgreso}</div>
              <p className="text-sm text-gray-500">vs otros estudiantes</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Fortalezas */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-green-600">
                <TrendingUp className="h-5 w-5 mr-2" />
                Fortalezas Identificadas
              </CardTitle>
              <CardDescription>Áreas donde destacas según el análisis de IA</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {fortalezasDebilidades.fortalezas.map((fortaleza, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{fortaleza.area}</span>
                    <Badge className="bg-green-600">{fortaleza.nivel}%</Badge>
                  </div>
                  <Progress value={fortaleza.nivel} className="h-2" />
                  <p className="text-sm text-gray-600">{fortaleza.descripcion}</p>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Debilidades */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center text-orange-600">
                <AlertCircle className="h-5 w-5 mr-2" />
                Áreas de Oportunidad
              </CardTitle>
              <CardDescription>Temas que requieren atención adicional</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {fortalezasDebilidades.debilidades.map((debilidad, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{debilidad.area}</span>
                    <Badge variant="outline" className="border-orange-600 text-orange-600">
                      {debilidad.nivel}%
                    </Badge>
                  </div>
                  <Progress value={debilidad.nivel} className="h-2" />
                  <p className="text-sm text-gray-600">{debilidad.descripcion}</p>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Recomendaciones de IA */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Lightbulb className="h-5 w-5 mr-2 text-yellow-600" />
              Recomendaciones Personalizadas de IA
            </CardTitle>
            <CardDescription>Sugerencias basadas en tu patrón único de aprendizaje</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recomendacionesIA.map((rec, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <Badge variant="outline">{rec.tipo}</Badge>
                      <Badge
                        className={
                          rec.prioridad === "Alta"
                            ? "bg-red-600"
                            : rec.prioridad === "Media"
                              ? "bg-yellow-600"
                              : "bg-green-600"
                        }
                      >
                        {rec.prioridad}
                      </Badge>
                    </div>
                    <div className="flex items-center text-sm text-gray-600">
                      <Clock className="h-4 w-4 mr-1" />
                      {rec.tiempoEstimado}
                    </div>
                  </div>
                  <h4 className="font-semibold mb-1">{rec.titulo}</h4>
                  <p className="text-gray-600 text-sm mb-3">{rec.descripcion}</p>
                  <Button >Aplicar Recomendación</Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Predicciones */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Target className="h-5 w-5 mr-2 text-blue-600" />
              Predicciones de Progreso
            </CardTitle>
            <CardDescription>Proyecciones basadas en tu ritmo actual de aprendizaje</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {predicciones.map((pred, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex justify-between items-center mb-4">
                    <h4 className="font-semibold text-lg">{pred.tema}</h4>
                    <Badge variant="outline">{pred.confianza}% confianza</Badge>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Dominio Actual</p>
                      <div className="flex items-center space-x-2">
                        <Progress value={pred.dominioActual} className="flex-1" />
                        <span className="text-sm font-medium">{pred.dominioActual}%</span>
                      </div>
                    </div>

                    <div>
                      <p className="text-sm text-gray-600 mb-1">Dominio Proyectado</p>
                      <div className="flex items-center space-x-2">
                        <Progress value={pred.dominioProyectado} className="flex-1" />
                        <span className="text-sm font-medium">{pred.dominioProyectado}%</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">
                      Tiempo estimado: <span className="font-medium">{pred.tiempoEstimado}</span>
                    </span>
                    <Button className="text-sm" variant="outline">
                      Ver Plan Detallado
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
