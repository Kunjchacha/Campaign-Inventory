export type Status = 'Booked' | 'On Hold' | 'Available';

export interface InventoryItem {
  id: number;
  slotName: string;
  client: string | null;
  status: Status;
  startDate: string;
  endDate: string;
  product: string;
  brand: string;
}

// New types for database integration
export interface DatabaseInventoryItem {
  id: number;
  slot_name: string;
  client: string | null;
  status: string;
  start_date: string;
  end_date: string;
  product: string;
  brand: string;
  table_source: string;
}

export interface CampaignLedgerItem {
  id: number;
  campaign_name: string;
  client: string;
  product: string;
  brand: string;
  start_date: string;
  end_date: string;
  status: string;
}

export interface TableSourceFilter {
  label: string;
  value: string;
  count: number;
}

export interface DatabaseStats {
  totalSlots: number;
  bookedSlots: number;
  onHoldSlots: number;
  availableSlots: number;
  tableSources: TableSourceFilter[];
}
