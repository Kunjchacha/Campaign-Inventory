import React, { useState, useMemo, useCallback } from 'react';
import { inventoryData, products, brands, statusStyles } from './constants';
import type { InventoryItem, Status, DatabaseInventoryItem, CampaignLedgerItem, TableSourceFilter } from './types';
import { ClientsModal } from './components/ClientsModal';
import { BrandOverviewCard } from './components/BrandOverviewCard';
import { ProductDetailCard } from './components/ProductDetailCard';
import { PieChart } from './components/PieChart';
import { DatabaseOverviewCard } from './components/DatabaseOverviewCard';
import { useDatabase } from './hooks/useDatabase';

const formatDateForInput = (date: Date): string => {
    return date.toISOString().split('T')[0];
};

export const App = () => {
  const [selectedBrand, setSelectedBrand] = useState('All');
  const [selectedProduct, setSelectedProduct] = useState('Overall');
  const [isClientsModalOpen, setClientsModalOpen] = useState(false);
  const [selectedTableSource, setSelectedTableSource] = useState<string>('All');

  // Date filter state
  const [filterStartDate, setFilterStartDate] = useState<string>('');
  const [filterEndDate, setFilterEndDate] = useState<string>('');
  const [quickView, setQuickView] = useState('custom');
  const [appliedDateRange, setAppliedDateRange] = useState<{ start: string; end: string } | null>(null);
  const [dateError, setDateError] = useState<string>('');

  // Use the database hook
  const { inventoryData: databaseInventory, isLoading, error } = useDatabase();

  // Fetch data on component mount
  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       setIsLoading(true);
  //       const [inventoryData, ledgerData] = await Promise.all([
  //         postgresService.fetchInventoryData(),
  //         postgresService.fetchCampaignLedger()
  //       ]);
  //       setDatabaseInventory(inventoryData);
  //       setCampaignLedger(ledgerData);
  //     } catch (error) {
  //       console.error('Error fetching data:', error);
  //     } finally {
  //       setIsLoading(false);
  //     }
  //   };

  //   fetchData();
  // }, []);

  const handleApplyDateFilter = useCallback(() => {
    if (!filterStartDate || !filterEndDate) {
      setDateError('Please select both a start and end date.');
      return;
    }
    if (new Date(filterStartDate) > new Date(filterEndDate)) {
      setDateError('Start date cannot be after end date.');
      setAppliedDateRange(null);
      return;
    }
    setDateError('');
    setAppliedDateRange({ start: filterStartDate, end: filterEndDate });
  }, [filterStartDate, filterEndDate]);
  
  const handleClearDateFilter = useCallback(() => {
      setFilterStartDate('');
      setFilterEndDate('');
      setAppliedDateRange(null);
      setDateError('');
      setQuickView('custom');
  }, []);

  const handleQuickViewChange = useCallback((view: string) => {
    setQuickView(view);
    
    if (view === 'custom') return;

    const now = new Date();
    let startDate: Date;
    let endDate: Date;

    const currentYear = now.getFullYear();
    const currentMonth = now.getMonth(); // 0-11
    const currentQuarter = Math.floor(currentMonth / 3); // 0-3

    switch (view) {
        case 'current_month':
            startDate = new Date(currentYear, currentMonth, 1);
            endDate = new Date(currentYear, currentMonth + 1, 0);
            break;
        case 'next_month':
            startDate = new Date(currentYear, currentMonth + 1, 1);
            endDate = new Date(currentYear, currentMonth + 1, 2, 0);
            break;
        case 'current_quarter':
            startDate = new Date(currentYear, currentQuarter * 3, 1);
            endDate = new Date(currentYear, currentQuarter * 3 + 3, 0);
            break;
        case 'next_quarter':
            const nextQuarterStartMonth = (currentQuarter * 3 + 3);
            startDate = new Date(currentYear, nextQuarterStartMonth, 1);
            endDate = new Date(currentYear, nextQuarterStartMonth + 3, 0);
            break;
        case 'current_year':
            startDate = new Date(currentYear, 0, 1);
            endDate = new Date(currentYear, 11, 31);
            break;
        case 'next_year':
            startDate = new Date(currentYear + 1, 0, 1);
            endDate = new Date(currentYear + 1, 11, 31);
            break;
        default:
            return;
    }
    
    setFilterStartDate(formatDateForInput(startDate));
    setFilterEndDate(formatDateForInput(endDate));
    setDateError('');
  }, []);

  const handleManualDateChange = (dateStr: string, type: 'start' | 'end') => {
    setQuickView('custom');
    if (type === 'start') {
        setFilterStartDate(dateStr);
    } else {
        setFilterEndDate(dateStr);
    }
  };

  // Filter database inventory based on selections
  const filteredDatabaseInventory = useMemo(() => {
    let filtered = databaseInventory;

    if (selectedBrand !== 'All') {
      filtered = filtered.filter(item => item.brand === selectedBrand);
    }

    if (selectedProduct !== 'Overall') {
      filtered = filtered.filter(item => item.product === selectedProduct);
    }

    if (selectedTableSource !== 'All') {
      filtered = filtered.filter(item => item.table_source === selectedTableSource);
    }

    if (appliedDateRange) {
      const { start, end } = appliedDateRange;
      const rangeStart = new Date(start + 'T00:00:00');
      const rangeEnd = new Date(end + 'T00:00:00');

      filtered = filtered.filter(item => {
        const itemStart = new Date(item.start_date + 'T00:00:00');
        const itemEnd = new Date(item.end_date + 'T00:00:00');
        return itemStart <= rangeEnd && itemEnd >= rangeStart;
      });
    }

    return filtered;
  }, [databaseInventory, selectedBrand, selectedProduct, selectedTableSource, appliedDateRange]);

  // Calculate database statistics
  const databaseStats = useMemo(() => {
    const stats = {
      totalSlots: filteredDatabaseInventory.length,
      bookedSlots: filteredDatabaseInventory.filter(item => item.status === 'Booked').length,
      onHoldSlots: filteredDatabaseInventory.filter(item => item.status === 'On Hold').length,
      availableSlots: filteredDatabaseInventory.filter(item => item.status === 'Available').length
    };

    // Create table source filters
    const tableSources: TableSourceFilter[] = [
      'aa_inventory',
      'bob_inventory', 
      'cfo_inventory',
      'cz_inventory',
      'gt_inventory',
      'hrd_inventory',
      'sew_inventory'
    ].map(source => {
      const count = databaseInventory.filter(item => item.table_source === source).length;
      return {
        label: source.replace('_', ' ').toUpperCase(),
        value: source,
        count
      };
    });

    return { ...stats, tableSources };
  }, [filteredDatabaseInventory, databaseInventory]);

  // Get available brands and products from database
  const availableBrands = useMemo(() => {
    const brands = [...new Set(databaseInventory.map(item => item.brand))];
    return brands.sort();
  }, [databaseInventory]);

  const availableProducts = useMemo(() => {
    const products = [...new Set(databaseInventory.map(item => item.product))];
    return products.sort();
  }, [databaseInventory]);

  const dateFilteredInventory = useMemo(() => {
    if (!appliedDateRange) {
        return inventoryData;
    }
    const { start, end } = appliedDateRange;
    const rangeStart = new Date(start + 'T00:00:00');
    const rangeEnd = new Date(end + 'T00:00:00');

    if (isNaN(rangeStart.getTime()) || isNaN(rangeEnd.getTime())) {
        return inventoryData;
    }

    return inventoryData.filter(item => {
        const itemStart = new Date(item.startDate + 'T00:00:00');
        const itemEnd = new Date(item.endDate + 'T00:00:00');
        return itemStart <= rangeEnd && itemEnd >= rangeStart;
    });
  }, [appliedDateRange]);

  const brandStats = useMemo(() => {
    const statsByBrand: Record<string, { booked: number, onHold: number, available: number, total: number }> = {};
    brands.forEach(brand => {
        statsByBrand[brand] = { booked: 0, onHold: 0, available: 0, total: 0 };
    });

    dateFilteredInventory.forEach(item => {
        if(statsByBrand[item.brand]){
            statsByBrand[item.brand].total++;
            if(item.status === 'Booked') statsByBrand[item.brand].booked++;
            else if(item.status === 'On Hold') statsByBrand[item.brand].onHold++;
            else if(item.status === 'Available') statsByBrand[item.brand].available++;
        }
    });
    return statsByBrand;
  }, [dateFilteredInventory]);

  const filteredStats = useMemo(() => {
    let filteredData = dateFilteredInventory;

    if (selectedProduct !== 'Overall') {
        filteredData = filteredData.filter(item => item.product === selectedProduct);
    }
    if (selectedBrand !== 'All') {
        filteredData = filteredData.filter(item => item.brand === selectedBrand);
    }

    const stats = {
        booked: filteredData.filter(i => i.status === 'Booked').length,
        onHold: filteredData.filter(i => i.status === 'On Hold').length,
        available: filteredData.filter(i => i.status === 'Available').length,
        total: filteredData.length
    };
    return stats;
  }, [selectedProduct, selectedBrand, dateFilteredInventory]);

  const chartData = useMemo(() => [
      { name: 'Booked' as Status, value: filteredStats.booked, color: statusStyles.Booked.colorHex },
      { name: 'On Hold' as Status, value: filteredStats.onHold, color: statusStyles['On Hold'].colorHex },
      { name: 'Available' as Status, value: filteredStats.available, color: statusStyles.Available.colorHex },
  ], [filteredStats]);

  const isOverallView = selectedProduct === 'Overall';

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading database data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">Error loading data</div>
          <p className="text-slate-400">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-4 sm:p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-6 flex flex-col sm:flex-row justify-between items-center gap-4">
          <h1 className="text-3xl font-bold text-slate-100">Campaign Inventory Dashboard</h1>
          <div className="flex items-center gap-2">
            <button 
              onClick={() => setClientsModalOpen(true)}
              className="bg-slate-700 hover:bg-slate-600 text-white font-bold py-2 px-4 rounded-lg transition-colors flex items-center gap-2 text-sm border border-slate-600">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" /></svg>
                Clients
            </button>
          </div>
        </header>

        {/* Database Overview Section */}
        <section className="mb-8">
          <h2 className="text-xl font-bold text-slate-100 mb-4">Database Tables Overview</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
            {databaseStats.tableSources.map((tableSource) => (
              <DatabaseOverviewCard
                key={tableSource.value}
                tableSource={tableSource}
                isSelected={selectedTableSource === tableSource.value}
                onClick={() => setSelectedTableSource(selectedTableSource === tableSource.value ? 'All' : tableSource.value)}
              />
            ))}
          </div>
        </section>

        {/* Database Statistics */}
        <section className="mb-8 p-4 bg-slate-800/50 border border-slate-700 rounded-lg">
          <h2 className="text-lg font-semibold text-slate-100 mb-4">Database Statistics</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">{databaseStats.totalSlots}</div>
              <div className="text-sm text-slate-400">Total Slots</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">{databaseStats.bookedSlots}</div>
              <div className="text-sm text-slate-400">Booked</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-400">{databaseStats.onHoldSlots}</div>
              <div className="text-sm text-slate-400">On Hold</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-slate-400">{databaseStats.availableSlots}</div>
              <div className="text-sm text-slate-400">Available</div>
            </div>
          </div>
        </section>

        {/* --- Unified Filters --- */}
        <section className="mb-8 p-4 bg-slate-800/50 border border-slate-700 rounded-lg">
            <div className="flex flex-wrap items-end gap-x-6 gap-y-4">
                {/* View Dropdown */}
                <div className="flex-grow" style={{minWidth: '150px'}}>
                    <label htmlFor="view-filter" className="block text-xs font-medium text-slate-400 mb-1">View</label>
                    <select
                        id="view-filter"
                        value={quickView}
                        onChange={(e) => handleQuickViewChange(e.target.value)}
                        className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="custom">Custom</option>
                        <option value="current_month">Current Month</option>
                        <option value="next_month">Next Month</option>
                        <option value="current_quarter">Current Quarter</option>
                        <option value="next_quarter">Next Quarter</option>
                        <option value="current_year">Current Year</option>
                        <option value="next_year">Next Year</option>
                    </select>
                </div>

                {/* Products Dropdown */}
                 <div className="flex-grow" style={{minWidth: '150px'}}>
                    <label htmlFor="product-filter" className="block text-xs font-medium text-slate-400 mb-1">Products</label>
                    <select 
                        id="product-filter"
                        value={selectedProduct}
                        onChange={(e) => setSelectedProduct(e.target.value)}
                        className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="Overall">Overall</option>
                        {availableProducts.map(p => <option key={p} value={p}>{p}</option>)}
                    </select>
                </div>
                
                {/* Brand Dropdown */}
                 <div className="flex-grow" style={{minWidth: '150px'}}>
                     <label htmlFor="brand-filter" className="block text-xs font-medium text-slate-400 mb-1">Brand</label>
                    <select 
                        id="brand-filter"
                        value={selectedBrand}
                        onChange={(e) => setSelectedBrand(e.target.value)}
                        className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="All">All Brands</option>
                        {availableBrands.map(b => <option key={b} value={b}>{b}</option>)}
                    </select>
                </div>

                {/* Table Source Filter */}
                <div className="flex-grow" style={{minWidth: '150px'}}>
                    <label htmlFor="table-source-filter" className="block text-xs font-medium text-slate-400 mb-1">Table Source</label>
                    <select 
                        id="table-source-filter"
                        value={selectedTableSource}
                        onChange={(e) => setSelectedTableSource(e.target.value)}
                        className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="All">All Tables</option>
                        {databaseStats.tableSources.map(ts => <option key={ts.value} value={ts.value}>{ts.label}</option>)}
                    </select>
                </div>
                
                {/* Date Inputs */}
                <div className="flex-grow" style={{minWidth: '150px'}}>
                    <label htmlFor="start-date-filter" className="block text-xs font-medium text-slate-400 mb-1">Start Date</label>
                    <input
                        type="date"
                        id="start-date-filter"
                        value={filterStartDate}
                        onChange={e => handleManualDateChange(e.target.value, 'start')}
                        className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                 <div className="flex-grow" style={{minWidth: '150px'}}>
                    <label htmlFor="end-date-filter" className="block text-xs font-medium text-slate-400 mb-1">End Date</label>
                    <input
                        type="date"
                        id="end-date-filter"
                        value={filterEndDate}
                        onChange={e => handleManualDateChange(e.target.value, 'end')}
                        className="w-full bg-slate-700 border border-slate-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                {/* Action Buttons */}
                <div className="flex items-center gap-2">
                    <button
                        onClick={handleApplyDateFilter}
                        className="w-full sm:w-auto bg-blue-600 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded-lg transition-colors">
                        Go
                    </button>
                    {appliedDateRange && (
                         <button
                            onClick={handleClearDateFilter}
                            className="w-full sm:w-auto bg-slate-600 hover:bg-slate-500 text-white font-bold py-2 px-4 rounded-lg transition-colors">
                            Clear
                        </button>
                    )}
                </div>
            </div>
            {dateError && <p className="text-red-400 text-sm mt-2">{dateError}</p>}
        </section>
        
        {isOverallView ? (
            <div>
                 <section className="mb-8">
                    <h2 className="text-xl font-bold text-slate-100 mb-4">
                        Brand Overview {appliedDateRange && <span className="text-base font-normal text-slate-400">- ({appliedDateRange.start} to {appliedDateRange.end})</span>}
                    </h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                        {brands.map(brand => (
                            <BrandOverviewCard 
                                key={brand}
                                brand={brand}
                                stats={brandStats[brand]}
                            />
                        ))}
                    </div>
                </section>
                <section>
                    <PieChart title="Overall Inventory Distribution" data={chartData} />
                </section>
            </div>
        ) : (
            <div>
                <h2 className="text-xl font-bold text-slate-100 mb-4">{selectedProduct} - {selectedBrand === 'All' ? 'All Brands' : selectedBrand}</h2>
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                   <div className="lg:col-span-1">
                        <ProductDetailCard 
                            product={selectedProduct}
                            brand={selectedBrand}
                            stats={filteredStats}
                        />
                   </div>
                   <div className="lg:col-span-2">
                        <PieChart title={`${selectedProduct} Distribution`} data={chartData} />
                   </div>
                </div>
            </div>
        )}
      </div>

      <ClientsModal 
        isOpen={isClientsModalOpen} 
        onClose={() => setClientsModalOpen(false)} 
      />
    </div>
  );
};