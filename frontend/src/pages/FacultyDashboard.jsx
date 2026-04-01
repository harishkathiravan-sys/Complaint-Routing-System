import { useState, useEffect } from 'react';
import { facultyApi } from '../services/api';
import ComplaintCard from '../components/ComplaintCard';
import FacultyComplaintModal from '../components/FacultyComplaintModal'; 
import { FileText, AlertCircle, CheckCircle, Eye } from 'lucide-react';

export default function FacultyDashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedComplaint, setSelectedComplaint] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      const response = await facultyApi.getDashboard();
      setDashboard(response.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load dashboard');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleComplaintClick = async (complaint) => {
    try {
      const response = await facultyApi.getComplaintDetails(complaint.complaint_id);
      setSelectedComplaint(response.data);
      setShowModal(true);
    } catch (err) {
      setError('Failed to load complaint details');
    }
  };

  const handleModalClose = () => {
    setShowModal(false);
    setSelectedComplaint(null);
    fetchDashboard(); // Refresh dashboard
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading dashboard...</p>
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

  const { profile, total_complaints, pending_complaints, resolved_complaints, unread_complaints, complaints } = dashboard;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          {profile.department.name} Department
        </h1>
        <p className="text-gray-600 mt-1">Manage and respond to student complaints</p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Total Complaints</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{total_complaints}</p>
            </div>
            <FileText className="w-10 h-10 text-blue-600 opacity-50" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Unread</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{unread_complaints}</p>
            </div>
            <Eye className="w-10 h-10 text-red-600 opacity-50" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-600">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Pending</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{pending_complaints}</p>
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

      {/* Complaints List */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Complaints</h2>

        {complaints.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600">No complaints for your department yet</p>
          </div>
        ) : (
          <div className="space-y-4">
            {complaints.map((complaint) => (
              <div
                key={complaint.id}
                onClick={() => handleComplaintClick(complaint)}
                className="cursor-pointer"
              >
                <ComplaintCard complaint={complaint} userRole="faculty" />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && selectedComplaint && (
        <FacultyComplaintModal
          complaint={selectedComplaint}
          onClose={handleModalClose}
          onUpdate={fetchDashboard}
        />
      )}
    </div>
  );
}
