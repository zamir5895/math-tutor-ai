
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Login from "./Pages/Login"
import StudentDashboard from "./Pages/StudentDashboard"
function App() {

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/student-dashboard" element={<StudentDashboard/>} />
        </Routes>

      </Router>
    </>
  )
}

export default App
