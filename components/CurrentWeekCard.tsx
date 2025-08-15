import React from 'react';

interface CurrentWeekData {
  brand: string;
  total_slots: number;
  booked_slots: number;
  booked_percentage: number;
}

interface CurrentWeekCardProps {
  data: CurrentWeekData[];
  isLoading: boolean;
}

export const CurrentWeekCard: React.FC<CurrentWeekCardProps> = ({ data, isLoading }) => {
  // Debug logging
  console.log('CurrentWeekCard render:', { data, isLoading, dataLength: data?.length });
  
  if (isLoading) {
    console.log('CurrentWeekCard: Loading state');
    return (
      <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">Current Week Inventory</h3>
        <div className="animate-pulse">
          <div className="h-4 bg-slate-600 rounded mb-2"></div>
          <div className="h-4 bg-slate-600 rounded mb-2"></div>
          <div className="h-4 bg-slate-600 rounded"></div>
        </div>
      </div>
    );
  }

  const totalSlots = data.reduce((sum, item) => sum + item.total_slots, 0);
  const totalBooked = data.reduce((sum, item) => sum + item.booked_slots, 0);
  const overallPercentage = totalSlots > 0 ? ((totalBooked / totalSlots) * 100).toFixed(1) : '0.0';

  console.log('CurrentWeekCard: Rendered with data', { totalSlots, totalBooked, overallPercentage, data });

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-slate-200 mb-4">Current Week Inventory</h3>
      
      {/* Overall Summary */}
      <div className="mb-6 p-4 bg-slate-700/30 rounded-lg border border-slate-600">
        <div className="flex justify-between items-center">
          <div>
            <p className="text-sm text-slate-400">Total Slots This Week</p>
            <p className="text-2xl font-bold text-blue-400">{totalSlots}</p>
          </div>
          <div>
            <p className="text-sm text-slate-400">Booked</p>
            <p className="text-2xl font-bold text-green-400">{totalBooked}</p>
          </div>
          <div>
            <p className="text-sm text-slate-400">Booked %</p>
            <p className="text-2xl font-bold text-purple-400">{overallPercentage}%</p>
          </div>
        </div>
      </div>

      {/* Brand Breakdown */}
      <div className="space-y-3">
        {data.map((item) => (
          <div key={item.brand} className="flex justify-between items-center p-3 bg-slate-700/30 rounded-lg border border-slate-600">
            <div className="flex-1">
              <p className="font-medium text-slate-200">{item.brand}</p>
              <p className="text-sm text-slate-400">
                {item.booked_slots} of {item.total_slots} slots booked
              </p>
            </div>
            <div className="text-right">
              <p className="text-lg font-semibold text-slate-200">
                {item.booked_percentage}%
              </p>
              <div className="w-16 h-2 bg-slate-600 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-green-500 rounded-full"
                  style={{ width: `${Math.min(item.booked_percentage, 100)}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {data.length === 0 && (
        <p className="text-slate-400 text-center py-4">No current week data available</p>
      )}
    </div>
  );
};
