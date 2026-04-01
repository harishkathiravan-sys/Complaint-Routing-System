import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { studentApi } from '../services/api';
import ComplaintCard from '../components/ComplaintCard';
import { FileText, AlertCircle, CheckCircle, Plus } from 'lucide-react';

export default function StudentDashboard() {
  const navigate = useNavigate();
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await studentApi.getDashboard();
      setDashboard(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load dashboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading your dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-900">Error</h3>
            <p className="text-sm text-red-700">{error}</p>
            <button
              onClick={fetchDashboard}
              className="mt-2 text-sm text-red-600 hover:text-red-700 font-medium"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!dashboard) {
    return null;
  }

  const { profile, total_complaints, active_complaints, resolved_complaints, recent_complaints } = dashboard;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Welcome, {profile.full_name || profile.email}!
        </h1>
        <p className="text-gray-600 mt-1">Manage and track your complaints</p>
      </div>

      {/* Action Button */}
      <div className="mb-8">
        <button
          onClick={() => navigate('/student/complaint/new')}
          className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
        >
          <Plus className="w-5 h-5" />
          Submit New Complaint
        </button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Total Complaints</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{total_complaints}</p>
            </div>
            <FileText className="w-10 h-10 text-blue-600 opacity-50" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Active Complaints</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{active_complaints}</p>
            </div>
            <AlertCircle className="w-10 h-10 text-yellow-600 opacity-50" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Resolved</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{resolved_complaints}</p>
            </div>
            <CheckCircle className="w-10 h-10 text-green-600 opacity-50" />
          </div>
        </div>
      </div>

      {/* Recent Complaints */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Recent Complaints</h2>

        {recent_complaints.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">No complaints submitted yet</p>
            <button
              onClick={() => navigate('/student/complaint/new')}
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Submit your first complaint
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {recent_complaints.map((complaint) => (
              <ComplaintCard
                key={complaint.id}
                complaint={complaint}
                userRole="student"
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
