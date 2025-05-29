"use client"

import { useState } from "react"
import { Button } from "../components/ui/Button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/Select"
import { Badge } from "../components/ui/Badge"
import { Input } from "../components/ui/Input"
import { Label } from "../components/ui/Label"
import { Textarea } from "../components/ui/Textarea"
import { ArrowLeft, Calculator, CheckCircle, XCircle, RefreshCw, Target } from "lucide-react"

export default function EjerciciosPage() {
  const [currentView, setCurrentView] = useState<"list" | "practice" | "custom">("list")
  const [selectedTema, setSelectedTema] = useState("")
  const [selectedNivel, setSelectedNivel] = useState("")
  const [currentExercise, setCurrentExercise] = useState(0)
  const [userAnswer, setUserAnswer] = useState("")
  const [showResult, setShowResult] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)

  // Datos ficticios
  const temas = [
    { id: "fracciones", nombre: "Fracciones", ejercicios: 45, completados: 38 },
    { id: "algebra", nombre: "Álgebra Básica", ejercicios: 32, completados: 23 },
    { id: "geometria", nombre: "Geometría", ejercicios: 28, completados: 12 },
    { id: "estadistica", nombre: "Estadística", ejercicios: 20, completados: 6 },
    { id: "trigonometria", nombre: "Trigonometría", ejercicios: 35, completados: 0 },
  ]

  const ejerciciosPorNivel = {
    facil: [
      {
        pregunta: "Resuelve: 1/2 + 1/4",
        respuesta: "3/4",
        explicacion: "Para sumar fracciones, necesitamos el mismo denominador. 1/2 = 2/4, entonces 2/4 + 1/4 = 3/4",
      },
      { pregunta: "¿Cuánto es 2/3 de 12?", respuesta: "8", explicacion: "2/3 × 12 = (2 × 12) ÷ 3 = 24 ÷ 3 = 8" },
      {
        pregunta: "Simplifica: 6/8",
        respuesta: "3/4",
        explicacion: "Dividimos numerador y denominador por 2: 6÷2 = 3, 8÷2 = 4",
      },
    ],
    intermedio: [
      {
        pregunta: "Resuelve: 3/4 - 1/6",
        respuesta: "7/12",
        explicacion: "MCM de 4 y 6 es 12. 3/4 = 9/12, 1/6 = 2/12, entonces 9/12 - 2/12 = 7/12",
      },
      {
        pregunta: "Calcula: (2/3) × (3/5)",
        respuesta: "2/5",
        explicacion: "Multiplicamos numeradores y denominadores: (2×3)/(3×5) = 6/15 = 2/5",
      },
    ],
    dificil: [
      {
        pregunta: "Resuelve: (1/2 + 1/3) ÷ (1/4 - 1/6)",
        respuesta: "10",
        explicacion:
          "Primero resolvemos los paréntesis: (3/6 + 2/6) ÷ (3/12 - 2/12) = (5/6) ÷ (1/12) = (5/6) × (12/1) = 10",
      },
    ],
  }

  const handleSubmitAnswer = () => {
    const currentExerciseData = ejerciciosPorNivel[selectedNivel as keyof typeof ejerciciosPorNivel]?.[currentExercise]
    if (currentExerciseData) {
      const correct = userAnswer.trim() === currentExerciseData.respuesta
      setIsCorrect(correct)
      setShowResult(true)
    }
  }

  const nextExercise = () => {
    setCurrentExercise((prev) => prev + 1)
    setUserAnswer("")
    setShowResult(false)
  }

  if (currentView === "practice" && selectedTema && selectedNivel) {
    const exercises = ejerciciosPorNivel[selectedNivel as keyof typeof ejerciciosPorNivel] || []
    const currentExerciseData = exercises[currentExercise]

    if (!currentExerciseData) {
      return (
        <div className="min-h-screen bg-gray-50 p-8">
          <div className="container mx-auto max-w-2xl">
            <Card>
              <CardHeader className="text-center">
                <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
                <CardTitle>¡Felicitaciones!</CardTitle>
                <CardDescription>Has completado todos los ejercicios de este nivel</CardDescription>
              </CardHeader>
              <CardContent className="text-center">
                <Button onClick={() => setCurrentView("list")}>Volver a Ejercicios</Button>
              </CardContent>
            </Card>
          </div>
        </div>
      )
    }

    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="container mx-auto max-w-2xl">
          <div className="mb-6">
            <Button variant="ghost" onClick={() => setCurrentView("list")} className="mb-4">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Volver
            </Button>

            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold capitalize">{selectedTema}</h1>
                <p className="text-gray-600 capitalize">Nivel: {selectedNivel}</p>
              </div>
              <Badge variant="outline">
                {currentExercise + 1} de {exercises.length}
              </Badge>
            </div>
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Calculator className="h-5 w-5 mr-2" />
                Ejercicio {currentExercise + 1}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="text-lg font-medium p-4 bg-blue-50 rounded-lg">{currentExerciseData.pregunta}</div>

              {!showResult ? (
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="answer">Tu respuesta:</Label>
                    <Input
                      id="answer"
                      value={userAnswer}
                      onChange={(e) => setUserAnswer(e.target.value)}
                      placeholder="Escribe tu respuesta aquí"
                      className="text-lg"
                    />
                  </div>
                  <Button onClick={handleSubmitAnswer} disabled={!userAnswer.trim()} className="w-full">
                    Verificar Respuesta
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div
                    className={`p-4 rounded-lg flex items-center ${
                      isCorrect ? "bg-green-50 text-green-800" : "bg-red-50 text-red-800"
                    }`}
                  >
                    {isCorrect ? <CheckCircle className="h-5 w-5 mr-2" /> : <XCircle className="h-5 w-5 mr-2" />}
                    <span className="font-medium">{isCorrect ? "¡Correcto!" : "Incorrecto"}</span>
                  </div>

                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="font-medium mb-2">Respuesta correcta: {currentExerciseData.respuesta}</p>
                    <p className="text-sm text-gray-600">{currentExerciseData.explicacion}</p>
                  </div>

                  <Button onClick={nextExercise} className="w-full">
                    Siguiente Ejercicio
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (currentView === "custom") {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="container mx-auto max-w-2xl">
          <Button variant="ghost" onClick={() => setCurrentView("list")} className="mb-6">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Volver
          </Button>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="h-5 w-5 mr-2" />
                Ejercicios Personalizados
              </CardTitle>
              <CardDescription>Genera ejercicios adaptados a tus dificultades específicas</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label htmlFor="tema-custom">Tema</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona un tema" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="fracciones">Fracciones</SelectItem>
                    <SelectItem value="algebra">Álgebra</SelectItem>
                    <SelectItem value="geometria">Geometría</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="dificultades">Dificultades Identificadas</Label>
                <Textarea
                  id="dificultades"
                  placeholder="Ej: suma de fracciones, fracciones equivalentes"
                  className="min-h-[100px]"
                />
              </div>

              <div>
                <Label htmlFor="cantidad">Cantidad de Ejercicios</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona cantidad" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="5">5 ejercicios</SelectItem>
                    <SelectItem value="10">10 ejercicios</SelectItem>
                    <SelectItem value="15">15 ejercicios</SelectItem>
                    <SelectItem value="20">20 ejercicios</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button className="w-full">
                <RefreshCw className="h-4 w-4 mr-2" />
                Generar Ejercicios Personalizados
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="container mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Ejercicios de Matemáticas</h1>
          <p className="text-gray-600">Selecciona un tema y nivel para comenzar a practicar</p>
        </div>

        <div className="mb-6 flex gap-4">
          <Button onClick={() => setCurrentView("custom")} variant="outline">
            <Target className="h-4 w-4 mr-2" />
            Ejercicios Personalizados
          </Button>
          <Button variant="outline">
            <RefreshCw className="h-4 w-4 mr-2" />
            Generar Nuevos Ejercicios
          </Button>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Temas Disponibles */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-semibold mb-4">Temas Disponibles</h2>
            <div className="grid gap-4">
              {temas.map((tema) => (
                <Card key={tema.id} className="cursor-pointer hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold">{tema.nombre}</h3>
                      <Badge variant="secondary">
                        {tema.completados}/{tema.ejercicios}
                      </Badge>
                    </div>

                    <div className="mb-4">
                      <div className="flex justify-between text-sm mb-1">
                        <span>Progreso</span>
                        <span>{Math.round((tema.completados / tema.ejercicios) * 100)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${(tema.completados / tema.ejercicios) * 100}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <Button
                        className="text-sm"
                        onClick={() => {
                          setSelectedTema(tema.id)
                          setSelectedNivel("facil")
                          setCurrentView("practice")
                          setCurrentExercise(0)
                        }}
                      >
                        Fácil
                      </Button>
                      <Button
                        className="text-sm"
                        variant="outline"
                        onClick={() => {
                          setSelectedTema(tema.id)
                          setSelectedNivel("intermedio")
                          setCurrentView("practice")
                          setCurrentExercise(0)
                        }}
                      >
                        Intermedio
                      </Button>
                      <Button
                        className="text-sm"
                        variant="outline"
                        onClick={() => {
                          setSelectedTema(tema.id)
                          setSelectedNivel("dificil")
                          setCurrentView("practice")
                          setCurrentExercise(0)
                        }}
                      >
                        Difícil
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Estadísticas Rápidas</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Total ejercicios:</span>
                  <span className="font-medium">160</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Completados:</span>
                  <span className="font-medium">79</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Precisión promedio:</span>
                  <span className="font-medium">85%</span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Recomendaciones</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm font-medium">Continúa con Fracciones</p>
                    <p className="text-xs text-gray-600">Vas muy bien, ¡sigue así!</p>
                  </div>
                  <div className="p-3 bg-yellow-50 rounded-lg">
                    <p className="text-sm font-medium">Practica Geometría</p>
                    <p className="text-xs text-gray-600">Necesitas más práctica aquí</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
