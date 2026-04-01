import { useNavigate } from 'react-router-dom';
import authService from '../services/auth';
import { LogOut, Menu, X } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const user = authService.getCurrentUser();

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  const isStudent = user?.role === 'student';

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div 
            onClick={() => navigate(isStudent ? '/student/dashboard' : '/faculty/dashboard')}
            className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition"
          >
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <div className="hidden sm:block">
              <p className="font-bold text-gray-900 text-sm">Complaint System</p>
              <p className="text-xs text-gray-600">Karunya</p>
            </div>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <div className="text-sm">
              <p className="text-gray-600">{isStudent ? 'Student' : 'Faculty'}</p>
              <p className="font-medium text-gray-900">{user?.email}</p>
            </div>

            {isStudent && (
              <button
                onClick={() => navigate('/student/complaint/new')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-medium"
              >
                Submit Complaint
              </button>
            )}

            <button
              onClick={handleLogout}
              className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition"
              title="Logout"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            {mobileMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200 py-4 space-y-4">
            <div className="px-4">
              <p className="text-sm text-gray-600">{isStudent ? 'Student' : 'Faculty'}</p>
              <p className="font-medium text-gray-900">{user?.email}</p>
            </div>

            {isStudent && (
              <button
                onClick={() => {
                  navigate('/student/complaint/new');
                  setMobileMenuOpen(false);
                }}
                className="w-full mx-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition text-sm font-medium"
              >
                Submit Complaint
              </button>
            )}

            <button
              onClick={handleLogout}
              className="w-full mx-4 px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition text-sm font-medium flex items-center justify-center gap-2"
            >
              <LogOut className="w-4 h-4" /> Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
