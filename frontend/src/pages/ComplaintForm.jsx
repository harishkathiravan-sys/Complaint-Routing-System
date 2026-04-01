import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { studentApi } from '../services/api';
import { AlertCircle, ArrowLeft, Send, CheckCircle } from 'lucide-react';

export default function ComplaintForm() {
  const navigate = useNavigate();
  const [complaintText, setComplaintText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [submittedComplaint, setSubmittedComplaint] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await studentApi.submitComplaint(complaintText);
      setSubmittedComplaint(response.data);
      setSuccess(true);
      setComplaintText('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit complaint');
    } finally {
      setLoading(false);
    }
  };

  if (success && submittedComplaint) {
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Complaint Submitted Successfully!</h1>
          <p className="text-gray-600 mb-6">Your complaint has been registered and automatically routed to the appropriate department.</p>

          <div className="bg-gray-50 rounded-lg p-6 mb-6 text-left border border-gray-200">
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600 font-medium">Complaint ID</p>
                <p className="text-lg font-bold text-blue-600">{submittedComplaint.complaint_id}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 font-medium">Department</p>
                <p className="font-semibold text-gray-900">{submittedComplaint.department.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 font-medium">Current Status</p>
                <p className="font-semibold text-gray-900">{submittedComplaint.status}</p>
              </div>
            </div>
          </div>

          <p className="text-gray-600 mb-6 text-sm">You can track your complaint from the dashboard. We'll notify you of any updates.</p>

          <div className="flex gap-4 justify-center">
            <button
              onClick={() => navigate(`/student/complaint/${submittedComplaint.complaint_id}/status`)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
            >
              Track Complaint
            </button>
            <button
              onClick={() => navigate('/student/dashboard')}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition font-medium"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  const charCount = complaintText.length;
  const minChars = 10;
  const maxChars = 2000;
  const isValidLength = charCount >= minChars && charCount <= maxChars;

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8 flex items-center gap-4">
        <button
          onClick={() => navigate('/student/dashboard')}
          className="p-2 hover:bg-gray-100 rounded-lg transition"
        >
          <ArrowLeft className="w-6 h-6 text-gray-600" />
        </button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Submit a Complaint</h1>
          <p className="text-gray-600 mt-1">Describe your issue in detail</p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-red-900">Error</p>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Form Card */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Complaint Textarea */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-3">
              Describe Your Complaint
            </label>
            <textarea
              value={complaintText}
              onChange={(e) => setComplaintText(e.target.value)}
              placeholder="Example: The computer lab PCs are not working properly. Many machines won't start up, affecting our practical sessions..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"
              rows="10"
              maxLength={maxChars}
            />

            {/* Character Counter */}
            <div className="mt-2 flex justify-between items-center">
              <p className={`text-sm ${isValidLength ? 'text-gray-600' : 'text-red-600'}`}>
                <span className={charCount < minChars ? 'font-semibold' : ''}>
                  {charCount}
                </span>
                / {maxChars} characters
              </p>
              {charCount < minChars && (
                <p className="text-sm text-red-600">
                  Minimum {minChars} characters required
                </p>
              )}
            </div>
          </div>

          {/* Department Note */}
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-blue-900">
              <span className="font-semibold">Auto-Routing:</span> Your complaint will be automatically classified and routed to the most appropriate department using our NLP system.
            </p>
          </div>

          {/* Example Complaints */}
          <div>
            <p className="text-sm font-semibold text-gray-900 mb-3">Example Complaints:</p>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>• <strong>IT:</strong> WiFi in the hostel is not working</li>
              <li>• <strong>Electrical:</strong> Power supply has been cut off in the classroom</li>
              <li>• <strong>Plumbing:</strong> Water leakage in the bathroom</li>
              <li>• <strong>CSE:</strong> Computer lab systems are malfunctioning</li>
              <li>• <strong>Admin:</strong> Certificate approval is delayed</li>
            </ul>
          </div>

          {/* Submit Button */}
          <div className="flex gap-4 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={() => navigate('/student/dashboard')}
              className="flex-1 px-6 py-3 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={!isValidLength || loading}
              className={`flex-1 px-6 py-3 rounded-lg transition font-medium flex items-center justify-center gap-2 ${
                !isValidLength || loading
                  ? 'bg-gray-400 text-white cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              <Send className="w-5 h-5" />
              {loading ? 'Submitting...' : 'Submit Complaint'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
