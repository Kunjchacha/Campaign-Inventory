import React from 'react';
import { statusStyles } from '../constants';

interface BrandOverviewCardProps {
    brand: string;
    stats: {
        booked: number;
        onHold: number;
        available: number;
        total: number;
    }
}

const ProgressBar: React.FC<{ stats: BrandOverviewCardProps['stats'] }> = ({ stats }) => {
    const segments = [
        { value: stats.booked, color: statusStyles.Booked.color },
        { value: stats.onHold, color: statusStyles['On Hold'].color },
        { value: stats.available, color: statusStyles.Available.color },
    ];

    return (
        <div className="w-full flex h-1.5 rounded-full overflow-hidden bg-slate-700">
            {segments.map((segment, index) => {
                if (segment.value === 0) return null;
                const width = (segment.value / stats.total) * 100;
                return (
                    <div
                        key={index}
                        className={`${segment.color} transition-all duration-300`}
                        style={{ width: `${width}%` }}
                    />
                );
            })}
        </div>
    );
};


export const BrandOverviewCard: React.FC<BrandOverviewCardProps> = ({ brand, stats }) => {
    const { booked, onHold, available, total } = stats;

    const getPercentage = (value: number) => {
        if (total === 0) return 0;
        return Math.round((value / total) * 100);
    }

    return (
        <div className="bg-slate-800/70 p-4 rounded-lg border border-slate-700 flex flex-col gap-4">
            <div className="flex justify-between items-baseline">
                <h3 className="font-bold text-lg text-slate-100">{brand}</h3>
                <span className="text-xs text-slate-400">{total} slots</span>
            </div>
            
            <div className="flex justify-between items-center text-center">
                <div>
                    <p className="font-bold text-2xl text-slate-50">{getPercentage(booked)}%</p>
                    <p className="text-xs text-slate-400">Booked</p>
                </div>
                 <div>
                    <p className="font-bold text-2xl text-slate-50">{getPercentage(onHold)}%</p>
                    <p className="text-xs text-slate-400">On Hold</p>
                </div>
                 <div>
                    <p className="font-bold text-2xl text-slate-50">{getPercentage(available)}%</p>
                    <p className="text-xs text-slate-400">Available</p>
                </div>
            </div>

            <ProgressBar stats={stats} />
        </div>
    )
}