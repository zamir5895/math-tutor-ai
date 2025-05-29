"use client"

import { Button } from "../components/ui/Button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/Card"
import { BookOpen, Calculator, TrendingUp, Users } from "lucide-react"

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Ejercicios Completados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-500">127</div>
              <p className="text-xs text-gray-500">+12 esta semana</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Precisión Promedio</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-emerald-500">85%</div>
              <p className="text-xs text-gray-500">+5% vs mes anterior</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Temas Dominados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-violet-500">3</div>
              <p className="text-xs text-gray-500">de 8 temas</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Racha Actual</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-amber-500">7</div>
              <p className="text-xs text-gray-500">días consecutivos</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Acciones Rápidas</CardTitle>
                <CardDescription>Continúa tu aprendizaje donde lo dejaste</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  <Button className="h-20 flex-col">
                    <BookOpen className="h-6 w-6 mb-2" />
                    Practicar Fracciones
                  </Button>
                  <Button variant="outline" className="h-20 flex-col">
                    <TrendingUp className="h-6 w-6 mb-2" />
                    Ver Mi Progreso
                  </Button>
                  <Button variant="outline" className="h-20 flex-col">
                    <Calculator className="h-6 w-6 mb-2" />
                    Ejercicios Personalizados
                  </Button>
                  <Button variant="outline" className="h-20 flex-col">
                    <Users className="h-6 w-6 mb-2" />
                    Reportes de Análisis
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Actividad Reciente</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div>
                      <p className="font-medium">Fracciones - Nivel Intermedio</p>
                      <p className="text-sm text-gray-600">8/10 ejercicios correctos</p>
                    </div>
                    <div className="text-emerald-500 font-bold">80%</div>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                    <div>
                      <p className="font-medium">Álgebra Básica - Nivel Fácil</p>
                      <p className="text-sm text-gray-600">9/10 ejercicios correctos</p>
                    </div>
                    <div className="text-blue-500 font-bold">90%</div>
                  </div>

                  <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                    <div>
                      <p className="font-medium">Geometría - Nivel Intermedio</p>
                      <p className="text-sm text-gray-600">6/10 ejercicios correctos</p>
                    </div>
                    <div className="text-amber-500 font-bold">60%</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Progress Overview */}
            <Card>
              <CardHeader>
                <CardTitle>Progreso por Tema</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Fracciones</span>
                    <span>85%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: "85%" }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Álgebra</span>
                    <span>72%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-emerald-500 h-2 rounded-full" style={{ width: "72%" }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Geometría</span>
                    <span>45%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-amber-500 h-2 rounded-full" style={{ width: "45%" }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Estadística</span>
                    <span>30%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-pink-600 h-2 rounded-full" style={{ width: "30%" }}></div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Recommendations */}
            <Card>
              <CardHeader>
                <CardTitle>Recomendaciones</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm font-medium text-blue-800">Practica más geometría</p>
                  <p className="text-xs text-blue-500">Tu rendimiento ha bajado en este tema</p>
                </div>

                <div className="p-3 bg-green-50 rounded-lg">
                  <p className="text-sm font-medium text-green-800">¡Excelente en fracciones!</p>
                  <p className="text-xs text-emerald-500">Considera avanzar al siguiente nivel</p>
                </div>

                <div className="p-3 bg-purple-50 rounded-lg">
                  <p className="text-sm font-medium text-purple-800">Sesión de repaso</p>
                  <p className="text-xs text-violet-500">Revisa conceptos de álgebra básica</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
