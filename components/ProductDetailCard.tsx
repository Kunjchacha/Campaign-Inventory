import React from 'react';
import { statusStyles } from '../constants';

interface ProductDetailCardProps {
    product: string;
    brand: string;
    stats: {
        booked: number;
        onHold: number;
        available: number;
        total: number;
    }
}

const ProgressBar: React.FC<{ stats: ProductDetailCardProps['stats'] }> = ({ stats }) => {
    const segments = [
        { value: stats.booked, color: statusStyles.Booked.color },
        { value: stats.onHold, color: statusStyles['On Hold'].color },
        { value: stats.available, color: statusStyles.Available.color },
    ];

    return (
        <div className="w-full flex h-2 rounded-full overflow-hidden bg-slate-700">
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

export const ProductDetailCard: React.FC<ProductDetailCardProps> = ({ product, brand, stats }) => {
    const { booked, onHold, available, total } = stats;
    
    return (
        <div className="bg-slate-800/70 p-6 rounded-lg border border-slate-700 flex flex-col gap-6 h-full">
            <div>
                 <h3 className="font-bold text-xl text-slate-100">{product}</h3>
                 <p className="text-sm text-slate-400">{brand === 'All' ? 'All Brands' : brand}</p>
            </div>
            
            <div className="space-y-3">
                <div className="flex justify-between items-center">
                    <span className="text-slate-300">Booked</span>
                    <span className="font-medium text-slate-100">{booked} / {total}</span>
                </div>
                <div className="flex justify-between items-center">
                    <span className="text-slate-300">On Hold</span>
                    <span className="font-medium text-slate-100">{onHold} / {total}</span>
                </div>
                <div className="flex justify-between items-center">
                    <span className="text-slate-300">Available</span>
                    <span className="font-medium text-slate-100">{available} / {total}</span>
                </div>
            </div>

            <ProgressBar stats={stats} />
        </div>
    );
};