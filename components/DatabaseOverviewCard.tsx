import React from 'react';
import type { TableSourceFilter } from '../types';

interface DatabaseOverviewCardProps {
  tableSource: TableSourceFilter;
  onClick?: () => void;
  isSelected?: boolean;
}

export const DatabaseOverviewCard: React.FC<DatabaseOverviewCardProps> = ({
  tableSource,
  onClick,
  isSelected = false
}) => {
  return (
    <div
      className={`p-4 rounded-lg border transition-all cursor-pointer ${
        isSelected
          ? 'bg-blue-600/20 border-blue-500/50 text-blue-300'
          : 'bg-slate-800/50 border-slate-700 hover:bg-slate-700/50 text-slate-300'
      }`}
      onClick={onClick}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-semibold text-sm">{tableSource.label}</h3>
        <span className="text-xs bg-slate-600 px-2 py-1 rounded">
          {tableSource.count}
        </span>
      </div>
      <div className="text-xs text-slate-400">
        {tableSource.value}
      </div>
    </div>
  );
};
