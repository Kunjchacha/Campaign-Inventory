import React from 'react';
import type { Status } from '../types';

interface PieChartProps {
    title: string;
    data: {
        name: Status;
        value: number;
        color: string;
    }[];
}

export const PieChart: React.FC<PieChartProps> = ({ title, data }) => {
    const totalValue = data.reduce((acc, d) => acc + d.value, 0);
    let cumulativePercent = 0;

    const radius = 85;
    const circumference = 2 * Math.PI * radius;

    // Filter out slices with zero value
    const visibleData = data.filter(d => d.value > 0);

    return (
        <div className="bg-slate-800/70 border border-slate-700 rounded-lg p-6 h-full">
            <h2 className="text-xl font-bold text-slate-100 mb-6 text-center">{title}</h2>
            <div className="flex flex-col items-center justify-center gap-6">
                <div className="relative w-48 h-48">
                    <svg viewBox="0 0 200 200" className="-rotate-90">
                        {visibleData.map((slice) => {
                            const percent = totalValue > 0 ? (slice.value / totalValue) * 100 : 0;
                            const offset = circumference - (cumulativePercent / 100) * circumference;
                            const dashArray = (percent / 100) * circumference;
                            cumulativePercent += percent;

                            return (
                                <circle
                                    key={slice.name}
                                    r={radius}
                                    cx="100"
                                    cy="100"
                                    fill="transparent"
                                    stroke={slice.color}
                                    strokeWidth="32"
                                    strokeDasharray={`${dashArray} ${circumference - dashArray}`}
                                    strokeDashoffset={-offset}
                                    className="transition-all duration-300"
                                />
                            );
                        })}
                    </svg>
                </div>
                <div className="flex items-center justify-center space-x-6">
                    {data.map((slice) => (
                        <div key={slice.name} className="flex items-center space-x-2">
                            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: slice.color }}></div>
                            <span className="text-sm text-slate-400">{slice.name}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};