import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { studentApi } from '../services/api';
import StatusBar from '../components/StatusBar';
import { AlertCircle, ArrowLeft, MessageCircle } from 'lucide-react';

export default function ComplaintStatus() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [complaint, setComplaint] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchComplaintStatus();
  }, [id]);

  const fetchComplaintStatus = async () => {
    try {
      setLoading(true);
      const [complaintRes, statusRes] = await Promise.all([
        studentApi.getComplaintDetails(id),
        studentApi.getComplaintStatus(id),
      ]);
      setComplaint(complaintRes.data);
      setStatus(statusRes.data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load complaint details');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading complaint details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3 mb-6">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-900">Error</h3>
            <p className="text-sm text-red-700 mt-1">{error}</p>
            <button
              onClick={fetchComplaintStatus}
              className="mt-2 text-sm text-red-600 hover:text-red-700 font-medium"
            >
              Try Again
            </button>
          </div>
        </div>
        <button
          onClick={() => navigate('/student/dashboard')}
          className="text-blue-600 hover:text-blue-700 font-medium flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Dashboard
        </button>
      </div>
    );
  }

  if (!complaint || !status) {
    return null;
  }

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const statusColors = {
    'Submitted': 'bg-yellow-100 text-yellow-800',
    'Sent to Department': 'bg-blue-100 text-blue-800',
    'Read by Faculty': 'bg-purple-100 text-purple-800',
    'Resolved': 'bg-green-100 text-green-800',
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8 flex items-center gap-4">
        <button
          onClick={() => navigate('/student/dashboard')}
          className="p-2 hover:bg-gray-100 rounded-lg transition"
        >
          <ArrowLeft className="w-6 h-6 text-gray-600" />
        </button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Complaint Details</h1>
          <p className="text-gray-600 mt-1">{complaint.complaint_id}</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Status Bar */}
          <StatusBar currentStage={status.current_stage} stages={status.stages} />

          {/* Complaint Details */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Complaint Details</h2>

            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600 font-medium mb-1">Status</p>
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColors[complaint.status]}`}>
                    {complaint.status}
                  </span>
                </div>
              </div>

              <div>
                <p className="text-sm text-gray-600 font-medium mb-1">Department</p>
                <p className="text-gray-900 font-semibold">{complaint.department.name}</p>
                <p className="text-xs text-gray-500">{complaint.department.code}</p>
              </div>

              <div>
                <p className="text-sm text-gray-600 font-medium mb-1">Complaint Description</p>
                <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded">
                  {complaint.complaint_text}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                <div>
                  <p className="text-xs text-gray-600 font-medium mb-1">Submitted</p>
                  <p className="text-sm text-gray-900">{formatDate(complaint.created_at)}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-600 font-medium mb-1">Last Updated</p>
                  <p className="text-sm text-gray-900">{formatDate(status.last_update)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Faculty Replies */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <MessageCircle className="w-5 h-5" />
              Faculty Responses {complaint.replies.length > 0 && `(${complaint.replies.length})`}
            </h2>

            {complaint.replies.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <p>No responses from faculty yet</p>
                <p className="text-sm mt-1">We'll notify you when your complaint is reviewed</p>
              </div>
            ) : (
              <div className="space-y-4">
                {complaint.replies.map((reply, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <div className="flex justify-between items-start mb-2">
                      <p className="font-semibold text-gray-900">Faculty Response</p>
                      <p className="text-xs text-gray-500">{formatDate(reply.created_at)}</p>
                    </div>
                    <p className="text-gray-700 leading-relaxed">{reply.reply_text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Column - Timeline */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6 sticky top-20">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Timeline</h2>

            <div className="space-y-6">
              {/* Submitted */}
              <div className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-4 h-4 rounded-full bg-blue-600 ring-2 ring-blue-200"></div>
                  <div className="w-0.5 h-12 bg-gray-300 my-2"></div>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 text-sm">Submitted</p>
                  <p className="text-xs text-gray-600 mt-1">{formatDate(complaint.created_at)}</p>
                </div>
              </div>

              {/* Sent to Department */}
              <div className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className={`w-4 h-4 rounded-full ring-2 ${
                    complaint.submitted_to_dept_at ? 'bg-green-600 ring-green-200' : 'bg-gray-300 ring-gray-200'
                  }`}></div>
                  <div className="w-0.5 h-12 bg-gray-300 my-2"></div>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 text-sm">Sent to Department</p>
                  <p className="text-xs text-gray-600 mt-1">
                    {complaint.submitted_to_dept_at ? formatDate(complaint.submitted_to_dept_at) : 'Pending'}
                  </p>
                </div>
              </div>

              {/* Read by Faculty */}
              <div className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className={`w-4 h-4 rounded-full ring-2 ${
                    complaint.read_by_faculty_at ? 'bg-green-600 ring-green-200' : 'bg-gray-300 ring-gray-200'
                  }`}></div>
                  <div className="w-0.5 h-12 bg-gray-300 my-2"></div>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 text-sm">Read by Faculty</p>
                  <p className="text-xs text-gray-600 mt-1">
                    {complaint.read_by_faculty_at ? formatDate(complaint.read_by_faculty_at) : 'Pending'}
                  </p>
                </div>
              </div>

              {/* Resolved */}
              <div className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className={`w-4 h-4 rounded-full ring-2 ${
                    complaint.resolved_at ? 'bg-green-600 ring-green-200' : 'bg-gray-300 ring-gray-200'
                  }`}></div>
                </div>
                <div>
                  <p className="font-semibold text-gray-900 text-sm">Resolved</p>
                  <p className="text-xs text-gray-600 mt-1">
                    {complaint.resolved_at ? formatDate(complaint.resolved_at) : 'Pending'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
