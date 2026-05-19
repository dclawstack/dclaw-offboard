"use client";

interface ProgressTrackerProps {
  percent: number;
}

export function ProgressTracker({ percent }: ProgressTrackerProps) {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-sm font-medium text-gray-700">Completion</span>
        <span className="text-sm font-semibold text-gray-900">{percent}%</span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500 ease-out"
          style={{
            width: `${percent}%`,
            backgroundColor: percent === 100 ? "#10B981" : "#6366F1",
          }}
        />
      </div>
    </div>
  );
}
