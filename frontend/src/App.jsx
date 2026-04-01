import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import authService from './services/auth';

// Pages
import LoginPage from './pages/LoginPage';
import StudentDashboard from './pages/StudentDashboard';
import FacultyDashboard from './pages/FacultyDashboard';
import ComplaintForm from './pages/ComplaintForm';
import ComplaintStatus from './pages/ComplaintStatus';
import NotFound from './pages/NotFound';

// Components
import Navbar from './components/Navbar';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on app load
    const currentUser = authService.getCurrentUser();
    setUser(currentUser);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  const ProtectedRoute = ({ children, requiredRole }) => {
    if (!user) {
      return <Navigate to="/" replace />;
    }

    if (requiredRole && user.role !== requiredRole) {
      return <Navigate to="/" replace />;
    }

    return children;
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {user && <Navbar />}
        <main>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={!user ? <LoginPage setUser={setUser} /> : <Navigate to={user.role === 'student' ? '/student/dashboard' : '/faculty/dashboard'} />} />

            {/* Student Routes */}
            <Route
              path="/student/dashboard"
              element={
                <ProtectedRoute requiredRole="student">
                  <StudentDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/complaint/new"
              element={
                <ProtectedRoute requiredRole="student">
                  <ComplaintForm />
                </ProtectedRoute>
              }
            />
            <Route
              path="/student/complaint/:id/status"
              element={
                <ProtectedRoute requiredRole="student">
                  <ComplaintStatus />
                </ProtectedRoute>
              }
            />

            {/* Faculty Routes */}
            <Route
              path="/faculty/dashboard"
              element={
                <ProtectedRoute requiredRole="faculty">
                  <FacultyDashboard />
                </ProtectedRoute>
              }
            />

            {/* 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
