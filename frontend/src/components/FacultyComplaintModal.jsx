import { useState } from 'react';
import { facultyApi } from '../services/api';
import { X, Send, CheckCircle, AlertCircle } from 'lucide-react';

const statusColors = {
  'Submitted': 'bg-yellow-100 text-yellow-800',
  'Sent to Department': 'bg-blue-100 text-blue-800',
  'Read by Faculty': 'bg-purple-100 text-purple-800',
  'Resolved': 'bg-green-100 text-green-800',
};

export default function FacultyComplaintModal({ complaint, onClose, onUpdate }) {
  const [replyText, setReplyText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleMarkAsRead = async () => {
    try {
      setLoading(true);
      await facultyApi.markAsRead(complaint.complaint_id);
      setMessage('Marked as read');
      setTimeout(() => {
        setMessage('');
        onUpdate();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to mark as read');
    } finally {
      setLoading(false);
    }
  };

  const handleAddReply = async (e) => {
    e.preventDefault();
    if (!replyText.trim()) {
      setError('Reply cannot be empty');
      return;
    }

    try {
      setLoading(true);
      await facultyApi.addReply(complaint.complaint_id, replyText);
      setMessage('Reply added successfully');
      setReplyText('');
      setTimeout(() => {
        setMessage('');
        onUpdate();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to add reply');
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async () => {
    if (!window.confirm('Are you sure you want to mark this complaint as resolved?')) {
      return;
    }

    try {
      setLoading(true);
      await facultyApi.resolveComplaint(complaint.complaint_id);
      setMessage('Complaint resolved');
      setTimeout(() => {
        setMessage('');
        onClose();
        onUpdate();
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to resolve complaint');
    } finally {
      setLoading(false);
    }
  };

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

  const isResolved = complaint.status === 'Resolved';

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex justify-between items-start">
          <div>
            <h2 className="text-xl font-bold text-gray-900">{complaint.complaint_id}</h2>
            <p className="text-sm text-gray-600 mt-1">{complaint.student_email}</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition"
          >
            <X className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Status */}
          <div>
            <p className="text-sm text-gray-600 font-medium mb-2">Status</p>
            <span className={`px-4 py-2 rounded-full text-sm font-semibold ${statusColors[complaint.status]}`}>
              {complaint.status}
            </span>
          </div>

          {/* Complaint Text */}
          <div>
            <p className="text-sm text-gray-600 font-medium mb-2">Complaint</p>
            <p className="text-gray-700 bg-gray-50 p-4 rounded leading-relaxed">
              {complaint.complaint_text}
            </p>
          </div>

          {/* Messages */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {message && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg flex gap-3">
              <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-green-700">{message}</p>
            </div>
          )}

          {/* Existing Replies */}
          {complaint.replies.length > 0 && (
            <div>
              <p className="text-sm text-gray-600 font-medium mb-3">Previous Responses</p>
              <div className="space-y-3">
                {complaint.replies.map((reply, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded border border-gray-200">
                    <p className="text-xs text-gray-500 mb-2">{formatDate(reply.created_at)}</p>
                    <p className="text-gray-700">{reply.reply_text}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Reply Form */}
          {!isResolved && (
            <form onSubmit={handleAddReply} className="space-y-3">
              <div>
                <label className="block text-sm text-gray-600 font-medium mb-2">
                  Your Response
                </label>
                <textarea
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  placeholder="Enter your response to the student..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none"
                  rows="4"
                  maxLength={2000}
                />
                <p className="text-xs text-gray-500 mt-1">{replyText.length}/2000</p>
              </div>

              <div className="flex gap-3 pt-3 border-t border-gray-200">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 px-4 py-2 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 transition font-medium"
                >
                  Close
                </button>
                <button
                  type="submit"
                  disabled={!replyText.trim() || loading}
                  className={`flex-1 px-4 py-2 rounded-lg transition font-medium flex items-center justify-center gap-2 ${
                    !replyText.trim() || loading
                      ? 'bg-gray-400 text-white cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  <Send className="w-4 h-4" />
                  {loading ? 'Sending...' : 'Send Reply'}
                </button>
              </div>
            </form>
          )}

          {/* Action Buttons */}
          {!isResolved && (
            <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-200">
              {complaint.status !== 'Read by Faculty' && (
                <button
                  onClick={handleMarkAsRead}
                  disabled={loading}
                  className="flex-1 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition font-medium disabled:opacity-50"
                >
                  Mark as Read
                </button>
              )}
              <button
                onClick={handleResolve}
                disabled={loading}
                className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium disabled:opacity-50"
              >
                Mark as Resolved
              </button>
            </div>
          )}

          {isResolved && (
            <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-center">
              <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <p className="text-sm text-green-700 font-medium">This complaint has been resolved</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
