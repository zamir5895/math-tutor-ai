import { FaThLarge, FaUsers, FaRegListAlt, FaCog } from 'react-icons/fa'
import logoMateMix from '../../assets/Vector (1).svg'


const TeacherDashboardComponent = () => {
  return (
    <div className="relative bg-white overflow-hidden flex">
      <aside className="bg-white border-r border-gray-300 p-6">
        <div className="flex items-center gap-2 mb-8">
          <img src={logoMateMix} alt="MateMix Logo" className="h-8 w-auto"/>
        </div>

        <div className="text-gray-500 font-semibold text-sm mb-4">Menu</div>

        <nav className="flex flex-col gap-4 text-gray-500">
          <button className="flex items-center gap-2 px-2 py-2 hover:text-gray-700">
            <FaThLarge /> Panel
          </button>
          <button className="flex items-center gap-2 px-2 py-2 hover:text-gray-700">
            <FaUsers /> Estudiantes
          </button>
          <button className="flex items-center gap-2 px-2 py-2 hover:text-gray-700">
            <FaRegListAlt /> Temas
          </button>
          <button className="flex items-center gap-2 px-2 py-2 hover:text-gray-700">
            <FaCog /> Configuración
          </button>
        </nav>
      </aside>

      <main className=" p-8 overflow-y-auto">
        <h1 className="text-3xl font-bold">Panel de la Clase</h1>
        <p className="text-gray-500 mb-6">
          Gestiona a tus estudiantes y realiza un seguimiento de su progreso
        </p>

        {/* Tarjetas de resumen */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white shadow-md rounded-xl p-4 flex flex-col items-center justify-center w-64">
            <span className="text-yellow-500 text-3xl">👤</span>
            <p className="text-gray-500 text-sm">Total de estudiantes</p>
            <p className="text-2xl font-bold">30</p>
          </div>
          <div className="bg-white shadow-md rounded-xl p-4 flex flex-col items-center justify-center w-64">
            <span className="text-green-500 text-3xl">📊</span>
            <p className="text-gray-500 text-sm">Promedio del Salón</p>
            <p className="text-2xl font-bold">15</p>
          </div>
          <div className="bg-white shadow-md rounded-xl p-4 flex flex-col items-center justify-center w-64">
            <span className="text-blue-500 text-3xl">📘</span>
            <p className="text-gray-500 text-sm">Temas Activos</p>
            <p className="text-2xl font-bold">4</p>
          </div>
          <div className="bg-white shadow-md rounded-xl p-4 flex flex-col items-center justify-center w-64">
            <span className="text-red-400 text-3xl">⭐</span>
            <p className="text-gray-500 text-sm">Mejor Promedio</p>
            <p className="text-2xl font-bold">Bianca A.</p>
          </div>
        </div>

        {/* Progreso de estudiantes y desempeño */}
        <div className="grid grid-cols-3 gap-6">
          {/* Tabla */}
          <div className="col-span-2 bg-white shadow-md rounded-xl p-6">
            <h2 className="text-lg font-bold mb-4">Progreso de los estudiantes</h2>
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="text-gray-500 border-b">
                  <th>Estudiante</th>
                  <th>Progreso</th>
                  <th>Racha</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {[
                  {
                    nombre: "Bianca Aguinaga",
                    progreso: "92%",
                    racha: "7 días",
                    estado: "en línea",
                    color: "bg-yellow-400"
                  },
                  {
                    nombre: "Jorge Melgarejo",
                    progreso: "78%",
                    racha: "3 días",
                    estado: "advertencia",
                    color: "bg-green-500"
                  },
                  {
                    nombre: "Zamir Lizardo",
                    progreso: "85%",
                    racha: "6 días",
                    estado: "en línea",
                    color: "bg-blue-400"
                  },
                  {
                    nombre: "Matias Meneses",
                    progreso: "65%",
                    racha: "0 días",
                    estado: "desconectado",
                    color: "bg-red-400"
                  },
                  {
                    nombre: "Zamir Lizardo",
                    progreso: "85%",
                    racha: "6 días",
                    estado: "en línea",
                    color: "bg-blue-400"
                  },
                  {
                    nombre: "Matias Meneses",
                    progreso: "65%",
                    racha: "0 días",
                    estado: "desconectado",
                    color: "bg-red-400"
                  },
                  {
                    nombre: "Zamir Lizardo",
                    progreso: "85%",
                    racha: "6 días",
                    estado: "en línea",
                    color: "bg-blue-400"
                  },
                  {
                    nombre: "Matias Meneses",
                    progreso: "65%",
                    racha: "0 días",
                    estado: "desconectado",
                    color: "bg-red-400"
                  }
                ].map((alumno, i) => (
                  <tr key={i} className="border-b hover:bg-gray-50">
                    <td className="flex items-center gap-2 py-2">
                      <span className={`h-6 w-6 rounded-full ${alumno.color}`} />
                      {alumno.nombre}
                    </td>
                    <td>{alumno.progreso}</td>
                    <td>
                      <span className="bg-yellow-100 text-yellow-700 px-2 py-1 rounded text-xs">
                        {alumno.racha}
                      </span>
                    </td>
                    <td>
                      <span className={`text-white text-xs px-2 py-1 rounded ${alumno.estado === "en línea"
                        ? "bg-green-400"
                        : alumno.estado === "advertencia"
                        ? "bg-pink-400"
                        : "bg-gray-400"
                      }`}>
                        {alumno.estado}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Desempeño */}
          <div className="bg-white shadow-md rounded-xl p-6">
            <h2 className="text-lg font-bold mb-4">Desempeño</h2>

            <div className="mb-4">
              <p className="text-sm text-gray-600">Mejores Temas</p>
              <div className="my-1">
                <p className="text-sm">Aritmética</p>
                <div className="h-2 bg-gray-200 rounded">
                  <div className="h-2 bg-orange-400 rounded w-[90%]" />
                </div>
              </div>
              <div className="my-1">
                <p className="text-sm">Geometría</p>
                <div className="h-2  bg-gray-200 rounded">
                  <div className="h-2 bg-blue-500 rounded w-[70%]" />
                </div>
              </div>
              <div className="my-1">
                <p className="text-sm">Álgebra</p>
                <div className="h-2 bg-gray-200 rounded">
                  <div className="h-2 bg-purple-400 rounded w-[60%]" />
                </div>
              </div>
            </div>

            <p className="text-sm text-gray-600 mt-4 mb-2">Actividad Semanal</p>
            <div className="flex gap-1 items-end h-20">
              {[80, 60, 70, 90, 100, 60, 85].map((val, i) => (
                <div
                  key={i}
                  className="bg-pink-500 w-10 rounded-t"
                  style={{ height: `${val}%` }}
                />
              ))}
            </div>
            <div className="flex justify-between text-xs mt-1 text-gray-500">
              <span>L</span><span>M</span><span>M</span><span>J</span><span>V</span><span>S</span><span>D</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default TeacherDashboardComponent
