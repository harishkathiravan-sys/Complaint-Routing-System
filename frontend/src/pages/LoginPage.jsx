import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { studentApi, facultyApi } from '../services/api';
import authService from '../services/auth';
import { LogIn, AlertCircle } from 'lucide-react';

export default function LoginPage({ setUser }) {
  const navigate = useNavigate();
  const [loginType, setLoginType] = useState('student'); // student or faculty
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [fullName, setFullName] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let response;
      if (loginType === 'student') {
        response = await studentApi.login(email, password);
      } else {
        response = await facultyApi.login(email, password);
      }

      const { access_token, user_id, role } = response.data;
      const userData = {
        user_id,
        email,
        role
      };

      authService.login(access_token, userData);
      setUser(userData);

      // Redirect based on role
      navigate(role === 'student' ? '/student/dashboard' : '/faculty/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (loginType !== 'student') {
        setError('Only students can register. Faculty accounts are pre-configured.');
        setLoading(false);
        return;
      }

      const response = await studentApi.register(email, password, fullName);
      const { access_token, user_id, role } = response.data;

      const userData = {
        user_id,
        email,
        role
      };

      authService.login(access_token, userData);
      setUser(userData);
      navigate('/student/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-full mb-4">
            <LogIn className="w-8 h-8 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">
            Smart Complaint Routing
          </h1>
          <p className="text-blue-100">Karunya Institute of Technology</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          {/* Tab Selection */}
          <div className="flex gap-2 mb-6 bg-gray-100 p-1 rounded-lg">
            <button
              onClick={() => {
                setLoginType('student');
                setShowRegister(false);
                setError('');
              }}
              className={`flex-1 py-2 px-4 rounded transition-colors font-medium ${
                loginType === 'student'
                  ? 'bg-blue-600 text-white'
                  : 'bg-transparent text-gray-700 hover:bg-gray-200'
              }`}
            >
              Student
            </button>
            <button
              onClick={() => {
                setLoginType('faculty');
                setShowRegister(false);
                setError('');
              }}
              className={`flex-1 py-2 px-4 rounded transition-colors font-medium ${
                loginType === 'faculty'
                  ? 'bg-blue-600 text-white'
                  : 'bg-transparent text-gray-700 hover:bg-gray-200'
              }`}
            >
              Faculty
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-2">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0" />
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          {/* Registration Toggle */}
          {loginType === 'student' && (
            <div className="text-center mb-6">
              <p className="text-sm text-gray-600">
                {showRegister ? 'Already have an account?' : "Don't have an account?"}{' '}
                <button
                  onClick={() => {
                    setShowRegister(!showRegister);
                    setError('');
                  }}
                  className="text-blue-600 font-medium hover:underline"
                >
                  {showRegister ? 'Login' : 'Register'}
                </button>
              </p>
            </div>
          )}

          {/* Form */}
          <form onSubmit={showRegister ? handleRegister : handleLogin} className="space-y-4">
            {showRegister && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Full Name
                </label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="input-field"
                  placeholder="John Doe"
                  required
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input-field"
                placeholder={
                  loginType === 'student'
                    ? 'john@karunya.edu.in'
                    : 'cse@karunya.edu'
                }
                required
              />
              {loginType === 'student' && !showRegister && (
                <p className="text-xs text-gray-500 mt-1">
                  Must end with @karunya.edu.in
                </p>
              )}
              {loginType === 'faculty' && !showRegister && (
                <p className="text-xs text-gray-500 mt-1">
                  Must end with @karunya.edu (e.g., cse@karunya.edu)
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field"
                placeholder={
                  showRegister ? 'Enter strong password' : loginType === 'student' ? 'URK25CSXXXX' : 'admin123'
                }
                required
              />
              {loginType === 'student' && !showRegister && (
                <p className="text-xs text-gray-500 mt-1">
                  Format: URK25CSXXXX (your roll number)
                </p>
              )}
              {loginType === 'faculty' && !showRegister && (
                <p className="text-xs text-gray-500 mt-1">
                  Default password: admin123
                </p>
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 rounded-lg font-medium transition-colors ${
                loading
                  ? 'bg-gray-400 text-white cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {loading ? 'Processing...' : showRegister ? 'Register' : 'Login'}
            </button>
          </form>

          {/* Help Text */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <p className="text-xs text-gray-600 mb-3 font-medium">Demo Accounts:</p>
            <div className="space-y-2 text-xs text-gray-600">
              {loginType === 'student' ? (
                <>
                  <p><strong>Student:</strong> Create account or use any @karunya.edu.in email</p>
                </>
              ) : (
                <>
                  <p><strong>Email:</strong> cse@karunya.edu</p>
                  <p><strong>Password:</strong> admin123</p>
                  <p className="mt-2">Other departments: it@karunya.edu, electrical@karunya.edu, plumbing@karunya.edu, administration@karunya.edu</p>
                </>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-blue-100 text-sm">
          <p>An intelligent complaint management system powered by NLP</p>
        </div>
      </div>
    </div>
  );
}
