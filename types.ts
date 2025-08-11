export type Status = 'Booked' | 'On Hold' | 'Available';

export interface InventoryItem {
  id: number;
  slotName: string;
  client: string | null;
  status: Status;
  startDate: string;
  endDate: string;
  revenue: number;
  product: string;
  brand: string;
}
