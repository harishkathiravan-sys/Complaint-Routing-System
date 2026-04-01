import { CheckCircle, Circle } from 'lucide-react';

export default function StatusBar({ currentStage, stages }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="font-semibold text-gray-900 mb-6">Complaint Progress</h3>
      
      <div className="flex items-center justify-between">
        {stages.map((stage, index) => {
          const stageNumber = index + 1;
          const isCompleted = stageNumber < currentStage;
          const isActive = stageNumber === currentStage;
          const isPending = stageNumber > currentStage;

          return (
            <div key={index} className="flex items-center flex-1">
              {/* Stage Circle */}
              <div className="flex flex-col items-center flex-1">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors ${
                    isCompleted
                      ? 'bg-green-500 text-white'
                      : isActive
                      ? 'bg-blue-500 text-white ring-2 ring-blue-300'
                      : 'bg-gray-300 text-gray-700'
                  }`}
                >
                  {isCompleted ? (
                    <CheckCircle className="w-6 h-6" />
                  ) : (
                    stageNumber
                  )}
                </div>
                <p className="text-xs text-center mt-2 text-gray-700 font-medium max-w-20">
                  {stage}
                </p>
              </div>

              {/* Connector Line (not on last stage) */}
              {index < stages.length - 1 && (
                <div
                  className={`h-1 flex-1 mx-2 transition-colors ${
                    isCompleted ? 'bg-green-500' : 'bg-gray-300'
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* Progress Percentage */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Progress</span>
          <span className="text-sm font-bold text-blue-600">
            {Math.round((currentStage / stages.length) * 100)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(currentStage / stages.length) * 100}%` }}
          />
        </div>
      </div>
    </div>
  );
}
