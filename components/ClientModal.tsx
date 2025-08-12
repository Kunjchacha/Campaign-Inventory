import React from 'react';
import type { CampaignLedgerItem } from '../types';

interface ClientModalProps {
  isOpen: boolean;
  onClose: () => void;
  campaigns: CampaignLedgerItem[];
  selectedBrand: string;
  selectedProduct: string;
  appliedDateRange: { start: string; end: string } | null;
}

export const ClientModal: React.FC<ClientModalProps> = ({
  isOpen,
  onClose,
  campaigns,
  selectedBrand,
  selectedProduct,
  appliedDateRange
}) => {
  if (!isOpen) return null;

  // Filter campaigns based on current selections
  const filteredCampaigns = campaigns.filter(campaign => {
    const brandMatch = selectedBrand === 'All' || campaign.brand === selectedBrand;
    const productMatch = selectedProduct === 'Overall' || campaign.product === selectedProduct;
    
    let dateMatch = true;
    if (appliedDateRange) {
      const campaignStart = new Date(campaign.start_date);
      const campaignEnd = new Date(campaign.end_date);
      const filterStart = new Date(appliedDateRange.start);
      const filterEnd = new Date(appliedDateRange.end);
      
      // Check if campaign overlaps with filter date range
      dateMatch = campaignStart <= filterEnd && campaignEnd >= filterStart;
    }
    
    return brandMatch && productMatch && dateMatch;
  });

  // Group campaigns by client
  const clientGroups = filteredCampaigns.reduce((acc, campaign) => {
    if (!acc[campaign.client]) {
      acc[campaign.client] = [];
    }
    acc[campaign.client].push(campaign);
    return acc;
  }, {} as Record<string, CampaignLedgerItem[]>);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-slate-800 rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-hidden">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-slate-100">Client Overview</h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        {/* Filter Summary */}
        <div className="mb-6 p-4 bg-slate-700/30 rounded-lg">
          <h3 className="font-semibold text-slate-200 mb-2">Current Filters:</h3>
          <div className="flex flex-wrap gap-2 text-sm">
            <span className="bg-blue-500/20 text-blue-300 px-2 py-1 rounded">
              Brand: {selectedBrand}
            </span>
            <span className="bg-green-500/20 text-green-300 px-2 py-1 rounded">
              Product: {selectedProduct}
            </span>
            {appliedDateRange && (
              <span className="bg-yellow-500/20 text-yellow-300 px-2 py-1 rounded">
                Date Range: {appliedDateRange.start} to {appliedDateRange.end}
              </span>
            )}
          </div>
        </div>

        {/* Client List */}
        <div className="overflow-y-auto max-h-96">
          {Object.keys(clientGroups).length === 0 ? (
            <div className="text-center text-slate-400 py-8">
              No clients found for the current filters
            </div>
          ) : (
            <div className="space-y-4">
              {Object.entries(clientGroups).map(([clientName, clientCampaigns]) => (
                <div key={clientName} className="border border-slate-700 rounded-lg p-4">
                  <h4 className="font-semibold text-slate-200 text-lg mb-3">{clientName}</h4>
                  
                  <div className="space-y-3">
                    {clientCampaigns.map((campaign) => (
                      <div key={campaign.id} className="bg-slate-700/30 rounded-lg p-3">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="font-medium text-slate-200">{campaign.campaign_name}</div>
                            <div className="text-sm text-slate-400">
                              {campaign.product} • {campaign.brand}
                            </div>
                            <div className="text-xs text-slate-500">
                              {campaign.start_date} - {campaign.end_date}
                            </div>
                          </div>
                          <div className="text-right">
                            <span className={`text-xs px-2 py-1 rounded ${
                              campaign.status === 'Active'
                                ? 'bg-green-500/20 text-green-300'
                                : 'bg-slate-500/20 text-slate-300'
                            }`}>
                              {campaign.status}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-3 pt-3 border-t border-slate-600">
                    <div className="text-sm text-slate-400">
                      <span className="font-medium">Total Campaigns:</span> {clientCampaigns.length}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Summary Stats */}
        {Object.keys(clientGroups).length > 0 && (
          <div className="mt-6 p-4 bg-slate-700/30 rounded-lg">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-blue-400">{Object.keys(clientGroups).length}</div>
                <div className="text-sm text-slate-400">Total Clients</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-400">{filteredCampaigns.length}</div>
                <div className="text-sm text-slate-400">Total Campaigns</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-yellow-400">
                  {filteredCampaigns.filter(c => c.status === 'Active').length}
                </div>
                <div className="text-sm text-slate-400">Active Campaigns</div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
