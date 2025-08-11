import React from 'react';
import type { CampaignLedgerItem } from '../types';

interface CampaignLedgerCardProps {
  campaigns: CampaignLedgerItem[];
}

export const CampaignLedgerCard: React.FC<CampaignLedgerCardProps> = ({
  campaigns
}) => {
  const totalRevenue = campaigns.reduce((sum, campaign) => sum + campaign.revenue, 0);
  const activeCampaigns = campaigns.filter(campaign => campaign.status === 'Active').length;

  return (
    <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
      <h3 className="text-lg font-semibold text-slate-100 mb-4">Campaign Ledger</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-400">{campaigns.length}</div>
          <div className="text-sm text-slate-400">Total Campaigns</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-400">{activeCampaigns}</div>
          <div className="text-sm text-slate-400">Active</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-400">£{totalRevenue.toLocaleString()}</div>
          <div className="text-sm text-slate-400">Total Revenue</div>
        </div>
      </div>

      <div className="space-y-3 max-h-64 overflow-y-auto">
        {campaigns.map((campaign) => (
          <div key={campaign.id} className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
            <div className="flex-1">
              <div className="font-medium text-slate-200">{campaign.campaign_name}</div>
              <div className="text-sm text-slate-400">
                {campaign.client} • {campaign.product} • {campaign.brand}
              </div>
              <div className="text-xs text-slate-500">
                {campaign.start_date} - {campaign.end_date}
              </div>
            </div>
            <div className="text-right">
              <div className="font-semibold text-green-400">£{campaign.revenue.toLocaleString()}</div>
              <div className={`text-xs px-2 py-1 rounded ${
                campaign.status === 'Active' 
                  ? 'bg-green-500/20 text-green-300' 
                  : 'bg-slate-500/20 text-slate-300'
              }`}>
                {campaign.status}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
