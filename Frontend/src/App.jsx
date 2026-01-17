import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import CitiesPage from './pages/CitiesPage';
import DashboardPage from './pages/DashboardPage';
import SimulationPage from './pages/SimulationPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/cities" element={<CitiesPage />} />
        <Route path="/dashboard/:cityId" element={<DashboardPage />} />
        <Route path="/simulation" element={<SimulationPage />} />
      </Routes>
    </Router>
  )
}

export default App
