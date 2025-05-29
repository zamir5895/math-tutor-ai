
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Login from "./Pages/Login"
import StudentDashboard from "./Pages/StudentDashboard"
import TeacherDashboard from "./Pages/TeacherDashboard"
function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/student-dashboard" element={<StudentDashboard/>} />
          <Route path="/teacher-dashboard" element={<TeacherDashboard/>} />
        </Routes>

      </Router>
    </>
  )
}

export default App
