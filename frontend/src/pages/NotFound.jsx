import { useNavigate } from 'react-router-dom';
import { AlertCircle } from 'lucide-react';
import authService from '../services/auth';

export default function NotFound() {
  const navigate = useNavigate();
  const user = authService.getCurrentUser();

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-gray-50">
      <div className="text-center">
        <AlertCircle className="w-20 h-20 text-gray-400 mx-auto mb-6" />
        <h1 className="text-4xl font-bold text-gray-900 mb-2">404</h1>
        <p className="text-xl text-gray-600 mb-6">Page not found</p>
        <p className="text-gray-500 mb-8">The page you're looking for doesn't exist or has been moved.</p>

        <button
          onClick={() => {
            if (user) {
              navigate(user.role === 'student' ? '/student/dashboard' : '/faculty/dashboard');
            } else {
              navigate('/');
            }
          }}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
        >
          Go Home
        </button>
      </div>
    </div>
  );
}
