import React, { useState, useMemo } from 'react';
import { inventoryData, products, brands } from '../constants';

interface ClientsModalProps {
    isOpen: boolean;
    onClose: () => void;
}

interface ClientBooking {
    product: string;
    startDate: string;
    endDate: string;
}

const isValidDate = (d: Date | null) => d && !isNaN(d.getTime());

export const ClientsModal: React.FC<ClientsModalProps> = ({ isOpen, onClose }) => {
    const [startDate, setStartDate] = useState<Date | null>(null);
    const [endDate, setEndDate] = useState<Date | null>(null);
    const [selectedProduct, setSelectedProduct] = useState('All');
    const [selectedBrand, setSelectedBrand] = useState('All');
    const [dateError, setDateError] = useState<string>('');

    const handleDateChange = (dateString: string, type: 'start' | 'end') => {
        const selectedDate = new Date(dateString + 'T00:00:00');

        if (!isValidDate(selectedDate)) {
            if(type === 'start') setStartDate(null);
            else setEndDate(null);
            setDateError('');
            return;
        }
        
        setDateError('');

        if (type === 'start') {
            if (endDate && selectedDate > endDate) {
                setDateError('Start date cannot be after end date.');
            } else {
                setStartDate(selectedDate);
            }
        } else { // 'end'
             if (startDate && selectedDate < startDate) {
                setDateError('End date cannot be before start date.');
            } else {
                setEndDate(selectedDate);
            }
        }
    };
    
    const clientBookings = useMemo(() => {
        if (!startDate || !endDate) {
            return {};
        }

        const filteredSlots = inventoryData.filter(item => {
            if (item.status !== 'Booked' || !item.client) return false;

            const brandMatch = selectedBrand === 'All' || item.brand === selectedBrand;
            const productMatch = selectedProduct === 'All' || item.product === selectedProduct;
            if (!brandMatch || !productMatch) return false;

            const itemStartDate = new Date(item.startDate + 'T00:00:00');
            const itemEndDate = new Date(item.endDate + 'T00:00:00');

            return itemStartDate <= endDate && itemEndDate >= startDate;
        });

        const bookingsByClient: Record<string, ClientBooking[]> = {};

        filteredSlots.forEach(item => {
            if (item.client) {
                if (!bookingsByClient[item.client]) {
                    bookingsByClient[item.client] = [];
                }
                bookingsByClient[item.client].push({
                    product: item.product,
                    startDate: item.startDate,
                    endDate: item.endDate,
                });
                bookingsByClient[item.client].sort((a, b) => new Date(a.startDate).getTime() - new Date(b.startDate).getTime());
            }
        });
        
        return bookingsByClient;

    }, [startDate, endDate, selectedBrand, selectedProduct]);

    if (!isOpen) return null;

    const getInputValue = (date: Date | null) => date ? date.toISOString().split('T')[0] : '';

    return (
        <div 
          className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4"
          onClick={onClose}
          aria-modal="true"
          role="dialog"
        >
            <div 
              className="bg-slate-800 w-full max-w-2xl rounded-xl shadow-lg border border-slate-700 p-6 sm:p-8 flex flex-col gap-6"
              onClick={e => e.stopPropagation()} // Prevent closing modal on inner click
            >
                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-bold text-slate-100">Find Client Bookings</h2>
                    <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors" aria-label="Close modal">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                </div>
                
                {/* Filters */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Date Filters */}
                    <div>
                        <label htmlFor="start-date" className="block text-sm font-medium text-slate-300 mb-1">Start Date</label>
                        <input 
                            type="date" 
                            id="start-date"
                            value={getInputValue(startDate)}
                            onChange={(e) => handleDateChange(e.target.value, 'start')}
                            className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>
                     <div>
                        <label htmlFor="end-date" className="block text-sm font-medium text-slate-300 mb-1">End Date</label>
                        <input 
                            type="date" 
                            id="end-date"
                            value={getInputValue(endDate)}
                            onChange={(e) => handleDateChange(e.target.value, 'end')}
                            className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </div>

                    {/* Product Filter */}
                    <div>
                        <label htmlFor="modal-product-filter" className="block text-sm font-medium text-slate-300 mb-1">Product</label>
                         <select 
                            id="modal-product-filter"
                            value={selectedProduct}
                            onChange={(e) => setSelectedProduct(e.target.value)}
                            className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="All">All Products</option>
                            {products.map(p => <option key={p} value={p}>{p}</option>)}
                        </select>
                    </div>

                    {/* Brand Filter */}
                    <div>
                        <label htmlFor="modal-brand-filter" className="block text-sm font-medium text-slate-300 mb-1">Brand</label>
                        <select 
                            id="modal-brand-filter"
                            value={selectedBrand}
                            onChange={(e) => setSelectedBrand(e.target.value)}
                            className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="All">All Brands</option>
                            {brands.map(b => <option key={b} value={b}>{b}</option>)}
                        </select>
                    </div>
                </div>
                 {dateError && <p className="text-red-400 text-sm -mt-2">{dateError}</p>}
                
                {/* Results */}
                <div className="bg-slate-900/50 rounded-lg border border-slate-700 min-h-[150px] max-h-[300px] overflow-y-auto p-4">
                     <h3 className="text-lg font-semibold text-slate-200 mb-3">Booked Clients</h3>
                     {(!startDate || !endDate) ? (
                        <p className="text-slate-500">Please select a start and end date to see clients.</p>
                     ) : Object.keys(clientBookings).length > 0 ? (
                        <div className="space-y-4">
                           {Object.entries(clientBookings).map(([client, bookings]) => (
                               <div key={client}>
                                   <h4 className="font-semibold text-slate-200">{client}</h4>
                                   <ul className="list-disc list-inside pl-4 mt-1 space-y-1 text-slate-400 text-sm">
                                      {bookings.map((booking, index) => (
                                         <li key={index}>
                                            <span className="font-medium text-slate-300">{booking.product}:</span> {booking.startDate} to {booking.endDate}
                                         </li>
                                      ))}
                                   </ul>
                               </div>
                           ))}
                        </div>
                     ) : (
                        <p className="text-slate-500">No clients found for the selected criteria.</p>
                     )}
                </div>
            </div>
        </div>
    );
};