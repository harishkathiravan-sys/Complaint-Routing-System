import { useNavigate } from 'react-router-dom';
import { ChevronRight, MessageCircle, Calendar } from 'lucide-react';

const statusColors = {
  'Submitted': 'bg-yellow-100 text-yellow-800',
  'Sent to Department': 'bg-blue-100 text-blue-800',
  'Read by Faculty': 'bg-purple-100 text-purple-800',
  'Resolved': 'bg-green-100 text-green-800',
};

const priorityColors = {
  'low': 'text-gray-600',
  'medium': 'text-orange-600',
  'high': 'text-red-600',
};

export default function ComplaintCard({ complaint, userRole = 'student' }) {
  const navigate = useNavigate();

  const handleClick = () => {
    if (userRole === 'student') {
      navigate(`/student/complaint/${complaint.complaint_id}/status`);
    } else {
      // Faculty view would be different
      console.log('View complaint details');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-IN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div
      onClick={handleClick}
      className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 cursor-pointer hover:bg-gray-50"
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="font-semibold text-gray-900">{complaint.complaint_id}</h3>
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[complaint.status]}`}>
              {complaint.status}
            </span>
          </div>
          <p className="text-sm text-gray-600 mb-2">{complaint.department.code}</p>
        </div>
        <ChevronRight className="w-5 h-5 text-gray-400" />
      </div>

      <p className="text-gray-700 mb-4 line-clamp-2">{complaint.complaint_text}</p>

      <div className="flex items-center justify-between text-xs text-gray-600">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            {formatDate(complaint.created_at)}
          </div>
          {complaint.reply_count > 0 && (
            <div className="flex items-center gap-1">
              <MessageCircle className="w-4 h-4" />
              {complaint.reply_count} {complaint.reply_count === 1 ? 'reply' : 'replies'}
            </div>
          )}
        </div>
        <span className={`font-medium capitalize ${priorityColors[complaint.priority]}`}>
          {complaint.priority}
        </span>
      </div>
    </div>
  );
}
