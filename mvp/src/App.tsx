// App.tsx
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import HomePage from "./pages/Home"
import DashboardPage from "./pages/Dashboard"
import RootLayout from "./components/ui/layout"
import EjerciciosPage from "./pages/Ejercicios"
import ProgresoPage from "./pages/Progreso"
import AnalisisPage from "./pages/Analisis"
import ReportesPage from "./pages/Reportes"

function App() {
  return (
    <Router>
      <RootLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/ejercicios" element={<EjerciciosPage />} />
          <Route path="/progreso" element={<ProgresoPage />} />
          <Route path="/analisis" element={<AnalisisPage />} />
          <Route path="/reportes" element={<ReportesPage />} />
        </Routes>
      </RootLayout>
    </Router>
  )
}

export default App